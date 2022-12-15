#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import Tuple

# Very useful for this problem...
import tqdm

from advent.utils import run_default


@dataclass(frozen=True)
class Point:
    x: int
    y: int


PART1_Y = 2_000_000
PATTERN = re.compile(r"Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)")


class Sensor:
    def __init__(self, loc: Point, closest_beacon: Point) -> None:
        self.loc = loc
        self.closest_dist = self.dist_to(closest_beacon)

    def dist_to(self, beacon: Point) -> int:
        return abs(self.loc.x - beacon.x) + abs(self.loc.y - beacon.y)

    def is_in_range(self, p: Point) -> int:
        return self.dist_to(p) <= self.closest_dist

    def first_valid_y_after(self, p: Point) -> int:
        # What the hell is this? I'm solving inequalities.
        # Hope this is right...
        # find (p.x, y) s.t. self.dist_to(p2) > self.closest_dist
        # self.dist_to(p.x, y) > self.closest_dist
        # abs(self.loc.x - p.x) + abs(self.loc.y - y) > self.closest_dist
        # xdiff = abs(self.loc.x - p.x)
        # abs(self.loc.y - y) > self.closest_dist - xdiff
        # y - self.loc.y > self.closest_dist - xdiff
        # y > self.closest_dist - xdiff + self.loc.y
        return self.closest_dist - abs(self.loc.x - p.x) + self.loc.y + 1

    def first_valid_x_after(self, p: Point) -> int:
        # Same logic as above?
        return self.closest_dist - abs(self.loc.y - p.y) + self.loc.x + 1


def solve(input_file: str) -> Tuple[int, int]:
    part1_target = 2000000
    min_loc = 0
    max_loc = 4000000 + 1
    if input_file.endswith("test.txt"):
        part1_target = 10
        max_loc = 20

    sensors = set()
    beacons = set()
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if match := PATTERN.match(line):
                loc = Point(int(match.group(1)), int(match.group(2)))
                beacon = Point(int(match.group(3)), int(match.group(4)))
                sensor = Sensor(loc, beacon)
                sensors.add(sensor)
                beacons.add(beacon)
            else:
                raise ValueError(f"Couldn't parse `{line}`")

    # Find the relevant bounds for x
    min_x = list(sensors)[0].loc.x
    max_x = list(sensors)[0].loc.x
    relevant_sensors = {
        s for s in sensors if s.is_in_range(Point(s.loc.x, part1_target))
    }
    for sensor in relevant_sensors:
        min_x = min(min_x, sensor.loc.x - sensor.closest_dist)
        max_x = max(max_x, sensor.loc.x + sensor.closest_dist)

    part1 = 0
    x = min_x
    while x <= max_x:
        p = Point(x, part1_target)
        no_sensors_in_range = True
        for sensor in sensors:
            if sensor.is_in_range(p):
                no_sensors_in_range = False
                # Jump x forward
                next_x = sensor.first_valid_x_after(p)
                # Assume everything in between is invalid
                # We have to make a minor adjustment later
                part1 += next_x - x
                x = next_x
                break
        if no_sensors_in_range:
            x += 1
    # If we ever marked a space as invalid, but it contained
    # another element (a sensor or beacon), un-count that now
    for beacon in beacons:
        if min_x <= beacon.x <= max_x and beacon.y == part1_target:
            part1 -= 1

    # Part 2
    part2 = None
    for x in tqdm.trange(min_loc, max_loc):
        y = min_loc
        while y < max_loc:
            p = Point(x, y)
            can_be_here = True
            for sensor in sensors:
                if sensor.is_in_range(p):
                    # Jump y forward
                    y = max(y, sensor.first_valid_y_after(p))
                    can_be_here = False
                    break

            if can_be_here:
                part2 = p.x * 4000000 + p.y
                break
        if part2 is not None:
            break

    assert part2 is not None
    return (part1, part2)


run_default(__file__, solve, 26, 56000011)
