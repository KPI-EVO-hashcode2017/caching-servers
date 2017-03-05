from collections import defaultdict
from ortools.linear_solver import pywraplp


def solve(profit, sizes, capacity):
    # Instantiate a mixed-integer solver
    solver = pywraplp.Solver('SolveCachingServersProblem',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    n_caches, n_videos = profit.shape

    # Variables
    x = {}

    print("Define variables")
    for c in range(n_caches):
        for v in range(n_videos):
            if profit[c][v] > 0:
                x[c, v] = solver.IntVar(0, 1, 'x[%i,%i]' % (c, v))

    print("Define constraints")
    # The total size of the videos on each server is at most capacity.
    for c in range(n_caches):
        print("Define constraint for cache %s" % c)
        solver.Add(
            solver.Sum([sizes[v] * x[c, v] for v in range(n_videos)
                                           if profit[c][v] > 0])
            <= capacity
        )

    print("Define objective function")
    objective_members = []
    for c in range(n_caches):
        print("Define objective function members for cache %s" % c)
        for v in range(n_videos):
            if profit[c][v] > 0:
                objective_members.append(x[c,v] * profit[c][v])
    objective = solver.Sum(objective_members)

    print("Define maximization operation")
    solver.Maximize(objective)

    print("Start solve")
    sol = solver.Solve()
    print("Solved")
    
    print("Format result")
    result = defaultdict(list)
    for c in range(n_caches):
        for v in range(n_videos):
            if profit[c][v] > 0:
                if x[c, v].solution_value() > 0:
                    result[c].append(v)
    return result
