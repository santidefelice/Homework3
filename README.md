## Homework 3 — Complexity Analysis

### Q1: Sudoku (CSP Backtracking)

- **Decision (solve one board)**: Worst-case O(9^m), where m is the number of empty cells; each empty cell has up to 9 choices with heavy pruning from row/col/box checks. Space O(m) recursion.
- **Counting solutions (capped at S)**: Same branching factor, but exploration stops after S solutions. Worst-case still exponential; practical time ≈ O(min(9^m, explored_nodes_until_S)). Space O(m).
- **Validity check per placement (`is_valid`)**: O(1) constant-time bounded by 27 cell checks (9 row + 9 col + 9 box).
- **Random puzzle generation (ensure solvable)**: Up to T attempts; each attempt places up to k clues with O(1) checks per placement and one solve call.
  - Per attempt: O(k) local checks + Solve complexity. Overall ≈ O(T·(k + 9^m_attempt)), dominated by solving a candidate.

Key notes: Real instances prune heavily; structure of givens drastically reduces search vs worst-case.

### Q2: Task Scheduling with Conflicts (Graph Coloring via CSP)

- **Build conflict graph**: O(n^2) time and O(n^2) space in worst case (dense overlaps).
- **Validity check for assignment**: O(d) where d is the degree of the task in the conflict graph.
- **Backtracking search**: Worst-case O(K^n), where K is resources (colors) and n is tasks, with pruning from the conflict graph. Space O(n) recursion.
- **Overall**: O(n^2 + K^n) time, dominated by backtracking; space O(n^2) due to the conflict graph.

### Q3: Multiple Combination Sums (CSP Backtracking with Quantity Limits)

- **Find all combinations**: Worst-case O((B/p_min)^n), where B is budget, p_min is the smallest item price, n is number of items; each item tries up to ⌊B/p_i⌋ quantities. Space O(n) recursion plus O(k·n) to store k solutions.
- **Find first combination**: Same worst-case but usually faster due to early termination upon first valid solution.
- **Pruning effects**: Budget pruning (breaks on overflow), feasibility checks, and ordering can substantially reduce explored nodes in practice.

General remark: All three problems are NP-hard variants (Sudoku solving, graph coloring, and unbounded/limited subset sum), so exponential worst-case behavior is expected; constraint checks and pruning make them tractable on typical inputs.
