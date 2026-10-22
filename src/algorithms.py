from collections import deque
from src.node import Node
from src.puzzle import get_neighbors, GOAL_STATE

def solve_bfs(initial_state):
    """Solves the 8-puzzle using Breadth-First Search (BFS)."""
    start_node = Node(initial_state)
    frontier = deque([start_node])
    visited = {initial_state}
    nodes_expanded = 0

    while frontier:
        node = frontier.popleft()

        if node.state == GOAL_STATE:
            # Reconstruct path and move history
            path = []
            states = []
            curr = node
            while curr:
                states.append(curr.state)
                if curr.action:
                    path.append(curr.action)
                curr = curr.parent
            return path[::-1], states[::-1], nodes_expanded, node.depth

        nodes_expanded += 1

        for action, neighbor_state in get_neighbors(node.state):
            if neighbor_state not in visited:
                visited.add(neighbor_state)
                child_node = Node(neighbor_state, parent=node, action=action, depth=node.depth + 1)
                frontier.append(child_node)

    return None, None, nodes_expanded, 0

def solve_dfs(initial_state):
  """Solves the 8-puzzle using Depth-First Search (DFS)."""
  start_node = Node(initial_state)
  frontier = [start_node]  # Use standard Python list as a LIFO stack
  visited = set()
  nodes_expanded = 0

  while frontier:
    node = frontier.pop()  # Pops from the top of the stack (LIFO)

    if node.state == GOAL_STATE:
      # Reconstruct path and move history
      path = []
      states = []
      curr = node
      while curr:
        states.append(curr.state)
        if curr.action:
          path.append(curr.action)
        curr = curr.parent
      return path[::-1], states[::-1], nodes_expanded, node.depth

    if node.state in visited:
      continue

    visited.add(node.state)
    nodes_expanded += 1

    # Explore child nodes
    for action, neighbor_state in get_neighbors(node.state):
      if neighbor_state not in visited:
        child_node = Node(
            neighbor_state, parent=node, action=action, depth=node.depth + 1
        )
        frontier.append(child_node)

  return None, None, nodes_expanded, 0