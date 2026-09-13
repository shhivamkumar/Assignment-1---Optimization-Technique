import numpy as np
def get_potentials(cost, allocation):
    m, n = cost.shape
    basic = [(i, j) for i in range(m) for j in range(n)if allocation[i][j] > 1e-9]
    u = [None] * m
    v = [None] * n
    u[0] = 0
    changed = True
    while changed:
        changed = False
        for i, j in basic:
            if u[i] is not None and v[j] is None:
                v[j] = cost[i][j] - u[i]
                changed = True
            elif v[j] is not None and u[i] is None:
                u[i] = cost[i][j] - v[j]
                changed = True
    return basic, u, v

def find_cycle(start, basic_cells):
    start = tuple(start)
    basic_cells = set(basic_cells)
    def dfs(path, move_row):
        current = path[-1]
        r, c = current
        # Check whether the path can return to the entering cell
        if len(path) >= 4:
            if move_row and r == start[0]:
                return path + [start]
            if not move_row and c == start[1]:
                return path + [start]
        # Move horizontally
        if move_row:
            candidates = [cell for cell in basic_cells if cell[0] == r]
        # Move vertically
        else:
            candidates = [cell for cell in basic_cells if cell[1] == c]
        for cell in candidates:
            if cell in path:
                continue
            result = dfs(path + [cell],not move_row)
            if result is not None:
                return result
        return None
    # horizontal check
    result = dfs([start], True)
    # Trying vertical if reqd.
    if result is None:
        result = dfs([start], False)
    return result

def modi_method(cost, allocation):
    cost = np.array(cost, dtype=float)
    allocation = allocation.copy().astype(float)
    m, n = cost.shape
    iteration = 1
    while True:
        basic, u, v = get_potentials(cost,allocation)
        delta = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                delta[i][j] = (cost[i][j]- u[i]- v[j])
        print("\n")
        print("MODI ITERATION", iteration)
        print("\n")
        print("U values:", [round(float(x), 2) for x in u])
        print("V values:", [round(float(x), 2) for x in v])
        print("\nOpportunity Cost Matrix:")
        print(delta)
        # Find most negative opportunity cost
        entering = None
        minimum = 0
        for i in range(m):
            for j in range(n):
                if (i, j) not in basic:
                    if delta[i][j] < minimum:
                        minimum = delta[i][j]
                        entering = (i, j)
        # Optimality condition
        if entering is None:
            print("\nAll opportunity costs are non-negative.")
            print("Therefore, the current solution is optimal.")
            break
        print("\nEntering Cell:", entering)
        cycle = find_cycle(entering,basic)
        if cycle is None:
            raise ValueError("Unable to find closed loop.")
        print("Closed Loop:", cycle)
        # Remove repeated starting cell
        cycle = cycle[:-1]
        # Negative positions
        negative_cells = cycle[1::2]
        theta = min(allocation[i][j] for i, j in negative_cells)
        print("Theta =", theta)
        # + - + - adjustment
        for k, (i, j) in enumerate(cycle):
            if k % 2 == 0:
                allocation[i][j] += theta
            else:
                allocation[i][j] -= theta
        allocation[np.abs(allocation) < 1e-9] = 0
        print("\nUpdated Allocation:")
        print(allocation)
        iteration += 1
    minimum_cost = np.sum(allocation * cost)
    return allocation, minimum_cost

# Transportation Problem

cost = np.array([[23, 20, 13, 19],[9, 6, 17, 10],[9, 28, 5, 18],[24, 21, 27, 13]], dtype=float)
# Initial BFS obtained using VAM
initial = np.array([[10, 0, 4, 4],[5, 17, 0, 0],[0, 0, 16, 0],[0, 0, 0, 14]], dtype=float)

solution, minimum_cost = modi_method(cost,initial)

print("\n")
print("OPTIMAL TRANSPORTATION PLAN")
print("\n")
print(solution)
print("\nMinimum Transportation Cost =",
      minimum_cost)