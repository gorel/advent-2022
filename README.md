# advent-2022

https://adventofcode.com/2022/

Setup

```
# Recommended
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Running for a given day (let's say day1)

```
python -m advent.day1 [-i INPUT_FILE] [-t TEST_FILE]
```

By default, it uses test.txt as the test file and input.txt for the real input file.
Place these files in the _directory_ of the respective day. So the folder structure is:

```
advent-2022/
    advent/
        __init__.py
        day1/
            __init__.py
            __main__.py
            test.txt
            input.txt
        day2/
            __init__.py
            __main__.py
            test.txt
            input.txt
        ...
```
