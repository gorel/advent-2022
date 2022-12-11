#!/usr/bin/env python3

from typing import Optional, Tuple

from advent.utils import run_default


def solve(input_file: str) -> Tuple[int, int]:
    with open(input_file) as f:
        instructions = f.readlines()

    pc = 0
    cycle = 0
    cur_value = 1

    signal_strength = 0
    defer_value: Optional[int] = None
    grid = [list("." * 40) for _ in range(6)]

    while pc < len(instructions) or defer_value is not None:
        if abs(cur_value - (cycle % 40)) <= 1:
            row, col = divmod(cycle, 40)
            grid[row][col] = "#"

        cycle += 1
        if (cycle + 20) % 40 == 0:
            signal_strength += cycle * cur_value

        if defer_value is not None:
            cur_value += defer_value
            defer_value = None
        else:
            match instructions[pc].split(" "):
                case "noop":
                    defer_value = None
                case "addx", val_str:
                    defer_value = int(val_str)
            pc += 1

    grid_str = "\n".join("".join(line) for line in grid)
    print(f"\n{grid_str}\n")

    return (signal_strength, 0)


run_default(__file__, solve, 13140)
