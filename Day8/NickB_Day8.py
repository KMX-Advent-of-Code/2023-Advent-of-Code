"""
Day 8: Haunted Wasteland
https://adventofcode.com/2023/day/8
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 8

I = {'R' : 1, 'L' : 0}

from math import lcm

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse(s):
    block1, block2 = tuple(split(s))
    directions = [I[char] for char in block1[0]]
    map = {}
    for line in block2:
        node, t = _parse_line(line)
        map[node] = t
    return directions, map

def _parse_line(line):
    aux = line.split('=')
    node = aux[0].strip()
    node1, node2 = tuple(aux[1].strip()[1:-1].split(', '))
    return node, (node1, node2)

def get_steps_1(directions, map):
    i = 0
    steps = 0
    n = len(directions)
    node = 'AAA'
    
    while node != 'ZZZ':
        node = map[node][directions[i]]
        steps += 1
        i += 1
        if i == n:
            i = 0
    
    return steps

def get_period(start_node, directions, map):
    i = 0
    steps = 0
    n = len(directions)
    node = start_node
    history = {}
    
    while not (i, node) in history:
        history[(i, node)] = steps
        node = map[node][directions[i]]
        steps += 1
        i += 1
        if i == n:
            i = 0
    
    return steps - history[(i, node)]

def get_steps_2(start_node, directions, map):
    i = 0
    steps = 0
    n = len(directions)
    node = start_node
    
    while node[2] != 'Z':
        node = map[node][directions[i]]
        steps += 1
        i += 1
        if i == n:
            i = 0
    
    return steps

def part1(s):
    """Solve part 1"""
    directions, map = parse(s)
    return get_steps_1(directions, map)
    
    
def part2(s):
    """Solve part 2"""
    directions, map = parse(s)
    start_nodes = [node for node in map if node[2] == 'A']
    periods = [get_period(node, directions, map) for node in start_nodes]
    return lcm(*periods)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))