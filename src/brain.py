import random
class Brain:
    def __init__(self):
        pass

    def reset(self, maze, start, goal):
        """Initialize internal state for step-based navigation."""
        raise NotImplementedError

    def next_move(self):
        """Return the next (x, y) move, or None if stuck or done."""
        raise NotImplementedError


class RandomBrain(Brain):
    def reset(self, maze, start, goal):
        self.maze = maze
        self.goal = goal
        self.visited = set()
        self.stack = [start]  # Path stack
        self.visited.add(start)

    def next_move(self):
        if not self.stack:
            return None  # Stuck or finished

        current = self.stack[-1]

        if current == self.goal:
            return None  # Goal reached

        x, y = current
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze):
                if self.maze[ny][nx] == 0 and (nx, ny) not in self.visited:
                    self.visited.add((nx, ny))
                    self.stack.append((nx, ny))
                    return (nx, ny)

        # Dead end: backtrack
        self.stack.pop()
        if self.stack:
            return self.stack[-1]  # Move visually back to previous cell
        return None  # Nothing to do

import heapq

class AStarBrain(Brain):
    def reset(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.open_set = []
        self.came_from = {}
        self.g_score = {start: 0}
        self.f_score = {start: self.heuristic(start, goal)}
        heapq.heappush(self.open_set, (self.f_score[start], start))
        self.path = []
        self.path_index = 0
        self.completed = False

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, current):
        path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        path.reverse()
        return path

    def next_move(self):
        if self.completed:
            if self.path_index < len(self.path):
                move = self.path[self.path_index]
                self.path_index += 1
                return move
            else:
                return None  # Path fully traversed

        while self.open_set:
            _, current = heapq.heappop(self.open_set)

            if current == self.goal:
                self.path = self.reconstruct_path(current)
                self.completed = True
                self.path_index = 1  # Skip the start
                return self.path[0]  # First move

            x, y = current
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze):
                    if self.maze[ny][nx] == 1:  # Wall
                        continue

                    tentative_g_score = self.g_score[current] + 1
                    if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                        self.came_from[neighbor] = current
                        self.g_score[neighbor] = tentative_g_score
                        f = tentative_g_score + self.heuristic(neighbor, self.goal)
                        self.f_score[neighbor] = f
                        heapq.heappush(self.open_set, (f, neighbor))

        return None  # No path found


class HeuristicBrain(Brain):
    def reset(self, maze, start, goal):
        self.maze = maze
        self.goal = goal
        self.visited = set()
        self.stack = [start]
        self.visited.add(start)

    def next_move(self):
        if not self.stack:
            return None  # Stuck or done

        current = self.stack[-1]
        if current == self.goal:
            return None  # Reached goal

        x, y = current
        neighbors = []

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze):
                if self.maze[ny][nx] == 0 and (nx, ny) not in self.visited:
                    dist = abs(nx - self.goal[0]) + abs(ny - self.goal[1])
                    neighbors.append(((nx, ny), dist))

        if neighbors:
            # Pick the neighbor closest to the goal
            best = min(neighbors, key=lambda n: n[1])[0]
            self.visited.add(best)
            self.stack.append(best)
            return best

        # Dead-end: backtrack
        self.stack.pop()
        if self.stack:
            return self.stack[-1]  # Optional: return previous move visually
        return None  # Fully stuck

class DFSBrain(Brain):
    def reset(self, maze, start, goal):
        self.maze = maze
        self.goal = goal
        self.stack = [start]
        self.visited = set()
        self.visited.add(start)

    def next_move(self):
        if not self.stack:
            return None  # All paths explored, goal not found

        current = self.stack[-1]

        if current == self.goal:
            return None  # Goal reached

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze):
                if self.maze[ny][nx] == 0 and neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.stack.append(neighbor)
                    return neighbor  # Go deeper

        # No unvisited neighbors, backtrack
        self.stack.pop()
        if self.stack:
            return self.stack[-1]  # Visual "step back"
        return None  # Stuck

