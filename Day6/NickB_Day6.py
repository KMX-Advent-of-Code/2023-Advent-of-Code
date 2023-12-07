"""
Day 6: Wait For It
https://adventofcode.com/2023/day/6
"""

import numpy as np

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 6

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_input_1(s):
    line1, line2 = tuple(split(s))
    line1 = line1.split(':')[1].strip()
    line2 = line2.split(':')[1].strip()
    times = [int(x) for x in line1.split(' ') if x]
    distances = [int(x) for x in line2.split(' ') if x]
    return times, distances

def parse_input_2(s):
    line1, line2 = tuple(split(s))
    line1 = line1.split(':')[1].strip()
    line2 = line2.split(':')[1].strip()
    time = int(line1.replace(' ', ''))
    distance = int(line2.replace(' ', ''))
    return time, distance

def count_winning_charge_times(total_time, record):
    """Lazy way"""
    c = 0
    for charge_time in range(total_time + 1):
        if distance(charge_time, total_time) > record:
            c += 1
    return c
        
def distance(charge_time, total_time):
    return charge_time * (total_time - charge_time)
    
def part1(s):
    """Solve part 1"""
    # This comes out to times = [56, 97, 77, 93], distances = [499, 2210, 1097, 1440]
    times, distances = parse_input_1(s)
    
    counts = [count_winning_charge_times(t,d) for t, d in zip(times, distances)]
    return np.prod(counts)
    
    
def part2(s):
    """Solve part 2"""
    # This is t, d = 56977793, 499221010971440
    t, d = parse_input_2(s)

    # use the quadratic formula to estimate the charge times that give the record distance
    _t1 = (t - np.sqrt(t**2 - 4*d))/2
    _t2 = (t + np.sqrt(t**2 - 4*d))/2
    
    # round to integers
    t1 = int(np.floor(_t1))
    t2 = int(np.ceil(_t1))
    t3 = int(np.floor(_t2))
    t4 = int(np.ceil(_t2))
    
    # affirm these give the distances I expect
    assert distance(t1, t) < d
    assert distance(t2, t) > d
    assert distance(t3, t) > d
    assert distance(t4, t) < d
    
    return t3 - t2 + 1
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))