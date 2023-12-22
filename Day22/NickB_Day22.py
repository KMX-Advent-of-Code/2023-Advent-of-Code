"""
Day 22: Sand Slabs
https://adventofcode.com/2023/day/22

I'm proud of how neat the Brick class is, but the falling bricks aren't fast
Each part takes about 30 seconds to run
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 22

from collections import deque

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

class Brick:
    def __init__(self, line, name=''):
        t1, t2 = tuple(line.split('~'))
        self.x1, self.y1, self.z1 = [int(t) for t in t1.split(',')]
        self.x2, self.y2, self.z2 = [int(t) for t in t2.split(',')]

        # sanity check
        dx = self.x1 - self.x2
        dy = self.y1 - self.y2
        dz = self.z1 - self.z2
        assert (dx == 0 and dy == 0 and dz == 0) | (dx != 0 and dy == 0 and dz == 0) | (dx == 0 and dy != 0 and dz == 0) | (dx == 0 and dy == 0 and dz != 0)

        self.name = name
        
        self.shadow = self.get_shadow()
        
        self.supports = None # list of bricks that support self
        self.supporting = None # list of bricks that are supported by self

    def get_shadow(self):
        """(x, y) coordinates that we take up"""
        x1, x2 = tuple(sorted([self.x1, self.x2]))
        y1, y2 = tuple(sorted([self.y1, self.y2]))

        if x1 == x2:
            return {(x1, y) for y in range(y1, y2+1)}
        else:
            return {(x, y1) for x in range(x1, x2+1)}

    def __repr__(self):
        return self.name

    @property
    def bottom_z(self):
        return min(self.z1, self.z2)

    @property
    def top_z(self):
        return max(self.z1, self.z2)

    @property
    def bottom(self):
        """Bottom layer (x, y, z)"""
        z = self.bottom_z
        return {(x, y, z) for x, y in self.shadow}

    @property
    def top(self):
        """Top layer (x, y, z)"""
        z = self.top_z
        return {(x, y, z) for x, y in self.shadow}

    def shadow_intersects(self, brick):
        """Check if our shadows overlap"""
        return len(self.shadow & brick.shadow) > 0
    
    def strong_intersects(self, brick):
        """Check if we intersect this other brick as far as top/bottom goes"""
        return (len(self.bottom & brick.top) > 0) | (len(self.top & brick.bottom) > 0)

    def move_up(self):
        self.z1 += 1
        self.z2 += 1

    def move_down(self):
        self.z1 -= 1
        self.z2 -= 1

    @property
    def would_fall(self):
        """Figure out what bricks would fall if we were removed"""
        # keep track of what's fallen, and iterate upwards (by z level) to check if things will fall
        falls = {self}
        explore = {self.top_z + 1 : self.supporting}
        Z = []
        Z.append(self.top_z + 1)

        # look through increasing z levels
        while Z:
            # sloppy but Z never gets big so this is fine
            Z = sorted(Z)[::-1]
            z = Z.pop()

            # the bricks we want to check if they'll fall
            bricks = explore[z]

            # go through the bricks
            for brick in bricks:
                _z = brick.top_z + 1
                
                # check if the stuff that's fallen so far makes it fall
                if len(set(brick.supports) - falls) == 0:
                    # it falls! note that
                    falls.add(brick)

                    # also add it to the Z levels and list of bricks to explore
                    if not _z in explore:
                        explore[_z] = []
                        Z.append(_z)
                    for _brick in brick.supporting:
                        explore[_z].append(_brick)

        # we technically don't fall, since we were removed
        return falls - {self}

class World:
    """Manages bricks"""
    
    def __init__(self, bricks):
        self.bricks = sorted(bricks, key=lambda brick: brick.bottom_z)
        self.neighbors = self.get_neighbors()

    def get_neighbors(self):
        """The bricks each brick could potentially intersect based on shadows, to narrow what each brick can intersect with"""
        neighbors = {}
        for brick in self.bricks:
            neighbors[brick] = []
            for _brick in self.bricks:
                if brick == _brick:
                    continue
                if brick.shadow_intersects(_brick):
                    neighbors[brick].append(_brick)
        return neighbors

    def fall(self):
        """Let all the bricks fall"""
        something_fell = True
        while something_fell:
            #print('Height', max([brick.top_z for brick in bricks]))
            something_fell = False

            # try lowering every brick
            for brick in self.bricks[::-1]:
                # move down
                brick.move_down()

                # see if nothing broke
                try:
                    assert brick.bottom_z > 0
                    for _brick in self.neighbors[brick]:
                        assert not brick.strong_intersects(_brick)

                    # if nothing broke, note that something fell so we should keep iterating
                    something_fell = True
                except:
                    brick.move_up()

    def set_support(self):
        """Set the supports and supporting for every brick"""
        for brick in self.bricks:
            # check what it supports by moving it down 1 and seeing what it intersects
            brick.supports = []
            brick.move_down()
            for _brick in self.bricks:
                if brick == _brick:
                    continue
                if brick.strong_intersects(_brick):
                    brick.supports.append(_brick)
            brick.move_up()

            # check what it's supporting by moving it up 1 and seeing what it intersects
            brick.supporting = []
            brick.move_up()
            for _brick in self.bricks:
                if brick == _brick:
                    continue
                if brick.strong_intersects(_brick):
                    brick.supporting.append(_brick)
            brick.move_down()

    def count_multi_supported(self):
        """Count the bricks that have multiple supports"""
        can_remove = set(self.bricks)
        for brick in self.bricks:
            if len(brick.supports) == 1 and brick.supports[0] in can_remove:
                can_remove.remove(brick.supports[0])
        return len(can_remove)

def part1(s):
    """Solve part 1"""
    bricks = [Brick(line) for line in split(s)]
    w = World(bricks)
    w.fall()
    w.set_support()
    return w.count_multi_supported()
    
def part2(s):
    """Solve part 2"""
    bricks = [Brick(line) for line in split(s)]
    w = World(bricks)
    w.fall()
    w.set_support()
    return sum([len(brick.would_fall) for brick in w.bricks])
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
