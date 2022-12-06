#!/usr/bin/env python3

import re
from typing import List, Tuple

from advent.utils import run_default

# This doesn't even work if there are more than 9 columns, this is so lazy
SETUP_IDX_HOP = 4
MOVE_PATTERN = re.compile(r"move (\d*) from (\d*) to (\d*)")


def extract_setup(line: str) -> List[str]:
    res = []
    # God, this is lazy
    idx_offset = 1
    while idx_offset < len(line):
        res.append(line[idx_offset])
        idx_offset += SETUP_IDX_HOP
    return res


def solve(input_file: str) -> Tuple[str, str]:
    stacks = []
    with open(input_file) as f:
        # Parse first section
        for line in f:
            if "[" not in line:
                break

            for i, char in enumerate(extract_setup(line)):
                if i >= len(stacks):
                    stacks.append([])
                if char != " ":
                    stacks[i].append(char)

        # Ignore the next line, we know it's empty
        next(f)

        # We parsed them all upside down lol
        stacks_pt2 = []
        for i in range(len(stacks)):
            stacks[i].reverse()
            stacks_pt2.append(stacks[i].copy())

        # Parse move ops
        for line in f:
            match = MOVE_PATTERN.match(line)
            assert match is not None
            quantity = int(match.group(1))
            # They use 1-indexing
            from_stack = int(match.group(2)) - 1
            to_stack = int(match.group(3)) - 1
            for _ in range(quantity):
                stacks[to_stack].append(stacks[from_stack].pop())

            chars = stacks_pt2[from_stack][-quantity:]
            stacks_pt2[to_stack].extend(chars)
            del stacks_pt2[from_stack][-quantity:]

    # Get result
    res1 = "".join(s[-1] for s in stacks)
    res2 = "".join(s[-1] for s in stacks_pt2)

    return (res1, res2)


run_default(__file__, solve, "CMZ", "MCD")
