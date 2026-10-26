# 8-Puzzle Search Algorithm Visualizer

A modular, high-performance Python implementation and graphical visualizer for solving the classic 8-puzzle problem using various uninformed and informed search strategies. Built as part of the Artificial Intelligence course lab assignment.

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Implemented Algorithms](#implemented-algorithms)
- [Project Architecture](#project-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
  - [GUI Mode (Interactive Visualizer)](#gui-mode-interactive-visualizer)
  - [CLI Mode (Terminal Execution)](#cli-mode-terminal-execution)
- [Contributors](#contributors)

---

## Overview

The 8-puzzle is a sliding puzzle that consists of a $3 \times 3$ grid holding 8 distinct numbered tiles (1–8) and a single empty space represented by `0`. The goal is to reach the target configuration `(0, 1, 2, 3, 4, 5, 6, 7, 8)` from an initial state by swapping adjacent tiles with the blank space.

$$\text{Goal State} = \begin{bmatrix} 0 & 1 & 2 \\ 3 & 4 & 5 \\ 6 & 7 & 8 \end{bmatrix}$$

---

## Key Features

- **Multi-Algorithm Support:** Full implementations of BFS, DFS, Iterative Deepening DFS (IDDFS), and $A^*$ Search.
- **Dual Heuristic Evaluation:** $A^*$ search supports both **Manhattan Distance** and **Euclidean Distance** heuristics.
- **Interactive GUI Visualizer:** Built using Tkinter with animated step-by-step state transitions, background threading to keep the interface responsive, option freezing during execution, and manual stop controls.
- **Custom Input & Presets:** Flexible input options allowing users to pick from pre-configured difficulty benchmark states or manually enter custom puzzle configurations with input validation.
- **Asynchronous Execution & Safety:** Non-blocking multi-threaded search operations accompanied by visual and acoustic alerts (`root.bell()`) for unsolvable states.

---

## Implemented Algorithms

| Category | Algorithm | Frontier Data Structure | Key Characteristics |
| :--- | :--- | :--- | :--- |
| **Uninformed** | **Breadth-First Search (BFS)** | FIFO Queue (`deque`) | Guarantees optimal path cost $d$; explores level-by-level. |
| **Uninformed** | **Depth-First Search (DFS)** | LIFO Stack (`list`) | Explores deep branches first; uses low memory but non-optimal. |
| **Uninformed** | **Iterative DFS (IDDFS)** | Recursive Call Stack | Combines completeness/optimality of BFS with memory efficiency of DFS. |
| **Informed** | **$A^*$ (Manhattan Distance)** | Min-Heap Priority Queue | Uses grid-distance sum $h = \sum (\Delta x + \Delta y)$; highly admissible & efficient. |
| **Informed** | **$A^*$ (Euclidean Distance)** | Min-Heap Priority Queue | Uses straight-line distance sum $h = \sum \sqrt{\Delta x^2 + \Delta y^2}$; admissible heuristic. |

---

## Project Architecture

The repository adheres to a clean, modular structure separating data structures, state logic, algorithms, and interface presentation:

```text
8-puzzle-solver/
├── src/
│   ├── node.py           # Node class for search tree representation (g, h, f costs, parent tracking)
│   ├── puzzle.py         # Board representation, state transitions, validation, and preset benchmarks
│   ├── algorithms.py     # BFS, DFS, IDDFS, and A* algorithm implementations
│   └── gui.py            # Tkinter graphical interface, background threading, & animation controller
├── main.py               # Main application entry point (GUI default, CLI via --cli flag)
├── README.md             # Project documentation
└── .gitignore            # Version control exclusion rules
```

---

## Installation & Setup

### Prerequisites
- **Python 3.8+** (Tkinter is included in standard Python installations for Windows/macOS).

### Clone the Repository
```bash
git clone https://github.com/BadrAshraf20/8-puzzle-solver.git
cd 8-puzzle-solver
```

---

## Usage Guide

### GUI Mode (Interactive Visualizer)
Run the application without arguments to launch the graphical user interface:

```bash
python main.py
```

**GUI Capabilities:**
1. **Choose Board State:** Select a preset (`Easy`, `Medium`, `Hard`) or click **Custom Input...** to enter 9 space-separated digits (0–8).
2. **Select Search Strategy:** Pick from BFS, DFS, IDDFS, $A^*$ (Manhattan), or $A^*$ (Euclidean).
3. **Solve & Animate:** Click **Solve & Animate** to trigger non-blocking search execution with live status updates (*Thinking...*).
4. **Control Animation:** Use the **Stop** button at any point to cancel active searches or halt animation.

---

### CLI Mode (Terminal Execution)
Run the program with the `--cli` flag to execute in the command-line interface:

```bash
python main.py --cli
```

---

## Contributors

Developed for the **Intro to Artificial Intelligence Course** (Alexandria University, Faculty of Engineering).

- **Badr Ashraf** - [GitHub Profile](https://github.com/BadrAshraf20)
- **Adham Hamdy** - [GitHub Profile](https://github.com/AdhamHamdy14)
