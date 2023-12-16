"""
Day 13: Point of Incidence
https://adventofcode.com/2023/day/13
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 13

import numpy as np

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def solve(s, smudge):
    """smudge is a boolean for whether to use the smudge factor"""
    # parse the problems into arrays
    LOOKUP = {'.' : 0, '#' : 1}
    problems = [np.array([[LOOKUP[x] for x in line] for line in problem]) for problem in split(s)]

    # determine symmeties, minding the smudge
    horizontal = [find_horizontal_symmetries(problem, smudge) for problem in problems]
    vertical   = [find_vertical_symmetries(problem, smudge) for problem in problems]

    # make sure we never find symmetry for both directions
    for sym1, sym2 in zip(horizontal, vertical):
        assert sym1 is None or sym2 is None
        assert isinstance(sym1, int) or isinstance(sym2, int)

    # turn this into the answer
    out = 0
    for sym in horizontal:
        if sym:
            out += sym * 100
    for sym in vertical:
        if sym:
            out += sym
    return out

def find_horizontal_symmetries(problem, smudge):
    """Return the number of rows before the symmetry for each symmetry"""
    matches = []
    problem = [list(row) for row in problem]

    # iterate through locations of the mirror symmetry
    for i in range(1, len(problem)):
        match = True

        # check pairs of rows out from the line, to see if they all match
        # first gather them up into lists to compare
        rows1 = []
        rows2 = []
        for ii in range(len(problem)):
            # done checking once I hit indexing issues
            try:
                assert i-1-ii >= 0 and i+ii < len(problem)
            except:
                break

            rows1 = rows1 + problem[i-1-ii]
            rows2 = rows2 + problem[i+ii]

        # check how many places they disagree
        disagree = 0
        for x, y in zip(rows1, rows2):
            if x != y:
                disagree += 1

        # check for a match, minding the smudge idea
        #print(i)
        #print(disagree, smudge)
        #print()
        if smudge and disagree == 1:
            #print('    1')
            matches.append(i)
        if not smudge and disagree == 0:
            #print('    2')
            matches.append(i)

    #print(matches)
    assert len(matches) <= 1

    if matches:
        return matches[0]
    else:
        return None

def find_vertical_symmetries(problem, smudge):
    """Return the number of columns before the symmetry for each symmetry"""
    return find_horizontal_symmetries(problem.transpose(), smudge)
    
def part1(s):
    """Solve part 1"""
    return solve(s, False)
    
def part2(s):
    """Solve part 2"""
    return solve(s, True)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
