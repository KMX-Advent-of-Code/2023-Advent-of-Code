digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def flatten_list(list_of_lists):
    return [y for x in list_of_lists for y in x]


def getnumbers(x):
    l = [(i, x) for i, x in enumerate(list(x)) if x.isdigit()]
    return l


def myregex(s):
    t = [[(x.start(), digits[d]) for x in (re.finditer(d, s))]
         for d in digits.keys()]
    return flatten_list([z for z in t if z])


def alldigits(s):
    thedigits = sorted(myregex(s) + getnumbers(s), key=lambda x: x[0])
    return int(thedigits[0][1] + thedigits[-1][1])


def alldigits_part1(s):
    thedigits = sorted(getnumbers(s), key=lambda x: x[0])
    return int(thedigits[0][1] + thedigits[-1][1])


#part 1

## actual solution of part 2 was overwritten I as I scrambled due to do part 2, but the _part1 function captures the spirit.
# I didn't have to track the indexes or sort in my original alldigits function.

sum([alldigits_part1(x) for x in myinput])

# part 2
sum([alldigits(x) for x in myinput])
