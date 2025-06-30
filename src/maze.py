# maze.py

import random
import pygame

class Maze:
    def __init__(self, width, height, cell_size=12):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.generate()

    def generate(self):
        stack = [(1, 1)]

        def cell_neighbors(x, y): 
            neighbors = []
            for nx, ny in ((x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)):
                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1 and self.grid[ny][nx] == 1:
                    neighbors.append((nx, ny))
            return neighbors

        def remove_wall(x1, y1, x2, y2):
            self.grid[(y1 + y2) // 2][(x1 + x2) // 2] = 0
            self.grid[y2][x2] = 0

        self.grid[1][1] = 0
        while stack:
            x, y = stack[-1]
            neighbors = cell_neighbors(x, y)
            if not neighbors:
                stack.pop()
                continue
            nx, ny = random.choice(neighbors)
            remove_wall(x, y, nx, ny)
            stack.append((nx, ny))

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        pygame.display.set_caption('Maze')

        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)

        screen.fill(white)

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = black if cell == 1 else white
                if cell == 2:
                    color = red
                pygame.draw.rect(screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()

        pygame.quit()

    def mark_path(self, path):
        for x, y in path:
            self.grid[y][x] = 2
