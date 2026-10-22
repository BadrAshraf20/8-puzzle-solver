import time
import tkinter as tk
from tkinter import ttk
from src.algorithms import solve_bfs, solve_dfs
from src.puzzle import GOAL_STATE


class PuzzleGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("8-Puzzle Search Algorithm Visualizer")
    self.root.geometry("520x620")
    self.root.configure(bg="#2c3e50")

    # Configuration
    self.initial_state = ((1, 2, 3), (4, 0, 5), (6, 7, 8))
    self.goal_state = GOAL_STATE

    self.full_state_path = []
    self.current_step = 0

    self._build_ui()
    self._draw_board(self.initial_state)

  def _build_ui(self):
    title = tk.Label(
        self.root,
        text="8-PUZZLE SOLVER",
        font=("Helvetica", 18, "bold"),
        fg="#ecf0f1",
        bg="#2c3e50",
    )
    title.pack(pady=10)

    # Grid Frame
    self.grid_frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
    self.grid_frame.pack(pady=10)

    self.tiles = [[None for _ in range(3)] for _ in range(3)]
    for r in range(3):
      for c in range(3):
        lbl = tk.Label(
            self.grid_frame,
            text="",
            font=("Helvetica", 24, "bold"),
            width=4,
            height=2,
            relief="raised",
            bd=3,
        )
        lbl.grid(row=r, column=c, padx=5, pady=5)
        self.tiles[r][c] = lbl

    # Controls
    control_frame = tk.Frame(self.root, bg="#2c3e50")
    control_frame.pack(pady=10)

    tk.Label(
        control_frame,
        text="Algorithm:",
        font=("Helvetica", 11),
        fg="#ecf0f1",
        bg="#2c3e50",
    ).grid(row=0, column=0, padx=5)

    self.algo_var = tk.StringVar(value="BFS")
    algo_menu = ttk.Combobox(
        control_frame,
        textvariable=self.algo_var,
        values=["BFS", "DFS", "Iterative DFS", "A* (Manhattan)", "A* (Euclidean)"],
        state="readonly",
        width=15,
    )
    algo_menu.grid(row=0, column=1, padx=5)

    solve_btn = tk.Button(
        control_frame,
        text="Solve & Animate",
        font=("Helvetica", 11, "bold"),
        bg="#27ae60",
        fg="white",
        command=self.run_solver,
    )
    solve_btn.grid(row=0, column=2, padx=10)

    # Metrics Panel
    self.metrics_frame = tk.LabelFrame(
        self.root,
        text=" Execution Report Metrics ",
        font=("Helvetica", 11, "bold"),
        fg="#ecf0f1",
        bg="#2c3e50",
        padx=15,
        pady=10,
    )
    self.metrics_frame.pack(pady=10, fill="both", expand=True, padx=20)

    self.lbl_cost = tk.Label(
        self.metrics_frame,
        text="Cost of path: -",
        fg="#ecf0f1",
        bg="#2c3e50",
        anchor="w",
    )
    self.lbl_cost.pack(fill="x")

    self.lbl_expanded = tk.Label(
        self.metrics_frame,
        text="Nodes expanded: -",
        fg="#ecf0f1",
        bg="#2c3e50",
        anchor="w",
    )
    self.lbl_expanded.pack(fill="x")

    self.lbl_depth = tk.Label(
        self.metrics_frame,
        text="Search depth: -",
        fg="#ecf0f1",
        bg="#2c3e50",
        anchor="w",
    )
    self.lbl_depth.pack(fill="x")

    self.lbl_time = tk.Label(
        self.metrics_frame,
        text="Running time: -",
        fg="#ecf0f1",
        bg="#2c3e50",
        anchor="w",
    )
    self.lbl_time.pack(fill="x")

    self.lbl_status = tk.Label(
        self.metrics_frame,
        text="Status: Ready",
        fg="#f1c40f",
        bg="#2c3e50",
        font=("Helvetica", 10, "italic"),
        anchor="w",
    )
    self.lbl_status.pack(fill="x", pady=(5, 0))

  def _draw_board(self, state):
    for r in range(3):
      for c in range(3):
        val = state[r][c]
        if val == 0:
          self.tiles[r][c].config(text="", bg="#7f8c8d", relief="sunken")
        else:
          self.tiles[r][c].config(
              text=str(val), bg="#e74c3c", fg="white", relief="raised"
          )

  def run_solver(self):
    selected_algo = self.algo_var.get()

    # Routing based on selected algorithm
    if selected_algo == "BFS":
      start_time = time.time()
      path, state_trace, nodes_expanded, depth = solve_bfs(self.initial_state)
      elapsed_time = (time.time() - start_time) * 1000
    elif selected_algo == "DFS":
      start_time = time.time()
      path, state_trace, nodes_expanded, depth = solve_dfs(self.initial_state)
      elapsed_time = (time.time() - start_time) * 1000
    else:
      self.lbl_status.config(
          text=f"Status: {selected_algo} not implemented yet!"
      )
      return

    if path is not None:
      self.lbl_cost.config(text=f"Cost of path: {len(path)}")
      self.lbl_expanded.config(text=f"Nodes expanded: {nodes_expanded}")
      self.lbl_depth.config(text=f"Search depth: {depth}")
      self.lbl_time.config(text=f"Running time: {elapsed_time:.2f} ms")

      self.full_state_path = state_trace
      self.current_step = 0
      self.animate_solution()
    else:
      self.lbl_status.config(text="Status: No solution found!")

  def animate_solution(self):
    if self.current_step < len(self.full_state_path):
      current_state = self.full_state_path[self.current_step]
      self._draw_board(current_state)

      total_steps = len(self.full_state_path) - 1
      self.lbl_status.config(
          text=f"Status: Animating Step {self.current_step}/{total_steps}"
      )

      self.current_step += 1
      self.root.after(600, self.animate_solution)
    else:
      self.lbl_status.config(text="Status: Goal State Reached!")


def launch_gui():
  root = tk.Tk()
  app = PuzzleGUI(root)
  root.mainloop()