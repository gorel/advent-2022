#!/usr/bin/env python3

import string
from typing import Tuple

from advent.utils import run_default


def priority(c: str) -> int:
    if c in string.ascii_lowercase:
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 26 + 1

def solve(input_file: str) -> Tuple[int, int]:
    score = 0
    badge_score = 0
    with open(input_file) as f:
        badges = set(string.ascii_letters)
        for i, line in enumerate(f):
            if i > 0 and i % 3 == 0:
                badge_score += priority(badges.pop())
                badges = set(string.ascii_letters)

            line = line.strip()
            first, last = set(line[:len(line)//2]), set(line[len(line)//2:])
            score += priority((first & last).pop())
            badges &= set(line)
            
    # Remember the last group
    badge_score += priority(badges.pop())
    return (score, badge_score)


run_default(__file__, solve, 157, 70)
