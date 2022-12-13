#!/usr/bin/env python3

import functools
from typing import List, Tuple

from advent.utils import run_default

Packet = int | List["Packet"]

DIVIDER_PACKET_1 = [[2]]
DIVIDER_PACKET_2 = [[6]]


def right_order(left: Packet, right: Packet) -> int:
    if isinstance(left, int):
        if isinstance(right, int):
            return left - right
        else:
            return right_order([left], right)
    else:
        if isinstance(right, int):
            return right_order(left, [right])
        else:
            N, M = len(left), len(right)
            for i in range(min(N, M)):
                res = right_order(left[i], right[i])
                if res != 0:
                    return res
            if N < M:
                return -1
            elif N == M:
                return 0
            else:
                return 1


def solve(input_file: str) -> Tuple[int, int]:
    part1 = 0
    pair_idx = 0
    done_reading = False

    all_packets = []
    with open(input_file) as f:
        while not done_reading:
            pair_idx += 1
            try:
                left = eval(next(f))
                right = eval(next(f))
                all_packets.append(left)
                all_packets.append(right)
                if right_order(left, right) < 0:
                    part1 += pair_idx
                # read the empty line
                next(f)
            except StopIteration:
                done_reading = True

    all_packets.append(DIVIDER_PACKET_1)
    all_packets.append(DIVIDER_PACKET_2)
    all_packets.sort(key=functools.cmp_to_key(right_order))
    part2 = (all_packets.index(DIVIDER_PACKET_1) + 1) * (
        all_packets.index(DIVIDER_PACKET_2) + 1
    )

    return (part1, part2)


run_default(__file__, solve, 13, 140)
