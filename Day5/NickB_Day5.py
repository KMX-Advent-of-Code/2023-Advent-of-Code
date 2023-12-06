"""
Day 5: If You Give A Seed A Fertilizer
https://adventofcode.com/2023/day/5

Approach: represent all indices as tuples (id_start, id_end) giving a range of tuples
So in part 2 we just need to propagate these id ranges through each of the provided maps
And part 1 is the same, but where our tuples will just be (id, id)
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 5

import pandas as pd

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def parse_seeds_1(line):
    """Parse the seeds line as in part 1, returning tuples (start_seed, end_seed)"""
    nums = [int(x) for x in line.split(':')[1].strip().split(' ')]
    return [(num, num) for num in nums]

def parse_seeds_2(line):
    """Parse the seeds line as in part 2, returning tuples (start_seed, end_seed)"""
    nums = [int(x) for x in line.split(':')[1].strip().split(' ')]
    assert len(nums) % 2 == 0
    out = []
    for i in range(0, len(nums), 2):
        out.append((nums[i], nums[i] + nums[i + 1] - 1))
    return out

def parse_map(block):
    """Parse the string block of a map into a dataframe representing the map"""
    # info about the map
    line = block[0]
    source, _, destination = tuple(line.split(' ')[0].split('-'))

    # parse the text into a DataFrame giving the map
    map = pd.DataFrame([parse_map_line(line) for line in block[1:]])
    map.columns = ['start_source', 'start_destination', 'length']
    map['source_min'] = map['start_source']
    map['source_max'] = map['start_source'] + map['length'] - 1
    map['destination_min'] = map['start_destination']
    map['destination_max'] = map['start_destination'] + map['length'] - 1
    map.sort_values('source_min', inplace=True)

    return source, destination, map

def parse_map_line(line):
    """Parse a single line of a map block"""
    start_destination, start_source, length = tuple([int(x) for x in line.split()])
    return start_source, start_destination, length

def augment_map(map, MAX=100000000000):
    """Add rows to a map so the rows cover the real line (up to +/-MAX)"""
    id1s = []
    id2s = []

    # start the first range
    id1s.append(-MAX)
    
    for row in map[['source_min', 'source_max']].apply(tuple, axis=1):
        source_min, source_max = row
    
        # range that ends right before the row
        id2s.append(source_min - 1)
    
        # range that starts right after the row
        id1s.append(source_max + 1)

    # end the last range
    id2s.append(MAX)
    
    map = pd.concat([map, pd.DataFrame({'source_min' : id1s, 'source_max' : id2s})])
    map = map.loc[map['source_min'] <= map['source_max']]
    map['destination_min'] = map['destination_min'].fillna(map['source_min'])
    map['destination_max'] = map['destination_max'].fillna(map['source_max'])
    map.sort_values('source_min', inplace=True)

    return map

def restrict_map(map, id_range):
    """Reduce a map to match a provided id range"""
    map = map.apply(lambda row: restrict_row(row, id_range), axis=1)
    map = map.loc[map['source_min'] <= map['source_max']]
    return map

def restrict_row(row, id_range):
    """Reduce the range of a map row to match the provided id range"""
    id_min = max(row['source_min'], id_range[0])
    id_max = min(row['source_max'], id_range[1])
    offset_min = id_min - row['source_min']
    offset_max = id_max - row['source_max']
    row['source_min'] = row['source_min'] + offset_min
    row['source_max'] = row['source_max'] + offset_max
    row['destination_min'] = row['destination_min'] + offset_min
    row['destination_max'] = row['destination_max'] + offset_max
    #print(row)
    #print()
    return row

def part1(s):
    """Solve part 1"""
    # parse the seeds (as ranges)
    seed_ranges = parse_seeds_1(split(s)[0][0])

    # parse the maps (as DataFrames)
    maps = {}
    for block in split(s)[1:]:
        source, destination, map = parse_map(block)
        maps[(source, destination)] = map

    # apply the maps to the seeds
    id_ranges = seed_ranges
    for conversion in [('seed', 'soil'), ('soil', 'fertilizer'), ('fertilizer', 'water'), ('water', 'light'), ('light', 'temperature'), ('temperature', 'humidity'), ('humidity', 'location')]:
        map = maps[conversion]

        # first augment the map DataFrame to effectively go from -inf to +inf
        map = augment_map(map)

        # for each range of ids, restrict the map to match the ids and record the converted ids
        id_ranges_new = []
        for id_range in id_ranges:
            id_ranges_new = id_ranges_new + list(restrict_map(map.copy(), id_range)[['destination_min', 'destination_max']].apply(tuple, axis=1))
        id_ranges = id_ranges_new
        
    return int(min([a for a, b in id_ranges]))
    
def part2(s):
    """Solve part 2"""
    # parse the seeds (as ranges)
    seed_ranges = parse_seeds_2(split(s)[0][0])

    # parse the maps (as DataFrames)
    maps = {}
    for block in split(s)[1:]:
        source, destination, map = parse_map(block)
        maps[(source, destination)] = map

    # apply the maps to the seeds
    id_ranges = seed_ranges
    for conversion in [('seed', 'soil'), ('soil', 'fertilizer'), ('fertilizer', 'water'), ('water', 'light'), ('light', 'temperature'), ('temperature', 'humidity'), ('humidity', 'location')]:
        map = maps[conversion]

        # first augment the map DataFrame to effectively go from -inf to +inf
        map = augment_map(map)

        # for each range of ids, restrict the map to match the ids and record the converted ids
        id_ranges_new = []
        for id_range in id_ranges:
            id_ranges_new = id_ranges_new + list(restrict_map(map.copy(), id_range)[['destination_min', 'destination_max']].apply(tuple, axis=1))
        id_ranges = id_ranges_new
        
    return int(min([a for a, b in id_ranges]))
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))