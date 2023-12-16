"""
Day 16: The Floor Will Be Lava
https://adventofcode.com/2023/day/16

Represent beams as (i, j, io, jo) giving the location and direction vector
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 16

import numpy as np

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_grid(s):
    """Parse the input into a np.array of characters, with added "walls" to simplify propagation logic"""
    out = [['#'] + list(line) + ['#'] for line in split(s)]
    m = len(out[0])
    out = [['#'] * m] + out + [['#'] * m]
    return np.array(out)

def print_grid(grid):
    """Something much more human readable than a np.array"""
    for line in grid:
        print(''.join(line))

def propagate(beam, grid):
    """Given a beam and the grid, return the set of beams it propagates to"""
    i, j, io, jo = beam

    # cases based on what the block has
    match grid[i,j]:
        case '#':
            # hit a wall
            return {}
        case '.':
            # passing through empty space
            return {(i+io, j+jo, io, jo)}
        case '|':
            # vertical splitter

            # cases based on the direction the beam is going
            match (io, jo):
                case (1, 0):
                    # traveling down, so just pass through
                    return {(i+io, j+jo, io, jo)}
                case (-1, 0):
                    return {(i+io, j+jo, io, jo)}
                case (0, 1):
                    # traveling right, so split up and down
                    return {(i+1, j, 1, 0), (i-1, j, -1, 0)}
                case (0, -1):
                    return {(i+1, j, 1, 0), (i-1, j, -1, 0)}
                case _:
                    assert False
        case '-':
            match (io, jo):
                case (1, 0):
                    return {(i, j+1, 0, 1), (i, j-1, 0, -1)}
                case (-1, 0):
                    return {(i, j+1, 0, 1), (i, j-1, 0, -1)}
                case (0, 1):
                    return {(i+io, j+jo, io, jo)}
                case (0, -1):
                    return {(i+io, j+jo, io, jo)}
                case _:
                    assert False
        case '/':
            match (io, jo):
                case (1, 0):
                    # traveling down, so reflect left
                    return {(i, j-1, 0, -1)}
                case (-1, 0):
                    return {(i, j+1, 0, 1)}
                case (0, 1):
                    return {(i-1, j, -1, 0)}
                case (0, -1):
                    return {(i+1, j, 1, 0)}
                case _:
                    assert False
        case '\\':
            match (io, jo):
                case (1, 0):
                    return {(i, j+1, 0, 1)}
                case (-1, 0):
                    return {(i, j-1, 0, -1)}
                case (0, 1):
                    return {(i+1, j, 1, 0)}
                case (0, -1):
                    return {(i-1, j, -1, 0)}
                case _:
                    assert False
        case _:
            assert False

def spread(beam, grid):
    """Given a beam and the grid, propagate it until there's nothing new to propagate"""
    # the beams we've seen
    beams_history = set()

    # the queue of beams we still need to propagate
    beams_new = [beam]

    # propagate until the queue is empty
    while beams_new:
        # beam to propagate
        beam = beams_new.pop()

        # don't propagate if we've already seen it
        if beam in beams_history:
            continue

        # find the propagated locations
        _beams_new = propagate(beam, grid)

        # if it didn't go anywhere, "beam" was in a wall so don't log it
        if len(_beams_new) == 0:
            continue

        # otherwise, log it in the history and add the new beams to the queue
        beams_history.add(beam)
        for _beam in _beams_new:
            beams_new.append(_beam)

    return beams_history

def count_locations(beams_history):
    """Count the number of locations covered by a set of beams (since beams can hit a location more than once)"""
    locs = set()
    for (i,j,io,jo) in beams_history:
        locs.add((i,j))
    return len(locs)

def part1(s):
    """Solve part 1"""
    grid = parse_grid(s)
    #print_grid(grid)
    beams_history = spread((1, 1, 0, 1), grid)
    return count_locations(beams_history)
    
def part2(s):
    """Solve part 2"""
    grid = parse_grid(s)

    # figure out all the possible starting beams
    beams_starting = []
    n, m = grid.shape
    
    # from the corners
    beams_starting.append((1, 1, 1, 0))
    beams_starting.append((1, 1, 0, 1))
    beams_starting.append((1, m-2, 1, 0))
    beams_starting.append((1, m-2, 0, -1))
    beams_starting.append((n-2, 1, -1, 0))
    beams_starting.append((n-2, 1, 0, 1))
    beams_starting.append((n-2, m-2, -1, 0))
    beams_starting.append((n-2, m-2, 0, -1))
    
    # from the left and right
    for i in range(2, n-2):
        beams_starting.append((i, 1, 0, 1))
        beams_starting.append((i, m-2, 0, -1))
    
    # from the top and bottom
    for j in range(2, m-2):
        beams_starting.append((1, j, 1, 0))
        beams_starting.append((n-2, j, -1, 0))

    # for each starting beam count up the locations it ends up covering, and find the biggest one
    return max([count_locations(spread(beam, grid)) for beam in beams_starting])
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
