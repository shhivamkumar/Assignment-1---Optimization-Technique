Experiments
1. Big-M Simplex Method

Case Study: Solar-Powered EV Charging Station Planning
The problem determines the optimal combination of standard, fast, and premium charging sessions while satisfying resource constraints.
Objective: Maximize total contribution.

Maximize:
Z = 7x1 + 5x2 + 4x3
Subject to:
2x1 + x2 + x3 <= 30
x1 + 2x2 + x3 >= 20
x1 + x2 + 3x3 = 25
x1, x2, x3 >= 0

Optimal solution:
x1 = 5
x2 = 20
x3 = 0
Maximum objective value = 135

---------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Transportation Problem

Case Study: Emergency Power-Bank Distribution
The problem determines the minimum-cost shipment plan from four warehouses to four relief centers.

Transportation Cost Matrix

|    | R1 | R2 | R3 | R4 |Supply|
| W1 | 23 | 20 | 13 | 19 | 18 |
| W2 | 9  | 6  | 17 | 10 | 22 |
| W3 | 9  | 28 | 5  | 18 | 16 |
| W4 | 24 | 21 | 27 | 13 | 14 |
|Demand|15| 17 | 20 | 18 | 

Total Supply = 70  
Total Demand = 70

The initial basic feasible solution is obtained using Vogel's Approximation Method (VAM), followed by optimality testing and improvement using the MODI Method.
Results:
Initial VAM cost = 767
MODI iteration 1 = 707
Final optimal transportation cost = 703