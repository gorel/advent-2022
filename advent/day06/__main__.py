#!/usr/bin/env python3

import collections
from typing import Tuple

from advent.utils import run_default


def solve(input_file: str) -> Tuple[int, int]:
    with open(input_file) as f:
        line = f.read().strip()

    left, left2 = 0, 0
    s, s2 = collections.defaultdict(int), collections.defaultdict(int)
    res1, res2 = -1, -1

    for right in range(len(line)):
        c = line[right]
        s[c] += 1
        s2[c] += 1

        # Fix constraint
        if right >= 4:
            c_l = line[left]
            s[c_l] -= 1
            if s[c_l] == 0:
                del s[c_l]
            left += 1

        if len(s) == 4 and res1 == -1:
            # 1 indexing...
            res1 = right + 1

        # Fix constraint for part2
        if right >= 14:
            c_l = line[left2]
            s2[c_l] -= 1
            if s2[c_l] == 0:
                del s2[c_l]
            left2 += 1

        if len(s2) == 14:
            # 1 indexing...
            res2 = right + 1
            # We must have found the right answer for part1 already
            break

    return (res1, res2)


run_default(__file__, solve, 7, 19)
