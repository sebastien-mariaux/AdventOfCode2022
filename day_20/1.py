from pprint  import pprint
import re
import itertools
from collections import deque, Counter

def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    N = [(ix, int(el)) for (ix, el) in enumerate(data.splitlines())]
    L = len(N)
    d = N.copy()
    for n in N:
        ix = d.index(n)
        d.remove(n)
        new_ix = n[1] + ix
        if new_ix >=L:
            new_ix = new_ix % L + int(new_ix  / L)
        elif new_ix < 0:
            new_ix = new_ix % L + int(new_ix  / L) -1
        d.insert(new_ix, n)

    print(d)
    ref = next(i for i,v in enumerate(d) if v[1] == 0)
    print(ref)
    t_1000 = d[(ref+1000)%L][1]
    t_2000 = d[(ref+2000)%L][1]
    t_3000 = d[(ref+3000)%L][1]
    print(t_1000, t_2000, t_3000)
    return sum([t_1000, t_2000, t_3000])


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 3

def test_real():
    assert solve(import_data(False)) == 14888