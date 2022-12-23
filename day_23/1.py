from pprint import pprint
import re
import itertools
from collections import deque


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def draw_map(elfs):
    min_x = min([x for x, y in elfs])
    max_x = max([x for x, y in elfs])
    min_y = min([y for x, y in elfs])
    max_y = max([y for x, y in elfs])
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if (x, y) in elfs:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

def count_empty(elfs):
    min_x = min([x for x, y in elfs])
    max_x = max([x for x, y in elfs])
    min_y = min([y for x, y in elfs])
    max_y = max([y for x, y in elfs])
    count = 0
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if (x, y) not in elfs:
                count += 1
    return count

def adjacents(elf):
    x, y = elf
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if (i, j) != elf:
                yield (i, j)


def solve(data):
    R = deque(['N', 'S', 'W', 'E'])
    M = [list(row) for row in data.splitlines()]
    elfs = []
    for i, row in enumerate(M):
        for j, cell in enumerate(row):
            if cell == '#':
                elfs.append((i, j))
    draw_map(elfs)

    # starts rounds
    for i in range(10):
        next_elfs = {}
        for elf in elfs:
            # find adjacents
            adj = [a for a in adjacents(elf) if a in elfs]
            n_adj = [a for a in adj if a[0] < elf[0]]
            s_adj = [a for a in adj if a[0] > elf[0]]
            e_adj = [a for a in adj if a[1] > elf[1]]
            w_adj = [a for a in adj if a[1] < elf[1]]
            if not adj:
                continue
            for r in R:
                if r == 'N' and not n_adj:
                    next_elfs[elf] = (elf[0]-1, elf[1])
                    break
                if r == 'S' and not s_adj:
                    next_elfs[elf] = (elf[0]+1, elf[1])
                    break
                if r == 'E' and not e_adj:
                    next_elfs[elf] = (elf[0], elf[1]+1)
                    break
                if r == 'W' and not w_adj:
                    next_elfs[elf] = (elf[0], elf[1]-1)
                    break
        for elf, next_elf in next_elfs.items():
            same_target = [1 for e, ne in next_elfs.items() if ne == next_elf and e != elf]
            if not same_target:
                elfs.remove(elf)
                elfs.append(next_elf)
        R.rotate(-1)
        print('== End of round ==', i+1)
        draw_map(elfs)
    return(count_empty(elfs))


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 110


def test_real():
    assert solve(import_data(False)) == 3947
