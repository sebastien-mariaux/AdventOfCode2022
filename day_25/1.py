from pprint import pprint
import re
import itertools
from collections import deque, defaultdict


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

def MAPPING(value):
    if value == -2:
        return '='
    if value == -1:
        return '-'
    return str(value)


def SNAFU(decimal):
    snafu = defaultdict(int)
    snafu[0] = decimal // 5**0
    while True:
        i = next( (i for i, v in snafu.items() if v >= 3), None )
        if i is None:
            break
        value = snafu[i]
        remainder = max(value // 5, 1)
        snafu[i] -= 5 * (remainder )
        snafu[i+1] += remainder

    snafu = [MAPPING(x) for x in reversed(snafu.values())]
    return ''.join(snafu)


def DECIMAL(snafu):
    decimal = 0
    for i, char in enumerate(reversed(snafu)):
        if char == '=':
            char = -2
        if char == '-':
            char = -1
        decimal += 5**i * int(char)
    return decimal


def solve(data):
    total = 0
    for snafu in data.splitlines():
        total += DECIMAL(snafu)
    return SNAFU(total)


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


mapping = [
    ['1=-0-2', 1747],
    ['12111', 906],
    ['2=0=', 198],
    ['21', 11],
    ['2=01', 201],
    ['111', 31],
    ['20012', 1257],
    ['112', 32],
    ['1=-1=', 353],
    ['1-12', 107],
    ['12', 7],
    ['1=', 3],
    ['122', 37],
]




def test_snafu_to_decimal():
    for snafu, decimal in mapping:
        assert DECIMAL(snafu) == decimal

def test_snafu_simple():
    assert SNAFU(3) == '1='
    assert SNAFU(7) == '12'
    assert SNAFU(8) == '2='
    assert SNAFU(10) == '20'

def test_decimal_to_snafu():
    for snafu, decimal in mapping:
        assert SNAFU(decimal) == snafu


def test_sample():
    assert solve(import_data(True)) == '2=-1=0'


def test_real():
    assert solve(import_data(False)) == '2=0--0---11--01=-100'
