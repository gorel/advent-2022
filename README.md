[![Update README ⭐](https://github.com/gorel/advent-2022/actions/workflows/readme-stars.yml/badge.svg)](https://github.com/gorel/advent-2022/actions/workflows/readme-stars.yml)

# advent-2022

https://adventofcode.com/2022/

<!--- advent_readme_stars table --->
## 2022 Results

| Day | Part 1 | Part 2 |
| :---: | :---: | :---: |
| [Day 1](https://adventofcode.com/2022/day/1) | ⭐ | ⭐ |
| [Day 2](https://adventofcode.com/2022/day/2) | ⭐ | ⭐ |
| [Day 3](https://adventofcode.com/2022/day/3) | ⭐ | ⭐ |
| [Day 4](https://adventofcode.com/2022/day/4) | ⭐ | ⭐ |
| [Day 5](https://adventofcode.com/2022/day/5) | ⭐ | ⭐ |
| [Day 6](https://adventofcode.com/2022/day/6) | ⭐ | ⭐ |
| [Day 7](https://adventofcode.com/2022/day/7) | ⭐ | ⭐ |
| [Day 8](https://adventofcode.com/2022/day/8) | ⭐ | ⭐ |
| [Day 9](https://adventofcode.com/2022/day/9) | ⭐ | ⭐ |
| [Day 10](https://adventofcode.com/2022/day/10) | ⭐ | ⭐ |
| [Day 11](https://adventofcode.com/2022/day/11) | ⭐ | ⭐ |
| [Day 12](https://adventofcode.com/2022/day/12) | ⭐ | ⭐ |
| [Day 13](https://adventofcode.com/2022/day/13) | ⭐ | ⭐ |
| [Day 14](https://adventofcode.com/2022/day/14) | ⭐ | ⭐ |
<!--- advent_readme_stars table --->

## Setup

```
# Recommended
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Running for a given day (let's say day01)

```
python -m advent.day01 [-i INPUT_FILE] [-t TEST_FILE]
```

By default, it uses test.txt as the test file and input.txt for the real input file.
Place these files in the _directory_ of the respective day. So the folder structure is:

```
advent-2022/
    advent/
        __init__.py
        day01/
            __init__.py
            __main__.py
            test.txt
            input.txt
        day02/
            __init__.py
            __main__.py
            test.txt
            input.txt
        ...
```
