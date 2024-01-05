from urllib.request import Request, urlopen
day = 12
session = '53616c7465645f5fa006ca78caa9a5bdd51f76aaf36ef6f669483cd6ec5502aa674c533c924d954b4c497c04f7f7b8cb27f2b5781fd7b8042c0f733d6e0b4047'

request = Request(f"https://adventofcode.com/2023/day/{day}/input")
request.add_header('Cookie', f'session={session}')
data1 = urlopen(request).read()

with open(f"q{day}.txt", "wb") as _fl2:
    _fl2.write(data1)

with open(f'q{day}.txt') as _fl:
    txt = _fl.read()
data1 = txt.split('\n')


data1 = data1[:-1] 
data1 = [row.split(' ') for row in data1]
data = []
for row in data1:
    row1 = (row[1]+','+row[1]+','+row[1]+','+row[1]+','+row[1]).split(',')
    data.append([row[0]+'?'+row[0]+'?'+row[0]+'?'+row[0]+'?'+row[0], [int(x) for x in row1]])

def first_num_tester(begin_char_num, chars, nums):
    """Given a string (chars), and a list of numbers (nums),
    can a sequence of "#"s starting at begin_char_num solve the first number in nums?
    (One example for each condition, respectively)
    
    Ex: begin_char_num=5, chars='.?.?.?.', nums=[1,1]
        .?.?.?.
        .....#.
        False, # could be placed at third ?.  However, this does not leave enough chars to handle the second 1.

    Ex: begin_char_num=0, chars='.?.?.?.', nums=[1,1]
        .?.?.?.
        #.
        False.  Char 0 is '.'  So, we can't put "#" there.

    Ex: begin_char_num=3, chars='.#.?.?.', nums=[1,1]
        .#.?.?.
        ...#.
        False.  We're solving the first "1".  Placing # at the first ? solves the second "1", not the first.

    Ex: begin_char_num=3, chars='.?.?#.?.', nums=[1,1]
        .?.?#.?.
        ...#.
        False.  Char 3 can be "#", but Char 4 must be "#" not "."

    Ex: begin_char_num=3, chars='.?.#.', [1] (final number)
        .?.#.
        .#.
        False.  Char 2 can be "#".  But, the remaining "#" adds an extra 1 to the schema.
    """
    first_num = nums[0]
    if len(chars) < sum(nums)+len(nums)-1-begin_char_num: #must be enough chars remaining to handle all remaining nums
        return False
    if '.' in chars[begin_char_num:begin_char_num+first_num]: #area for # can have no .
        return False
    if '#' in chars[:begin_char_num]: #before first # for first_num, can have no #
        return False
    if not begin_char_num+first_num >= len(chars) and chars[begin_char_num+first_num]=='#': #if char after #s, char after #s must not be #
        return False
    if len(nums)==1 and '#' in chars[begin_char_num+first_num+1:]: #if final num, all remaining chars must not be #
        return False
    return True

def first_num_placer(prev_char_count, prev_solution_count, chars, nums):
    """Given that number n was solved with prev_char_count characters, solve for number n+1.
    Number n has prev_solution_count solutions of length prev_char_count.  So, each solution
    we find for number n+1 contributes prev_solution_count total solutions.
    chars is only remaining chars.  nums is only remaining nums

    Ex.  '.?.?.?.', [1,1]
    Solve first 1:
    first_num_placer(0, 1, '.?.?.?.', [1,1])
        returns: {3:1, 5:1} (The first "1" has 1 solution of length 3 and 1 solution of length 5)
    Solve second 1:
    first_num_placer(3, 1, '?.?.', [1])
        returns: {5:1, 7:1}
    first_num_placer(5, 1, '?.', [1])
        returns: {5:1, 7:2} (3 solutions, total)
    """
    first_num_placements = {}
    for begin_char_num in range(len(chars)-sum(nums)-(len(nums)-1)+1): #total_chars - min_space_for_# - min_space_for_._between_# + 1
        if first_num_tester(begin_char_num, chars, nums):
            if prev_char_count+begin_char_num+nums[0]+1 in first_num_placements:
                first_num_placements[prev_char_count+begin_char_num+nums[0]+1] += prev_solution_count
            else:
                first_num_placements[prev_char_count+begin_char_num+nums[0]+1] = prev_solution_count
    return first_num_placements

total_ways = 0
for row in data:
    placements = {0:{0:1}} #there's one way, to use zero characters, to deal with the zero-th number (first number listed is numbered "1", zero-th number does not exist)
    chars = row[0]
    nums = row[1]
    for num_num in range(len(nums)): #each iteration handles one number on the list, solutions for first number on list are in placements[1]
        placements[num_num+1] = {}
        for prev_char_count, prev_solution_count in placements[num_num].items():
            first_num_placements = first_num_placer(prev_char_count, prev_solution_count, chars[prev_char_count:], nums[num_num:])
            for length, solution_count in first_num_placements.items():
                if length in placements[num_num+1]:
                    placements[num_num+1][length] += prev_solution_count
                else:
                    placements[num_num+1][length] = prev_solution_count
    total_ways += sum(placements[num_num+1].values())
total_ways
