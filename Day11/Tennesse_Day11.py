"""
Day 11: Cosmic Expansion
https://adventofcode.com/2023/day/11
"""
import logging
from utilities import run_aoc
import numpy as np


def run_part1(input_text: str) -> int:
    """Expand the space between galaxies, and calculate the total
    distance between all pairs of galaxies.
    """
    coordinates = parse_input(input_text)
    logging.debug("Initial coordinates: \n%s", display(coordinates))

    coordinates = expand_2d(coordinates)
    logging.debug("Expanded coordinates: \n%s", display(coordinates))

    total_distance = 0
    for i, galaxy1 in enumerate(coordinates):
        for j, galaxy2 in enumerate(coordinates):
            if j >= i:
                break
            distance = get_distance(galaxy1, galaxy2)
            logging.debug("Distance between %s and %s is %s", j + 1, i + 1, distance)
            total_distance += distance
    return total_distance


def run_part2(input_text: str) -> int:
    """Expand the space between galaxies a million times, and calculate
    the total distance between all pairs of galaxies.
    """
    coordinates = parse_input(input_text)
    coordinates = expand_2d(coordinates, expansion_factor=1_000_000)
    total_distance = 0
    for i, galaxy1 in enumerate(coordinates):
        for j, galaxy2 in enumerate(coordinates):
            if j >= i:
                break
            distance = get_distance(galaxy1, galaxy2)
            total_distance += distance
    return total_distance


def parse_input(input_text: str):
    """Parse the input text into a list of coordinates."""
    return [
        (i, j)
        for i, line in enumerate(input_text.splitlines())
        for j, char in enumerate(line)
        if char == "#"
    ]


def expand_1d(x, expansion_factor=2):
    """Expand a 1d array of integers, adding space whenever a
    value is missing from the list.
    """
    offsets = np.cumsum(np.bincount(x) == 0)
    return [x_i + (expansion_factor - 1) * int(offsets[x_i]) for x_i in x]


def expand_2d(coordinates, expansion_factor=2):
    """Expand a 2d array of coordinates, adding space whenever a
    row or column is missing from the list.
    """
    x, y = zip(*coordinates)
    x = expand_1d(x, expansion_factor)
    y = expand_1d(y, expansion_factor)
    return list(zip(x, y))


def display(coordinates):
    """Display a list of coordinates as a grid. Reverse of
    parse_input.
    """
    x, y = zip(*coordinates)
    x_max = max(x)
    y_max = max(y)
    grid = np.zeros((x_max + 1, y_max + 1), dtype=int)
    grid[x, y] = 1
    return "\n".join("".join("#" if cell else "." for cell in row) for row in grid)


def get_distance(p1, p2):
    """Get the distance between two points."""
    return sum(abs(p1_i - p2_i) for p1_i, p2_i in zip(p1, p2))


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
