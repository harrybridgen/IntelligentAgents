class Agent:
    def __init__(self, brain, start=(1, 1), goal=None):
        self.brain = brain
        self.start = start
        self.goal = goal
        self.path = []

    def run_stepwise(self, maze):
        if self.goal is None:
            self.goal = (len(maze.grid[0]) - 2, len(maze.grid) - 2)
        self.brain.reset(maze.grid, self.start, self.goal)
        self.path = [self.start]
