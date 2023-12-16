"""
Day 14: Parabolic Reflector Dish
https://adventofcode.com/2023/day/14

Runtime isn't too much of an issue, so I aimed for intuitive functions over efficiency
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 14

import numpy as np

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse(s):
    """Parse the input text into a numpy array"""
    return np.array([list(line) for line in split(s)])

def tilt_west(grid):
    """Tilt the grid west"""
    return np.array([tilt_row_left(row) for row in grid.copy()])

def tilt_north(grid):
    """Tilt the grid north"""
    return tilt_west(grid.transpose()).transpose()

def tilt_east(grid):
    """Tilt the grid east"""
    return tilt_west(grid[:,::-1])[:,::-1]

def tilt_south(grid):
    """Tilt the grid south"""
    return tilt_north(grid[::-1,:])[::-1,:]

def tilt_row_left(row):
    """Tilt a single row 'left'"""
    n = len(row)

    # look for rounded rocks from left to right
    for i in range(n):

        # when we find a rounded rock, shift it left
        if row[i] == 'O':
            # scan right to left to find out where to put it
            ii = i
            for j in range(i-1, -1, -1):
                if row[j] == '.':
                    ii = j
                else:
                    break

            # put it there
            row[i] = '.'
            row[ii] = 'O'

    return row

def cycle(grid):
    """Tilt cycle"""
    return tilt_east(tilt_south(tilt_west(tilt_north(grid))))

def score_grid_west(grid):
    """Score the grid according to the load on the west side"""
    scores = [score_row_left(row) for row in grid]
    return sum(scores)

def score_grid_north(grid):
    """Score the grid according to the load on the north side"""
    return score_grid_west(grid.transpose())

def score_row_left(row):
    """Score a row according to the load on the 'left' side"""
    n = len(row)
    score = 0
    s = n
    for x in row:
        if x == 'O':
            score += s
        s -= 1
    return score

def nice(grid):
    """String representation of a grid"""
    return '\n'.join([''.join(row) for row in grid])
    
def part1(s):
    """Solve part 1"""
    grid = parse(s)
    return score_grid_north(tilt_north(grid))
    
def part2(s):
    """Solve part 2"""
    grid = parse(s)

    # perform cycles until we repeat a previous one, tracking the history with both np.array and string representations
    nice_grid = nice(grid)
    history = [grid.copy()]
    history_nice = [nice_grid]
    while nice_grid not in history_nice[:-1]:
        grid = cycle(grid)
        nice_grid = nice(grid)
        history.append(grid.copy())
        history_nice.append(nice_grid)

    # this next bit returns [81, 119], so the period is 38
    #nice_grid = history_nice[-1]
    #[i for i, _nice_grid in enumerate(history_nice) if nice_grid == _nice_grid]
    
    # 1000000000 = 94 (mod 38) and 94 > 81 means we've entered the main loop after 94 cycles
    # so the state after 1000000000 cycles will be the same as the state after 94 cycles

    return score_grid_north(history[94])


if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
