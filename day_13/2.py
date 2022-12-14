from ast import literal_eval
from pprint import pprint
from functools import cmp_to_key

def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def is_right(L, R):
    for ix, l in enumerate(L):
        if ix + 1 > len(R):
            return False
        r = R[ix]
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return True
            elif l > r:
                return False
            continue
        if isinstance(l, int):
            l = [l]
        if isinstance(r, int):
            r = [r]
        if (x := is_right(l, r)) is None:
            continue
        else:
            return x
    if len(R) > len(L):
        return True
    else:
        return None


def solve(data):
    valid = []
    P = [literal_eval(p) for p in data.split('\n') if  p != ''] + [[[2]], [[6]]]
    P = sorted(P, key=cmp_to_key(lambda L, R: -1 if is_right(L, R) else 1))
    dividers = [ix +1 for (ix, p)  in enumerate(P) if p in [[[2]], [[6]]]]
    print(dividers[0] * dividers[1])

def main():
    solve(import_data(True))
    solve(import_data(False))


def test_case_1():
    L = [1, 1, 3, 1, 1]
    R = [1, 1, 5, 1, 1]
    assert is_right(L, R)
    assert not is_right(R, L)


def test_case_5():
    L = [7, 7, 7, 7]
    R = [7, 7, 7]
    assert not is_right(L, R)
    assert is_right(R, L)


def test_case_8():
    L = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
    R = [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
    assert not is_right(L, R)
    assert is_right(R, L)


def test_case_7():
    L = [[[]]]
    R = [[]]
    assert not is_right(L, R)
    assert is_right(R, L)


def test_case_4():
    L = [[4, 4], 4, 4]
    R = [[4, 4], 4, 4, 4]
    assert is_right(L, R)
    assert not is_right(R, L)


def test_case_custom():
    L = [0, [1, 2], 4]
    R = [0, [1, 2], 3]
    assert not is_right(L, R)
    assert is_right(R, L)


def test_case_custom_bis():
    L = [0, [1, 1], 4]
    R = [0, [1, 2], 3]
    assert is_right(L, R)
    assert not is_right(R, L)


def test_equal():
    X = [0, [1, 1], 4]
    assert is_right(X, X) == None


if __name__ == '__main__':
    main()
