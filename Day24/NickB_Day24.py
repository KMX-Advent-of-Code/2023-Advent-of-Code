"""
Day 24: Never Tell Me The Odds
https://adventofcode.com/2023/day/24

Part 1: I used formulas on this page https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment

Part 2: I had trouble getting a "direct" system of equations working, so I broke it up into steps. This wasn't pretty.
1. Find the line that the rock follows, by finding the line that intersects the lines the hailstones travel along.
    I did do this with pytorch to get x and dx giving a parameterization of the rock's line, since my heart tells me the distance between lines is convex in spirit if you ignore redundancy in parametrizations of lines.
    The dx I got was precise enough to fix the rock's velocity, but x wasn't precise enough to get an answer.
2. Use the finalized dx to back out what x (the inital position of the rock) should be.
    I grabbed two hailstones and checked when the rock would need to hit the first so that later on it hits the second, using two single variable minimizations.
    This is enough to back out where the rock started.

In retrospect I should have spent more time working on a single system of equations, and using only 3 or 4 hailstones instead of the full data.
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 24

import torch
import numpy as np
from scipy.optimize import minimize_scalar

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_hailstone(line):
    """Convert a line of the input into the x, y, z, dx, dy, dz for a hailstone"""
    pos, vect = tuple(line.replace(' ', '').split('@'))
    x, y, z = [int(t) for t in pos.split(',')]
    dx, dy, dz = [int(t) for t in vect.split(',')]
    return x, y, z, dx, dy, dz

def loc_at_x(hailstone, x):
    """Get the location of a hailstone at a given value of x"""
    x0, y0, _, dx, dy, _ = hailstone
    t = (x - x0) / dx
    return (t, x, y0 + t * dy)

def loc_at_y(hailstone, y):
    """Get the location of a hailstone at a given value of y"""
    x0, y0, _, dx, dy, _ = hailstone
    t = (y - y0) / dy
    return (t, x0 + t * dx, y)

def get_key_segment(hailstone, m, M):
    """Get the segment (represented by its 2 endpoints) that lies within [m, M] bounds for x and y"""
    x, y, z, dx, dy, dz = hailstone

    # key locations
    loc_xm = loc_at_x(hailstone, m)
    loc_xM = loc_at_x(hailstone, M)
    loc_ym = loc_at_y(hailstone, m)
    loc_yM = loc_at_y(hailstone, M)

    segment = []

    # if the hailstone at t=0 is within the [m, M] bounds
    if (m <= x <= M) and (m <= y <= M):
        segment.append((0, x, y))

    # these check if the hailstone is ever at the m or M bounds (at t >= 0)
    if (loc_xm[0] >= 0) and (m <= loc_xm[2] <= M):
        segment.append(loc_xm)
    if (loc_xM[0] >= 0) and (m <= loc_xM[2] <= M):
        segment.append(loc_xM)
    if (loc_ym[0] >= 0) and (m <= loc_ym[1] <= M):
        segment.append(loc_ym)
    if (loc_yM[0] >= 0) and (m <= loc_yM[1] <= M):
        segment.append(loc_yM)

    assert len(segment) <= 2

    return segment

def intersectQ(segment1, segment2):
    """Check if two segments (given by their endpoints) intersect"""
    if len(segment1) == 0 or len(segment2) == 0:
        return False

    (_, x1, y1), (_, x2, y2) = segment1[0], segment1[-1]
    (_, x3, y3), (_, x4, y4) = segment2[0], segment2[-1]
    
    # using https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
    t_numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    u_numerator = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)
    u_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if t_denominator < 0:
        t_numerator *= -1
        t_denominator *= -1

    if u_denominator < 0:
        u_numerator *= -1
        u_denominator *= -1

    return (gte(t_numerator, 0) and gte(t_denominator, t_numerator)) and (gte(u_numerator, 0) and gte(u_denominator, u_numerator))

def equal(x1, x2, tol=1e-6):
    return abs(x1 - x2) < tol

def gte(x1, x2, tol=1e-6):
    return x1 - x2 > -tol

class Solver(torch.nn.Module):
    """Pytorch class for getting an approximate solution to part 2
    Searches for x and dx (position and direction) for the rock so that the line represented by the rock intersects the lines given by the hailstones
    """

    DTYPE = torch.double
    
    def __init__(self, s):
        """Set up the data X and DX for the hailstones, and x and dx (which we want to find) for the rock"""
        super().__init__()

        # parse input
        self.hailstones = [parse_hailstone(line) for line in split(s)]

        # friendlier format
        self.X = torch.tensor(np.array([list(hailstone[:3]) for hailstone in self.hailstones]), dtype=self.DTYPE)
        self.DX = torch.tensor(np.array([list(hailstone[3:]) for hailstone in self.hailstones]), dtype=self.DTYPE)
        self._DX = self.DX / np.linalg.norm(self.DX, axis=1).reshape(-1, 1)
        self.n = len(self.X)

        # variables for representing the main line
        self.x = torch.nn.Parameter(torch.randn(3, dtype=self.DTYPE) + self.X.mean(axis=0))
        self.dx = torch.nn.Parameter(torch.randn(3, dtype=self.DTYPE))

    def forward(self):
        """Calculate how far the rock's line is from touching the hailstones' lines"""
        # normalize the direction
        _dx = torch.nn.functional.normalize(self.dx, dim=0)

        # find normal vectors to planes containing the main line and the data lines
        normals = torch.nn.functional.normalize(torch.cross(self._DX, _dx.expand_as(self._DX), dim=1), dim=1)

        # return the sum of squared distances between lines
        d1 = (normals * self.X).sum(axis=1)
        d2 = (normals * self.x).sum(axis=1)
        return ((d1 - d2)**2).sum()

def part1(s):
    """Solve part 1"""
    hailstones = [parse_hailstone(line) for line in split(s)]
    segments = [get_key_segment(hailstone, 200_000_000_000_000, 400_000_000_000_000) for hailstone in hailstones]
    
    count = 0
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            if intersectQ(segments[i], segments[j]):
                count += 1
    
    return count
    
def part2(s):
    """Solve part 2"""

    # I ran this next block in a notebook, running the iterate() several times and tweaking the learning rate until it was below 1e10

    # set up the pytorch
    solver = Solver(s)
    #criterion = torch.nn.MSELoss(reduction='sum')
    #y = torch.tensor(0, dtype=solver.DTYPE)
    #
    # for running a few iterations
    #def iterate(iterations, iterations_print, learning_rate):
    #    optimizer = torch.optim.Adam(solver.parameters(), lr=learning_rate)
    #    for t in range(1, iterations+1):
    #        # Forward
    #        y_pred = solver.forward()
    #    
    #        # Compute and print loss
    #        loss = criterion(y_pred, y)
    #        if t % iterations_print == 0:
    #            print(t, loss.item())
    #    
    #        # Zero gradients, perform a backward pass, and update the weights.
    #        optimizer.zero_grad()
    #        loss.backward()
    #        optimizer.step()
    #
    # manually iterate until we're at acceptable error
    #iterate(10000, 1000, 1e8)

    # from here I did some messy work in a notebook, but you can just check that after rescaling we have solver.dx = [154, 75, 290]
    #dx = solver.dx.detach().numpy()
    #dx = dx / np.linalg.norm(dx)
    #dx = dx * np.linalg.norm([154, 75, 290])

    # so the only thing left to do is find x (the intial position of the rock), using this finalized dx value (since solver.x is not precise enough)

    # grab two hailstones to work with, chosen so that the rock would first hit x1 and then x2
    X = solver.X.detach().numpy()
    DX = solver.DX.detach().numpy()
    x1 = X[1,:]
    dx1 = DX[1,:]
    x2 = X[0,:]
    dx2 = DX[0,:]

    # using this dx, the goal is to find t for when the rock should hit hailstone 1 and dt for how long the rock would then travel to hit hailstone 2
    # I did this in a notebook with lots of tweaking, so the optimization bounds here are there just to speed up this demo
    dx = np.array([154, 75, 290])

    def distance_t_dt(t, dt):
        """The distance between the rock and hailstone 2 if we launched the rock from hailstone 1 at time t and let it travel for dt"""
        return np.sum(np.abs((x1 + dx1 * t) + dx * dt - (x2 + dx2 * (t + dt))))
    
    def distance_t(t):
        """The minimum distance between the rock and hailstone 2 if we launched the rock from hailstone 1 at time t"""
        return minimize_scalar(lambda dt: distance_t_dt(t, dt), bracket=[0.5e12, 0.6e12], tol=1e-20, options={'maxiter' : 10_000}).fun

    # when the rock would need to hit hailstone 1 so that it then goes on to hit hailstone 2
    t = int(minimize_scalar(distance_t, bracket=[0.2e12, 0.3e12], tol=1e-16, options={'maxiter' : 1_000}).x)

    # back out the intial position of the rock
    x = list((x1 + dx1 * t) - dx * t)
    
    return int(sum(x))

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
