from aoc_helper import get_input
from tqdm import tqdm
import re

test_data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split('\n\n')


class myMapper():
    def __init__(self):
        self.records = []

    def add_data(self, dest_start, source_start, length):
        self.records.append({
            'source_start': source_start,
            'source_end': source_start + length - 1,
            'delta': dest_start - source_start
        })

    def get(self, n):
        for rec in self.records:
            if rec['source_start'] <= n <= rec['source_end']:
                return n + rec['delta']
        return n


def process_map(x):
    m = myMapper()
    nums = []
    for item in x.split('\n'):
        out = [int(x) for x in re.findall("\d+", item)]
        if out:
            nums.append((out))
    for num in nums:
        m.add_data(*num)
    return m


def process_all_maps(data):
    return [int(x) for x in re.findall("\d+", data[0])
            ], [process_map(row) for row in data[1:]]


def process_one_seed(seed, maps):
    val = seed
    for map in maps:
        val = map.get(val)
    return val


def solve_part1(data):
    seeds, maps = process_all_maps(data)
    return min([process_one_seed(x, maps) for x in seeds])


def search_seeds(start_range, end_range, maps, current_best=None):
    """Scan the range at 10000 spots, then pick the lowest and scan down by 1 """
    search_space = range(start_range, end_range,
                         (end_range - start_range) // 1000)
    candidate_seed, candidate_location = sorted([(x, process_one_seed(x, maps))
                                                 for x in tqdm(search_space)],
                                                key=lambda x: x[1])[0]
    loc = candidate_location
    seed = candidate_seed
    print(f"Candidate seed {seed} at final loc {loc}")
    ## it's possible for some other input that the candidate could be larger
    ## than the best one already, but the by down 1 scan could go below the existing
    ## lowest. So not sure if this is a universal solution. But if it was  wrong
    ## I could just turn this optimization off (which I did not use in the original solve)


    if current_best is not None:
        if current_best < candidate_location:
            print("returning candidate not final loc")
            return candidate_location

    print("Scanning for exact")

    while True:
        seed = seed - 1
        new_loc = process_one_seed(seed, maps)
        if new_loc > loc:
            break
        loc = new_loc
    return loc


def solve_part2(test_data):
    out = []
    seeds, maps = process_all_maps(test_data)
    seed_pairs = []
    for i in range(0, len(seeds), 2):
        seed_pairs.append((seeds[i], seeds[i + 1]))
    current_best = None
    for a, b in seed_pairs:
        start_range, end_range = a, a + b - 1
        search_result = search_seeds(start_range,
                                     end_range,
                                     maps,
                                     current_best=current_best)
        if current_best is None:
            current_best = search_result
        elif search_result < current_best:
            current_best = search_result
        print(search_result)
        out.append(search_result)
    return min(out)


if __name__ == '__main__':
    day5_string, day5_list = get_input()
    real_data = day5_string.split('\n\n')
    print(f"Part 1 test answer is {solve_part1(test_data)}")
    print(f"Part 1 answer is {solve_part1(real_data)}")
    print(f"Part 2 answer is {solve_part2(real_data)}")
