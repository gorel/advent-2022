#!/usr/bin/env python3

from __future__ import annotations

import copy
import functools
import re
from dataclasses import dataclass
from typing import Dict, FrozenSet

from advent.utils import run_default

SEARCH_TIME = 30
ELEPHANT_SEARCH_TIME = 26
ELEPHANT_TRAINING_TIME = 4
PATTERN = re.compile(r"Valve (.*) has flow rate=(.*); tunnels? leads? to valve.? (.*)")


@dataclass
class Valve:
    label: str
    flow: int
    dist: Dict[str, int]
    is_open: bool = False
    is_being_opened: bool = False


class VolcanoGame:
    def __init__(self, valves: Dict[str, Valve]) -> None:
        self.valves = copy.deepcopy(valves)

    # I struggled on this one for a *long* time. I rewrote this three
    # times before eventually giving up and searching online to figure out
    # my issue. Ultimately, I was influenced heavily by this solution:
    # https://old.reddit.com/r/adventofcode/comments/zn6k1l/2022_day_16_solutions/j0fti6c/
    @functools.cache
    def search(
        self,
        time_left: int,
        unopened: FrozenSet[str],
        cur: str = "AA",
        bring_a_friend: bool = False,
    ) -> int:
        best = 0
        cur_valve = self.valves[cur]
        for valve in unopened:
            dist = cur_valve.dist[valve]
            if dist < time_left:
                time_after_open = time_left - dist - 1
                flow_from_opening = self.valves[valve].flow * time_after_open
                flow_from_other_actions = self.search(
                    time_left=time_after_open,
                    unopened=unopened - {valve},
                    cur=valve,
                    bring_a_friend=bring_a_friend,
                )
                best = max(best, flow_from_opening + flow_from_other_actions)

            if bring_a_friend:
                best = max(
                    best,
                    self.search(
                        ELEPHANT_SEARCH_TIME,
                        unopened=unopened,
                    ),
                )
        return best


def load_input(input_file: str) -> VolcanoGame:
    valves: Dict[str, Valve] = {}
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if match := PATTERN.match(line):
                label = match.group(1)
                flow = int(match.group(2))
                outputs = {s.strip(): 1 for s in match.group(3).split(",")}
                valves[label] = Valve(label, flow, outputs)
            else:
                raise ValueError(f"Could not parse `{line}`")

    # Build dists from important valves using Floyd-Warshall algorithm
    for label_k, valve_k in valves.items():
        for valve_i in valves.values():
            for label_j in valves.keys():
                dist_ij = valve_i.dist.get(label_j, float("inf"))
                dist_ik = valve_i.dist.get(label_k, float("inf"))
                dist_kj = valve_k.dist.get(label_j, float("inf"))
                middle_dist = dist_ik + dist_kj
                if dist_ij > middle_dist:
                    assert isinstance(middle_dist, int)
                    valve_i.dist[label_j] = middle_dist

    # Trick to avoid trying to open valve AA
    # This is okay since it has 0 flow
    valves["AA"].is_open = True

    # Strip all valves with no flow
    useful_valves = {
        label: valve
        for label, valve in valves.items()
        if valve.flow > 0 or label == "AA"
    }

    for valve in useful_valves.values():
        # Only keep dists to useful valves
        valve.dist = {
            k: v
            for k, v in valve.dist.items()
            if k in useful_valves.keys() and k != valve.label
        }

    # Debugging -- show paths from each useful node
    for label, valve in useful_valves.items():
        dists = {ll: valve.dist[ll] for ll in useful_valves if ll != label}
        print(f"{label} => {dists}")

    # Simulate
    return VolcanoGame(useful_valves)


def solve1(input_file: str) -> int:
    game = load_input(input_file)
    unopened = frozenset(game.valves) - {"AA"}
    return game.search(time_left=SEARCH_TIME, unopened=unopened)


def solve2(input_file: str) -> int:
    game = load_input(input_file)
    unopened = frozenset(game.valves) - {"AA"}
    return game.search(
        time_left=ELEPHANT_SEARCH_TIME, unopened=unopened, bring_a_friend=True
    )


run_default(__file__, (solve1, solve2), 1651, 1707)
