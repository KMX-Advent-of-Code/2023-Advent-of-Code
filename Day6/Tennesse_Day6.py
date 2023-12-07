"""
Day 6: Wait For It
https://adventofcode.com/2023/day/6
"""
import logging
from utilities import run_aoc
import numpy as np


def run_part1(input_text: str) -> int:
    """
    Count the number of options to win each race, and return the product.
    """
    times, best_distances = parse_input(input_text)
    logging.debug("times: %s, best_distances: %s", times, best_distances)
    num_options = []
    for t, d in zip(times, best_distances):
        result = get_num_options_formula(t, d)
        logging.debug("t: %s, d: %s, result: %s", t, d, result)
        num_options.append(result)
    return np.prod(num_options)


def run_part2(input_text: str) -> int:
    """
    Concatenate all the input numbers together, and calculate the number
    of options for that single longer race.
    """
    times, best_distances = parse_input(input_text)
    time = concat_ints(times)
    best_distance = concat_ints(best_distances)
    logging.debug("time: %s, best_distance: %s", time, best_distance)
    return get_num_options_formula(time, best_distance)


def parse_input(input_text: str) -> list:
    """
    Parse input text into two lists of integers, one for times and
    one for distances.
    """
    lines = input_text.split("\n")
    times = [int(t) for t in lines[0].split()[1:]]
    distances = [int(d) for d in lines[1].split()[1:]]
    return times, distances


def concat_ints(ints: list[int]) -> int:
    """
    Concatenate a list of integers into a single integer.
    """
    return int("".join([str(i) for i in ints]))


def get_num_options_brute_force(t, d) -> int:
    """
    Brute force method to get the number of options for a given time and
    distance.
    """
    time_pressed = np.arange(t + 1)
    distance_travelled = time_pressed * (t - time_pressed)
    return np.sum(distance_travelled > d)


def get_num_options_formula(t, d) -> int:
    """
    Formulaic method to get the number of options for a given time and
    distance.
    """
    # Radius around the optimal button press time (t/2) that will still
    # result in winning the race.
    radius = 0.5 * np.sqrt(t**2 - 4 * d)
    # Min and max time for the button press, as integers.
    min_time = int(np.ceil(t / 2 - radius + 1e-6))
    max_time = int(np.floor(t / 2 + radius - 1e-6))
    # Return the number of integers between the min and max times, inclusive.
    return max_time - min_time + 1


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
