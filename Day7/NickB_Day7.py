"""
Day 7: Camel Cards
https://adventofcode.com/2023/day/7

Made the code for part 1, and then just copy-pasted and modified it for part 2
"""

from collections import Counter
from functools import cmp_to_key

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 7

# ordering on cards
RANK1 = {card : rank for card, rank in zip('AKQJT98765432', [14,13,12,11,10,9,8,7,6,5,4,3,2])}
RANK2 = {card : rank for card, rank in zip('AKQJT98765432', [14,13,12,0,10,9,8,7,6,5,4,3,2])}

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_line(line):
    """A hand is a tuple (cards, bid)"""
    cards, bid = tuple(line.split(' '))
    bid = int(bid)
    return cards, bid

def compare_cards_1(cards1, cards2):
    """Compare two sets of cards"""
    # check the type rank of each and compare
    rank1 = type_rank_1(cards1)
    rank2 = type_rank_1(cards2)

    # decide based on hand ranks
    if rank1 > rank2:
        return 1
    if rank2 > rank1:
        return -1

    # decide based on ranks of the cards
    for card1, card2 in zip(cards1, cards2):
        rank1 = RANK1[card1]
        rank2 = RANK1[card2]

        if rank1 > rank2:
            return 1
        if rank2 > rank1:
            return -1

    # if we failed to compare them
    assert False

def type_rank_1(cards):
    """Return a number for the strength of the type (five of a kind, etc.)"""
    counts = Counter(cards).values()
    # 5 of a kind
    if 5 in counts:
        return 10

    # 4 of a kind
    if 4 in counts:
        return 9

    # full house
    if (3 in counts) and (2 in counts):
        return 8

    # 3 of a kind
    if 3 in counts:
        return 7

    # two pairs
    if Counter(counts)[2] == 2:
        return 6

    # one pair
    if 2 in counts:
        return 5

    # high card
    return 0

def compare_hands_1(hand1, hand2):
    return compare_cards_1(hand1[0], hand2[0])

def compare_cards_2(cards1, cards2):
    """Compare two sets of cards"""
    # check the type rank of each and compare
    rank1 = type_rank_2(cards1)
    rank2 = type_rank_2(cards2)

    # decide based on hand ranks
    if rank1 > rank2:
        return 1
    if rank2 > rank1:
        return -1

    # decide based on ranks of the cards
    for card1, card2 in zip(cards1, cards2):
        rank1 = RANK2[card1]
        rank2 = RANK2[card2]

        if rank1 > rank2:
            return 1
        if rank2 > rank1:
            return -1

    # if we failed to compare them
    assert False

def type_rank_2(cards):
    """Return a number for the strength of the type (five of a kind, etc.)
    Treats J as a joker
    """
    # counts, keeping jokers separately
    counter = Counter(cards)
    Js = counter.get('J', 0)
    if 'J' in counter:
        del counter['J']
    counts = sorted(counter.values())

    # edge case: all jokers, which is a 5 of a kind
    if Js == 5:
        return 10
    
    # 5 of a kind
    if counts[-1] + Js == 5:
        return 10

    # 4 of a kind
    if counts[-1] + Js == 4:
        return 9

    # full house
    # at this point we know we have at least 2 non-joker cards, so counts[-2] won't give an indexing error
    # if we have this, our hand is one of XXYYY, XJYYY, XXYYJ, JJYYY, XXYJJ, XXJJJ
    # only XXYYY and XXYYJ avoid making a 4 or 5 of a kind so just check for those
    if ((counts[-1] == 3) and (counts[-2] == 2)) or ((counts[-1] == 2) and (counts[-2] == 2) and (Js == 1)):
        return 8

    # 3 of a kind
    if counts[-1] + Js == 3:
        return 7

    # two pairs
    # ignore jokers, since two pairs where the hand has a joker means we have at least a 3 of a kind
    if (counts[-1] == 2) and (counts[-2] == 2):
        return 6

    # one pair
    if counts[-1] + Js == 2:
        return 5

    # high card
    return 0

def compare_hands_2(hand1, hand2):
    return compare_cards_2(hand1[0], hand2[0])

def part1(s):
    """Solve part 1"""
    hands = [parse_line(line) for line in split(s)]
    hands = sorted(hands, key=cmp_to_key(compare_hands_1))
    scores = [bid * (i+1) for i, (cards, bid) in enumerate(hands)]
    return sum(scores)
    
def part2(s):
    """Solve part 2"""
    hands = [parse_line(line) for line in split(s)]
    hands = sorted(hands, key=cmp_to_key(compare_hands_2))
    scores = [bid * (i+1) for i, (cards, bid) in enumerate(hands)]
    return sum(scores)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))