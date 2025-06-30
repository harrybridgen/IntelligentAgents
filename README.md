Intelligent Agent project.
Multiple agents attempt to solve a maze, then the program outputs graphs and statistics.
•	RandomBrain selects random unvisited directions, serving as a baseline.
•	DFSBrain explores paths deeply before backtracking, suitable for exploring but not optimized for efficiency.
•	HeuristicBrain uses a greedy approach based on Manhattan distance to the goal.
•	AStarBrain combines actual cost (g(n)) and heuristic estimate (h(n)) for optimal, informed pathfinding.
