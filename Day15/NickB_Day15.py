"""
Day 15: Lens Library
https://adventofcode.com/2023/day/15

For part 2, the boxes are a list with length 256 and each one has a list of the lenses ('id', focal_length)
This is inefficient when searching the list to remove a lens, but runtime isn't an issue
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 15

def hash(x):
    """Hash a string"""
    h = 0
    for c in x:
        h += ord(c)
        h = (h * 17) % 256
    return h

def get_instruction(x):
    """Parse the string input into an instruction (including some hashing)"""
    if '=' in x:
        x, i = tuple(x.split('='))
        i = int(i)
        assert (i >= 1) & (i <= 9)
        return {
            'box' : hash(x),
            'label' : x,
            'operation' : '=',
            'focal_length' : i
        }
    elif '-' in x:
        x, i = tuple(x.split('-'))
        assert i == ''
        return {
            'box' : hash(x),
            'label' : x,
            'operation' : '-'
        }
    else:
        assert False

def apply_instruction(boxes, instruction):
    """Apply an instruction dictionary to our boxes"""
    # unpack
    box = instruction['box']
    label = instruction['label']
    operation = instruction['operation']
    focal_length = instruction.get('focal_length')

    # remove
    if operation == '-':
        # see if it's in the box
        i = None
        for j, (_label, _focal_length) in enumerate(boxes[box]):
            if label == _label:
                i = j
                break
        if not i is None:
            boxes[box].pop(i)

    # add
    if operation == '=':
        # see if it's in the box
        i = None
        for j, (_label, _focal_length) in enumerate(boxes[box]):
            if label == _label:
                i = j
                break

        # if it isn't
        if i is None:
            boxes[box].append((label, focal_length))
        # if it is
        else:
            boxes[box][i] = (label, focal_length)
            
def part1(s):
    """Solve part 1"""
    return sum([hash(x) for x in s.strip().split(',')])
    
def part2(s):
    """Solve part 2"""
    instructions = [get_instruction(x) for x in s.strip().split(',')]

    # boxes to work in
    boxes = [[] for i in range(256)]

    # do the instructions
    for instruction in instructions:
        apply_instruction(boxes, instruction)

    # measure the power
    power = 0
    for i, box in enumerate(boxes):
        for j, (label, focal_length) in enumerate(box):
            power += (i+1) * (j+1) * focal_length
    return power
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))