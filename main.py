# main.py
import sys

from src.algorithms import solve_astar, solve_bfs, solve_dfs, solve_iddfs
from src.gui import launch_gui
from src.puzzle import (
    PRESET_EXAMPLES,
    is_valid_board,
    parse_input_to_matrix,
    print_board,
)

ALGORITHMS = {
    "1": ("BFS (Breadth-First Search)", solve_bfs),
    "2": ("DFS (Depth-First Search)", solve_dfs),
    "3": ("IDDFS (Iterative Deepening DFS)", solve_iddfs),
    "4": (
        "A* Search (Manhattan Distance)",
        lambda s: solve_astar(s, heuristic_type="manhattan"),
    ),
    "5": (
        "A* Search (Euclidean Distance)",
        lambda s: solve_astar(s, heuristic_type="euclidean"),
    ),
}

DIFFICULTY = {
    "1": ("Easy (3 moves)", PRESET_EXAMPLES["Easy (3 moves)"]),
    "2": ("Medium (14 moves)", PRESET_EXAMPLES["Medium (14 moves)"]),
    "3": ("Hard (No solution)", PRESET_EXAMPLES["Hard (No solution)"])
}


def get_cli_algorithm():
    print("\nSelect Search Algorithm:")
    for key, (name, _) in ALGORITHMS.items():
        print(f"{key}. {name}")

    choice = input("Enter choice (1-5): ").strip()
    if choice in ALGORITHMS:
        return ALGORITHMS[choice]

    print("[!] Invalid choice. Falling back to default (BFS).\n")
    return ALGORITHMS["1"]


def get_cli_initial_state():
    print("Select initial board configuration mode:")
    print("1. Continue with the pre-defined example")
    print("2. Enter custom 8-puzzle board")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        print("\nSelect level of difficulty")
        for key, (name, _) in DIFFICULTY.items():
            print(f"{key}. {name}")

        choice = input("Enter choice (1-3): ").strip()
        if choice in DIFFICULTY:
            return DIFFICULTY[choice][1]

        print("[!] Invalid choice. Falling back to easy level.\n")
        return DIFFICULTY["1"][1]

    elif choice == "2":
        print(
            "\nEnter 9 space-separated numbers (0-8) representing the board row by row:"
        )
        print("Example: 1 2 5 3 4 0 6 7 8")
        user_input = input("Board: ").strip().split()
        try:
            flat_vals = [int(x) for x in user_input]
            if is_valid_board(flat_vals):
                return parse_input_to_matrix(flat_vals)
            else:
                print(
                    "[!] Invalid board! Must contain digits 0-8 with no duplicates. Falling back to default example.\n"
                )
        except ValueError:
            print("[!] Invalid input numbers. Falling back to default example.\n")

    return PRESET_EXAMPLES["Easy (3 moves)"]


def run_cli():
    initial_state = get_cli_initial_state()
    algo_name, solve_func = get_cli_algorithm()

    print("\n====================================")
    print("      8-PUZZLE SOLVER (CLI)         ")
    print("====================================\n")
    print("\nInitial State:")
    print_board(initial_state)
    print(f"Running Algorithm: {algo_name}...")

    path, state_trace, nodes_expanded, depth = solve_func(initial_state)

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
    else:
        print("\n[!] No solution found for this board.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        launch_gui()
