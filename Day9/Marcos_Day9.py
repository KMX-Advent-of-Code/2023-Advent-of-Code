import sys
import pandas as pd

sys.path.append("../../aoc_2023")

from aoc_helper import get_input

s, s2 = get_input()


def process_line(x):
    init = pd.Series([int(y) for y in x.split()])
    out = []
    while init.nunique() != 1:
        out.append(init.copy().tolist())
        init = (init.shift(-1) - init).dropna()
    delta = init.tolist()[-1]

    while out:
        x = out.pop()
        delta = x[-1] + delta
        #print (x,delta)

    return int(delta)


def process_line2(x):
    init = pd.Series([int(y) for y in x.split()])
    out = []
    while init.nunique() != 1:
        out.append(init.copy().tolist())
        init = (init.shift(-1) - init).dropna()
    delta = init.tolist()[-1]
    while out:
        x = out.pop()
        delta = x[0] - delta
        #print(x, delta)

    return int(delta)


#part 1
print("part 1")
print(sum([process_line(x) for x in s2]))

#part 2
print("part 2")
print(sum([process_line2(x) for x in s2]))
