#!/usr/bin/env python3

from __future__ import annotations

import re
from typing import Generator, Optional, Tuple

from advent.utils import run_default

MAX_SIZE = 100000
DISK_SPACE_AVAILABLE = 70000000
REQUIRED_SPACE = 30000000

CD_CMD = re.compile(r"^\$ cd (.*)")
LS_CMD = re.compile(r"^\$ ls")


class File:
    def __init__(
        self,
        name: str,
        parent: Optional[File] = None,
        is_dir: bool = True,
        size: int = 0,
    ) -> None:
        self.name = name
        self.parent = parent
        self.is_dir = is_dir
        self.size = size

        self.files = {}

    def root(self) -> File:
        cur = self
        while cur.parent is not None:
            cur = cur.parent
        return cur

    def cd(self, path: str) -> File:
        if path == "/":
            return self.root()

        cur = self
        for part in path.split("/"):
            assert cur is not None
            if part == "..":
                # Hack to allow this to work in root dir
                cur = cur.parent or cur
            else:
                cur.files[part] = File(part, parent=cur)
                cur = cur.files[part]
        return cur

    def record(self, line: str) -> None:
        if line.startswith("dir "):
            dirname = line[len("dir ") :]
            if dirname not in self.files:
                self.files[dirname] = File(dirname, parent=self)
        else:
            size_str, name = line.split(" ")
            self.files[name] = File(name, parent=self, is_dir=False, size=int(size_str))

    def size_recursive(self) -> int:
        if self.is_dir:
            return sum(f.size_recursive() for f in self.files.values())
        else:
            return self.size

    def __str__(self, indent: int = 0) -> str:
        s = " " * indent
        if self.is_dir:
            s += f"{self.name}/\n"
            for f in self.files.values():
                s += f.__str__(indent=indent + 2)
            pass
        else:
            s += f"{self.name} ({self.size})\n"
        return s

    def walk(self) -> Generator[File, None, None]:
        yield self
        for f in self.files.values():
            yield from f.walk()


def solve(input_file: str) -> Tuple[int, int]:
    root = File("")
    cwd = root

    with open(input_file) as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if match := CD_CMD.match(line):
                cwd = cwd.cd(match.group(1))
                i += 1
            elif match := LS_CMD.match(line):
                i += 1
                while i < len(lines) and lines[i][0] != "$":
                    next_res = lines[i].strip()
                    cwd.record(next_res)
                    i += 1

    unused_space = DISK_SPACE_AVAILABLE - root.size_recursive()
    needed_to_free = REQUIRED_SPACE - unused_space

    total = 0
    min_winner = float("inf")
    for f in root.walk():
        if f.is_dir:
            size = f.size_recursive()

            # Part 1
            if size <= MAX_SIZE:
                total += size
            # Part 2
            if needed_to_free <= size < min_winner:
                min_winner = size

    return (total, int(min_winner))


run_default(__file__, solve, 95437, 24933642)
