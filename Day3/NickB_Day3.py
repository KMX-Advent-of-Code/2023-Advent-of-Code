"""
Day 3: Gear Ratios
https://adventofcode.com/2023/day/3
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 3

NUMBERS = set(list('1234567890'))
IGNORE = '.'

def get_ints(line, i):
    """Return list of tuples (n, []) giving the ints and a list of indices they cover"""
    out = []
    n = ''
    indices = []
    for j, x in enumerate(line):
        if x in NUMBERS:
            n += x
            indices.append((i,j))
        else:
            if n:
                out.append((int(n), tuple(indices)))
                n = ''
                indices = []
    if n:
        out.append((int(n), tuple(indices)))
    return out

def get_symbols(line, i):
    """Return list of locations of the symbols"""
    out = []
    for j, x in enumerate(line):
        if not((x == IGNORE) or (x in NUMBERS)):
            out.append((i,j))
    return out

def includeQ(locs, symbols):
    """Check if a set of locations is adjacent to a symbol"""
    for i,j in locs:
        for io in (-1,0,1):
            for jo in (-1,0,1):
                try:
                    if (i+io,j+jo) in symbols:
                        return True
                except:
                    pass
    return False

def get_gears(line, i):
    """Return list of locations of the gears"""
    out = []
    for j, x in enumerate(line):
        if x == '*':
            out.append((i,j))
    return out

def get_ratio(gear, ints):
    """Get the ratio of a given gear"""
    i, j = gear
    _ints = []

    # Check which ints are next to it
    for n, locs in ints:
        adjacent = False
        
        # Look for adjacency left/right/up/down/diagonally
        for io in (-1,0,1):
            for jo in (-1,0,1):
                try:
                    if (i+io,j+jo) in locs:
                        adjacent = True
                except:
                    pass

        if adjacent:
            _ints.append(n)

    if len(_ints) == 2:
        return _ints[0] * _ints[1]
    else:
        return 0

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def part1(s):
    """Solve part 1"""
    # Ints with a list of locations
    ints = [x for i, line in enumerate(split(s)) for x in get_ints(line, i)]

    # Locations of symbols
    symbols = set([x for i, line in enumerate(split(s)) for x in get_symbols(line, i)])

    # Which numbers are next to symbols
    include = []
    for n, locs in ints:
        if includeQ(locs, symbols):
            include.append(n)

    return sum(include)
    
    
def part2(s):
    """Solve part 2"""
    # Ints with a list of locations
    ints = [x for i, line in enumerate(split(s)) for x in get_ints(line, i)]

    # Locations of symbols
    gears = set([x for i, line in enumerate(split(s)) for x in get_gears(line, i)])

    # Compute ratios for the gears
    ratios = [get_ratio(gear, ints) for gear in gears]

    return sum(ratios)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))