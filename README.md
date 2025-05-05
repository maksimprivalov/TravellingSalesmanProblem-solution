# 🐜 Ant Colony Optimization for Travelling Salesman Problem (TSP)

This project is a Python implementation of the **Ant Colony Optimization (ACO)** algorithm for solving the **Travelling Salesman Problem (TSP)**, created as part of a university course in nonlinear programming and evolutionary algorithms.

Inspired by the collective intelligence of ants, the algorithm simulates how artificial agents (ants) explore cities, leave pheromone trails, and gradually converge toward the shortest route connecting all cities exactly once and returning to the starting point.

---

## 💡 Problem Description

The **Travelling Salesman Problem** (TSP) requires finding the shortest possible route that visits each city exactly once and returns to the starting point. For large numbers of cities, brute-force search becomes intractable (e.g., with >66 cities, even billions of years aren’t enough).

This implementation uses **Ant Colony Optimization**, a bio-inspired metaheuristic where artificial ants:
- Explore paths guided by distance and pheromone concentration
- Leave pheromones on routes they travel
- Prefer paths with stronger pheromone trails in the future
- Gradually converge to the optimal or near-optimal solution

Advanced techniques like **Elite Strategy** and **Max-Min Ant System** are also implemented to improve convergence.

---

## 🧠 Algorithm Highlights

- **Ants** probabilistically move based on distance and pheromone concentration
- **Pheromones** evaporate over time and are reinforced on shorter routes
- **Elite ants** reinforce the best route more strongly
- **Min-max pheromone bounds** prevent premature convergence

---

## ⚙️ Implementation Overview

The code is modular and structured in the following functions:

- `build_source_table(filename)` – builds a distance and pheromone matrix from city coordinates
- `solve(table, alpha, beta, n, Q)` – core logic of the algorithm (ant iterations, route selection)
- `update_feromon(table, routes, amountOfFeromonToAdd)` – pheromone evaporation and update
- `update_coefficient(table)` – resets binary visitation flags
- `draw(file_name, route, length)` – visualizes the final best path using matplotlib

Parameters like `alpha`, `beta`, `Q`, and pheromone evaporation rate are chosen experimentally.

---

## 🔬 Optimizations

- Execution time reduced from 2 minutes to **23 seconds** by:
  - Grouping pheromone updates
  - Avoiding redundant checks
  - Using Elite Ants every 10th generation
- Implemented route filtering, random city starts, and smarter transition rules

---

## 📊 Example Constants

These values produced the best results in this implementation:

```python
alpha = 1.0
beta = 4.0
c = 450
Q = 320
evaporation_rate = 0.3
min_pheromone = 0.1
```
## 🎯 Result
The algorithm consistently produces routes that are close to the optimal solution. Although not guaranteed to always find the shortest path, it effectively balances exploration and exploitation.

## 📈 Visualization
Final routes are drawn using `matplotlib`, clearly showing the optimal or near-optimal traversal path.
![Result](https://raw.githubusercontent.com/maksimprivalov/TravellingSalesmanProblem-solution/main/result.png)
## 📚 References
- Thomas Stützle, Holger Hoos – MAX–MIN Ant System
- FengYun Huang, ShiQiu Jiang – Research of Ant Colony Algorithm with Elite Strategy
- Yong Wang, Zunpu Han – Ant Colony Optimization for TSP
- Wikipedia – Travelling Salesman Problem

---
🧪 Created as part of the course “Nonlinear Programming and Evolutionary Algorithms” at the University of Novi Sad – FTN.

📌 Author: Maksim Privalov
