import pytest
import re


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve():
    data = import_data(False).split("\n\n")
    data = [sum([int(i) for i in el.split("\n")]) for el in data]
    print(max(data))




if __name__ == '__main__':
    solve()


