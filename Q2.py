"""
Homework 3 - Problem 2: Task Scheduling with Conflict Detection
CSP and Backtracking Implementation

Author: Solution for CSP Assignment
Description: Assigns resources to tasks with time conflicts using backtracking
"""

class Task:
    """Represents a task with start time, end time, and assigned resource"""
    def __init__(self, task_id, start, end):
        self.id = task_id
        self.start = start
        self.end = end
        self.resource = None
    
    def overlaps(self, other):
        """
        Check if this task overlaps with another task.
        Two tasks overlap if their time intervals intersect.
        
        Time Complexity: O(1)
        """
        return not (self.end <= other.start or other.end <= self.start)
    
    def __repr__(self):
        return f"Task{self.id}[{self.start}-{self.end}]"


class TaskScheduler:
    def __init__(self, tasks, max_resources):
        """
        Initialize task scheduler.
        
        Args:
            tasks: List of Task objects
            max_resources: Maximum number of resources (K)
        """
        self.tasks = tasks
        self.max_resources = max_resources
        self.conflict_graph = self.build_conflict_graph()
    
    def build_conflict_graph(self):
        """
        Build a conflict graph where edges represent overlapping tasks.
        
        This is a preprocessing step that identifies all constraints.
        Two tasks that overlap cannot share the same resource.
        
        Time Complexity: O(n^2) where n is number of tasks
        Space Complexity: O(n^2) for adjacency list in worst case
        """
        conflicts = {i: [] for i in range(len(self.tasks))}
        
        for i in range(len(self.tasks)):
            for j in range(i + 1, len(self.tasks)):
                if self.tasks[i].overlaps(self.tasks[j]):
                    conflicts[i].append(j)
                    conflicts[j].append(i)
        
        return conflicts
    
    def is_valid_assignment(self, task_idx, resource_id):
        """
        Check if assigning resource_id to task at task_idx is valid.
        
        A resource assignment is valid if no conflicting task uses the same resource.
        
        Pruning Strategy:
        - Check only tasks that conflict with current task
        - If any conflicting task already uses this resource, prune this branch
        
        Time Complexity: O(d) where d is degree of task in conflict graph
        """
        for conflict_idx in self.conflict_graph[task_idx]:
            if self.tasks[conflict_idx].resource == resource_id:
                return False
        return True
    
    def solve_backtracking(self, task_idx):
        """
        Solve task scheduling using backtracking with constraint checking.
        
        Algorithm:
        1. If all tasks assigned, return success
        2. For current task, try each resource (1 to K)
        3. Check if assignment is valid (pruning step)
        4. If valid, assign and recursively solve next task
        5. If recursive call fails, backtrack (try next resource)
        6. If no resource works, return failure
        
        WHY BACKTRACKING?
        - This is a Constraint Satisfaction Problem (CSP)
        - Variables: Each task needs a resource assignment
        - Domain: Resources {1, 2, ..., K}
        - Constraints: Overlapping tasks cannot share resources
        - Backtracking systematically explores assignment space
        - Pruning eliminates invalid assignments early
        
        This problem is equivalent to Graph Coloring:
        - Tasks = vertices
        - Conflicts = edges
        - Resources = colors
        - Find K-coloring of conflict graph
        
        Time Complexity: O(K^n) in worst case where n is number of tasks
        - Each task has K choices, n tasks total
        - Pruning reduces actual complexity significantly
        - With dense conflicts, many branches pruned early
        
        Space Complexity: O(n) for recursion stack
        """
        # Base case: all tasks assigned
        if task_idx == len(self.tasks):
            return True
        
        # Try each resource for current task
        for resource_id in range(1, self.max_resources + 1):
            # Pruning: check if this assignment violates constraints
            if self.is_valid_assignment(task_idx, resource_id):
                # Make assignment
                self.tasks[task_idx].resource = resource_id
                
                # Recursively assign remaining tasks
                if self.solve_backtracking(task_idx + 1):
                    return True
                
                # Backtrack: undo assignment
                self.tasks[task_idx].resource = None
        
        # No valid resource found for this task
        return False
    
    def solve(self):
        """
        Main solving method. Returns True if solution exists, False otherwise.
        """
        return self.solve_backtracking(0)
    
    def print_solution(self):
        """Print the resource assignment for all tasks"""
        print(f"\nResource Assignment (K={self.max_resources}):")
        print("-" * 60)
        for task in self.tasks:
            status = f"Resource {task.resource}" if task.resource else "UNASSIGNED"
            print(f"{task}: {status}")
    
    def print_conflicts(self):
        """Print the conflict graph"""
        print("\nConflict Graph:")
        print("-" * 60)
        for i, conflicts in self.conflict_graph.items():
            if conflicts:
                conflict_tasks = [self.tasks[j] for j in conflicts]
                print(f"{self.tasks[i]} conflicts with: {conflict_tasks}")


