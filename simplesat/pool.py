from __future__ import absolute_import

from .utils import DefaultOrderedDict
from simplesat.constraints import transform_requirement


class Pool(object):
    """ A pool of repositories.

    The main feature of a pool is to search for every package matching a
    given requirement.
    """

    def __init__(self, repositories=None, modifiers=None):
        self._id = 1
        self._repositories = []
        # FIXME Mar-9-2016: temporarily changing these names to catch places
        # that were using the private API. If it has been awhile and you feel
        # like everything is ok, you can remove these trailing underscores.
        self._package_to_id_ = {}
        self._id_to_package_ = {}
        self._packages_by_name_ = DefaultOrderedDict(list)

        self.modifiers = modifiers

        for repository in repositories or []:
            self.add_repository(repository)

    def add_repository(self, repository):
        """ Add the repository to this pool.

        Parameters
        ----------
        repository : Repository
            The repository to add
        """
        self._repositories.append(repository)
        for package in repository:
            current_id = self._id
            self._id += 1
            self._id_to_package_[current_id] = package
            self._package_to_id_[package] = current_id
            self._packages_by_name_[package.name].append(package)

    def what_provides(self, requirement, transform=True):
        """ Computes the list of packages fulfilling the given
        requirement.

        Parameters
        ----------
        requirement : Requirement
            The requirement to match candidates against.
        transform : bool
            If True, transform the requirement according to self.modifiers.
        """
        ret = []
        if requirement.name in self._packages_by_name_:
            if transform:
                requirement = self.transform_requirement(requirement)
            for package in self._packages_by_name_[requirement.name]:
                if requirement.matches(package.version):
                    ret.append(package)
        return ret

    def transform_requirement(self, requirement):
        """Return requirement transformed by the pool's ConstraintModifiers."""
        if self.modifiers:
            requirement = transform_requirement.with_modifiers(
                requirement, self.modifiers)
        return requirement

    def package_id(self, package):
        """ Returns the 'package id' of the given transformed package."""
        try:
            return self._package_to_id_[package]
        except KeyError:
            msg = "Package {0!r} not found in the pool.".format(package)
            raise ValueError(msg)

    def id_to_package(self, package_id):
        """ Returns the package of the given 'package id'."""
        try:
            return self._id_to_package_[package_id]
        except KeyError:
            msg = "Package ID {0!r} not found in the pool.".format(package_id)
            raise ValueError(msg)

    def id_to_string(self, package_id):
        """
        Convert a package id to a nice string representation.
        """
        package = self._id_to_package_[abs(package_id)]
        package_string = package.name + "-" + str(package.version)
        if package_id > 0:
            return "+" + package_string
        else:
            return "-" + package_string

    def name_to_packages(self, name):
        return tuple(self._packages_by_name_[name])

    @property
    def package_ids(self):
        return tuple(self._id_to_package_.keys())
