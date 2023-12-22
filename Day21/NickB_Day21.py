"""
Day 21: Step Counter
https://adventofcode.com/2023/day/21

My original solution for part 2 was pretty manual and awful, but I got inspiration from reddit so I coded that up here

The problem input has some nice properties (you can move freely along edges and vertically/horizontally from the start) which I think means we get to the "asymptotic" regime quicker

The key idea is that it takes 262 steps to traverse from (0, 0) on the grid to (0, 0) on the next grid diagonally in the infinite "meta grid" of grids, so you can expect things to work on a period of 262
And you can reason that the number of garden plots we can reach along this period of 262 grows quadratically
So just fit a quadratic polynomial to the first few counts of garden plots we can reach on odd steps, and use that to extrapolate to the desired number of steps
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 21

import numpy as np

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_grid(s):
    """Parse the input into a "blank" grid and the i, j where we start"""
    grid = np.array([list(line) for line in split(s)])
    i,j  = np.where(grid == 'S')
    assert len(i) == 1 and len(j) == 1
    i, j = i[0], j[0]
    grid[i, j] = '.'
    return grid, i ,j
    
class MetaGridWanderer:
    """Handles moving us on the infinite meta grid of grids"""
    
    def __init__(self, s):
        blank_grid, i, j = parse_grid(s)
        self.blank_grid = blank_grid
        self.n, self.m = self.blank_grid.shape
        self.meta_grid = {(0, 0) : self.blank_grid.copy()}
        self.num_step = 0
        self.locs = [(0, 0, i, j)]
    
    def wander(self, num_steps):
        """Wander on the meta grid for num_steps"""
        # during a round of steps, this will hold the steps for the next round
        locs = []
        
        # take all the rounds of steps
        for _ in range(num_steps):
            self.num_step += 1
            
            # take a step from each location
            for k, l, i, j in self.locs:
                _locs = self.step(k, l, i, j)
                for loc in _locs:
                    locs.append(loc)
    
            # move the new steps into the queue
            self.locs, locs = locs, []

    def step(self, k, l, i, j):
        """Do a single step from (i, j) on grid (k, l)"""
        steps = []
        for (io, jo) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            _i, _j = i + io, j + jo
            _k, _l, _i, _j = k + _i // self.n, l + _j // self.m, _i % self.n, _j % self.m
    
            if not (_k, _l) in self.meta_grid:
                self.meta_grid[(_k, _l)] = self.blank_grid.copy()
            
            if self.meta_grid[(_k, _l)][_i, _j] == '.':
                if self.num_step % 2 == 0:
                    self.meta_grid[(_k, _l)][_i, _j] = 'E'
                else:
                    self.meta_grid[(_k, _l)][_i, _j] = 'O'
                steps.append((_k, _l, _i, _j))
                
        return steps

    def count(self, marker):
        """Count up the 'E' or 'O' markers"""
        c = 0
        for grid in self.meta_grid.values():
            c += len(np.where(grid == marker)[0])
        return c

def part1(s):
    """Solve part 1"""
    # 64 steps doesn't leave the original grid so moving on the meta grid is fine
    w = MetaGridWanderer(s)
    w.wander(64)
    return w.count('E')
    
    
def part2(s):
    """Solve part 2"""
    # parameters
    num_steps = 26501365
    period = 262

    # the offset to look on, and how many periods to do to get the answer
    offset = 26501365 % period
    num_periods = 26501365 // period
    assert offset + num_periods * period == num_steps

    # for taking data on the number of locations we can reach
    counts = []
    w = MetaGridWanderer(s)

    # at 0 periods
    w.wander(offset)
    counts.append(w.count('O'))

    # at 1 period
    w.wander(period)
    counts.append(w.count('O'))

    # at 2 periods
    w.wander(period)
    counts.append(w.count('O'))

    # at 3 periods
    w.wander(period)
    counts.append(w.count('O'))

    # fit a quadratic to the first 3 data points
    coeffs = np.polyfit([0, 1, 2], counts[:3], deg=2)
    coeffs = [int(np.round(x)) for x in coeffs]
    p = lambda n : coeffs[0] * n**2 + coeffs[1] * n + coeffs[2]

    # check it matches our data (including the last data point we didn't fit on)
    for i in range(4):
        assert p(i) == counts[i]
    
    return p(num_periods)

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
