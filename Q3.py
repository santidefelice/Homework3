"""
Homework 3 - Problem 3: Multiple Combination Sums (Custom Shopping)
CSP and Backtracking Implementation
"""

class Item:
    """Represents a shopping item with name, price, and purchase limit"""
    def __init__(self, name, price, max_quantity):
        self.name = name
        self.price = price
        self.max_quantity = max_quantity  # 0 = unlimited
    
    def __repr__(self):
        limit = "unlimited" if self.max_quantity == 0 else f"max {self.max_quantity}"
        return f"{self.name}(${self.price}, {limit})"


class ShoppingSolver:
    def __init__(self, items, budget, min_items=0):
        """
        Initialize shopping solver.
        
        Args:
            items: List of Item objects
            budget: Maximum budget
            min_items: Minimum number of items needed (party requirements)
        """
        self.items = items
        self.budget = budget
        self.min_items = min_items
        self.solutions = []
    
    def solve_all_combinations(self, idx, current_combo, current_cost, current_count):
        """
        Find all valid purchasing combinations using backtracking.
        
        BASE MODEL: This is a variant of the Subset Sum Problem with repetition
        and quantity constraints.
        
        CSP Formulation:
        - Variables: Quantity of each item to purchase (x₁, x₂, ..., xₙ)
        - Domain: For item i, xᵢ ∈ [0, max_quantity_i] (or [0, ∞) if unlimited)
        - Constraints:
          1. Budget constraint: Σ(price_i × xᵢ) ≤ budget
          2. Minimum items: Σ(xᵢ) ≥ min_items
          3. Quantity limits: xᵢ ≤ max_quantity_i
        
        WHY BACKTRACKING?
        1. Need to explore all possible combinations (exponential search space)
        2. Constraints allow early pruning (budget exceeded → backtrack)
        3. Decision tree structure: at each level, decide quantity of item i
        4. CSP framework: assign values to variables subject to constraints
        5. No greedy solution exists (need all combinations, not just one optimal)
        6. Cannot use DP directly as asked to use CSP/backtracking approach
        
        Backtracking Algorithm:
        1. If processed all items:
           - Check if constraints satisfied (budget met, min items met)
           - If yes, record solution
        2. For current item, try all valid quantities (0 to max_quantity):
           - Pruning: Skip if adding item exceeds budget
           - Recursively explore with updated combo and cost
        3. Backtrack after exploring each quantity
        
        Pruning Strategies:
        - Budget pruning: If current_cost + item_cost > budget, skip
        - Feasibility pruning: If remaining items can't meet min_items, skip
        
        Time Complexity: O(budget/min_price)^n in worst case
        - For each item, try up to budget/price quantities
        - n items total
        - With pruning, much better in practice
        
        Space Complexity: O(n) for recursion stack and current combination
        """
        # Base case: processed all items
        if idx == len(self.items):
            # Check if combination meets requirements
            if current_count >= self.min_items and current_cost <= self.budget:
                self.solutions.append((list(current_combo), current_cost))
            return
        
        item = self.items[idx]
        max_qty = item.max_quantity if item.max_quantity > 0 else int(self.budget / item.price) + 1
        
        # Try different quantities of current item
        for qty in range(max_qty + 1):
            new_cost = current_cost + (qty * item.price)
            
            # Pruning: skip if budget exceeded
            if new_cost > self.budget:
                break  # No point trying higher quantities
            
            # Add item to combination
            if qty > 0:
                current_combo.append((item.name, qty, qty * item.price))
            
            # Recursive call for next item
            self.solve_all_combinations(idx + 1, current_combo, new_cost, current_count + qty)
            
            # Backtrack: remove item
            if qty > 0:
                current_combo.pop()
    
    def solve_first_combination(self, idx, current_combo, current_cost, current_count):
        """
        Find first valid combination (optimized version).
        Returns True if solution found, False otherwise.
        
        Time Complexity: O(budget/min_price)^n worst case
        - Same as solve_all but stops at first solution
        - Average case much better due to early termination
        """
        # Base case: found valid combination
        if idx == len(self.items):
            if current_count >= self.min_items and current_cost <= self.budget:
                self.solutions.append((list(current_combo), current_cost))
                return True
            return False
        
        item = self.items[idx]
        max_qty = item.max_quantity if item.max_quantity > 0 else int(self.budget / item.price) + 1
        
        for qty in range(max_qty + 1):
            new_cost = current_cost + (qty * item.price)
            
            if new_cost > self.budget:
                break
            
            if qty > 0:
                current_combo.append((item.name, qty, qty * item.price))
            
            # Return immediately if solution found
            if self.solve_first_combination(idx + 1, current_combo, new_cost, current_count + qty):
                return True
            
            if qty > 0:
                current_combo.pop()
        
        return False
    
    def find_all_solutions(self):
        """Find all valid combinations"""
        self.solutions = []
        self.solve_all_combinations(0, [], 0, 0)
        return self.solutions
    
    def find_one_solution(self):
        """Find one valid combination"""
        self.solutions = []
        self.solve_first_combination(0, [], 0, 0)
        return self.solutions[0] if self.solutions else None
    
    def print_solution(self, solution):
        """Print a solution in readable format"""
        combo, total_cost = solution
        if not combo:
            print("  Empty combination (buying nothing)")
        else:
            for item_name, qty, cost in combo:
                print(f"  - {item_name}: {qty} × ${cost/qty:.2f} = ${cost:.2f}")
        print(f"  Total: ${total_cost:.2f} (Budget: ${self.budget:.2f})")
    
    def print_all_solutions(self):
        """Print all solutions"""
        if not self.solutions:
            print("✗ No valid combinations found!")
            return
        
        print(f"\n✓ Found {len(self.solutions)} valid combination(s):")
        print("-" * 60)
        for i, solution in enumerate(self.solutions, 1):
            print(f"\nCombination {i}:")
            self.print_solution(solution)


