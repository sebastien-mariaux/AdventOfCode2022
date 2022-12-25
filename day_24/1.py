from pprint  import pprint
import re
import itertools
import time
from collections import defaultdict

def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

def print_map(M, col_num, row_num):
    for i in range(row_num):
        for j in range(col_num):
            el = M[(i,j)]
            if len(el) == 1:
                print(el[0], end='')
            elif len(el) == 0:
                print('.', end='')
            else:
                print('+', end='')
        print()
    print()

def solve(data):
    M = {(i,j): [] if el == '.' else [el] for i, row in enumerate(data.splitlines()) for j, el in enumerate(row)}
    M[(0,1)] = ['E']
    print(M)

    col_num = len(data.splitlines()[0])
    row_num = len(data.splitlines())
    last_row = data.splitlines()[-1]
    end = next((row_num-1, i) for i, el in enumerate(last_row) if  el == '.')


    visited = defaultdict(list)

    for minute in range(1000):
        print(f'==== Minute {minute} ====')
        print_map(M, col_num, row_num)
        new_M = defaultdict(list)
        for position, elts in M.copy().items():
            next_position = position
            for el in elts:
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
                new_M[next_position].append(el)

        # Elf moves
        cp = next(k for k,v in M.items() if 'E' in v)
        print('cp', cp)
        adjacents = [
            (cp[0]+1, cp[1]),
            (cp[0], cp[1]+1),
            (cp[0], cp[1]),
            (cp[0]-1, cp[1]),
            (cp[0], cp[1]-1),
        ]
        adjacents = [el for el in adjacents if el[0] >= 0 and el[0] < row_num and el[1] >= 0 and el[1] < col_num]
        valid_adj = [el for el in adjacents if new_M[el] == [] and el not in visited[minute]]

        print('valid next positions', valid_adj)
        if end in valid_adj:
            print_map(M, col_num, row_num)
            return minute
        if not valid_adj:
            pass
        if len(valid_adj) == 1:
            new_M[valid_adj[0]].append('E')
            new_M[cp].remove('E')
        if len(valid_adj) > 1:
            visited[minute].append(valid_adj[0])
            new_M[valid_adj[0]].append('E')
            new_M[cp].remove('E')
        M = new_M.copy()





def main():
    print(solve(import_data(True)))
    # print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 0

def test_real():
    assert solve(import_data(False)) == 0