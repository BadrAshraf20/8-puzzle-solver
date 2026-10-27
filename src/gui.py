# src/gui.py
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from src.algorithms import solve_astar, solve_bfs, solve_dfs, solve_iddfs
from src.puzzle import (
    GOAL_STATE,
    PRESET_EXAMPLES,
    is_valid_board,
    parse_input_to_matrix,
)


class PuzzleGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Search Algorithm Visualizer")
        self.root.geometry("560x720")
        self.root.configure(bg="#2c3e50")

        # Map cleaner display names to board states without hardcoded step counts
        self.presets = {
            "Easy": PRESET_EXAMPLES["Easy (3 moves)"],
            "Medium": PRESET_EXAMPLES["Medium (14 moves)"],
            "Hard": PRESET_EXAMPLES["Hard (No solution)"],
        }

        self.initial_state = self.presets["Easy"]
        self.goal_state = GOAL_STATE

        self.full_state_path = []
        self.current_step = 0
        self.is_running = False
        self.animation_job = None
        self.search_id = 0
        self.cancel_event = None

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

        # 3x3 Board Grid
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

        # Board Input Control Bar
        input_frame = tk.Frame(self.root, bg="#2c3e50")
        input_frame.pack(pady=5)

        tk.Label(
            input_frame,
            text="Preset Input:",
            font=("Helvetica", 10),
            fg="#ecf0f1",
            bg="#2c3e50",
        ).grid(row=0, column=0, padx=5)

        self.preset_var = tk.StringVar(value="Easy")
        self.preset_menu = ttk.Combobox(
            input_frame,
            textvariable=self.preset_var,
            values=list(self.presets.keys()),
            state="readonly",
            width=12,
        )
        self.preset_menu.grid(row=0, column=1, padx=5)
        self.preset_menu.bind("<<ComboboxSelected>>", self.on_preset_selected)

        self.custom_btn = tk.Button(
            input_frame,
            text="Custom Input...",
            font=("Helvetica", 9, "bold"),
            bg="#3498db",
            fg="white",
            command=self.open_custom_input_dialog,
        )
        self.custom_btn.grid(row=0, column=2, padx=5)

        # Algorithm Controls & Stop Button
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
        self.algo_menu = ttk.Combobox(
            control_frame,
            textvariable=self.algo_var,
            values=[
                "BFS",
                "DFS",
                "Iterative DFS",
                "A* (Manhattan)",
                "A* (Euclidean)",
            ],
            state="readonly",
            width=15,
        )
        self.algo_menu.grid(row=0, column=1, padx=5)

        self.solve_btn = tk.Button(
            control_frame,
            text="Solve & Animate",
            font=("Helvetica", 11, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.start_solver_thread,
        )
        self.solve_btn.grid(row=0, column=2, padx=5)

        self.stop_btn = tk.Button(
            control_frame,
            text="Stop",
            font=("Helvetica", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            state="disabled",
            command=self.stop_execution,
        )
        self.stop_btn.grid(row=0, column=3, padx=5)

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

        tk.Label(
            self.metrics_frame,
            text="Path to goal:",
            fg="#ecf0f1",
            bg="#2c3e50",
            anchor="w",
            font=("Helvetica", 10, "bold"),
        ).pack(fill="x", pady=(0, 2))

        self.txt_path = scrolledtext.ScrolledText(
            self.metrics_frame,
            height=3,
            wrap="word",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 9),
            bd=1,
            relief="solid",
        )
        self.txt_path.pack(fill="x", pady=(0, 8))
        self.txt_path.insert("1.0", "-")
        self.txt_path.config(state="disabled")

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

    def set_controls_state(self, state):
        """Enables or disables interactive controls to freeze/unfreeze options."""
        combo_state = "readonly" if state == "normal" else "disabled"
        self.preset_menu.config(state=combo_state)
        self.algo_menu.config(state=combo_state)
        self.custom_btn.config(state=state)
        self.solve_btn.config(state=state)
        self.stop_btn.config(state="normal" if state == "disabled" else "disabled")

    def _update_path_text(self, text):
        """Helper to update read-only ScrolledText box for path display."""
        self.txt_path.config(state="normal")
        self.txt_path.delete("1.0", tk.END)
        self.txt_path.insert("1.0", text)
        self.txt_path.config(state="disabled")

    def reset_metrics(self):
        """Resets all metrics display labels back to default initial state."""
        self._update_path_text("-")
        self.lbl_cost.config(text="Cost of path: -")
        self.lbl_expanded.config(text="Nodes expanded: -")
        self.lbl_depth.config(text="Search depth: -")
        self.lbl_time.config(text="Running time: -")
        self.lbl_status.config(text="Status: Ready")

    def on_preset_selected(self, event):
        selected = self.preset_var.get()
        self.initial_state = self.presets[selected]
        self._draw_board(self.initial_state)
        self.reset_metrics()  # Reset metrics on new preset selection

    def open_custom_input_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Custom Board State")
        dialog.geometry("320x220")
        dialog.configure(bg="#2c3e50")
        dialog.grab_set()

        tk.Label(
            dialog,
            text=(
                "Enter 9 numbers (0-8) separated by spaces:\n(Use 0 for blank" " space)"
            ),
            fg="#ecf0f1",
            bg="#2c3e50",
            font=("Helvetica", 10),
        ).pack(pady=10)

        entry = tk.Entry(dialog, font=("Helvetica", 12), width=20)
        entry.insert(0, "1 2 5 3 4 0 6 7 8")
        entry.pack(pady=10)

        def apply_custom_input():
            try:
                raw_vals = [int(x) for x in entry.get().strip().split()]
                if is_valid_board(raw_vals):
                    self.initial_state = parse_input_to_matrix(raw_vals)
                    self._draw_board(self.initial_state)
                    self.preset_var.set("Custom State")
                    self.reset_metrics()  # Reset metrics on custom board input
                    dialog.destroy()
                else:
                    messagebox.showerror(
                        "Invalid Input",
                        "Please enter exactly 9 unique numbers from 0 to 8.",
                    )
            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    "Please enter valid integers separated by spaces.",
                )

        tk.Button(
            dialog,
            text="Apply Board State",
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10, "bold"),
            command=apply_custom_input,
        ).pack(pady=10)

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

    def start_solver_thread(self):
        """Launches the solver on a background thread to prevent UI freezing."""
        self.search_id += 1
        search_id = self.search_id
        cancel_event = threading.Event()
        self.cancel_event = cancel_event
        initial_state = self.initial_state
        selected_algo = self.algo_var.get()
        self.is_running = True
        self.reset_metrics()  # Clear old metrics right as a new search starts
        self.set_controls_state("disabled")
        self.lbl_status.config(text="Status: Thinking... Searching for path...")

        threading.Thread(
            target=self.run_solver,
            args=(search_id, initial_state, selected_algo, cancel_event),
            daemon=True,
        ).start()

    def run_solver(self, search_id, initial_state, selected_algo, cancel_event):
        start_time = time.time()

        try:
            if selected_algo == "BFS":
                result = solve_bfs(initial_state, cancel_event=cancel_event)
            elif selected_algo == "DFS":
                result = solve_dfs(initial_state, cancel_event=cancel_event)
            elif selected_algo == "Iterative DFS":
                result = solve_iddfs(initial_state, cancel_event=cancel_event)
            elif selected_algo == "A* (Manhattan)":
                result = solve_astar(
                    initial_state,
                    heuristic_type="manhattan",
                    cancel_event=cancel_event,
                )
            elif selected_algo == "A* (Euclidean)":
                result = solve_astar(
                    initial_state,
                    heuristic_type="euclidean",
                    cancel_event=cancel_event,
                )
            else:
                raise ValueError(f"Unknown search algorithm: {selected_algo}")
        except Exception as error:
            self.root.after(
                0, self.handle_solver_error, search_id, str(error)
            )
            return

        elapsed_time = (time.time() - start_time) * 1000
        path, state_trace, nodes_expanded, depth = result

        # Schedule UI updates back on the main thread
        self.root.after(
            0,
            self.handle_solver_results,
            search_id,
            path,
            state_trace,
            nodes_expanded,
            depth,
            elapsed_time,
        )

    def handle_solver_error(self, search_id, error):
        if search_id != self.search_id or not self.is_running:
            return

        self.is_running = False
        self.cancel_event = None
        self.lbl_status.config(text="Status: Search failed.")
        self.set_controls_state("normal")
        messagebox.showerror(
            "Search Failed", f"The solver encountered an error:\n{error}"
        )

    def handle_solver_results(
        self, search_id, path, state_trace, nodes_expanded, depth, elapsed_time
    ):
        """
        Processes search results, updates UI labels,
        and initiates animation or alerts.
        """
        if search_id != self.search_id or not self.is_running:
            return  # Search was stopped by user

        if path is not None:
            # 1. Construct path string safely with truncation for long paths (e.g., deep DFS solutions)
            if len(path) > 100:
                path_str = (
                    " -> ".join(path[:10])
                    + f" ... [{len(path) - 20} steps omitted] ... "
                    + " -> ".join(path[-10:])
                )
            else:
                path_str = " -> ".join(path) if path else "None (Start = Goal)"

            # 2. Update text metrics
            self._update_path_text(path_str)
            self.lbl_cost.config(text=f"Cost of path: {len(path)}")
            self.lbl_expanded.config(text=f"Nodes expanded: {nodes_expanded}")
            self.lbl_depth.config(text=f"Search depth: {depth}")
            self.lbl_time.config(text=f"Running time: {elapsed_time:.2f} ms")

            # 3. Clear old negative status and set initial animation status
            self.lbl_status.config(text="Status: Solution found! Animating...")

            self.full_state_path = state_trace
            self.current_step = 0
            self.animate_solution(search_id)
        else:
            # Clear metrics when no path exists
            self._update_path_text("-")
            self.lbl_cost.config(text="Cost of path: -")
            self.lbl_expanded.config(text=f"Nodes expanded: {nodes_expanded}")
            self.lbl_depth.config(text="Search depth: -")
            self.lbl_time.config(text=f"Running time: {elapsed_time:.2f} ms")

            self.root.bell()
            messagebox.showwarning(
                "No Solution Found",
                "No valid path exists to transition this state into the goal state!",
            )
            self.lbl_status.config(text="Status: No solution path exists!")
            self.set_controls_state("normal")
            self.is_running = False
            self.cancel_event = None

    def animate_solution(self, search_id):
        if search_id != self.search_id or not self.is_running:
            return

        if self.current_step < len(self.full_state_path):
            current_state = self.full_state_path[self.current_step]
            self._draw_board(current_state)

            total_steps = len(self.full_state_path) - 1
            self.lbl_status.config(
                text=f"Status: Animating Step {self.current_step}/{total_steps}"
            )

            self.current_step += 1
            self.animation_job = self.root.after(
                600, self.animate_solution, search_id
            )
        else:
            self.lbl_status.config(text="Status: Goal State Reached!")
            self.set_controls_state("normal")
            self.is_running = False
            self.cancel_event = None

    def stop_execution(self):
        """Stops any running search or animation and restores controls."""
        self.search_id += 1
        self.is_running = False
        if self.cancel_event is not None:
            self.cancel_event.set()
            self.cancel_event = None
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None

        self.lbl_status.config(text="Status: Execution stopped. Select an option.")
        self.set_controls_state("normal")


def launch_gui():
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
