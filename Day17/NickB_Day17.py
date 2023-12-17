"""
Day 17: Clumsy Crucible
https://adventofcode.com/2023/day/17

Approach: focus on "states" (i, j, io, jo, k) giving
- (i, j): grid location
- (io, jo): vector of the movement that brought us into this location
- k: number of consecutive (io, jo) movements we've just finished making

For each state, record the heat loss to the target (n-1, m-1) location *so far* - initialize these all as np.inf.
Loop through all the states and update them based on their neighbors (but not recursively updating the neighbors), until we reach steady state.
This effectively means it'll consider more complex paths until we don't need to consider additional complexity.

My code runs in 30 seconds for part 1 and 90 seconds for part 2.
One good speedup would be using a queue to only attempt updates where necessary (on neighbors of states that got updates), rather than iterating through all states until steady state.
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 17

import numpy as np

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_grid(s):
    """Parse the string into a np.array of integers"""
    return np.array([[int(x) for x in list(line)] for line in split(s)])

def print_grid(grid):
    """Nice print of the grid"""
    for line in grid:
        print(''.join([str(x) for x in line]))

def update1(state):
    """Update the heat loss of a state (i, j, io, jo, k) [location] + [direction] + [number of steps so far in that direction] to the end location, with part 1 logic"""
    global heat_losses, grid
    i, j, io, jo, k = state

    # trivial if we're at the end location
    n, m = grid.shape
    if (i, j) == (n-1, m-1):
        heat_losses[state] = grid[n-1, m-1]
        return False

    # otherwise, use the neighbors to update the current guess at the answer
    ds = []
    for _io, _jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        # avoid backtracking
        if (_io, _jo) == (-io, -jo):
            continue
        # keep track if we're going in the same direction
        elif (_io, _jo) == (io, jo):
            _k = k + 1
        else:
            _k = 1

        # lookup, with a distance of np.inf if the state we're looking at isn't valid (ex. k > 3 or it's off the board)
        ds.append(heat_losses.get((i+_io, j+_jo, _io, _jo, _k), np.inf))

    # best distance
    d = min(ds) + grid[i,j]

    # return whether this gave an update
    if heat_losses[state] != d:
        heat_losses[state] = d
        return True
    else:
        return False

def update2(state):
    """Update the heat loss of a state (i, j, io, jo, k) [location] + [direction] + [number of steps so far in that direction] to the end location, with part 2 logic"""
    global heat_losses, grid
    i, j, io, jo, k = state

    # trivial if we're at the end location with at least 4 moves
    n, m = grid.shape
    if (i, j) == (n-1, m-1) and k >= 4:
        heat_losses[state] = grid[n-1, m-1]
        return False

    # otherwise, use the neighbors to update the current guess at the answer
    ds = []

    # if we can't turn yet
    if k < 4:
        ds.append(heat_losses.get((i+io, j+jo, io, jo, k+1), np.inf))
    # if we can turn
    else:
        for _io, _jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            if (_io, _jo) == (-io, -jo):
                continue
            elif (_io, _jo) == (io, jo):
                _k = k + 1
            else:
                _k = 1
    
            ds.append(heat_losses.get((i+_io, j+_jo, _io, _jo, _k), np.inf))

    # best distance
    d = min(ds) + grid[i,j]

    # return whether this gave an update
    if heat_losses[state] != d:
        heat_losses[state] = d
        return True
    else:
        return False
        
def part1(s):
    """Solve part 1"""
    global grid, heat_losses
    
    grid = parse_grid(s)
    #print_grid(grid)

    # locations to track the distances for
    n, m = grid.shape
    I = list(range(n))[::-1]
    J = list(range(m))[::-1]
    
    # initialize the current best guesses at distances to the end
    heat_losses = dict()
    for i in I:
        for j in J:
            for io, jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                for k in (1, 2, 3):
                    heat_losses[(i, j, io, jo, k)] = np.inf

    # update those best guesses until nothing is updated anymore
    # doing both "i then j" and "j then i" looping in case that helps get rid of np.infs faster
    any_updates = True
    while any_updates:
        any_updates = False
        for i in I:
            for j in J:
                for io, jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    for k in (1, 2, 3):
                        any_updates = update1((i, j, io, jo, k)) | any_updates
        for j in J:
            for i in I:
                for io, jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    for k in (1, 2, 3):
                        any_updates = update1((i, j, io, jo, k)) | any_updates

    # return the minimum distance from the 2 possible starting moves (down versus right)
    return min(heat_losses[(0, 1, 0, 1, 1)], heat_losses[(1, 0, 1, 0, 1)])
    
def part2(s):
    """Solve part 2"""
    global grid, heat_losses
    
    grid = parse_grid(s)
    
    # locations to track the distances for
    n, m = grid.shape
    I = list(range(n))[::-1]
    J = list(range(m))[::-1]
    
    # initialize
    heat_losses = dict()
    for i in I:
        for j in J:
            for io, jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                for k in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
                    heat_losses[(i, j, io, jo, k)] = np.inf

    # updates
    any_updates = True
    while any_updates:
        any_updates = False
        for i in I:
            for j in J:
                for io, jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    for k in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
                        any_updates = update2((i, j, io, jo, k)) | any_updates
        for j in J:
            for i in I:
                for io, jo in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    for k in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
                        any_updates = update2((i, j, io, jo, k)) | any_updates

    return min(heat_losses[(0, 1, 0, 1, 1)], heat_losses[(1, 0, 1, 0, 1)])


if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
