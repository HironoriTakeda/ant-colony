# -*- coding: utf-8 -*-
"""Simple ant colony simulation with communication by pheromones.

This script simulates 100 ants searching for food from a nest in a
2D grid. Ants communicate via pheromone trails which influence their
movement. Running the script steps the simulation forward and prints
statistics about ants reaching food and returning to the nest.
"""

import random
from collections import defaultdict
from typing import List, Tuple

# Grid dimensions
WIDTH = 20
HEIGHT = 20

# Number of ants
ANT_COUNT = 100

# Locations
NEST = (0, 0)
FOOD = (WIDTH - 1, HEIGHT - 1)

# Pheromone evaporation rate per step
EVAPORATION = 0.02
# Amount of pheromone deposited by returning ants
DEPOSIT = 1.0

# Directions: up, down, left, right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Ant:
    def __init__(self, idx: int):
        self.id = idx
        self.pos = list(NEST)
        self.carrying = False  # True if carrying food

    def move(self, pheromones: List[List[float]]):
        """Move the ant one step influenced by pheromones."""
        x, y = self.pos

        # Evaluate neighbor cells
        candidates: List[Tuple[int, int]] = []
        weights: List[float] = []
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                candidates.append((nx, ny))
                weight = 1.0 + pheromones[ny][nx]
                weights.append(weight)

        # Choose next position based on pheromone-weighted random choice
        total = sum(weights)
        r = random.uniform(0, total)
        cumulative = 0.0
        for (nx, ny), w in zip(candidates, weights):
            cumulative += w
            if r <= cumulative:
                self.pos = [nx, ny]
                break

    def step(self, pheromones: List[List[float]]):
        """Perform one simulation step for this ant."""
        if not self.carrying:
            # If at food, pick it up and start returning
            if tuple(self.pos) == FOOD:
                self.carrying = True
            else:
                self.move(pheromones)
        else:
            # If at nest, drop food
            if tuple(self.pos) == NEST:
                self.carrying = False
            else:
                self.move(pheromones)
                # Deposit pheromone while carrying food back
                x, y = self.pos
                pheromones[y][x] += DEPOSIT


def evaporate(pheromones: List[List[float]]):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pheromones[y][x] *= (1.0 - EVAPORATION)


def simulate(steps: int = 200):
    pheromones = [[0.0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    ants = [Ant(i) for i in range(ANT_COUNT)]
    stats = defaultdict(int)
    for step in range(steps):
        for ant in ants:
            before = tuple(ant.pos)
            ant.step(pheromones)
            after = tuple(ant.pos)
            if not ant.carrying and after == FOOD and before != FOOD:
                stats['found_food'] += 1
            if ant.carrying and after == NEST and before != NEST:
                stats['returned'] += 1
        evaporate(pheromones)
    print(f"Simulation finished after {steps} steps.")
    print(f"Ants reached food {stats['found_food']} times.")
    print(f"Ants returned to nest {stats['returned']} times.")


if __name__ == "__main__":
    simulate()
