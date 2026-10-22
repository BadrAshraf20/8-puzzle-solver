GOAL_STATE = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

def find_zero(state):
    """Locates the (row, col) position of the blank tile (0)."""
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c
    return -1, -1

def get_neighbors(state):
    """Generates all valid successor states by moving tile 0."""
    zero_r, zero_c = find_zero(state)
    moves = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }
    
    neighbors = []
    for action, (dr, dc) in moves.items():
        nr, nc = zero_r + dr, zero_c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [list(row) for row in state]
            new_state[zero_r][zero_c], new_state[nr][nc] = new_state[nr][nc], new_state[zero_r][zero_c]
            neighbors.append((action, tuple(tuple(row) for row in new_state)))
            
    return neighbors

def print_board(state):
    """Prints a 3x3 board in readable grid format."""
    for row in state:
        print(" ".join(str(val) for val in row))
    print()