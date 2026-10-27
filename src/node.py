class Node:
    """
    A Node represents a single "snapshot" of the puzzle at a specific moment.
    It keeps track of the board state and the history of how we got here.
    """
    def __init__(
        self, state,
        parent=None,
        action=None,
        depth=0,
        cost=0,
        heuristic=0
        ):
        # The current layout of the board (stored as a tuple of tuples)
        self.state = state

        # The previous Node we came from (used to trace back the winning path)
        self.parent = parent

        # The move that resulted in this state (e.g., "Up", "Down", "Left", "Right")
        self.action = action

        # The number of moves made so far from the starting board
        self.depth = depth

        # g(n): The actual cost to reach this node (usually 1 per move)
        self.cost = cost

        # h(n): The "smart guess" (heuristic) of how many moves are left to win
        self.heuristic = heuristic

    @property
    def total_cost(self):
        """
        f(n) = g(n) + h(n)
        Calculates the total expected cost of this path.
        Algorithms like A* use this to always pick the cheapest/best node first.
        """
        return self.cost + self.heuristic

    def __lt__(self, other):
        """
        Overloads the Less-Than (<) operator.
        This tells the Priority Queue (used in A*) to sort nodes based on their total_cost.
        The node with the smallest total_cost gets processed first.
        """
        return self.total_cost < other.total_cost
