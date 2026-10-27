# Goal state representation for the 8-puzzle (3x3 grid()
# We used a tuple within a tuple to ensure the constants are immutable
# and quick to compare.
GOAL_STATE = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

# Pre-defined preset board examples for testing and visualizer dropdowns
PRESET_EXAMPLES = {
    "Easy (3 moves)": ((1, 2, 5), (3, 4, 0), (6, 7, 8)),
    "Medium (14 moves)": ((1, 2, 3), (4, 0, 5), (6, 7, 8)),
    "Hard (No solution)": ((0, 2, 3), (1, 4, 5), (8, 7, 6)),
}


def count_inversions(state):
    """
    - Counts the number of inversions in a board state.
    - An inversion occurs when a larger tile number appears before a smaller
    tile number.
    - The blank space (0) is ignored.
    """
    # Flatten the grid and ignore blank tile (0)
    flat_board = [num for row in state for num in row if num != 0]
    inversions = 0

    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            # If it finds a larger number appearing before a smaller number,
            # it increments the counter.
            if flat_board[i] > flat_board[j]:
                inversions += 1

    return inversions


def is_solvable(state):
    """
    Determines whether a given board state can reach the goal state.
    For a standard 3x3 8-puzzle, a state is solvable if and only if
    the total inversion count is EVEN.
    """
    return count_inversions(state) % 2 == 0


def is_valid_board(flat_list):
    """
    Validates custom inputs entered by the user.
    Returns True if the input contains exactly 9 unique integers from 0 to 8.
    """
    return len(flat_list) == 9 and sorted(flat_list) == list(range(9))


def parse_input_to_matrix(flat_list):
    """
    Converts a flat list of 9 numbers into a 3x3 matrix (tuple of tuples).
    Example: [1, 2, 3, 4, 5, 6, 7, 8, 0] -> ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    """
    return (
        tuple(flat_list[0:3]),
        tuple(flat_list[3:6]),
        tuple(flat_list[6:9]),
    )


def find_zero(state):
    """
    Finds and returns the (row, column) position of the blank space (0).
    """
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c
    return -1, -1


def get_neighbors(state):
    """
    - Generates all valid child nodes (neighboring board states) from the
    current node.
    - Moves the blank space (0) Up, Down, Left, or Right within grid boundaries.
    """
    zero_r, zero_c = find_zero(state)

    # Available movement offsets: (row_delta, col_delta, direction_label)
    moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}

    neighbors = []
    for action, (current_row, current_column) in moves.items():
        new_row, new_column = zero_r + current_row, zero_c + current_column

        # Check boundary conditions to prevent moving outside the 3x3 grid
        if 0 <= new_row < 3 and 0 <= new_column < 3:

            # Create a mutable copy of the 2D grid to swap values
            new_state = [list(row) for row in state]

            # Swap blank space (0) with the target tile
            new_state[zero_r][zero_c], new_state[new_row][new_column] = (
                new_state[new_row][new_column],
                new_state[zero_r][zero_c],
            )
            neighbors.append((action, tuple(tuple(row) for row in new_state)))

    return neighbors


def print_board(state):
    """
    Prints a 3x3 board in readable grid format.
    """
    for row in state:
        print(" ".join(str(val) for val in row))
    print()
