"""
Day 4: Scratchcards
https://adventofcode.com/2023/day/4
"""
import logging
import argparse
import pathlib
from dataclasses import dataclass


def run_part1(input_text: str) -> int:
    """
    Count how many numbers match between left and right halves of each row,
    and return the total points of all rows.
    """
    total_points = 0
    for row in input_text.split("\n"):
        scratch_card = ScratchCard.from_row(row)
        logging.debug("Parsed scratch card:\n%s", scratch_card)
        points = scratch_card.get_points()
        logging.debug("Card %s points: %s", scratch_card.card_number, points)
        total_points += points
    return total_points


def run_part2(input_text: str) -> int:
    """
    Count the total number of scorecards according if each card makes
    a copy of the next N cards, where N is the number of matches.
    """
    num_matches_array = [
        ScratchCard.from_row(row).get_num_matches() for row in input_text.split("\n")
    ]
    return count_scorecards(num_matches_array)


@dataclass
class ScratchCard:
    """Represents a single row in the input file."""

    card_number: int
    winning_numbers: set[int]
    your_numbers: set[int]

    @classmethod
    def from_row(cls, row: str):
        """
        Parse the scratch card from a row of text of the form:
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        """
        card_number, numbers = row.split(": ")
        card_number = int(card_number.split()[1])
        numbers = numbers.split(" | ")
        winning_numbers = {int(n) for n in numbers[0].split()}
        your_numbers = {int(n) for n in numbers[1].split()}
        return cls(card_number, winning_numbers, your_numbers)

    def get_num_matches(self) -> int:
        """
        Return the number of matching numbers between the winning numbers
        and your numbers.
        """
        return len(self.winning_numbers & self.your_numbers)

    def get_points(self) -> int:
        """
        Return the points for this scratch card, which is two raised to
        the power of the number of matching numbers between the winning
        numbers and your numbers.
        """
        num_matches = self.get_num_matches()
        if num_matches == 0:
            return 0
        else:
            return 2 ** (num_matches - 1)


def count_scorecards(num_matches_array: list[int]) -> int:
    """
    Count the total number of scorecards if each card makes
    a copy of the next N cards, where N is the number of matches.
    """
    # This array keeps track of the number of copies of each card
    # we currently have. It's updated dynamically as we process the
    # cards in order of card number.
    num_copies = [1] * len(num_matches_array)
    for i, num_matches in enumerate(num_matches_array):
        # Process all copies of the ith card.
        for j in range(num_matches):
            # Which card to create copies of.
            card_idx = i + j + 1
            if card_idx >= len(num_copies):
                # If the card index is out of bounds, skip it.
                break
            # Each copy of the ith card creates a copy of the card at card_idx.
            num_copies[card_idx] += num_copies[i]
    # Return the total number of scorecards after all cards have been processed.
    return sum(num_copies)


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
