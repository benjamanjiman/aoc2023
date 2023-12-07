from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

rankings = {'A': 14, 'K': 13, 'Q':12, 'J':11, 'T':10}

def rank(hand):
    res = '.'
    for char in hand:
        val = rankings.get(char)
        if val is None:
            res = res + '0' + char
        else:
            res = res  + str(val)
    return res

def score(hand):
    lst = sorted(hand)
    if all([lst[i] == lst[i+1] for i in range(4)]):
        return '7' + rank(hand)

    if all([lst[i] == lst[i+1] for i in range(3)]) or  all([lst[i] == lst[i+1] for i in range(1,4)]):
        return '6' + rank(hand)

    if lst[0] == lst[1] and lst[2] == lst[3] and lst[3] == lst[4]:
        return '5' + rank(hand)

    if lst[0] == lst[1] and lst[1] == lst[2] and lst[3] == lst[4]:
        return '5' + rank(hand)

    if all([lst[i] == lst[i+1] for i in range(2)]) or  all([lst[i] == lst[i+1] for i in range(1,3)]) or  all([lst[i] == lst[i+1] for i in range(2,4)]):
        return '4' + rank(hand)
    tmp = {}
    for char in lst:
        if char in tmp:
            tmp[char] += 1
        else:
            tmp[char] = 1
    num_pairs = 0
    for k,v in tmp.items():
        if v == 2:
            num_pairs +=1
    if num_pairs == 2:
        return '3' + rank(hand)
    if num_pairs == 1:
        return '2' + rank(hand)
    for i in range(4):
        if lst[i] == lst[i+1]:
            raise Exception
    return '1' + rank(hand)

def compute(s: str) -> int:
    lines = s.splitlines()

    hands = []
    for row_num, line in enumerate(lines):
        hands.append((score(line.split()[0]),
                          int(line.split()[1])
, line.split()[0]))
    hands.sort(key = lambda x: x[0])
    res = 0
#    print(hands)
#    for hand in hands:
#        if hand[2][0] == '2':
#            print(hand)
    for rnk, (_, bid, cards) in enumerate(hands):
        res += (1 + rnk) * bid
    # TODO: implement solution here!
#    print(rnk, bid)
    return sum(e*bid for e, (_,bid,_) in enumerate(hands, 1))
    return res


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 6440


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
