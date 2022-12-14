#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, List, Tuple

from advent.utils import run_default


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point

    def __iter__(self) -> Iterator[Point]:
        if self.start.x == self.end.x:
            if self.start.y < self.end.y:
                for yy in range(self.start.y, self.end.y + 1):
                    yield Point(self.start.x, yy)
            else:
                for yy in range(self.end.y, self.start.y + 1):
                    yield Point(self.start.x, yy)
        else:
            if self.start.x < self.end.x:
                for xx in range(self.start.x, self.end.x + 1):
                    yield Point(xx, self.start.y)
            else:
                for xx in range(self.end.x, self.start.x + 1):
                    yield Point(xx, self.start.y)


class FallingIntoAbyssError(StopIteration):
    pass


class PluggedTheSandHoleError(StopIteration):
    pass


class Graph:
    def __init__(
        self, lines: List[Line], origin: Point = Point(500, 0), floor: bool = False
    ) -> None:
        self.origin = origin
        self.filled = set()
        self.max_y = lines[0].start.y
        for line in lines:
            for point in line:
                self.filled.add(point)
                self.max_y = max(self.max_y, point.y)

        self.floor = None
        if floor:
            self.floor = self.max_y + 2

    def add_sand(self) -> None:
        # simulate a fall
        sand = Point(self.origin.x, self.origin.y)
        if sand in self.filled:
            raise PluggedTheSandHoleError()

        while True:
            if self.floor and sand.y + 1 == self.floor:
                break

            if sand.y > self.max_y and self.floor is None:
                raise FallingIntoAbyssError()

            below = Point(sand.x, sand.y + 1)
            below_left = Point(sand.x - 1, sand.y + 1)
            below_right = Point(sand.x + 1, sand.y + 1)

            if below not in self.filled:
                sand = below
            elif below_left not in self.filled:
                sand = below_left
            elif below_right not in self.filled:
                sand = below_right
            else:
                break

        self.filled.add(sand)

    def fill(self) -> int:
        res = 0
        while True:
            try:
                self.add_sand()
                res += 1
            except (FallingIntoAbyssError, PluggedTheSandHoleError):
                break
        return res

    @classmethod
    def parse_lines(cls, s: str) -> List[Line]:
        res = []
        last = None
        for part in s.split("->"):
            x, y = part.strip().split(",")
            this = Point(int(x), int(y))
            if last is not None:
                res.append(Line(start=last, end=this))
            last = this
        return res


def solve(input_file: str) -> Tuple[int, int]:
    lines = []
    with open(input_file) as f:
        for line in f:
            lines += Graph.parse_lines(line.strip())

    part1 = Graph(lines).fill()
    part2 = Graph(lines, floor=True).fill()
    return (part1, part2)


run_default(__file__, solve, 24, 93)
