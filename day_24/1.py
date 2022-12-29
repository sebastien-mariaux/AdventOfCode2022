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


def display(cell):
    if len(cell) == 1:
        return cell[0]
    elif len(cell) == 0:
        return '.'
    return '+'


def print_map(M):
    for row in M:
        row = [display(x) for x in row]
        print(''.join(row))
    print()


def get_new_position(M, C, R, i, j, el):
    ii,jj = (i, j)
    if el == '>':
        ii, jj = (i, j+1)
        if M[ii][jj] == ['#']:
            ii, jj = (i, 1)
    elif el == '<':
        ii, jj = (i, j-1)
        if M[ii][jj] == ['#']:
            ii, jj = (i, C-2)
    elif el == '^':
        ii, jj = (i-1, j)
        if ii < 0:
            ii, jj = (R-2, j)
        if M[ii][jj] == ['#']:
            ii, jj = (R-1, j)
        if M[ii][jj] == ['#']:
            ii, jj = (R-2, j)
    elif el == 'v':
        ii, jj = (i+1, j)
        if ii == R:
            ii, jj = (0, j)
        if M[ii][jj] == ['#']:
            ii, jj = (0, j)
        if M[ii][jj] == ['#']:
            ii, jj = (1, j)
    return ii, jj


def solve(data):
    # M = [[] if el == '.' else [el]
    #      for i, row in enumerate(data.splitlines()) for j, el in enumerate(row)]
    M = [list(map(lambda x: [] if x == '.' else [x], list(r)))
         for r in data.splitlines()]
    M[0][1] = ['E']

    C = len(data.splitlines()[0])
    R = len(data.splitlines())
    last_row = data.splitlines()[-1]
    end = next((R-1, i) for i, el in enumerate(last_row) if el == '.')
    best = float('inf')
    print_map(M)

    s = (M, 0)
    Q = [s]
    seen = []
    while Q:
        state = Q.pop()
        m, minute = state

        if state in seen:
            continue
        seen.append(state)

        if minute >= best:
            continue

        # get next position for blizzards
        new_M = deepcopy(m)
        for i in range(R):
            for j in range(C):
                for el in m[i][j]:
                    ii, jj = get_new_position(m, C, R, i, j, el)
                    new_M[i][j].remove(el)
                    new_M[ii][jj].append(el)

        # Elf moves
        ei,ej = next((i,j) for i in range(R) for j in range(C) if m[i][j] == ['E'])
        adjacents = [
            (ei-1, ej),
            (ei, ej-1),
            (ei, ej),
            (ei+1, ej),
            (ei, ej+1),
        ]
        adjacents = [el for el in adjacents if el[0] >=
                     0 and el[0] < R and el[1] >= 0 and el[1] < C]
        valid_adj = [(i,j) for (i,j) in adjacents if new_M[i][j]
                     in [[], ['E']] and (i,j) != (0, 1)]

        # If no place to go then elf is on the wrong path
        if not valid_adj:
            continue
        if end in valid_adj:
            best = min(best, minute+1)
            print(best)
            continue

        for (i,j) in valid_adj:
            next_M = deepcopy(new_M)
            # print_map(next_M, C, R)
            # es = [k for k, v in next_M.items() if 'E' in v]
            next_M[ei][ej].remove('E')
            next_M[i][j].append('E')

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
