from maze import Maze
from agent import Agent
from brain import RandomBrain, AStarBrain, HeuristicBrain, DFSBrain
from constants import CELL_SIZE, GRID_SIZE, SIMULATION_COUNT, SIMULATION_SPEED, RENDER
import pygame
import sys
import math

AGENT_CLASSES = [RandomBrain, AStarBrain, HeuristicBrain, DFSBrain]
AGENT_NAMES = ["Random", "A*", "Heuristic", "DFS"]

def create_maze_and_agents():
    maze = Maze(GRID_SIZE, GRID_SIZE, cell_size=CELL_SIZE)
    agents = [Agent(brain=brain()) for brain in AGENT_CLASSES]
    for agent in agents:
        agent.run_stepwise(maze)
    return maze, agents

def run_simulation(sim_id):
    maze, agents = create_maze_and_agents()
    agent_done = [False] * len(agents)
    results = [0] * len(agents)

    screen_width = GRID_SIZE * CELL_SIZE * len(agents)
    screen_height = GRID_SIZE * CELL_SIZE

    if RENDER:
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()

    running = True
    while running:
        if RENDER:
            screen.fill((255, 255, 255))

        for i, agent in enumerate(agents):
            offset_x = i * GRID_SIZE * CELL_SIZE

            if RENDER:
                for y, row in enumerate(maze.grid):
                    for x, cell in enumerate(row):
                        color = (0, 0, 0) if cell == 1 else (255, 255, 255)
                        pygame.draw.rect(screen, color, (offset_x + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            if not agent_done[i]:
                next_pos = agent.brain.next_move()
                if next_pos:
                    agent.path.append(next_pos)
                else:
                    agent_done[i] = True
                    results[i] = len(agent.path)
                    print(f"Simulation {sim_id+1} - {AGENT_NAMES[i]}: {results[i]} steps")

            if RENDER:
                for idx, (x, y) in enumerate(agent.path):
                    wave = math.sin(idx * 0.1)
                    green_value = int(100 + (wave + 1) / 2 * 125)
                    pygame.draw.rect(screen, (0, green_value, 0), (offset_x + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if RENDER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(SIMULATION_SPEED)

        if all(agent_done):
            running = False

    if RENDER:
        pygame.time.delay(1000)
        pygame.quit()

    return results

import numpy as np

def rolling_average(data, window=10):
    return np.convolve(data, np.ones(window)/window, mode='valid')

import matplotlib.pyplot as plt  # Add this to your imports

def main():
    print(f"Running {SIMULATION_COUNT} simulations on {len(AGENT_CLASSES)} agents...\n")
    total_steps = [0] * len(AGENT_CLASSES)
    agent_results = {name: [] for name in AGENT_NAMES}

    for i in range(SIMULATION_COUNT):
        result = run_simulation(i)
        total_steps = [sum(x) for x in zip(total_steps, result)]
        for j, name in enumerate(AGENT_NAMES):
            agent_results[name].append(result[j])

    print("\nAverage Steps per Agent:")
    averages = {}
    for name, steps in zip(AGENT_NAMES, total_steps):
        avg = steps / SIMULATION_COUNT
        averages[name] = avg
        print(f"  {name:10s}: {avg:.2f} steps")

    plt.figure(figsize=(12, 6))
    for name in AGENT_NAMES:
        smoothed = rolling_average(agent_results[name])
        plt.plot(range(1, len(smoothed)+1), smoothed, label=name)

    plt.xlabel("Simulation Number")
    plt.ylabel("Steps Taken")
    plt.title("Steps Taken per Agent Across Simulations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Bar Chart of Averages
    plt.figure(figsize=(8, 5))
    plt.bar(averages.keys(), averages.values(), color=['gray', 'green', 'blue', 'red'])
    plt.ylabel("Average Steps")
    plt.title("Average Steps per Agent")
    plt.tight_layout()
    plt.show(block=True)

    # Plot Boxplot of Results
    plt.figure(figsize=(8, 6))
    plt.boxplot([agent_results[name] for name in AGENT_NAMES], labels=AGENT_NAMES)
    plt.ylabel("Steps Taken")
    plt.title("Distribution of Steps per Agent")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
