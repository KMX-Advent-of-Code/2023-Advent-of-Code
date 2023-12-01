"""
Day 1: Trebuchet?!
https://adventofcode.com/2023/day/1
"""
import logging
import argparse
import re

DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filepath", type=str)
    parser.add_argument("part", type=int, default=1, choices=[1, 2])
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main() -> None:
    """
    Main function that loads the input, calculates calibration values, and logs the results.
    """
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Load the input
    with open(args.input_filepath, "r", encoding="utf-8") as f:
        inputs = [line.strip() for line in f.readlines()]

    logging.debug(inputs)

    if args.part == 1:
        logging.info("Running Part 1...")
        calibration_values1 = [get_calibration_value1(line) for line in inputs]
        logging.debug(calibration_values1)
        logging.info(sum(calibration_values1))
    elif args.part == 2:
        logging.info("Running Part 2...")
        calibration_values1 = [get_calibration_value2(line) for line in inputs]
        logging.debug(calibration_values1)
        logging.info(sum(calibration_values1))


def get_calibration_value1(line: str) -> int:
    """
    Get the calibration value from a line using the first method.
    """
    matches = re.findall("(\d)", line)
    logging.debug(line)
    logging.debug(matches)
    return int(matches[0] + matches[-1])


def get_calibration_value2(line: str) -> int:
    """
    Get the calibration value from a line using the second method.
    """
    matches = find_all_overlapping("(" + "|".join(DIGITS) + "|\d)", line)
    logging.debug(line)
    logging.debug(matches)
    return 10 * to_int(matches[0]) + to_int(matches[-1])


def to_int(digit: str) -> int:
    """
    Convert a digit (either a string representation or an actual digit) to an integer.
    """
    if digit.isdigit():
        return int(digit)
    else:
        return DIGITS.index(digit) + 1


def find_all_overlapping(pattern: str, string: str) -> list[str]:
    """
    Find all overlapping matches of a pattern in a string.

    I initially used re.findall, but that gives the wrong answer in
    Part 2 because it ignores overlapping matches.
    """
    pattern = "(?=(" + pattern + "))"
    return [match.group(1) for match in re.finditer(pattern, string)]


if __name__ == "__main__":
    main()
