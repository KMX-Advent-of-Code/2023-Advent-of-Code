import re
import numpy as np
import sys

sys.path.append('../../aoc_2023')
from aoc_helper import get_input

s, s2 = get_input()

test = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split('\n')


def process_data_part1(test):
    numbers = []
    for i, l in enumerate(test):
        numbers.append((i, list(re.finditer("(\d+)", l))))

    symbols = []
    for i, l in enumerate(test):
        symbols.append((i, list(re.finditer("([\*\#\$\+\@\%\&\=\-/])", l))))

    coords = {}
    for y, x_list in symbols:
        for x_match in x_list:

            coords[(x_match.span()[0], y)] = 1
    return numbers, symbols, coords


def check_match(y, match, coords):
    m1, m2 = match.span()
    for x in range(m1, m2):
        # print(x,y)
        coord_check = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                       (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        if any(coords.get(c) for c in coord_check):
            #print([(c,coords.get(c)) for c in coord_check])
            return int(match.group(1))
    return 0


def solve_part1(numbers, coords):
    answer = 0
    for y, match_list in numbers:
        for m in match_list:
            answer += check_match(y, m, coords)
    return (answer)


print("Part 1")
numbers, symbols, coords = process_data_part1(test)
print(solve_part1(numbers, coords))

numbers, symbols, coords = process_data_part1(s2)
print(solve_part1(numbers, coords))


## If I had just found the numbers near the symbols originally I wouldn't have had to change methods here
## didn't occur to me until part 2 I could just find the numbers repeatedly near symbols and de-duplicate with a set.
def process_data_part2(s2):
    numbers = []
    for i, l in enumerate(s2):
        numbers.append((i, list(re.finditer("(\d+)", l))))

    symbols = []
    for i, l in enumerate(s2):
        symbols.append((i, list(re.finditer("([\*])", l))))

    coords = {}
    for y, x_list in numbers:
        for x_match in x_list:
            m1, m2 = x_match.span()
            for x in range(m1, m2):
                coords[(x, y)] = int(x_match.group(1))
    return numbers, symbols, coords


def check_match2(y, match):
    m1, m2 = match.span()
    for x in range(m1, m2):
        # print(x,y)
        coord_check = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y),
                       (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        if any(coords.get(c) for c in coord_check):
            #print([(c,coords.get(c)) for c in coord_check])
            return {coords.get(c) for c in coord_check if coords.get(c)}
    return []


import numpy as np

numbers, symbols, coords = process_data_part2(test)


def solve(symbols):
    answer = []
    final = 0
    for y, match_list in symbols:
        for m in match_list:
            answer.append(check_match2(y, m))
    for row in answer:
        if len(row) == 2:
            final += np.prod(list(row))
    return final


print("Part 2")
print(solve(symbols))
numbers, symbols, coords = process_data_part2(s2)
print(solve(symbols))
