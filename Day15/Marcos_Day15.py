import sys
import pandas as pd
import re

sys.path.append("../../aoc_2023")

from aoc_helper import get_input


def hash(x):
    value = 0
    for char in x:
        value = value + ord(char)
        value = value * 17
        value = value % 256
    return value


def extract_text(text):
    num = None
    m = re.match('([a-z]+)([=-])(\d?)', text)
    if text[-1].isdigit():
        num = int(m.group(3))
    return [m.group(1), m.group(2), num]


def make_records(myinput):
    df = pd.DataFrame(pd.Series(myinput))
    df.columns = ['text']
    df[['letters', 'op',
        'num']] = df[['text']].apply(lambda x: extract_text(x['text']),
                                     result_type='expand',
                                     axis=1)
    df['hash'] = df['letters'].map(hash)
    return df.to_dict('records')


def make_boxes(myrecords):
    boxes = dict.fromkeys(list(range(256)))
    for key in boxes.keys():
        boxes[key] = {}
    for rec in myrecords:
        #print(boxes)
        #print(rec['text'])
        #print(rec['hash'])
        if rec['op'] == '=':
            #print(rec)
            boxes[rec['hash']][rec['letters']] = int(rec['num'])
        elif rec['op'] == '-':
            try:
                del boxes[rec['hash']][rec['letters']]
            except:
                pass
    return boxes


def process_boxes(boxes):
    res = 0
    for key, val in boxes.items():

        if val:
            for i, v in enumerate(val.values()):
                # print(key+1,i+1,v)
                val = (key + 1) * (i + 1) * v
                #print(val)
                res += val

    return res


#df['hash_value'] = df['text'].map(hash)

if __name__ == '__main__':

    s, s2 = get_input()
    myinput = s.split(',')
    ans = sum([hash(x) for x in myinput])
    print(f"Part 1 answer is {ans}")
    myrecords = make_records(myinput)
    boxes = make_boxes(myrecords)
    print(f"Part 2 answers is {process_boxes(boxes=boxes)}")
