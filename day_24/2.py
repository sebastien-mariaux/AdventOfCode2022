from pprint import pprint
import re
import itertools
import time
from collections import defaultdict, deque
from copy import deepcopy


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def display(cell, E):
    if E:
        return 'E'
    if len(cell) == 1:
        return cell[0]
    elif len(cell) == 0:
        return '.'
    return '+'


def print_map(M, i, j):
    for ii, row in enumerate(M):
        row = [display(x, ii == i and jj == j) for jj, x in enumerate(row)]
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
    M = [list(map(lambda x: [] if x == '.' else [x], list(r)))
         for r in data.splitlines()]

    C = len(data.splitlines()[0])
    R = len(data.splitlines())
    last_row = data.splitlines()[-1]
    end = next((R-1, i) for i, el in enumerate(last_row) if el == '.')
    # print_map(M)
    start = (0,1)
    current_time = 0
    for start, end in [(start, end), (end,start), (start, end)]:
        s = (start[0],start[1],current_time+1)
        Q = deque([s])
        seen = set()
        while Q:
            state = Q.popleft()
            ei, ej, minute = state

            if state in seen:
                continue
            seen.add(state)

            # get next position for blizzards
            if minute > current_time:
                current_time = minute
                new_M = [[[] for j in range(C)] for i in range(R)]
                for i in range(R):
                    for j in range(C):
                        for el in M[i][j]:
                            ii, jj = get_new_position(M, C, R, i, j, el)
                            new_M[ii][jj].append(el)
                M = new_M
                # print(minute)
                # print_map(M, ei, ej)
            # Elf moves
            if start == (0,1):
                adjacents = [
                    (ei+1, ej),
                    (ei, ej+1),
                    (ei, ej),
                    (ei-1, ej),
                    (ei, ej-1),
                ]
            else:
                adjacents = [
                    (ei, ej-1),
                    (ei-1, ej),
                    (ei, ej),
                    (ei+1, ej),
                    (ei, ej+1),
                ]
            adjacents = [el for el in adjacents if el[0] >=
                        0 and el[0] < R and el[1] >= 0 and el[1] < C]
            valid_adj = [(i,j) for (i,j) in adjacents if not M[i][j]]

            # If no place to go then elf is on the wrong path
            if end in valid_adj:
                current_time = minute
                break

            for (i,j) in valid_adj:
                Q.append((i,j, minute+1))
    return current_time



def main():
    print(solve(import_data(True)))
    # print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 54


def test_real():
    assert solve(import_data(False)) == 789

