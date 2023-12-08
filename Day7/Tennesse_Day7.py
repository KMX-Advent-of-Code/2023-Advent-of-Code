"""
Day 7: Camel Cards
https://adventofcode.com/2023/day/7
"""
import logging
from utilities import run_aoc
import numpy as np

CARD_RANKS = "23456789TJQKA"
CARD_RANKS_JOKER = "J23456789TQKA"
TYPE_RANKS = [(1, 1, 1, 1, 1), (2, 1, 1, 1), (2, 2, 1), (3, 1, 1), (3, 2), (4, 1), (5,)]


def run_part1(input_text: str) -> int:
    """Parse the hands, sort them, and return the total winnings."""
    hands, bids = parse_input(input_text)
    hand_values = [hand_to_int(hand, CARD_RANKS, use_jokers=False) for hand in hands]
    sorted_bets = [bids[i] for i in np.argsort(hand_values)]
    return sum(bid * (i + 1) for i, bid in enumerate(sorted_bets))


def run_part2(input_text: str) -> int:
    """Same as part 1, but with jokers."""
    hands, bids = parse_input(input_text)
    hand_values = [
        hand_to_int(hand, CARD_RANKS_JOKER, use_jokers=True) for hand in hands
    ]
    sorted_bets = [bids[i] for i in np.argsort(hand_values)]
    return sum(bid * (i + 1) for i, bid in enumerate(sorted_bets))


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse the hands and bids from the input text."""
    hands = []
    bids = []
    for line in input_text.split("\n"):
        cards, bid = line.split()
        hands.append(cards)
        bids.append(int(bid))
    return hands, bids


def hand_to_int(hand: str, card_ranks: str, use_jokers: bool) -> int:
    """Convert a hand of cards to a 6-digit hexidecimal number,
    in a way that preserves the sort order specified in the problem.

    The first hexidecimal digit encodes the type, and the remaining 5
    encode the individual cards in the hand.
    """
    lex_value = sum(16**i * card_ranks.index(c) for i, c in enumerate(reversed(hand)))
    if use_jokers and "J" in hand and hand != "JJJJJ":
        # Replace all jokers with the most common non-joker card
        # for the purpose of determining the type value.
        most_common_non_joker = most_common_letter(hand.replace("J", ""))
        hand = hand.replace("J", most_common_non_joker)
    # Compute the type value
    counts = sorted(np.unique(list(hand), return_counts=True)[1])[::-1]
    type_value = TYPE_RANKS.index(tuple(counts))
    return 16**5 * type_value + lex_value


def most_common_letter(string: str) -> str:
    """Return the most common letter in a string."""
    return max(string, key=string.count)


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
