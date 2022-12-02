#!/usr/bin/env python3

from typing import Tuple

from advent.utils import run_default


def solve(input_file: str) -> Tuple[int, int]:
    elves = [0]
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                elves.append(0)
            else:
                elves[-1] += int(line)
    elves.sort()
    return (elves[-1], sum(elves[-3:]))


run_default(__file__, solve, 24000, 45000)
