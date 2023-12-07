import sys

sys.path.append("../../aoc_2023")

from aoc_helper import get_input

from collections import Counter

value_map = {'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'T': 10}


class Hand:

    def __init__(self, line):
        self.hand, bid = line.split()
        self.hand_values = [value_map.get(x) or int(x) for x in self.hand]
        self.bid = int(bid)
        self.counter = Counter(self.hand)
        self.top_counts = self.counter.most_common()[:2]

    def __repr__(self):
        return self.hand

    def __lt__(self, other):
        if self.top_counts[0][1] != other.top_counts[0][1]:
            return self.top_counts[0][1] < other.top_counts[0][1]
        elif (self.top_counts[0][1]
              == other.top_counts[0][1]) and (self.top_counts[0][1] != 5):
            if self.top_counts[1][1] == other.top_counts[1][1] == 2:
                # two full houses or two two pairs
                pass
            elif self.top_counts[1][1] != other.top_counts[1][1]:
                ## 3 of of a kind vs  full house
                return self.top_counts[1][1] < other.top_counts[1][1]
        for a, b in zip(self.hand_values, other.hand_values):
            if a != b:
                return a < b


def solve(hands):
    l = list(zip(range(1, len(hands) + 1), sorted(hands)))
    return sum([(rank * hand.bid) for rank, hand in l])


class Hand2(Hand):
    value_map = {'J': -1, 'Q': 12, 'K': 13, 'A': 14, 'T': 10}

    def __init__(self, line):
        my_hand, bid = line.split()
        self.orig_hand = my_hand
        self.hand = my_hand
        self.hand_values = [self.value_map.get(x) or int(x) for x in self.hand]
        self.bid = int(bid)
        self.counter = Counter(self.hand)
        self.top_counts = [
            x for x in self.counter.most_common() if x[0] != 'J'
        ]
        self.apply_joker()
        self.counter = Counter(self.hand)
        self.top_counts = self.counter.most_common()

    def apply_joker(self):
        if self.top_counts:
            self.hand = self.hand.replace('J', self.top_counts[0][0])

    def __repr__(self):
        return f"{self.orig_hand} -> {self.hand}"


if __name__ == '__main__':

    s, s2 = get_input()
    real_hands_part1 = [Hand(x) for x in s2]
    real_hands_part2 = [Hand2(x) for x in s2]

    print("part 1")
    print(solve(real_hands_part1))
    print("part 2")
    print(solve(real_hands_part2))
