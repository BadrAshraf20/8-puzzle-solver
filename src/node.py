class Node:
    def __init__(self, state, parent=None, action=None, depth=0, cost=0, heuristic=0):
        self.state = state          # 2D tuple representation: ((1, 2, 3), (4, 0, 5), (6, 7, 8))
        self.parent = parent        # Reference to parent node for path reconstruction
        self.action = action        # "Up", "Down", "Left", or "Right"
        self.depth = depth          # Search depth
        self.cost = cost            # g(n): Path cost from start
        self.heuristic = heuristic  # h(n): Heuristic value for A*
        
    @property
    def total_cost(self):
        """f(n) = g(n) + h(n) for A* Search."""
        return self.cost + self.heuristic

    def __lt__(self, other):
        """Comparator for Priority Queue ordering in A*."""
        return self.total_cost < other.total_cost