import heapq
import math
from collections import deque
from src.node import Node
from src.puzzle import get_neighbors, GOAL_STATE

GOAL_POSITIONS = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2),
}

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

def depth_limited_dfs(node, goal_state, limit, path_visited, nodes_expanded_counter):
  """Helper function that executes Depth-Limited DFS up to a given depth limit."""
  # Goal test
  if node.state == goal_state:
    return node, False

  # Reached depth limit without finding goal
  if node.depth >= limit:
    return None, True  # True indicates cut-off occurred

  nodes_expanded_counter[0] += 1
  cutoff_occurred = False

  for action, neighbor_state in get_neighbors(node.state):
    # Avoid cycles on the current active search branch
    if neighbor_state not in path_visited:
      path_visited.add(neighbor_state)
      child_node = Node(
          neighbor_state, parent=node, action=action, depth=node.depth + 1
      )

      result, cutoff = depth_limited_dfs(
          child_node,
          goal_state,
          limit,
          path_visited,
          nodes_expanded_counter,
      )

      if cutoff:
        cutoff_occurred = True

      if result is not None:
        return result, False

      # Backtrack path visited state for sibling branches
      path_visited.remove(neighbor_state)

  return None, cutoff_occurred


def solve_iddfs(initial_state, max_depth=50):
  """Solves the 8-puzzle using Iterative Deepening DFS (IDDFS)."""
  total_nodes_expanded = [0]

  for limit in range(max_depth + 1):
    start_node = Node(initial_state)
    path_visited = {initial_state}

    result_node, cutoff_occurred = depth_limited_dfs(
        start_node,
        GOAL_STATE,
        limit,
        path_visited,
        total_nodes_expanded,
    )

    if result_node is not None:
      # Reconstruct state and action path
      path = []
      states = []
      curr = result_node
      while curr:
        states.append(curr.state)
        if curr.action:
          path.append(curr.action)
        curr = curr.parent
      return (
          path[::-1],
          states[::-1],
          total_nodes_expanded[0],
          result_node.depth,
      )

    # If no cut-off occurred during the search, the state space is exhausted
    if not cutoff_occurred:
      break

  return None, None, total_nodes_expanded[0], 0


def heuristic_manhattan(state):
  """Calculates Manhattan distance heuristic for 8-puzzle."""
  h = 0
  for r in range(3):
    for c in range(3):
      val = state[r][c]
      if val != 0:  # Skip blank tile
        gr, gc = GOAL_POSITIONS[val]
        h += abs(r - gr) + abs(c - gc)
  return h


def heuristic_euclidean(state):
  """Calculates Euclidean distance heuristic for 8-puzzle."""
  h = 0.0
  for r in range(3):
    for c in range(3):
      val = state[r][c]
      if val != 0:  # Skip blank tile
        gr, gc = GOAL_POSITIONS[val]
        h += math.sqrt((r - gr) ** 2 + (c - gc) ** 2)
  return h


def solve_astar(initial_state, heuristic_type="manhattan"):
  """Solves the 8-puzzle using A* Search with Manhattan or Euclidean heuristic."""
  # Select heuristic function
  if heuristic_type == "manhattan":
    h_func = heuristic_manhattan
  elif heuristic_type == "euclidean":
    h_func = heuristic_euclidean
  else:
    raise ValueError("Invalid heuristic_type. Use 'manhattan' or 'euclidean'.")

  start_node = Node(
      initial_state,
      cost=0,
      heuristic=h_func(initial_state),
  )

  # Priority queue stores tuples: (f_cost, counter, node)
  # counter breaks ties when f_cost values are equal
  counter = 0
  frontier = []
  heapq.heappush(
      frontier, (start_node.cost + start_node.heuristic, counter, start_node)
  )

  # Visited dictionary tracks lowest g(n) path cost reached for each state
  visited = {initial_state: 0}
  nodes_expanded = 0

  while frontier:
    _, _, node = heapq.heappop(frontier)

    # Goal test
    if node.state == GOAL_STATE:
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
      g_cost = node.cost + 1  # Step cost is always 1

      if (
          neighbor_state not in visited
          or g_cost < visited[neighbor_state]
      ):
        visited[neighbor_state] = g_cost
        counter += 1
        h_cost = h_func(neighbor_state)
        child_node = Node(
            neighbor_state,
            parent=node,
            action=action,
            depth=node.depth + 1,
            cost=g_cost,
            heuristic=h_cost,
        )
        heapq.heappush(
            frontier, (g_cost + h_cost, counter, child_node)
        )

  return None, None, nodes_expanded, 0