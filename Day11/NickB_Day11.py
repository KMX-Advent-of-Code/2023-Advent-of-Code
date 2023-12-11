"""
Day 11: Cosmic Expansion
https://adventofcode.com/2023/day/11
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 11

import numpy as np

LOOKUP = {'.' : 0, '#' : 1}

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def get_universe(s):
    """Parse the input into the grid giving the universe, with 1s for galaxies and 0s for everything else"""
    return np.array([[LOOKUP[x] for x in line] for line in split(s)], dtype='uint8')

def get_expansion_indices(universe):
    """Get indices for rows/columns to expand"""
    # indices of rows/columns that don't have ones
    I = (universe.sum(axis=1) == 0).nonzero()[0]
    J = (universe.sum(axis=0) == 0).nonzero()[0]

    return I, J

def find_galaxies(universe):
    """List of (i,j) with the locations of galaxies"""
    return list(zip(*universe.nonzero()))

def distance(galaxy1, galaxy2, I, J, expansion_factor):
    """Distance between two galaxies, minding the expansion"""
    i1, j1 = galaxy1
    i2, j2 = galaxy2

    # distance without expansion
    d = abs(i1-i2) + abs(j1-j2)

    # added i expansion: for each expanded i that's between the two galaxies
    i1, i2 = min(i1, i2), max(i1, i2)
    di = len([i for i in I if i1 < i and i < i2]) * (expansion_factor - 1)

    # added j expansion: for each expanded j that's between the two galaxies
    j1, j2 = min(j1, j2), max(j1, j2)
    dj = len([j for j in J if j1 < j and j < j2]) * (expansion_factor - 1)

    return d + di + dj

def sum_distances(galaxies, I, J, expansion_factor):
    """Sum up the pairwise distances between all the galaxies"""
    d = 0

    l = len(galaxies)
    for g1 in range(l):
        for g2 in range(g1+1, l):
            d += distance(galaxies[g1], galaxies[g2], I, J, expansion_factor)
    
    return d

def part1(s):
    """Solve part 1"""
    universe = get_universe(s)
    I, J = get_expansion_indices(universe)
    galaxies = find_galaxies(universe)
    return sum_distances(galaxies, I, J, 2)
    
def part2(s):
    """Solve part 2"""
    universe = get_universe(s)
    I, J = get_expansion_indices(universe)
    galaxies = find_galaxies(universe)
    return sum_distances(galaxies, I, J, 1000000)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))