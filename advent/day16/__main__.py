#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from advent.utils import run_default

TOTAL_MINUTES = 30
PATTERN = re.compile(r"Valve (.*) has flow rate=(.*); tunnels? leads? to valve.? (.*)")


@dataclass(frozen=True)
class Valve:
    label: str
    flow_rate: int
    outputs: List[str]


def cachekey(
    cur_valve: Valve,
    open_valves: Set[str],
    remaining: int,
    cur_flow: int,
    ele_valve: Optional[Valve] = None,
) -> str:
    open_valve_str = "+".join(sorted(open_valves))
    cur_valve_str = cur_valve.label
    if ele_valve:
        e_str = ele_valve.label
        return f"{cur_valve_str}|{e_str}|{open_valve_str}|{remaining}|{cur_flow}"
    return f"{cur_valve_str}|{open_valve_str}|{remaining}|{cur_flow}"


def dfs(
    valves: Dict[str, Valve],
    cur_valve: Valve,
    cur_from: Valve,
    remaining: int,
    open_valves: Set[str],
    unopen_valves: Set[str],
    cache: Dict[str, int],
    cur_flow: int = 0,
) -> int:
    # tick - increase current flow
    cur_flow += sum(valves[v].flow_rate for v in open_valves)
    # base case
    if remaining == 0:
        return cur_flow
    elif len(unopen_valves) == 0:
        # The best we can do from here is wait
        return dfs(
            valves=valves,
            cur_valve=cur_valve,
            cur_from=cur_valve,
            remaining=remaining - 1,
            open_valves=open_valves,
            unopen_valves=unopen_valves,
            cache=cache,
            cur_flow=cur_flow,
        )

    # We've seen this exact state before
    key = cachekey(cur_valve, open_valves, remaining, cur_flow)
    if key in cache:
        return cache[key]

    # We've been in a better position before
    partialkey = key.rsplit("|", maxsplit=1)[0]
    if partialkey in cache and cur_flow <= cache[partialkey]:
        return -1

    # Find the best valve available
    best_to_open = None
    for valve in unopen_valves:
        if best_to_open is None:
            best_to_open = valves[valve]
        elif valves[valve].flow_rate > best_to_open.flow_rate:
            best_to_open = valves[valve]

    # Option 1: open this valve if not open
    best_option = -1
    if cur_valve.label not in open_valves and cur_valve.flow_rate > 0:
        open_valves.add(cur_valve.label)
        unopen_valves.remove(cur_valve.label)
        open_option = dfs(
            valves=valves,
            cur_valve=cur_valve,
            cur_from=cur_valve,
            remaining=remaining - 1,
            open_valves=open_valves,
            unopen_valves=unopen_valves,
            cur_flow=cur_flow,
            cache=cache,
        )
        best_option = max(best_option, open_option)
        open_valves.remove(cur_valve.label)
        unopen_valves.add(cur_valve.label)

    # Option 2: move to somewhere adjacent
    # Doesn't make sense if I am at best valve
    if cur_valve != best_to_open:
        for adj in cur_valve.outputs:
            if adj == cur_from:
                # It makes no sense to turn around
                continue
            move_option = dfs(
                valves=valves,
                cur_valve=valves[adj],
                cur_from=cur_valve,
                remaining=remaining - 1,
                open_valves=open_valves,
                unopen_valves=unopen_valves,
                cur_flow=cur_flow,
                cache=cache,
            )
            best_option = max(best_option, move_option)

    cache[key] = best_option
    return best_option