def main():
    print("=" * 60)
    print("TASK SCHEDULING WITH CONFLICT DETECTION")
    print("CSP and Backtracking Implementation")
    print("=" * 60)
    
    # Test Case 1: Simple case with clear conflicts
    print("\n[TEST CASE 1] Simple scheduling (3 tasks, K=2)")
    print("-" * 60)
    tasks1 = [
        Task(1, 0, 3),   # Task 1: 0-3
        Task(2, 2, 5),   # Task 2: 2-5 (overlaps with Task 1)
        Task(3, 4, 7)    # Task 3: 4-7 (overlaps with Task 2)
    ]
    
    scheduler1 = TaskScheduler(tasks1, max_resources=2)
    scheduler1.print_conflicts()
    
    if scheduler1.solve():
        print("\n✓ Solution found!")
        scheduler1.print_solution()
    else:
        print("\n✗ No solution possible with K=2 resources")
    
    # Test Case 2: Insufficient resources (edge case)
    print("\n\n[TEST CASE 2] Insufficient resources (3 overlapping tasks, K=2)")
    print("-" * 60)
    tasks2 = [
        Task(1, 0, 5),   # All three tasks overlap
        Task(2, 1, 6),
        Task(3, 2, 7)
    ]
    
    scheduler2 = TaskScheduler(tasks2, max_resources=2)
    scheduler2.print_conflicts()
    
    if scheduler2.solve():
        print("\n✓ Solution found!")
        scheduler2.print_solution()
    else:
        print("\n✗ No solution possible with K=2 resources")
        print("Analysis: All 3 tasks overlap, requiring 3 resources minimum")
    
    # Test Case 3: Complex scheduling scenario
    print("\n\n[TEST CASE 3] Complex scenario (6 tasks, K=3)")
    print("-" * 60)
    tasks3 = [
        Task(1, 0, 3),
        Task(2, 1, 4),
        Task(3, 2, 5),
        Task(4, 5, 8),
        Task(5, 6, 9),
        Task(6, 7, 10)
    ]
    
    scheduler3 = TaskScheduler(tasks3, max_resources=3)
    scheduler3.print_conflicts()
    
    if scheduler3.solve():
        print("\n✓ Solution found!")
        scheduler3.print_solution()
    else:
        print("\n✗ No solution possible with K=3 resources")
    
    # Test Case 4: No conflicts (edge case)
    print("\n\n[TEST CASE 4] No conflicts (sequential tasks, K=1)")
    print("-" * 60)
    tasks4 = [
        Task(1, 0, 2),
        Task(2, 2, 4),
        Task(3, 4, 6),
        Task(4, 6, 8)
    ]
    
    scheduler4 = TaskScheduler(tasks4, max_resources=1)
    scheduler4.print_conflicts()
    
    if scheduler4.solve():
        print("\n✓ Solution found!")
        scheduler4.print_solution()
        print("\nAnalysis: Sequential tasks need only 1 resource")
    else:
        print("\n✗ No solution possible with K=1 resource")
    
    # Test Case 5: Dense conflicts (worst case)
    print("\n\n[TEST CASE 5] Dense conflicts (all tasks overlap, K=5)")
    print("-" * 60)
    tasks5 = [
        Task(1, 0, 10),
        Task(2, 1, 9),
        Task(3, 2, 8),
        Task(4, 3, 7),
        Task(5, 4, 6)
    ]
    
    scheduler5 = TaskScheduler(tasks5, max_resources=5)
    scheduler5.print_conflicts()
    
    if scheduler5.solve():
        print("\n✓ Solution found!")
        scheduler5.print_solution()
        print("\nAnalysis: All tasks overlap, each needs separate resource")
    else:
        print("\n✗ No solution possible with K=5 resources")
    
    # Complexity Analysis Summary
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS SUMMARY")
    print("=" * 60)
    print("""
Build Conflict Graph: O(n²)
- Compare each pair of tasks for overlap

Is Valid Assignment: O(d)
- Check d conflicting tasks (d = max degree in conflict graph)

Backtracking Solve: O(K^n) worst case, much better with pruning
- K choices for each of n tasks
- Early pruning eliminates many branches
- Actual complexity depends on conflict density

Overall: O(n² + K^n) = O(K^n) dominated by backtracking
- Preprocessing: O(n²)
- Solving: O(K^n) with pruning

Space: O(n² + n) = O(n²)
- Conflict graph: O(n²)
- Recursion stack: O(n)
    """)


if __name__ == "__main__":
    main()