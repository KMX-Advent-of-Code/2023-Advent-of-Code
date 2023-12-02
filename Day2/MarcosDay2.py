import pandas as pd
import numpy as np


def parse_data(s2) -> pd.DataFrame:
    """s2 being a list of the lines of the input"""
    out = []
    for l in s2:
        game_id, data = l.split(':')
        for item in data.split(';'):
            for entry in item.split(','):
                n, color = entry.split()
                _, _id = game_id.split()
                out.append({'game_id': int(_id), 'n': int(n), 'color': color})
    return pd.DataFrame(out)


test = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split('\n')

query = "(color == 'red' and n > 12) or (color == 'green' and n > 13) or (color == 'blue' and n > 14)"

#test data
sum(
    set(parse_data(test)['game_id'].unique()).difference(
        parse_data(test).query(query)['game_id'].unique()))

# my input
sum(
    set(parse_data(s2)['game_id'].unique()).difference(
        parse_data(s2).query(query)['game_id'].unique()))

real_data = parse_data(s2)

real_data.groupby(['game_id', 'color'])[[
    'n'
]].max().reset_index().groupby('game_id')['n'].apply(np.prod).sum()
