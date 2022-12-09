#!/usr/bin/env python3

from __future__ import annotations

import math
from typing import Tuple

from advent.utils import run_default

DIRS = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


class RopeTerminal:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def pull(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def dist(self, other: RopeTerminal) -> int:
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return math.sqrt(dx**2 + dy**2)

    def move_towards(self, other: RopeTerminal) -> None:
        if self.x < other.x:
            self.x += 1
        elif self.x > other.x:
            self.x -= 1

        if self.y < other.y:
            self.y += 1
        elif self.y > other.y:
            self.y -= 1


def _solve(input_file: str, rope_len: int) -> int:
    snake = [RopeTerminal(0, 0) for _ in range(rope_len)]
    visited = {(snake[-1].x, snake[-1].y)}

    with open(input_file) as f:
        for line in f:
            direction, distance = line.strip().split(" ")
            dx, dy = DIRS[direction]
            distance = int(distance)

            for _ in range(distance):
                snake[0].pull(dx, dy)
                for i in range(1, len(snake)):
                    if snake[i].dist(snake[i - 1]) > math.sqrt(2):
                        snake[i].move_towards(snake[i - 1])
                        if i == len(snake) - 1:
                            visited.add((snake[-1].x, snake[-1].y))

    return len(visited)


def solve(input_file: str) -> Tuple[int, int]:
    return _solve(input_file, 2), _solve(input_file, 10)


run_default(__file__, solve)