def main():
    print("=" * 60)
    print("CUSTOM SHOPPING - COMBINATION SUM WITH CONSTRAINTS")
    print("CSP and Backtracking Implementation")
    print("=" * 60)
    
    # Test Case 1: Simple party shopping
    print("\n[TEST CASE 1] Simple party shopping")
    print("-" * 60)
    items1 = [
        Item("Soda", 2.50, 0),      # Unlimited
        Item("Chips", 3.00, 0),     # Unlimited
        Item("Cake", 15.00, 1),     # Limited to 1
        Item("Pizza", 12.00, 2)     # Limited to 2
    ]
    budget1 = 30.00
    min_items1 = 5
    
    print(f"Items available: {items1}")
    print(f"Budget: ${budget1:.2f}")
    print(f"Minimum items needed: {min_items1}")
    
    solver1 = ShoppingSolver(items1, budget1, min_items1)
    solver1.find_all_solutions()
    solver1.print_all_solutions()
    
    # Test Case 2: Tight budget (edge case)
    print("\n\n[TEST CASE 2] Tight budget - edge case")
    print("-" * 60)
    items2 = [
        Item("Water", 1.00, 0),
        Item("Sandwich", 5.00, 0),
        Item("Apple", 0.50, 0)
    ]
    budget2 = 10.00
    min_items2 = 8
    
    print(f"Items available: {items2}")
    print(f"Budget: ${budget2:.2f}")
    print(f"Minimum items needed: {min_items2}")
    
    solver2 = ShoppingSolver(items2, budget2, min_items2)
    solution2 = solver2.find_one_solution()
    
    if solution2:
        print("\n✓ Found a valid combination:")
        print("-" * 60)
        solver2.print_solution(solution2)
    else:
        print("\n✗ No valid combination possible!")
        print("Analysis: Budget too tight for minimum items required")
    
    # Test Case 3: Impossible scenario (edge case)
    print("\n\n[TEST CASE 3] Impossible scenario - budget insufficient")
    print("-" * 60)
    items3 = [
        Item("ExpensiveItem1", 20.00, 1),
        Item("ExpensiveItem2", 25.00, 1),
        Item("ExpensiveItem3", 30.00, 1)
    ]
    budget3 = 15.00
    min_items3 = 2
    
    print(f"Items available: {items3}")
    print(f"Budget: ${budget3:.2f}")
    print(f"Minimum items needed: {min_items3}")
    
    solver3 = ShoppingSolver(items3, budget3, min_items3)
    solver3.find_all_solutions()
    solver3.print_all_solutions()
    
    # Test Case 4: Many combinations
    print("\n\n[TEST CASE 4] Flexible scenario with many combinations")
    print("-" * 60)
    items4 = [
        Item("Balloon", 1.00, 0),
        Item("Plate", 2.00, 0),
        Item("Cup", 1.50, 0)
    ]
    budget4 = 10.00
    min_items4 = 3
    
    print(f"Items available: {items4}")
    print(f"Budget: ${budget4:.2f}")
    print(f"Minimum items needed: {min_items4}")
    
    solver4 = ShoppingSolver(items4, budget4, min_items4)
    solver4.find_all_solutions()
    
    print(f"\n✓ Found {len(solver4.solutions)} valid combinations!")
    print("(Showing first 10 combinations)")
    print("-" * 60)
    for i, solution in enumerate(solver4.solutions[:10], 1):
        print(f"\nCombination {i}:")
        solver4.print_solution(solution)
    
    if len(solver4.solutions) > 10:
        print(f"\n... and {len(solver4.solutions) - 10} more combinations")
    
    # Test Case 5: Large party planning (realistic scenario)
    print("\n\n[TEST CASE 5] Large party planning - realistic scenario")
    print("-" * 60)
    items5 = [
        Item("Soda (12-pack)", 5.00, 0),
        Item("Chips (bag)", 3.50, 0),
        Item("Cake", 25.00, 2),
        Item("Pizza (large)", 15.00, 0),
        Item("Salad (bowl)", 8.00, 3),
        Item("Dessert (box)", 12.00, 2)
    ]
    budget5 = 100.00
    min_items5 = 10
    
    print(f"Items available: {items5}")
    print(f"Budget: ${budget5:.2f}")
    print(f"Minimum items needed: {min_items5}")
    
    solver5 = ShoppingSolver(items5, budget5, min_items5)
    solution5 = solver5.find_one_solution()
    
    if solution5:
        print("\n✓ Found a valid combination:")
        print("-" * 60)
        solver5.print_solution(solution5)
    else:
        print("\n✗ No valid combination possible!")
    
    # Complexity Analysis
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS SUMMARY")
    print("=" * 60)
    print("""
MODEL MAPPING:
This problem maps to the Subset Sum with Repetition and Constraints.
- Classical Subset Sum: Select items (0 or 1) to reach target sum
- Our variant: Select quantities (0 to max_quantity) within budget

TIME COMPLEXITY:
Find All Solutions: O((budget/min_price)^n)
- For each of n items, try up to budget/min_price quantities
- Exponential in number of items
- Pruning reduces practical runtime significantly

Find One Solution: O((budget/min_price)^n) worst case
- Can terminate early on first valid solution
- Average case much better than worst case

SPACE COMPLEXITY: O(n)
- Recursion depth: n (one level per item)
- Current combination storage: O(n)
- Solution storage: O(k × n) for k solutions

OPTIMIZATION TECHNIQUES:
1. Budget pruning: Stop exploring if cost exceeds budget
2. Early termination: Stop at first solution if only one needed
3. Feasibility check: Verify constraints before deep recursion
4. Sorted items: Process expensive items first for faster pruning

WHY NOT DYNAMIC PROGRAMMING?
- Assignment requires CSP/Backtracking approach
- DP would work but doesn't demonstrate CSP concepts
- Backtracking allows finding ALL solutions, not just optimal
- CSP framework better illustrates constraint satisfaction
    """)


if __name__ == "__main__":
    main()