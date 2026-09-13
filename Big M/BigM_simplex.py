import numpy as np
def solve_big_m(A, b, c, basic, names, M=1000000):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)
    step = 1
    while True:

        B = A[:, basic]

        #current basic solution
        B_inv = np.linalg.inv(B)

        xb = B_inv @ b
        tableau = B_inv @ A

        cb = c[basic]

        zj = cb @ tableau
        cj_zj = c - zj

        print("\n")
        print("Iteration", step)
        print("\n")
        print("Basic variables:")
        for i, val in enumerate(xb):
            print(f"{names[basic[i]]} = {val:.4f}")

        print("\nCj - Zj:")
        for i in range(len(names)):
            print(f"{names[i]:>4} : {cj_zj[i]:.4f}")

        # Optimality condition
        if np.max(cj_zj) <= 1e-9:
            break

        entering = np.argmax(cj_zj)

        column = tableau[:, entering]

        ratios = []

        for i in range(len(xb)):
            if column[i] > 1e-9:
                ratios.append(xb[i] / column[i])
            else:
                ratios.append(np.inf)

        leaving = np.argmin(ratios)

        if ratios[leaving] == np.inf:
            raise ValueError("The problem is unbounded.")

        print("\nEntering variable:",names[entering])
        print("Leaving variable:",names[basic[leaving]])

        basic[leaving] = entering

        step += 1

        if step > 100:
            raise ValueError("Too many iterations.")

    # Final solution
    B = A[:, basic]
    xb = np.linalg.solve(B, b)

    answer = np.zeros(len(names))

    for i in range(len(basic)):
        answer[basic[i]] = xb[i]

    objective = c @ answer

    print("\n")
    print("Final Solution")
    print("\n")

    for i in range(len(names)):
        print(f"{names[i]} = {answer[i]:.4f}")

    print("\nMaximum objective value =", objective)

    # Feasibility check for artificial variables
    artificial = ["a2", "a3"]

    for variable in artificial:
        index = names.index(variable)

        if answer[index] > 1e-8:
            print("Artificial variable", variable,"is positive.")
            print("Therefore the original LPP is infeasible.")
            return

    print("\nAll artificial variables are zero.")
    print("Hence the solution is feasible and optimal.")

# Solar Charging Station LPP

names = ["x1", "x2", "x3", "s1", "s2", "a2", "a3"]

A = [[2, 1, 1, 1, 0, 0, 0],[1, 2, 1, 0, -1, 1, 0],[1, 1, 3, 0, 0, 0, 1]]
b = [30, 20, 25]
# Big-M penalties for artificial variables
c = [7,5,4,0,0,-1000000,-1000000]
# Initial basis: s1, a2, a3
basic = [3, 5, 6]
solve_big_m(A, b, c, basic, names)