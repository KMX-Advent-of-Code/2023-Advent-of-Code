"""
Day 18: Lavaduct Lagoon
https://adventofcode.com/2023/day/18

Approach: optimized for part 2, using a "block grid"
- Once we have a list of the locations of vertices of our path we could fill in the path segments in a grid, flood the outside, and count the inside area - but this isn't feasible because of the size of the grid
- Instead, we can first compress our grid to a "block grid", similar to block matrices: a large rectangle area in the full grid would be compressed down to a single entry
- Paritition into the blocks according to the locations of vertices: if there are vertices at i1 and i2 and no vertices at any i with i1 < i < i2 then [i1+1, ..., i2-1] can be a block, since that region is either all on the inside or all on the outside
- Do the flooding on the block grid, and determine areas by using the dimensions of the blocks

Ex. vertices of the path in the full grid:
*------*
--------
--------
--------
----*--*
*---*---

vertices of the path in the block grid:
*---*
-----
--*-*
*-*--

areas of the blocks represented by the block grid:
13121
39363
13121
13121
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 18

import numpy as np

DIRECTIONS1 = {'D' : (1, 0), 'U' : (-1, 0), 'R' : (0, 1), 'L' : (0, -1)}
DIRECTIONS2 = {'1' : (1, 0), '3' : (-1, 0), '0' : (0, 1), '2' : (0, -1)}

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_line_1(line):
    """Parse a line of the input according to part 1, returning ((io, jo), n) giving the direction and number of steps to move"""
    d, n, _ = tuple(line.split(' '))
    d = DIRECTIONS1[d]
    n = int(n)
    return d, n

def parse_line_2(line):
    """Parse a line of the input according to part 2, returning ((io, jo), n) giving the direction and number of steps to move"""
    _, _, hex = tuple(line.split(' '))
    d = DIRECTIONS2[hex[7]]
    n = int(hex[2:7], 16)
    return d, n

def move_step(i, j, step):
    """Move from (i, j) according to a step ((io, jo), n)"""
    (io, jo), n = step
    return i + n * io, j + n * jo

def find_area(steps):
    """Main method: finds the are outlined by a sequence of steps"""
    
    # lists I, J giving (i, j) of vertices along the path
    i, j = 0, 0
    I = [i]
    J = [j]
    for step in steps:
        i, j = move_step(i, j, step)
        I.append(i)
        J.append(j)

    # narrow down to possible vertex locations which set up the block grid
    Iv = sorted(set(I))
    Jv = sorted(set(J))

    # convert to intervals to define the block grid
    I_intervals = to_intervals(Iv)
    J_intervals = to_intervals(Jv)

    # convert I, J to lists K, L giving indices in I_intervals, J_intervals for blocks of the block grid
    I_intervals_to_K = {(i1, i2) : k for k, (i1, i2) in enumerate(I_intervals)}
    J_intervals_to_L = {(j1, j2) : l for l, (j1, j2) in enumerate(J_intervals)}
    K = [I_intervals_to_K[(i, i)] for i in I]
    L = [J_intervals_to_L[(j, j)] for j in J]

    # turn K and L into a 2x grid (with a border of zeros)
    # indices map as k -> 2k+1
    big_grid = make_big_grid(K, L)

    # flood the big grid and subset to a normal sized grid
    big_grid = flood(big_grid)
    grid = big_grid[1::2, 1::2]

    # entries equal to 0 or 1 are the interior, so add up the areas of the blocks of the block grid for these
    # could use numpy arrays, but it ran into precision issues so I'll do it manually to be safe
    I_interval_lengths = [i2 - i1 + 1 for i1, i2 in I_intervals]
    J_interval_lengths = [j2 - j1 + 1 for j1, j2 in J_intervals]
    area = 0
    n, m = grid.shape
    for k in range(n):
        for l in range(m):
            if grid[k, l] < 2:
                area += I_interval_lengths[k] * J_interval_lengths[l]

    return area

def to_intervals(I):
    """Turn a list of "vertex" indices into a list of intervals that respects the vertices
    i.e. for each vertex i there is an interval (i, i)
    """
    intervals = [(I[0], I[0])]
    i1 = I[0] + 1
    for i in I[1:]:
        if i1 <= i-1:
            intervals.append((i1, i-1))
        intervals.append((i, i))
        i1 = i + 1
    return intervals

def make_big_grid(I, J):
    """Indices map as i -> 2i+1
    Assumes I runs from 0 to n-1 (and similar for J)"""
    n = max(I) + 1
    m = max(J) + 1
    big_grid = np.zeros((2*n+1, 2*m+1), dtype=int)

    for k in range(1, len(I)):
        i1, j1 = 2*I[k-1]+1, 2*J[k-1]+1
        i2, j2 = 2*I[k]+1, 2*J[k]+1
        
        if i1 <= i2:
            _I = list(range(i1, i2+1))
        else:
            _I = list(range(i1, i2-1, -1))
        
        if j1 <= j2:
            _J = list(range(j1, j2+1))
        else:
            _J = list(range(j1, j2-1, -1))
        
        if len(_I) == 1:
            _I = _I * len(_J)
        
        if len(_J) == 1:
            _J = _J * len(_I)
        
        for _i, _j in zip(_I, _J):
            big_grid[_i, _j] = 1

    return big_grid

def flood(grid):
    """Flood the grid starting from (0, 0)"""
    flood = [(0,0)]

    while flood:
        i, j = flood.pop()
        
        # indexing check
        try:
            grid[i, j]
        except:
            continue
        
        # path or already filled
        if grid[i, j] in (1,2):
            continue

        # fill
        grid[i, j] = 2

        # flow to neighbors
        for (io, jo) in [(-1,0), (0,-1), (1,0), (0,1)]:
            flood.append((i + io, j + jo))

    return grid

def part1(s):
    """Solve part 1"""
    steps = [parse_line_1(line) for line in split(s)]
    return find_area(steps)
    
def part2(s):
    """Solve part 2"""
    steps = [parse_line_2(line) for line in split(s)]
    return find_area(steps)


if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
