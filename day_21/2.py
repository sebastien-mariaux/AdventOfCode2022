from pprint import pprint
import re
import itertools


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

# def compute(m, M):
#     if M[m].isnumeric():
#         return int(M[m])
#     elif '+' in M[m]:
#         a, b = M[m].split(' + ')
#         return compute(a, M) + compute(b, M)
#     elif '*' in M[m]:
#         a, b = M[m].split(' * ')
#         return compute(a, M) * compute(b, M)
#     elif '/' in M[m]:
#         a, b = M[m].split(' / ')
#         return compute(a, M) // compute(b, M)
#     elif '-' in M[m]:
#         a, b = M[m].split(' - ')
#         return compute(a, M) - compute(b, M)
#     else:
#         raise RuntimeError('impossible')


def compute(m, M):
    if m not in M.keys():
        return m
    if M[m].isnumeric():
        return M[m]
    else:
        value = M[m]
        terms = value.split(' ')
        for t in terms:
            if t.isalpha():
                value = value.replace(t, compute(t, M))
        return f"({value})"


def solve(data):
    M = {m: ope for m, ope in [x.split(': ') for x in data.splitlines()]}
    del M['humn']

    root_l, root_r = M['root'].split(' + ')

    l = compute(root_l, M)
    r = compute(root_r, M)
    print(eval(r))
    i =  0

    lo = 0
    hi = int(1e20)

    while lo < hi:
        print('lo', lo)
        print('hi', hi)
        mid = (lo + hi) // 2
        print('mid', mid)
        test = l.replace('humn', str(mid))
        if eval(test) == eval(r):
            return mid
        elif eval(test) < eval(r):
            hi = mid # this line needs to be reversed for sample case => probably a better way to do it...
        else:
            lo = mid # this line needs to be reversed for sample case => probably a better way to do it...
        import time




def main():
    # print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 301


def test_real():
    assert solve(import_data(False)) == 3782852515583
