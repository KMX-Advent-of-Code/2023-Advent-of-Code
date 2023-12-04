import sys

sys.path.append('../../aoc_2023')
from aoc_helper import get_input

from aoc_helper import get_input
import re

s, s2 = get_input()

test = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".split('\n')


def process_line(x):
    winners, mynums = [y.strip() for y in x.split('|')]
    _, winners = winners.split(':')
    win_set, my_set = {int(x)
                       for x in re.findall('\d+', winners)
                       }, {int(x)
                           for x in re.findall('\d+', mynums)}
    my_winners = my_set.intersection(win_set)
    return my_winners, 2**(len(my_winners) - 1) if my_winners else 0


def solve(x):
    ans = 0
    for l in x:
        mywin, n = process_line(l)
        ans += n
    return ans


print(solve(test))
print(solve(s2))


def process_line2(x):
    winners, mynums = [y.strip() for y in x.split('|')]
    card_num, winners = winners.split(':')
    _, card_num = card_num.split()
    card_num = int(card_num)
    win_set, my_set = {int(x)
                       for x in re.findall('\d+', winners)
                       }, {int(x)
                           for x in re.findall('\d+', mynums)}
    my_winners = my_set.intersection(win_set)
    return {card_num: len(my_winners)}


def winning_cards(card_num, n):
    return list(range(card_num + 1, card_num + n + 1))


def solve_part2(test):
    mapping_dict = {}
    for l in test:
        mapping_dict.update(process_line2(l))
    counter_dict = {key: 1 for key in mapping_dict.keys()}
    for key in counter_dict.keys():
        new_cards = winning_cards(key, mapping_dict[key])
        for new_card in new_cards:
            counter_dict[new_card] += counter_dict[key]
    return (sum(counter_dict.values()))


print(solve_part2(test))
print(solve_part2(s2))
