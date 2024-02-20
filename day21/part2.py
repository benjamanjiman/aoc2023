from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    rocks = []
    num_rows, num_cols = len(lines), len(lines[0])
    for row_num, line in enumerate(lines):
        for col_num, char in enumerate(line):
            if char == '#':
                rocks.append((row_num, col_num))
            elif char == 'S':
                start_pos = (row_num, col_num)
    num_steps = 2000
    four_directions = [(0, 1), (1,0), (0, -1), (-1,0)]
    curr_pos = [start_pos]
    evens = [start_pos]
    goal = 26501365
    odds = []
    def f(n):
        a0 = 3691 # odd at step 65
        a1 = 32975 # even at step 196
        a2 = 91439 # odd at step 327

        b1 = a1-a0
        b2 = a2-a1
        return a0 + b1*n + (n*(n-1)//2)*(b2-b1)
    return f(goal//num_rows)
    for step in range(1, num_steps + 1):
        next_pos = []
        for row, col in curr_pos:
            for drow, dcol in four_directions:
                new_row = row + drow
                new_col = col + dcol
                mod_row = new_row % num_rows
                mod_col = new_col % num_cols
                if  (mod_row, mod_col) not in rocks:
                    if step%2:
                        if not (new_row, new_col) in odds:
                            odds.append((new_row,new_col))
                            next_pos.append((new_row, new_col))
                    else:
                        if not (new_row, new_col) in evens:
                            evens.append((new_row,new_col))
                            next_pos.append((new_row, new_col))
        if step%num_rows == goal%num_cols:
            print(step, len(odds), len(evens), step/num_rows)
        curr_pos = next_pos



    return len(evens)


INPUT_S = '''\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''
EXPECTED = 16


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
