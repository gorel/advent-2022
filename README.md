[![Update README ⭐](https://github.com/jrodal98/advent-of-code-2022/actions/workflows/readme-stars.yml/badge.svg)](https://github.com/jrodal98/advent-of-code-2022/actions/workflows/readme-stars.yml)

# advent-2022

https://adventofcode.com/2022/

<!--- advent_readme_stars table --->
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
