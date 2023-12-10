"""
Day 9: Mirage Maintenance
https://adventofcode.com/2023/day/9
"""

import numpy as np

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 9

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def extrapolate_forward(seq):
    """Take differences of our sequence until we get all zeros, and then add them up to extrapolate forward"""
    seq = np.array(seq)
    diffs = [seq[-1]]
    while not (seq == 0).all():
        seq = np.diff(seq)
        diffs.append(seq[-1])
    return sum(diffs)

def extrapolate_backward(seq):
    """Like the forward extrapolation, just add a +/- to the differences as appropriate to go backwards"""
    seq = np.array(seq)
    diffs = [seq[0]]
    while not (seq == 0).all():
        seq = np.diff(seq)
        diffs.append(seq[0])

    out = 0
    parity = False
    for x in diffs:
        if parity:
            out = out - x
        else:
            out = out + x
        parity = not parity
    
    return out

def part1(s):
    """Solve part 1"""
    seqs = [[int(x) for x in line.split(' ')] for line in split(s)]
    nexts = [extrapolate_forward(seq) for seq in seqs]
    return sum(nexts)
    
def part2(s):
    """Solve part 2"""
    seqs = [[int(x) for x in line.split(' ')] for line in split(s)]
    nexts = [extrapolate_backward(seq) for seq in seqs]
    return sum(nexts)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))