#!/usr/bin/env python3

from __future__ import annotations

import re
from typing import List, Tuple

from advent.utils import run_default

MONKEY_START_REGEX = re.compile(r"Monkey (\d+):")
ITEMS_REGEX = re.compile(r"Starting items: (.*)")
OPERATION_REGEX = re.compile(r"Operation: new = old (.) (\w+)")
TEST_DIVISOR_REGEX = re.compile(r"Test: divisible by (\d+)")
TEST_TRUE_REGEX = re.compile(r"If true: throw to monkey (\d+)")
TEST_FALSE_REGEX = re.compile(r"If false: throw to monkey (\d+)")


def tryint(s: str) -> str | int:
    try:
        return int(s)
    except Exception:
        return s


class Monkey:
    def __init__(
        self,
        items: List[int],
        operator: str,
        operand: str | int,
        divisor: int,
        true_monkey: int,
        false_monkey: int,
    ) -> None:
        self.items = items
        self.operator = operator
        self.operand = operand
        self.divisor = divisor
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspections = 0

    def inspect_items(
        self, monkeys: List[Monkey], reduce_worry_after_inspection: bool, lcm: int
    ) -> None:
        for item in self.items:
            self.inspections += 1
            new_worry_level = self.apply_formula(item)
            if reduce_worry_after_inspection:
                new_worry_level //= 3
            new_worry_level %= lcm
            if new_worry_level % self.divisor == 0:
                monkeys[self.true_monkey].items.append(new_worry_level)
            else:
                monkeys[self.false_monkey].items.append(new_worry_level)
        self.items = []

    def apply_formula(self, item: int) -> int:
        operand = self.operand
        if isinstance(self.operand, str):
            operand = item
        # The type checker somehow isn't smart enough to figure this out
        assert isinstance(operand, int)

        match self.operator:
            case "+":
                return item + operand
            case "*":
                return item * operand
            case _:
                raise ValueError("You messed up in parsing")

    @classmethod
    def from_input(cls, s_list: List[str]) -> Monkey:
        items_match = ITEMS_REGEX.search(s_list[0])
        assert items_match is not None

        operation_match = OPERATION_REGEX.search(s_list[1])
        assert operation_match is not None

        test_divisor_match = TEST_DIVISOR_REGEX.search(s_list[2])
        assert test_divisor_match is not None

        test_true_match = TEST_TRUE_REGEX.search(s_list[3])
        assert test_true_match is not None

        test_false_match = TEST_FALSE_REGEX.search(s_list[4])
        assert test_false_match is not None

        return Monkey(
            items=[int(x) for x in items_match.group(1).split(",")],
            operator=operation_match.group(1),
            operand=tryint(operation_match.group(2)),
            divisor=int(test_divisor_match.group(1)),
            true_monkey=int(test_true_match.group(1)),
            false_monkey=int(test_false_match.group(1)),
        )


class MonkeySimulator:
    def __init__(self) -> None:
        self.monkeys = []

    def add(self, monkey: Monkey) -> None:
        self.monkeys.append(monkey)

    def run_one_round(self, reduce_worry_after_inspection: bool, lcm: int) -> None:
        for monkey in self.monkeys:
            monkey.inspect_items(self.monkeys, reduce_worry_after_inspection, lcm)

    def simulate(self, num_rounds: int, reduce_worry_after_inspection: bool) -> int:
        lcm = 1
        for monkey in self.monkeys:
            monkey.inspections = 0
            lcm *= monkey.divisor

        for _ in range(num_rounds):
            self.run_one_round(reduce_worry_after_inspection, lcm)

        two_most_active = sorted(
            self.monkeys, key=lambda monkey: monkey.inspections, reverse=True
        )[:2]
        return two_most_active[0].inspections * two_most_active[1].inspections

    @classmethod
    def from_input_file(cls, input_file: str) -> MonkeySimulator:
        sim = MonkeySimulator()
        with open(input_file) as f:
            monkey_input = []
            for line in f:
                line = line.strip()
                if match := MONKEY_START_REGEX.search(line):
                    monkey_id = int(match.group(1))
                    assert monkey_id == len(sim.monkeys)
                    monkey_input = []
                elif len(line) == 0:
                    sim.add(Monkey.from_input(monkey_input))
                else:
                    monkey_input.append(line)
            # Remember the last monkey
            sim.add(Monkey.from_input(monkey_input))
        return sim


def solve(input_file: str) -> Tuple[int, int]:
    sim = MonkeySimulator.from_input_file(input_file)
    part1 = sim.simulate(20, reduce_worry_after_inspection=True)

    # Since the inspection process changes the values of items,
    # we must reload the file. Otherwise we get the wrong answer.
    sim_part2 = MonkeySimulator.from_input_file(input_file)
    part2 = sim_part2.simulate(10000, reduce_worry_after_inspection=False)

    return (part1, part2)


run_default(__file__, solve, 10605, 2713310158)
