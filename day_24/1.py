from pprint import pprint
import re
import itertools
import time
from collections import defaultdict
from copy import deepcopy


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def print_map(M, col_num, row_num):
    for i in range(row_num):
        for j in range(col_num):
            el = M[(i, j)]
            if len(el) == 1:
                print(el[0], end='')
            elif len(el) == 0:
                print('.', end='')
            else:
                print('+', end='')
        print()
    print()


def get_new_position(M, col_num, row_num, position, el):
    next_position = position
    if el == '>':
        next_position = (position[0], position[1]+1)
        if M[next_position] == ['#']:
            next_position = (position[0], 1)
    elif el == '<':
        next_position = (position[0], position[1]-1)
        if M[next_position] == ['#']:
            next_position = (position[0], col_num-2)
    elif el == '^':
        next_position = (position[0]-1, position[1])
        if next_position[0] < 0:
            next_position = (row_num-2, position[1])
        if M[next_position] == ['#']:
            next_position = (row_num-1, position[1])
        if M[next_position] == ['#']:
            next_position = (row_num-2, position[1])
    elif el == 'v':
        next_position = (position[0]+1, position[1])
        if next_position[0] == row_num:
            next_position = (0, position[1])
        if M[next_position] == ['#']:
            next_position = (0, position[1])
        if M[next_position] == ['#']:
            next_position = (1, position[1])
    return next_position


def solve(data):
    M = {(i, j): [] if el == '.' else [el]
         for i, row in enumerate(data.splitlines()) for j, el in enumerate(row)}
    M[(0, 1)] = ['E']

    col_num = len(data.splitlines()[0])
    row_num = len(data.splitlines())
    last_row = data.splitlines()[-1]
    end = next((row_num-1, i) for i, el in enumerate(last_row) if el == '.')
    best = float('inf')

    s = (M, 0)
    Q = [s]
    seen = []
    while Q:
        state = Q.pop()
        m, minute = state

        if state in seen:
            print('seen')
            continue
        seen.append(state)

        if minute >= best:
            continue

        new_M = defaultdict(list)
        for position, elts in m.copy().items():
            for el in elts:
                next_position = get_new_position(
                    m, col_num, row_num, position, el)
                new_M[next_position].append(el)

        # Elf moves
        cp = next(k for k, v in m.items() if 'E' in v)
        adjacents = [
            (cp[0]-1, cp[1]),
            (cp[0], cp[1]-1),
            (cp[0], cp[1]),
            (cp[0]+1, cp[1]),
            (cp[0], cp[1]+1),
        ]
        adjacents = [el for el in adjacents if el[0] >=
                     0 and el[0] < row_num and el[1] >= 0 and el[1] < col_num]
        valid_adj = [el for el in adjacents if new_M[el]
                     in [[], ['E']] and el != (0, 1)]
        # If no place to go then elf is on the wrong path
        if not valid_adj:
            continue
        if end in valid_adj:
            best = min(best, minute+1)
            print(best)

            continue
        for valid in valid_adj:
            next_M = deepcopy(new_M)
            # print_map(next_M, col_num, row_num)
            # es = [k for k, v in next_M.items() if 'E' in v]
            next_M[valid].append('E')
            next_M[cp].remove('E')

            Q.append((next_M, minute+1))
    return best


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 18


def test_real():
    assert solve(import_data(False)) == 0
