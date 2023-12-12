import sys
import pandas as pd

sys.path.append("../../aoc_2023")

from aoc_helper import get_input

import numpy as np
from scipy.spatial.distance import pdist


def make_numpy_array(test):
    test_arr = np.array([list(x) for x in test])

    imarr = np.zeros(test_arr.shape)
    imarr[np.where(test_arr == '#')] = 1
    return imarr


def myinsert(imarr, x_list, y_list):
    print(imarr.shape)
    new_arr = np.insert(imarr, x_list, 0, axis=1)
    new_arr = np.insert(new_arr, y_list, 0, axis=0)
    return new_arr


def getexpansion(imarr):
    x_list = []
    y_list = []
    for x in range(imarr.shape[1]):
        if imarr[:, x].sum() == 0:
            x_list.append(x)
    for y in range(imarr.shape[0]):
        if imarr[y, :].sum() == 0:
            y_list.append(y)
    return x_list, y_list


def solve_part1(imarr, x_list, y_list):
    expanded_arr = myinsert(imarr, x_list, y_list)
    ys, xs = np.where(expanded_arr == 1)
    galaxy_coords = [(y, x) for y, x in zip(ys, xs)]
    return int(sum(pdist(galaxy_coords, metric='cityblock')))


def solve_part2(imarr, x_list, y_list, N):
    ys, xs = np.where(imarr == 1)
    test_gal_coords = [(y, x) for y, x in zip(ys, xs)]
    new_coords = []
    y_list = pd.Series(y_list)
    x_list = pd.Series(x_list)
    for y, x in test_gal_coords:
        yd = (y_list < y).sum() * (N - 1)
        xd = (x_list < x).sum() * (N - 1)
        new_coords.append((y + yd, x + xd))
    return int(sum(pdist(new_coords, metric='cityblock')))


if __name__ == '__main__':
    s, s2 = get_input(11)
    imarr = make_numpy_array(s2)
    x_list, y_list = getexpansion(imarr)
    print("part 1")
    print(solve_part1(imarr, x_list, y_list))
    print("part 2")
    print(solve_part2(imarr, x_list, y_list, 1_000_000))
