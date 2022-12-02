#!/usr/bin/env python3

import argparse
import os
from typing import Callable, Optional, Tuple

SolveFunc = Callable[[str], Tuple[int, int]]

DEFAULT_TEST_INPUT_NAME = "test.txt"
DEFAULT_INPUT_NAME = "input.txt"


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


def run_default(
    main_file: str,
    solve: SolveFunc,
    test_solution1: Optional[int] = None,
    test_solution2: Optional[int] = None,
) -> None:
    parser = get_parser(
        get_default_input_path(main_file), get_default_test_input_path(main_file)
    )
    args = parser.parse_args()

    res1, res2 = solve(args.test_file)
    if test_solution1 is not None:
        assert res1 == test_solution1, "Failed test for part 1"
    if test_solution2 is not None:
        assert res2 == test_solution2, "Failed test for part 2"

    res1, res2 = solve(args.input_file)
    print(f"Solution 1: {res1}")
    print(f"Solution 2: {res2}")
