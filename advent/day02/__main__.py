#!/usr/bin/env python3

from typing import Tuple

from advent.utils import run_default

# Precompute lol
SCORE = {
    # They choose rock, we choose rock-paper-scissors
    "A X": 1 + 3,  # draw
    "A Y": 2 + 6,  # win
    "A Z": 3 + 0,  # loss
    # They choose paper, we choose rock-paper-scissors
    "B X": 1 + 0,  # loss
    "B Y": 2 + 3,  # draw
    "B Z": 3 + 6,  # win
    # They choose scissors, we choose rock-paper-scissors
    "C X": 1 + 6,  # win
    "C Y": 2 + 0,  # loss
    "C Z": 3 + 3,  # draw
}
SCORE2 = {
    # They choose rock, we must lose-draw-win
    "A X": 3 + 0,  # choose scissors
    "A Y": 1 + 3,  # choose rock
    "A Z": 2 + 6,  # choose paper
    # They choose paper, we must lose-draw-win
    "B X": 1 + 0,  # choose rock
    "B Y": 2 + 3,  # choose paper
    "B Z": 3 + 6,  # choose scissors
    # They choose scissors, we must lose-draw-win
    "C X": 2 + 0,  # choose paper
    "C Y": 3 + 3,  # choose scissors
    "C Z": 1 + 6,  # choose rock
}


def solve(input_file: str) -> Tuple[int, int]:
    score = 0
    score2 = 0
    with open(input_file) as f:
        for line in f:
            score += SCORE[line.strip()]
            score2 += SCORE2[line.strip()]
    return (score, score2)


run_default(__file__, solve, 15, 12)
