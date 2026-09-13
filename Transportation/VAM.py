import numpy as np
def vogel_method(cost, supply, demand):

    cost = np.array(cost, dtype=float)
    supply = np.array(supply, dtype=float)
    demand = np.array(demand, dtype=float)
    m, n = cost.shape
    allocation = np.zeros((m, n))
    active_rows = set(range(m))
    active_cols = set(range(n))

    while active_rows and active_cols:
        row_penalty = {}
        col_penalty = {}
        # Row penalties
        for i in active_rows:
            values = sorted(cost[i][j]for j in active_cols)
            if len(values) >= 2:
                row_penalty[i] = values[1] - values[0]
            else:
                row_penalty[i] = values[0]
        # Column penalties
        for j in active_cols:

            values = sorted(cost[i][j]for i in active_rows)
            if len(values) >= 2:
                col_penalty[j] = values[1] - values[0]
            else:
                col_penalty[j] = values[0]

        largest = max(max(row_penalty.values()),max(col_penalty.values()))

        candidates = []
        # Candidate rows
        for i in active_rows:

            if row_penalty[i] == largest:

                j = min(active_cols,key=lambda x: cost[i][x])
                quantity = min(supply[i],demand[j])
                candidates.append((cost[i][j], -quantity, i, j))

        # Candidate columns
        for j in active_cols:
            if col_penalty[j] == largest:
                i = min(active_rows,key=lambda x: cost[x][j])

                quantity = min(supply[i],demand[j])

                candidates.append((cost[i][j], -quantity, i, j))
        _, _, i, j = min(candidates)
        amount = min(supply[i],demand[j])

        allocation[i][j] = amount

        supply[i] -= amount
        demand[j] -= amount

        if supply[i] == 0:
            active_rows.remove(i)

        if demand[j] == 0:
            active_cols.remove(j)

    total_cost = np.sum(allocation * cost)

    return allocation, total_cost

# Emergency Power Bank Transportation Problem

cost = [[23, 20, 13, 19],[9, 6, 17, 10],[9, 28, 5, 18],[24, 21, 27, 13]]

supply = [18, 22, 16, 14]
demand = [15, 17, 20, 18]

allocation, cost_value = vogel_method(cost,supply,demand)
print("\nVAM Initial Basic Feasible Solution")
print()
print(allocation)
print("\nInitial Transportation Cost =",cost_value)