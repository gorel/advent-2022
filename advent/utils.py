#!/usr/bin/env python3

import argparse
import datetime
import os
from typing import Callable, Optional, Tuple, TypeVar, Union

T1 = TypeVar("T1")
T2 = TypeVar("T2")

FirstPartSolveFunc = Callable[[str], T1]
SecondPartSolveFunc = Callable[[str], T1]
SolveFunc = Callable[[str], Tuple[T1, T2]]

DEFAULT_TEST_INPUT_NAME = "test.txt"
DEFAULT_INPUT_NAME = "input.txt"


def green(s: str) -> str:
    return f"\033[92m\033[1m{s}\033[0m"


def get_parser(input_filepath: str, test_filepath: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", default=input_filepath)
    parser.add_argument("-t", "--test-file", default=test_filepath)
    return parser


def get_default_test_input_path(main_file: str) -> str:
    directory = os.path.dirname(main_file)
    return os.path.join(directory, DEFAULT_TEST_INPUT_NAME)


def get_default_input_path(main_file: str) -> str:
    directory = os.path.dirname(main_file)
    return os.path.join(directory, DEFAULT_INPUT_NAME)


def validate_test_input(label: str, expected: Optional[T1], actual: T1) -> None:
    if expected is not None:
        assert expected == actual, f"Failed test [{label}]: {expected} != {actual}"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Passed test [{label}] ({now})")


def run_default(
    main_file: str,
    solver: Union[
        SolveFunc[T1, T2], Tuple[FirstPartSolveFunc[T1], SecondPartSolveFunc[T2]]
    ],
    test_solution1: Optional[T1] = None,
    test_solution2: Optional[T2] = None,
) -> None:
    parser = get_parser(
        get_default_input_path(main_file), get_default_test_input_path(main_file)
    )
    args = parser.parse_args()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Starting ({now})")
    res1 = 0
    res2 = 0

    if isinstance(solver, tuple):
        solve1, solve2 = solver
        res1 = solve1(args.test_file)
        validate_test_input("part 1", test_solution1, res1)
        res2 = solve2(args.test_file)
        validate_test_input("part 2", test_solution2, res2)

        real_res1 = solve1(args.input_file)
        print(green(f"Solution 1: {real_res1}"))
        real_res2 = solve2(args.input_file)
        print(green(f"Solution 2: {real_res2}"))
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Finished real input ({now})")
    else:
        res1, res2 = solver(args.test_file)
        validate_test_input("part 1", test_solution1, res1)
        validate_test_input("part 2", test_solution2, res2)
        real_res1, real_res2 = solver(args.input_file)
        print(green(f"Solution 1: {real_res1}"))
        print(green(f"Solution 2: {real_res2}"))

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Finished real input ({now})")
