#!/usr/bin/env python3

from typing import Tuple

from advent.utils import run_default

def solve(input_file: str) -> Tuple[int, int]:
    score = 0
    score2 = 0
    with open(input_file) as f:
        for line in f:
            elf1, elf2 = line.strip().split(",")
            elf1_a, elf1_b = [int(n) for n in elf1.split("-")]
            elf2_a, elf2_b = [int(n) for n in elf2.split("-")]
            elf1_range = set(range(elf1_a, elf1_b + 1))
            elf2_range = set(range(elf2_a, elf2_b + 1))

            overlap = len(elf1_range & elf2_range)
            if overlap in (len(elf1_range), len(elf2_range)):
                score += 1
            if overlap > 0:
                score2 += 1

    return (score, score2)


run_default(__file__, solve, 2, 4)
