#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

from advent.utils import run_default

TOTAL_MINUTES = 30
PATTERN = re.compile(r"Valve (.*) has flow rate=(.*); tunnels? leads? to valve.? (.*)")


@dataclass(frozen=True)
class Valve:
    label: str
    flow_rate: int
    outputs: List[str]


def cachekey(
    cur_valve: Valve, open_valves: Dict[str, int], remaining: int, cur_flow: int
) -> str:
    open_valve_str = "+".join(sorted(open_valves.keys()))
    cur_valve_str = cur_valve.label
    return f"{cur_valve_str}|{open_valve_str}|{remaining}|{cur_flow}"


def dfs(
    valves: Dict[str, Valve],
    cur_valve: Valve,
    remaining: int,
    open_valves: Dict[str, int],
    cache: Dict[str, int],
    cur_flow: int = 0,
) -> int:
    # tick - increase current flow
    cur_flow += sum(valves[v].flow_rate for v in open_valves)
    key = cachekey(cur_valve, open_valves, remaining, cur_flow)
    if key in cache:
        return cache[key]

    # base case
    if remaining == 0:
        return cur_flow

    # Option 1: open this valve if not open
    best_option = -1
    if cur_valve.label not in open_valves and cur_valve.flow_rate > 0:
        open_valves[cur_valve.label] = TOTAL_MINUTES - remaining
        open_option = dfs(
            valves=valves,
            cur_valve=cur_valve,
            remaining=remaining - 1,
            open_valves=open_valves,
            cur_flow=cur_flow,
            cache=cache,
        )
        best_option = max(best_option, open_option)
        del open_valves[cur_valve.label]

    # Option 2: move to somewhere adjacent
    for adj in cur_valve.outputs:
        move_option = dfs(
            valves=valves,
            cur_valve=valves[adj],
            remaining=remaining - 1,
            open_valves=open_valves,
            cur_flow=cur_flow,
            cache=cache,
        )
        best_option = max(best_option, move_option)

    cache[key] = best_option
    return best_option


def solve(input_file: str) -> Tuple[int, int]:
    valves = {}
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if match := PATTERN.match(line):
                label = match.group(1)
                flow_rate = int(match.group(2))
                outputs = [s.strip() for s in match.group(3).split(",")]
                valves[label] = Valve(label, flow_rate, outputs)
            else:
                raise ValueError(f"Could not parse `{line}`")

    part1 = dfs(
        valves=valves,
        cur_valve=valves["AA"],
        remaining=TOTAL_MINUTES - 1,
        open_valves={},
        cache={},
    )

    return (part1, 0)


run_default(__file__, solve, 1651)
