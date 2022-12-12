#!/usr/bin/env python3

import collections
from typing import Tuple

from advent.utils import run_default


def solve(input_file: str) -> Tuple[int, int]:
    part1, part2 = -1, -1
    g = []
    from_g = {}
    start = (-1, -1)
    end = (-1, -1)
    starts = []

    with open(input_file) as f:
        for row, line in enumerate(f):
            for i, c in enumerate(line):
                if c == "S":
                    start = (row, line.index("S"))
                    starts.append((row, i))
                elif c == "E":
                    end = (row, line.index("E"))
                elif c == "a":
                    starts.append((row, i))

            g.append(list(line.strip()))

    g[start[0]][start[1]] = "a"
    g[end[0]][end[1]] = "z"

    def bfs(start: Tuple[int, int]) -> int:
        res = -1
        visited = set(start)
        q = collections.deque()
        q.append((*start, 0))
        while q and res == -1:
            row, col, dist = q.popleft()

            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in dirs:
                rr, cc = row + dr, col + dc

                if 0 <= rr < len(g) and 0 <= cc < len(g[0]) and (rr, cc) not in visited:
                    from_height = ord(g[row][col])
                    to_height = ord(g[rr][cc])
                    if from_height + 1 >= to_height:
                        from_g[(rr, cc)] = (row, col)
                        q.append((rr, cc, dist + 1))
                        visited.add((rr, cc))
                        if (rr, cc) == end:
                            res = dist + 1
        return res

    part1 = bfs(start)
    part2 = part1
    for s in starts:
        res = bfs(s)
        if res != -1:
            part2 = min(part2, res)

    return (part1, part2)


run_default(__file__, solve, 31, 29)
