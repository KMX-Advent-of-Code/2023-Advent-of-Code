"""
Day 2: Cube Conundrum
https://adventofcode.com/2023/day/2
"""
import logging
import argparse
import pathlib
import pandas as pd
import numpy as np

CUBES_IN_BAG = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def run_part1(input_text: str) -> int:
    """Solve Part 1"""
    input_data = parse_input(input_text)
    logging.debug("Parsed input:\n%s", input_data.head())
    # Group by game_id and find the max cubes of each color shown per game
    max_cubes_shown = input_data.groupby("game_id").max()
    # Reshape CUBES_IN_BAG so that it can be compared against max_cubes_shown
    cubes_in_bag = pd.DataFrame(CUBES_IN_BAG, index=max_cubes_shown.index)
    # Find the valid games where the max cubes per game is less than or equal
    # to the cubes in bag for every color.
    is_valid_game = (max_cubes_shown <= cubes_in_bag).all(axis=1)
    valid_games = np.where(is_valid_game)[0] + 1
    logging.debug("Valid games: %s", valid_games)
    return sum(valid_games)


def run_part2(input_text: str) -> int:
    """Solve Part 2"""
    df = parse_input(input_text)
    logging.debug("Parsed input:\n%s", df.head())
    # Group by game_id and find the max cubes of each color shown per game
    max_cubes_shown = df.groupby("game_id").max()
    # Calculate the power of each game by multiplying the max cubes shown,
    # then add it up.
    return max_cubes_shown.prod(axis=1).sum()


def parse_input(input_text: str) -> pd.DataFrame:
    """
    Parse the input text into a pandas DataFrame with a row for each
    round of each game, and a column for each cube color (blue, red, green)
    indicating the number of cubes of that color in that round.
    """
    rows = []
    for line in input_text.split("\n"):
        game_info, rounds = line.split(": ")
        game_id = int(game_info.split(" ")[1])
        for i, round in enumerate(rounds.split("; ")):
            row = {"game_id": game_id, "round": i + 1}
            words = round.replace(",", "").split(" ")
            for num_cubes, color in zip(words[::2], words[1::2]):
                row[color] = int(num_cubes)
            rows.append(row)
    return (
        pd.DataFrame(rows)
        .fillna(0)
        .astype(int)
        .set_index(["game_id", "round"])[["red", "green", "blue"]]
        .sort_index()
    )


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
