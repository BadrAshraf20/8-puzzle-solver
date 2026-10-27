# main.py
import sys

from src.algorithms import solve_bfs
from src.gui import launch_gui
from src.puzzle import (
    PRESET_EXAMPLES,
    is_valid_board,
    parse_input_to_matrix,
    print_board,
)


def get_cli_initial_state():
    print("Select initial board configuration mode:")
    print("1. Choose a pre-defined example")
    print("2. Enter custom 8-puzzle board")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "2":
        print("\nEnter 9 space-separated numbers (0-8) representing the board row by row:")
        print("Example: 1 2 5 3 4 0 6 7 8")
        user_input = input("Board: ").strip().split()
        try:
            flat_vals = [int(x) for x in user_input]
            if is_valid_board(flat_vals):
                return parse_input_to_matrix(flat_vals)
            else:
                print("[!] Invalid board! Must contain digits 0-8 with no duplicates. Falling back to default example.\n")
        except ValueError:
            print("[!] Invalid input numbers. Falling back to default example.\n")

    return PRESET_EXAMPLES["Easy (3 moves)"]

def run_cli():
    initial_state = get_cli_initial_state()

    print("\n====================================")
    print("      8-PUZZLE SOLVER (CLI)         ")
    print("====================================\n")
    print("Initial State:")
    print_board(initial_state)

    path, state_trace, nodes_expanded, depth = solve_bfs(initial_state)

    if path is not None:
        print("--- Step-by-Step Path ---")
        for i, state in enumerate(state_trace):
            print(f"Step {i}:")
            print_board(state)

        print("--- Execution Report Metrics ---")
        print(f"Path to goal: {path}")
        print(f"Cost of path: {len(path)}")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Search depth: {depth}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        launch_gui()