def dfs2(
    valves: Dict[str, Valve],
    cur_valve: Valve,
    ele_valve: Valve,
    cur_from: Valve,
    ele_from: Valve,
    remaining: int,
    open_valves: Set[str],
    unopen_valves: Set[str],
    cache: Dict[str, int],
    cur_flow: int = 0,
) -> int:
    # tick - increase current flow
    cur_flow += sum(valves[v].flow_rate for v in open_valves)
    # base case
    if remaining == 0:
        return cur_flow
    elif len(unopen_valves) == 0:
        # The best we can do from here is wait
        return dfs2(
            valves=valves,
            cur_valve=cur_valve,
            cur_from=cur_valve,
            ele_from=ele_valve,
            ele_valve=ele_valve,
            remaining=remaining - 1,
            open_valves=open_valves,
            unopen_valves=unopen_valves,
            cache=cache,
            cur_flow=cur_flow,
        )

    # Check for short circuit
    # We've seen this exact state before
    key = cachekey(cur_valve, open_valves, remaining, cur_flow, ele_valve)
    if key in cache:
        return cache[key]

    # We've been in a better position before
    partialkey = key.rsplit("|", maxsplit=1)[0]
    if partialkey in cache and cur_flow <= cache[partialkey]:
        # We can't do better; we're at the same state with *lower* flow
        return -1

    best_option = -1
    i_can_open = cur_valve.label not in open_valves and cur_valve.flow_rate > 0
    ele_can_open = ele_valve.label not in open_valves and ele_valve.flow_rate > 0

    best_to_open = None
    for valve in valves.values():
        if best_to_open is None:
            best_to_open = valve
        elif (
            valve.label not in open_valves and valve.flow_rate > best_to_open.flow_rate
        ):
            best_to_open = valve

    # Option 1: both open valve (if not at same spot)
    if i_can_open and ele_can_open and cur_valve.label != ele_valve.label:
        open_valves.add(cur_valve.label)
        open_valves.add(ele_valve.label)
        unopen_valves.remove(cur_valve.label)
        unopen_valves.remove(ele_valve.label)
        open_option = dfs2(
            valves=valves,
            cur_valve=cur_valve,
            cur_from=cur_valve,
            ele_valve=ele_valve,
            ele_from=ele_valve,
            remaining=remaining - 1,
            open_valves=open_valves,
            unopen_valves=unopen_valves,
            cur_flow=cur_flow,
            cache=cache,
        )
        best_option = max(best_option, open_option)
        open_valves.remove(cur_valve.label)
        open_valves.remove(ele_valve.label)
        unopen_valves.add(cur_valve.label)
        unopen_valves.add(ele_valve.label)

    # Option 2: you open valve and elephant moves
    # Doesn't make sense if elephant at best valve
    if ele_valve != best_to_open and i_can_open:
        open_valves.add(cur_valve.label)
        unopen_valves.remove(cur_valve.label)
        for adj in ele_valve.outputs:
            if adj == ele_from:
                # It makes no sense to turn around
                continue
            open_option = dfs2(
                valves=valves,
                cur_valve=cur_valve,
                ele_valve=valves[adj],
                cur_from=cur_valve,
                ele_from=ele_valve,
                remaining=remaining - 1,
                open_valves=open_valves,
                unopen_valves=unopen_valves,
                cur_flow=cur_flow,
                cache=cache,
            )
            best_option = max(best_option, open_option)
        open_valves.remove(cur_valve.label)
        unopen_valves.add(cur_valve.label)

    # Option 3: elephant opens valve and you move
    # Doesn't make sense if I am at best valve
    if cur_valve != best_to_open and ele_can_open:
        open_valves.add(ele_valve.label)
        unopen_valves.remove(ele_valve.label)
        for adj in cur_valve.outputs:
            if adj == cur_from:
                # It makes no sense to turn around
                continue
            open_option = dfs2(
                valves=valves,
                cur_valve=valves[adj],
                ele_valve=ele_valve,
                cur_from=cur_valve,
                ele_from=ele_valve,
                remaining=remaining - 1,
                open_valves=open_valves,
                unopen_valves=unopen_valves,
                cur_flow=cur_flow,
                cache=cache,
            )
            best_option = max(best_option, open_option)
        open_valves.remove(ele_valve.label)
        unopen_valves.add(ele_valve.label)

    # Option 4: both move
    # Doesn't make sense if either at best valve
    if cur_valve != best_to_open and ele_valve != best_to_open:
        for my_adj in cur_valve.outputs:
            if my_adj == cur_from:
                # It makes no sense to turn around
                continue
            for ele_adj in ele_valve.outputs:
                if ele_adj == ele_from:
                    # It makes no sense to turn around
                    continue
                move_option = dfs2(
                    valves=valves,
                    cur_valve=valves[my_adj],
                    ele_valve=valves[ele_adj],
                    cur_from=cur_valve,
                    ele_from=ele_valve,
                    remaining=remaining - 1,
                    open_valves=open_valves,
                    unopen_valves=unopen_valves,
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

    unopen_valves = {k for k, v in valves.items() if v.flow_rate > 0}
    part1 = dfs(
        valves=valves,
        cur_valve=valves["AA"],
        cur_from=valves["AA"],
        remaining=TOTAL_MINUTES - 1,
        open_valves=set(),
        unopen_valves=unopen_valves,
        cache={},
    )

    part2 = dfs2(
        valves=valves,
        cur_valve=valves["AA"],
        ele_valve=valves["AA"],
        cur_from=valves["AA"],
        ele_from=valves["AA"],
        remaining=TOTAL_MINUTES - 4 - 1,
        open_valves=set(),
        unopen_valves=unopen_valves,
        cache={},
    )

    return (part1, part2)


run_default(__file__, solve, 1651, 1707)
