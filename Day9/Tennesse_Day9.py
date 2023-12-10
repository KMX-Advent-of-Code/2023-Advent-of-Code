"""
Day 9: Mirage Maintenance
https://adventofcode.com/2023/day/9
"""
from utilities import run_aoc
import numpy as np


def run_part1(input_text: str) -> int:
    return sum(extrapolate_polynomial(row, len(row)) for row in parse_input(input_text))


def run_part2(input_text: str) -> int:
    return sum(extrapolate_polynomial(row, -1) for row in parse_input(input_text))


def parse_input(input_text: str) -> list[tuple[str, int]]:
    return [[int(x) for x in line.split()] for line in input_text.splitlines()]


def extrapolate_polynomial(y: list[int], x_new: int) -> int:
    """The procedure described in the problem is just Newton's divided
    differences algorithm (https://en.wikipedia.org/wiki/Newton_polynomial)
    which fits a polynomial of degree N-1 to N data points. Instead of
    implementing that manually, I can just use numpy's implementation.
    """
    return round(
        np.polynomial.Polynomial.fit(np.arange(len(y)), y, deg=len(y) - 1)(x_new)
    )


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
