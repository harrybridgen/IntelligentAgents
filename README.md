# Maze Navigation Agents

By Harry Bridgen

## Overview

This is a Python simulation framework that compares the performance of multiple pathfinding agents in a procedurally generated maze environment. Each agent is driven by a different search strategy and is evaluated based on the number of steps it takes to reach the goal.

The simulation runs over multiple randomly generated mazes and produces visual and statistical comparisons of agent performance.

## Agents Implemented

- **RandomBrain** — Naive random walk with basic backtracking
- **DFSBrain** — Depth-First Search
- **HeuristicBrain** — Greedy best-first search using Manhattan distance
- **AStarBrain** — A* search with full path reconstruction

## Features

- Modular agent design for easy experimentation
- Procedural maze generation using recursive backtracking
- Step-wise agent execution for visualization or batch simulation
- Supports graphical rendering with Pygame
- Aggregates performance metrics and generates plots using Matplotlib

## Usage

Install dependencies:

```bash
pip install pygame matplotlib numpy
```

Run the simulation:

```bash
python main.py
```

By default, it runs 1000 simulations and plots the results.

You can enable real-time visualization by setting `RENDER = True` in `constants.py`, though this will slow down the simulation significantly.

## File Structure

- `main.py` — Entry point; manages simulations and plotting
- `agent.py` — Agent wrapper that interfaces with the maze and brain
- `brain.py` — Contains all brain (pathfinding) strategy implementations
- `maze.py` — Maze generation and rendering logic
- `constants.py` — Simulation parameters and rendering options

## Output

After running, the following plots will be generated:

- Line chart of steps taken over time per agent
- Bar chart of average steps per agent
- Boxplot showing distribution of performance

## Author

Harry Bridgen  
[github.com/harrybridgen](https://github.com/harrybridgen)
