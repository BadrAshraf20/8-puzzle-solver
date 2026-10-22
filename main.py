import time
from src.puzzle import GOAL_STATE, print_board
from src.algorithms import solve_bfs

def main():
    initial_state = ((1, 2, 3), (4, 0, 5), (6, 7, 8))

    print("====================================")
    print("      8-PUZZLE SOLVER (BFS)         ")
    print("====================================\n")
    print("Initial State:")
    print_board(initial_state)

    print("Goal State:")
    print_board(GOAL_STATE)

    start_time = time.time()
    path, state_trace, nodes_expanded, depth = solve_bfs(initial_state)
    elapsed_time = (time.time() - start_time) * 1000

    if path is not None:
        print("\n--- Traceable Step-by-Step Path ---")
        for i, state in enumerate(state_trace):
            print(f"Step {i}:")
            print_board(state)

        print("--- Execution Report Metrics ---")
        print(f"Path to goal: {path}")
        print(f"Cost of path: {len(path)}")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Search depth: {depth}")
        print(f"Running time: {elapsed_time:.2f} ms")
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()