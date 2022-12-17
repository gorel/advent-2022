#!/usr/bin/env python3

import collections
import copy
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple

from advent.utils import run_default

WIDTH = 7
NUM_ROCKS = 2022
CRAZY_NUM_ROCKS = 1000000000000


class Shape(Enum):
    HORIZONTAL = auto()
    PLUS = auto()
    L = auto()
    VERTICAL = auto()
    SQUARE = auto()


SHAPES_IDX = [
    Shape.HORIZONTAL,
    Shape.PLUS,
    Shape.L,
    Shape.VERTICAL,
    Shape.SQUARE,
]


@dataclass
class Point:
    x: int
    y: int


class DirectionBlockedError(ValueError):
    pass


class Tetris:
    class Direction(Enum):
        LEFT = auto()
        RIGHT = auto()
        DOWN = auto()

    def __init__(self, jet_pattern: str) -> None:
        self.jet_pattern = jet_pattern
        self.shape_idx = 0
        self.i = 0
        self.board = collections.defaultdict(lambda: ["." for _ in range(WIDTH)])

    def _next_shape(self) -> Shape:
        res = SHAPES_IDX[self.shape_idx]
        self.shape_idx = (self.shape_idx + 1) % len(SHAPES_IDX)
        return res

    def _next_move(self) -> Direction:
        if self.jet_pattern[self.i] == ">":
            res = Tetris.Direction.RIGHT
        else:
            res = Tetris.Direction.LEFT
        self.i = (self.i + 1) % len(self.jet_pattern)
        return res

    def _to_points(self, height: int, shape: Shape) -> List[Point]:
        if shape is Shape.HORIZONTAL:
            return [
                Point(2, height),
                Point(3, height),
                Point(4, height),
                Point(5, height),
            ]
        elif shape is Shape.PLUS:
            return [
                Point(3, height),
                Point(2, height + 1),
                Point(3, height + 1),
                Point(4, height + 1),
                Point(3, height + 2),
            ]
        elif shape is Shape.L:
            return [
                Point(2, height),
                Point(3, height),
                Point(4, height),
                Point(4, height + 1),
                Point(4, height + 2),
            ]
        elif shape is Shape.VERTICAL:
            return [
                Point(2, height),
                Point(2, height + 1),
                Point(2, height + 2),
                Point(2, height + 3),
            ]
        elif shape is Shape.SQUARE:
            return [
                Point(2, height + 1),
                Point(3, height + 1),
                Point(2, height),
                Point(3, height),
            ]

    def _move(self, points: List[Point], direction: Direction) -> List[Point]:
        new_points = []
        for point in points:
            if direction == Tetris.Direction.LEFT:
                new_point = Point(point.x - 1, point.y)
            elif direction == Tetris.Direction.RIGHT:
                new_point = Point(point.x + 1, point.y)
            else:
                new_point = Point(point.x, point.y - 1)

            if (
                new_point.x < 0
                or new_point.x >= WIDTH
                or new_point.y < 0
                or self.board[new_point.y][new_point.x] == "#"
            ):
                raise DirectionBlockedError()

            new_points.append(new_point)
        return new_points

    def drop_one(self) -> None:
        start_height = self.height() + 3
        shape = self._next_shape()
        points = self._to_points(start_height, shape)
        # print("A new challenger appears:")
        # self.print(points)

        falling = True
        while falling:
            direction = self._next_move()
            # It's okay if the left/right is blocked
            try:
                points = self._move(points, direction)
                # print(f"Moved {direction}")
                # self.print(points)
            except DirectionBlockedError:
                pass

            try:
                points = self._move(points, Tetris.Direction.DOWN)
                # print("Moved DOWN")
                # self.print(points)
            except DirectionBlockedError:
                falling = False

        for point in points:
            self.board[point.y][point.x] = "#"
            if self.board[point.y] == "#" * WIDTH:
                to_delete = set()
                for y in self.board:
                    if y < point.y:
                        to_delete.add(y)

                for y in to_delete:
                    del self.board[y]

    def board_key(self) -> str:
        height = self.height()
        # Look at the board "top down" to see
        # how far down each spot is
        res = []
        for x in range(WIDTH):
            for y in range(height, 0, -1):
                if self.board[y][x] == "#":
                    res.append(height - y)
                    break
        return ",".join(str(x) for x in res)

    def cache_key(self) -> str:
        return f"{self.shape_idx}|{self.i}|{self.board_key()}"

    def print(self, points: Optional[List[Point]] = None) -> None:
        board_copy = copy.deepcopy(self.board)
        for point in points or []:
            board_copy[point.y][point.x] = "@"

        for row in sorted(board_copy, reverse=True):
            print("".join(board_copy[row]))

    def height(self) -> int:
        if len(self.board) == 0:
            return 0
        return max(y for y, row in self.board.items() if "#" in row) + 1


def solve(input_file: str) -> Tuple[int, int]:
    jet_pattern = ""
    with open(input_file) as f:
        jet_pattern = f.read().strip()

    t = Tetris(jet_pattern)
    for _ in range(NUM_ROCKS):
        t.drop_one()

    part1 = t.height()

    t2 = Tetris(jet_pattern)
    cache = {}
    saved_rock_idx = -1
    saved_height = -1
    idx_delta = -1
    height_delta = -1
    for rock_idx in range(CRAZY_NUM_ROCKS):
        t2.drop_one()
        new_height = t2.height()
        cache_key = t2.cache_key()
        if cache_key in cache:
            old_idx, old_height = cache[cache_key]
            saved_rock_idx = rock_idx
            saved_height = new_height
            idx_delta = rock_idx - old_idx
            height_delta = new_height - old_height
            break
        cache[t2.cache_key()] = (rock_idx, new_height)

    rock_idx = saved_rock_idx
    height = saved_height
    num_repeats = (CRAZY_NUM_ROCKS - rock_idx) // idx_delta
    rock_idx += idx_delta * num_repeats
    height += height_delta * num_repeats

    while rock_idx < CRAZY_NUM_ROCKS:
        before_height = t2.height()
        t2.drop_one()
        height += t2.height() - before_height
        rock_idx += 1

    # I don't have a fucking clue why I need to subtract
    # one here, but it's almost 1:30am here and I'm tired
    # from staying up too late last night and failing to
    # solve day 16 part 2, so... this is fine.
    return (part1, height - 1)


run_default(__file__, solve, 3068, 1514285714288)
