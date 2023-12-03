"""
Day 3: Gear Ratios
https://adventofcode.com/2023/day/3
"""
import logging
import argparse
import pathlib
from typing import Iterator


def run_part1(input_text: str) -> int:
    """
    Find all part numbers that are next to a symbol, and return their sum.
    """
    # Get locations of all symbols.
    symbol_locs = [(x, y) for x, y, value in grid_iter(input_text) if is_symbol(value)]
    # Get locations of all squares next to any symbol.
    next_to_symbol = {n for x, y in symbol_locs for n in get_neighbors(x, y)}

    # Iterate over the grid and look for part numbers next to symbols.
    counter = EngineCounter()
    for x, y, value in grid_iter(input_text):
        if x == 0:
            # If we're at the beginning of a row, finish the current part.
            counter.finish_part()
        if value.isdigit():
            # If we're at a digit, add it to the current part number.
            counter.add(int(value))
            if (x, y) in next_to_symbol:
                # If this digit is next to a symbol, mark the current part
                # number as valid.
                counter.mark_valid()
        else:
            # The part number has ended.
            counter.finish_part()
    # Make sure to finish the last part.
    counter.finish_part()
    # Return the sum of all part numbers.
    return sum(counter.part_numbers)


def run_part2(input_text: str) -> int:
    """
    Find all gears (asterisks next to exactly two part numbers) and return the
    sum of the gear ratios (products of the two part numbers).
    """
    # Get locations of all asterisks.
    asterisks = [(x, y) for x, y, value in grid_iter(input_text) if value == "*"]
    # Build a dictionary where the keys are locations of squares next to one
    # or more asterisks, and the values are sets of locations of asterisks
    # that they're next to.
    adjacency = {}
    for aloc in asterisks:
        for nloc in get_neighbors(*aloc):
            # The setdefault method will initialize the entry to an empty set
            # if it doesn't already exist. Then we add the current asterisk
            # location to that set.
            adjacency.setdefault(nloc, set()).add(aloc)
    logging.debug("Neighboring gears:\n%s", adjacency)

    # Iterate over the grid and look for part numbers next to asterisks.
    counter = GearCounter()
    for x, y, value in grid_iter(input_text):
        if x == 0:
            # If we're at the beginning of a row, finish the current part.
            counter.finish_part()
        if value.isdigit():
            # If we're at a digit, add it to the current part number.
            counter.add(int(value))
            if (x, y) in adjacency:
                # If this digit is next to an asterisk, connect the current
                # part to that asterisk.
                counter.connect(adjacency[(x, y)])
        else:
            # The part number has ended.
            counter.finish_part()
    # Make sure to finish the last part.
    counter.finish_part()

    # Iterate over all asterisks found in the previous steps, identify which
    # ones are gears, and calculate the gear ratios.
    sum_of_ratios = 0
    for aloc, part_numbers in counter.part_numbers_by_asterisk.items():
        logging.debug("Asterisk at %s has part numbers %s", aloc, part_numbers)
        if len(part_numbers) == 2:
            # An asterisk is a gear if it's next to exactly two part numbers.
            gear_ratio = part_numbers[0] * part_numbers[1]
            logging.debug("\tThis is a gear with ratio %s", gear_ratio)
            sum_of_ratios += gear_ratio
        else:
            logging.debug("\tThis is not a gear")
    return sum_of_ratios


def grid_iter(input_text: str) -> Iterator[tuple[int, int, str]]:
    """
    Iterate over the input text, yielding a tuple of (x, y, value) for each
    square in the grid.
    """
    for y, line in enumerate(input_text.split("\n")):
        for x, value in enumerate(line):
            yield x, y, value


def is_symbol(value: str) -> bool:
    """
    Check if a character is a symbol (i.e., not a digit or a period).
    """
    return value not in "0123456789."


def get_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    """
    Return a list of the coordinates of the neighbors of the square at (x, y).
    Doesn't account for the edges of the grid, but that's okay for this problem.
    """
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors


class EngineCounter:
    """Helper class for counting part numbers next to symbols.

    Example usage:
    >>> counter = EngineCounter()
    >>> counter.add(1)
    >>> counter.add(2)
    >>> counter.mark_valid()
    >>> counter.finish_part()
    >>> counter.add(3)
    >>> counter.mark_valid()
    >>> counter.add(4)
    >>> counter.finish_part()
    >>> counter.add(5)
    >>> counter.finish_part()
    >>> counter.part_numbers
    [12, 34]

    If a part is finished without being marked valid (like 5 in the
    example), that part number won't be included in the overall list.
    """

    def __init__(self):
        self.part_numbers = []
        self.current = 0
        self.valid = False

    def add(self, value):
        """Add a digit to the current part number."""
        self.current = 10 * self.current + value

    def mark_valid(self):
        """
        Mark the current part number as valid (i.e., it's next to a symbol).
        """
        self.valid = True

    def finish_part(self):
        """
        Finish the current part number and, if it's valid,  add it to the
        overall list of part numbers.
        """
        if self.valid:
            logging.debug("Found valid part number: %s", self.current)
            self.part_numbers.append(self.current)
        elif self.current > 0:
            logging.debug("Invalid part number: %s", self.current)
        self.current = 0
        self.valid = False


class GearCounter:
    """Helper class for counting gears. As the input is parsed, it
    it keeps track of which part numbers were next to each asterisk.

    Example usage:
    >>> counter = GearCounter()
    >>> counter.add(1)
    >>> counter.add(2)
    >>> counter.connect({(0, 0)})
    >>> counter.finish_part()
    >>> counter.add(3)
    >>> counter.connect({(0, 0), (1, 0)})
    >>> counter.add(4)
    >>> counter.connect({(2, 0)})
    >>> counter.finish_part()
    >>> counter.add(5)
    >>> counter.finish_part()
    >>> counter.part_numbers_by_asterisk
    {(0, 0): [12, 34], (1, 0): [34], (2, 0): [34]}
    """

    def __init__(self):
        self.part_numbers_by_asterisk = {}
        self.current = 0
        self.asterisks = set()

    def add(self, value):
        """Add a digit to the current part number."""
        self.current = 10 * self.current + value

    def connect(self, aloc: set[tuple[int, int]]):
        """Connect the current part number to the asterisks at the given
        locations."""
        self.asterisks |= aloc

    def finish_part(self):
        """
        Finish the current part number and remember which asterisks it was
        connected to.
        """
        if len(self.asterisks) > 0:
            logging.debug(
                "Found valid part number %s connecting to %s",
                self.current,
                self.asterisks,
            )
        for aloc in self.asterisks:
            self.part_numbers_by_asterisk.setdefault(aloc, []).append(self.current)
        self.current = 0
        self.asterisks = set()


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_filepath", type=pathlib.Path)
    parser.add_argument("--part", type=str, choices=["1", "2", "both"], default="both")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    # Set up the logging configuration.
    if args.debug:
        # If debug mode is on, log both debug and info level messages,
        # and also includes the line number in the log.
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s - %(message)s - [LINE:%(lineno)d]",
        )
    else:
        # If debug mode is off, log only info level messages.
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
        )

    # Load the input from a text file.
    input_text = args.input_filepath.read_text()

    # Run solutions for one or both parts. The functions run_part1 and
    # run_part2 should be defined above.
    if args.part == "1" or args.part == "both":
        logging.info("Running Part 1...")
        answer1 = run_part1(input_text)
        logging.info("Answer to Part 1: %s", answer1)

    if args.part == "2" or args.part == "both":
        logging.info("Running Part 2...")
        answer2 = run_part2(input_text)
        logging.info("Answer to Part 2: %s", answer2)
