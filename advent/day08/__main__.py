#!/usr/bin/env python3

from __future__ import annotations

from typing import List, Tuple

from advent.utils import run_default


class Graph:
    def __init__(self, g: List[str]) -> None:
        self.g = g
        self.N = len(g)
        self.M = len(g[0]) if self.N > 0 else 0

    @classmethod
    def from_input_file(cls, input_file: str) -> Graph:
        g = []
        with open(input_file) as f:
            for line in f:
                g.append(line.strip())
        return Graph(g)

    def _check(self, r: int, c: int, dr: int, dc: int) -> int:
        scenic = 0
        my_height = self.g[r][c]
        r += dr
        c += dc
        while 0 <= r < self.N and 0 <= c < self.M:
            scenic += 1
            if self.g[r][c] >= my_height:
                return scenic
            r += dr
            c += dc
        return scenic

    def _visibility(self, r: int, c: int) -> Tuple[bool, int]:
        left = self._check(r, c, 0, -1)
        left_v = left == c
        right = self._check(r, c, 0, 1)
        right_v = right == self.M - c
        up = self._check(r, c, -1, 0)
        up_v = up == r
        down = self._check(r, c, 1, 0)
        down_v = down == self.N - r

        visible = left_v or right_v or up_v or down_v
        scenic = left * right * up * down
        return visible, scenic

    def advent(self) -> Tuple[int, int]:
        res1 = 0
        res2 = 0
        for r in range(self.N):
            for c in range(self.M):
                visible, scenic = self._visibility(r, c)
                res1 += visible
                res2 = max(res2, scenic)
        return res1, res2


def solve(input_file: str) -> Tuple[int, int]:
    g = Graph.from_input_file(input_file)
    return g.advent()


run_default(__file__, solve, 21)
