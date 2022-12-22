from pprint  import pprint
import re
import itertools

def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

def neighbors(cube):
    x, y, z = cube
    return [
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1),
    ]


def solve(data):
    cubes = list(map(lambda x: tuple([int(i) for i in x.split(',')]),data.splitlines()))
    faces = 0
    adjacents = {cube: 6 for cube in cubes}
    for cube in cubes:
        for n in neighbors(cube):
            if n in cubes:
                adjacents[cube] -= 1

    print (adjacents)
    return sum(adjacents.values())




def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 64

def test_real():
    assert solve(import_data(False)) == 4320