GOAL_STATE = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

# Pre-defined test cases for quick testing
PRESET_EXAMPLES = {
    "Easy (3 moves)": ((1, 2, 5), (3, 4, 0), (6, 7, 8)),
    "Medium (14 moves)": ((1, 2, 3), (4, 0, 5), (6, 7, 8)),
    "Hard (No solution)": ((0, 2, 3), (1, 4, 5), (8, 7, 6)),
}

def is_valid_board(flat_list):
    """Validates if input contains exactly 9 numbers from 0 to 8 without duplicates."""
    return len(flat_list) == 9 and sorted(flat_list) == list(range(9))


def parse_input_to_matrix(flat_list):
    """Converts a flat list of 9 numbers into a 3x3 tuple matrix."""
    return (
        tuple(flat_list[0:3]),
        tuple(flat_list[3:6]),
        tuple(flat_list[6:9]),
    )

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
