"""
Day 4: Scratchcards 
https://adventofcode.com/2023/day/4
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 4

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out
        
def get_nums(line):
    """Return a tuple of lists of the numbers found in this line"""
    head, body = tuple(line.split(':'))
    nums1, nums2 = tuple(body.split('|'))
    nums1 = [int(x) for x in nums1.split(' ') if x]
    nums2 = [int(x) for x in nums2.split(' ') if x]
    return nums1, nums2

def matches(nums_win, nums):
    """Count the matches in this line"""
    assert len(nums) == len(set(nums))
    return len(set(nums) & set(nums_win))

def score(matches):
    """Score the number of matches"""
    if matches:
        return 2**(matches-1)
    else:
        return 0

def part1(s):
    """Solve part 1"""
    list_of_num_pairs = [get_nums(line) for line in split(s)]
    matcheses = [matches(nums_win, nums) for nums_win, nums in list_of_num_pairs]
    scores = [score(matches) for matches in matcheses]
    return sum(scores)
    
    
def part2(s):
    """Solve part 2"""
    list_of_num_pairs = [get_nums(line) for line in split(s)]
    matcheses = [matches(nums_win, nums) for nums_win, nums in list_of_num_pairs]

    counts = [1] * len(matcheses)
    for i in range(len(counts)):
        have = counts[i]
        add = matcheses[i]
        for j in range(add):
            counts[i+j+1] += have

    return sum(counts)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))