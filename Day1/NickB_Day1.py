"""
Day 1: Trebuchet?!
https://adventofcode.com/2023/day/1
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 1

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def part1(input):
    """Solve part 1"""
    calibrations = [calibration(line) for line in split(input)]
    return sum(calibrations)
    
def part2(input):
    """Solve part 2"""
    calibrations = [smart_calibration(line) for line in split(input)]
    return sum(calibrations)

def calibration(line):
    digits = []
    for x in line:
        try:
            digits.append(int(x))
        except:
            pass
    return int(str(digits[0]) + str(digits[-1]))

def smart_calibration(line):
    # rules for reading digits
    convert_dict = {'one' : 1, 'two' : 2, 'three' : 3, 'four' : 4, 'five' : 5, 'six' : 6, 'seven' : 7, 'eight' : 8, 'nine' : 9, 'zero' : 0}
    for i in range(10):
        convert_dict[str(i)] = i
    
    # first digit
    digit1 = None
    found = False
    for i in range(len(line)):
        for s, x in convert_dict.items():
            try:
                if line[i:i+len(s)] == s:
                    digit1 = x
                    found = True
            except:
                pass

            if found:
                break
        if found:
            break

    # last digit
    digit2 = None
    found = False
    for i in range(len(line)-1, -1, -1):
        for s, x in convert_dict.items():
            try:
                if line[i:i+len(s)] == s:
                    digit2 = x
                    found = True
            except:
                pass

            if found:
                break
        if found:
            break

    return int(str(digit1) + str(digit2))

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        input = f.read()
    print('Part 1 solution:')
    print(part1(input))
    print()
    print('Part 2 solution:')
    print(part2(input))