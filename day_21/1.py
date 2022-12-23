from pprint  import pprint
import re
import itertools

def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

def compute(m, M):
    if M[m].isnumeric():
        return int(M[m])
    elif '+' in M[m]:
        a, b = M[m].split(' + ')
        return compute(a, M) + compute(b, M)
    elif '*' in M[m]:
        a, b = M[m].split(' * ')
        return compute(a, M) * compute(b, M)
    elif '/' in M[m]:
        a, b = M[m].split(' / ')
        return compute(a, M) // compute(b, M)
    elif '-' in M[m]:
        a, b = M[m].split(' - ')
        return compute(a, M) - compute(b, M)
    else:
        raise RuntimeError('impossible')

def solve(data):
    M = {m: ope for m, ope in [x.split(': ') for x in data.splitlines()]}
    print(M)

    return(compute('root', M))


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 152

def test_real():
    assert solve(import_data(False)) == 364367103397416