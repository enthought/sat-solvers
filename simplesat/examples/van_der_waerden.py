"""Run the simple SAT solver on the binary case of van der waerden's problem.

This problem asks for the smallest number n so that a binary number of n digits
that contains either j digits 0 or k digits 1, for given integers j and k.

"""


def _van_der_waerden_helper(j, n, sign):
    clause_data = []
    max_d = (n - 1) / (j - 1) + 1
    for d in range(1, max_d + 1):
        for i in range(1, n - (j - 1) * d + 1):
            clause = [sign * (i + p * d) for p in range(0, j)]
            clause_data.append(clause)
    return clause_data


def van_der_waerden(j, k, n):
    """Generate clauses for the van der Waerden problem.
    """
    return (
        _van_der_waerden_helper(j, n, +1) +
        _van_der_waerden_helper(k, n, -1)
    )


if __name__ == '__main__':
    import sys
    import time

    from simplesat.simple_solver import SimpleSATSolver

    j, k = map(int, sys.argv[1:])
    for n in range(5, 100):
        clauses = van_der_waerden(j, k, n)
        solver = SimpleSATSolver(clauses)
        solutions = solver.solve()
        print 'Solving van der waerden %d, %d, %d.' % (j, k, n)
        print 'Number of clauses: %d.' % len(clauses)
        print 'Solvable?',
        start = time.time()
        try:
            next(solutions)
            print 'Yes'
        except StopIteration:
            print 'No'
            break
        finally:
            stop = time.time()
            print 'Running time: %f' % (stop - start)
