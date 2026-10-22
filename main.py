import sys
import tkinter as tk
from src.gui import launch_gui
from src.puzzle import GOAL_STATE, print_board
from src.algorithms import solve_bfs

def run_cli():
    initial_state = ((1, 2, 3), (4, 0, 5), (6, 7, 8))

    print("====================================")
    print("      8-PUZZLE SOLVER (CLI)         ")
    print("====================================\n")
    print("Initial State:")
    print_board(initial_state)

    path, state_trace, nodes_expanded, depth = solve_bfs(initial_state)

    if path is not None:
        print("\n--- Step-by-Step Path ---")
        for i, state in enumerate(state_trace):
            print(f"Step {i}:")
            print_board(state)

        print("--- Execution Report Metrics ---")
        print(f"Path to goal: {path}")
        print(f"Cost of path: {len(path)}")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Search depth: {depth}")

if __name__ == "__main__":
    # If launched with `--cli`, run terminal output; otherwise launch GUI visualizer
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        launch_gui()