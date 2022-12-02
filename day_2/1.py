import pytest
import re

# A Rock
# B Paper
# C Scissors
# X loose
# Y draw
# Z zin

values = {
    'A': 1,
    'X': 1,
    'B': 2,
    'Y': 2,
    'C': 3,
    'Z': 3,
}


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

def score(x, y):
    return values[y] + win_score(x, y)

def win_score(x,y):
    if x == 'A' and y  == 'X' or x == 'B' and y  == 'Y' or x == 'C' and y  == 'Z':
        return 3
    if x == 'A' and y  == 'Y' or x == 'B' and y  == 'Z' or x == 'C' and y  == 'X':
        return 6
    return 0

def solve(data):
    data = [row.split(" ") for row in data.split("\n")]
    print(sum([score(row[0], row[1]) for row in data]))


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
