"""
Day 2: Cube Conundrum
https://adventofcode.com/2023/day/2
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 2

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out
        
def get_int(string):
    """Assuming a string contains a single integer, retrieve that int"""
    chars = set(list('1234567890'))
    n = ''
    for char in string:
        if char in chars:
            n = n + char
    return int(n)

def parse_desc(desc):
    """Parse something like "3 blue" into a dictionary"""
    aux = desc.strip().split(' ')
    n = int(aux[0])
    color = aux[1]
    return color, n

def parse_game(line):
    """Parse a line into (game ID, list of dictionaries giving sets of RGB cubes)"""
    aux = line.split(':')
    s1 = aux[0]
    s2 = aux[1].strip()

    # ID
    id = get_int(s1)

    # List of dictionaries giving sets of RGB cubes
    subsets = s2.split(';')
    sets = []
    for subset in subsets:
        sets.append({})
        for desc in subset.strip().split(','):
            color, n = parse_desc(desc)
            sets[-1][color] = n

    return id, sets

def power_of_sets(sets):
    """Given a list of dictionaries giving sets of RGB cubes, compute the "power" of them"""
    # Determine counts of the cubes necessary
    counts = {}
    for _set in sets:
        for color in ('red', 'green', 'blue'):
            counts[color] = max(counts.get(color, 0), _set.get(color, 0))

    # Multiply them to get the "power"
    return counts['red'] * counts['green'] * counts['blue']

def part1(s):
    """Solve part 1"""
    games = [parse_game(line) for line in split(s)]
    
    cubes = {'red' : 12, 'green' : 13, 'blue' : 14}
    ids = []
    for id, sets in games:
        try:
            for _set in sets:
                for color in _set.keys():
                    assert _set.get(color) <= cubes.get(color)
            ids.append(id)
        except:
            pass

    return sum(ids)
    
def part2(s):
    """Solve part 2"""
    games = [parse_game(line) for line in split(s)]
    powers = [power_of_sets(sets) for id, sets in games]
    return sum(powers)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
