#!/usr/bin/env python3

from advent.utils import run_default


def solve(r):
    s = open(r).read()
    f = lambda n: [i for i in range(n, len(s)) if len(s[i - n : i]) == len(set(s[i - n : i]))][0]
    return f(4), f(14)


run_default(__file__, solve, 7, 19)
