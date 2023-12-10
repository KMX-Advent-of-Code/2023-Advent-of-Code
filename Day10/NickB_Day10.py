"""
Day 10: Pipe Maze
https://adventofcode.com/2023/day/10

Part 1: follow the two sides of the path until they meet
Part 2:
- Using part 1 and keep track of locations of pipes in the path
- Note that using the standard size grid, to find in/out of the path we'd need to think about pipe orientations
- So scale up the grid so each pipe in the path can be represented as a 3x3 tile, which adds "gaps" that ensure all the "out" bits are connected
- Flood the grid from the outside, so the "in" bits won't get flooded
- Count the unflooded bits
"""

import numpy as np
import sys
#from matplotlib import pyplot as plt

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 10

# 0 = right, 1 = up, 2 = left, 3 = down, converting these to (i,j) changes
DIRECTIONS = {0 : (0, 1), 1 : (-1, 0), 2 : (0, -1), 3 : (1, 0)}

# converting each pipe to the (i,j) changes it would link
PIPES = {
    '|' : (DIRECTIONS[1], DIRECTIONS[3]),
    '-' : (DIRECTIONS[0], DIRECTIONS[2]),
    'L' : (DIRECTIONS[0], DIRECTIONS[1]),
    'J' : (DIRECTIONS[1], DIRECTIONS[2]),
    '7' : (DIRECTIONS[2], DIRECTIONS[3]),
    'F' : (DIRECTIONS[0], DIRECTIONS[3])
}

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_grid(s):
    """Parse input as a numpy array of characters"""
    lines = split(s)
    n = len(lines)
    m = len(lines[0])
    assert all([len(line) == m for line in lines])

    return np.array([list(line) for line in lines])

def find_s(grid):
    """Find the 'S' character"""
    n, m = grid.shape
    loc = None
    for i in range(n):
        for j in range(m):
            if grid[i,j] == 'S':
                # make sure we don't find it twice
                if loc:
                    assert False
                loc = (i,j)

    return loc

def get_far_away(grid, i , j):
    """Explore the main path in both directions until they meet, keeping track of distance and locations"""
    # how we'll start exploring
    pipe = PIPES[grid[i,j]]
    io1, jo1 = pipe[0]
    io2, jo2 = pipe[1]
    i1, j1 = i + io1, j + jo1
    i2, j2 = i + io2, j + jo2

    # keep track of the previous move
    i1_prev, j1_prev = i, j
    i2_prev, j2_prev = i, j

    # keep track of locations covered (for part 2)
    locs = [(i,j), (i1,j1), (i2,j2)]

    # keeping track of distance
    d = 1

    # explore until the two paths meet
    while True:
        d += 1
        
        # explore path 1
        i1, j1, i1_prev, j1_prev = next(grid, i1, j1, i1_prev, j1_prev)

        # check if that move made the paths meet
        if i1 == i2 and j1 == j2:
            break
        locs.append((i1,j1))

        # explore path 2
        i2, j2, i2_prev, j2_prev = next(grid, i2, j2, i2_prev, j2_prev)

        # check if that move made the paths meet
        if i1 == i2 and j1 == j2:
            break
        locs.append((i2,j2))

    return d, locs

def next(grid, i, j, i_prev, j_prev):
    """Given the current and previous pipe, move to the next one"""
    pipe = PIPES[grid[i,j]]
    io1, jo1 = pipe[0]
    io2, jo2 = pipe[1]

    # figure out which move brings us back to the previous
    move = 0
    if i + io1 == i_prev and j + jo1 == j_prev:
        move = 1
    if i + io2 == i_prev and j + jo2 == j_prev:
        move = 2

    assert move > 0

    # do the other move
    if move == 1:
        i_next, j_next = i + io2, j + jo2
    if move == 2:
        i_next, j_next = i + io1, j + jo1
    
    return i_next, j_next, i, j

def make_big_grid(grid, locs):
    """3x scale the grid and represent the pipes in the path as 3x3 tiles"""
    n, m = grid.shape
    big_grid = np.zeros((3*n, 3*m), dtype='uint8')
    for (i,j) in locs:
        i_big, j_big = 3*i+1, 3*j+1
        (io1, jo1), (io2, jo2) = PIPES[grid[i,j]]
        big_grid[i_big, j_big] = 1
        big_grid[i_big + io1, j_big + jo1] = 1
        big_grid[i_big + io2, j_big + jo2] = 1
    
    return big_grid

def fill(big_grid, i, j):
    """Fill a "out" parts of the 3x scale grid"""
    # indexing check
    try:
        big_grid[i,j]
    except:
        return
        
    # pipe or already filled
    if big_grid[i,j] in (1,2):
        return
    
    # fill this entry
    big_grid[i,j] = 2

    # fill the neighbors
    for (io, jo) in [(-1,0), (0,-1), (1,0), (0,1)]:
        fill(big_grid, i + io, j + jo)

def count_unfilled(big_grid):
    """Count the number of unfilled parts, only looking at the center of the 3x3 tiles"""
    N, M = big_grid.shape
    n, m = N // 3, M // 3
    c = 0
    for i in range(n):
        for j in range(m):
            if big_grid[3*i+1, 3*j+1] == 0:
                c += 1
    return c

def part1(s):
    """Solve part 1"""
    # parse the grid and find 'S'
    grid = parse_grid(s)
    i,j = find_s(grid)

    # running this lets you see that 'S' should be replaced by '|' to complete the big loop of pipe
    #print(grid[i-1:i+2, j-1:j+2])

    # replace 'S' with its intended pipe and count the length of the loop
    grid[i,j] = '|'
    d, locs = get_far_away(grid, i, j)
    return d
    
def part2(s):
    """Solve part 2"""
    # get the path
    grid = parse_grid(s)
    i,j = find_s(grid)
    grid[i,j] = '|'
    d, locs = get_far_away(grid, i, j)

    # scale up to 3x grid
    big_grid = make_big_grid(grid, locs)

    # increase recursion limit for the flooding
    # could have avoided this if I'd done breath first search for the flooding
    N, M = big_grid.shape
    sys.setrecursionlimit(N*M)

    # flood
    fill(big_grid, 0, 0)

    # visualize the flooded grid
    #fig, ax = plt.subplots()
    #ax.matshow(big_grid)

    # count "in" locations
    return count_unfilled(big_grid)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
