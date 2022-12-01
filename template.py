import pytest
import re


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.readlines()
    return data

def solve():
    data = import_data()
    print(data)



if __name__ == '__main__':
    solve()


