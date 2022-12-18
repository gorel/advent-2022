#!/usr/bin/env python3

import collections
from typing import Set, Tuple

from advent.utils import run_default

Point3 = Tuple[int, int, int]
BUFFER = 3
DIRS = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]


def prepare(input_file: str) -> Set[Point3]:
    cubes = set()
    with open(input_file) as f:
        for line in f:
            x, y, z = (int(n) for n in line.strip().split(","))
            cubes.add((x, y, z))
    return cubes


def get_source_and_sink(cubes: Set[Point3]) -> Tuple[Point3, Point3]:
    min_x, min_y, min_z = next(iter(cubes))
    max_x, max_y, max_z = next(iter(cubes))
    for x, y, z in cubes:
        min_x, min_y, min_z = min(min_x, x), min(min_y, y), min(min_z, z)
        max_x, max_y, max_z = max(max_x, x), max(max_y, y), max(max_z, z)
    # We add a bit of buffer just to ensure we explore every nook
    # This is totally based on guessing
    source = min_x - BUFFER, min_y - BUFFER, min_z - BUFFER
    sink = max_x + BUFFER, max_y + BUFFER, max_z + BUFFER
    return source, sink


def inbounds(source: Point3, sink: Point3, p: Point3) -> bool:
    min_x, min_y, min_z = source
    max_x, max_y, max_z = sink
    x, y, z = p
    return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z


def solve1(input_file: str) -> int:
    cubes = prepare(input_file)

    surface_area = 0
    for x, y, z in cubes:
        for dx, dy, dz in DIRS:
            if (x + dx, y + dy, z + dz) not in cubes:
                surface_area += 1
    return surface_area


def solve2(input_file: str) -> int:
    cubes = prepare(input_file)
    surface_area = 0

    # We're going _really_ lazy today
    source, sink = get_source_and_sink(cubes)
    visited = set()
    q = collections.deque([source])
    while q:
        x, y, z = q.popleft()
        for dx, dy, dz in DIRS:
            p2 = (x + dx, y + dy, z + dz)
            if not inbounds(source, sink, p2) or p2 in visited:
                continue

            # We've just reached the cube from a new direction
            if p2 in cubes:
                surface_area += 1
            else:
                visited.add(p2)
                q.append(p2)

    return surface_area


run_default(__file__, (solve1, solve2), 64, 58)
