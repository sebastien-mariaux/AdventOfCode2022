from pprint import pprint
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
    cubes = list(map(lambda x: tuple([int(i)
                 for i in x.split(',')]), data.splitlines()))
    faces = 0
    adjacents = {cube: 6 for cube in cubes}
    for cube in cubes:
        for n in neighbors(cube):
            if n in cubes:
                adjacents[cube] -= 1

    surface = sum(adjacents.values())

    min_x = min([x for x, y, z in cubes])
    max_x = max([x for x, y, z in cubes])
    min_y = min([y for x, y, z in cubes])
    max_y = max([y for x, y, z in cubes])
    min_z = min([z for x, y, z in cubes])
    max_z = max([z for x, y, z in cubes])

    air_cubes = {}

    all_cubes = [(x, y, z) for x in range(min_x-1, max_x+2)
                 for y in range(min_y-1, max_y+2) for z in range(min_z-1, max_z+2)]
    for cb in all_cubes:
        if cb not in cubes:
            is_air_cube = True
            if not [1 for x in range(cb[0], max_x+1) if (x, cb[1], cb[2]) in cubes]:
                is_air_cube = False
            elif not [1 for x in range(min_x, cb[0]) if (x, cb[1], cb[2]) in cubes]:
                is_air_cube = False
            elif not [1 for y in range(cb[1], max_y+1) if (cb[0], y, cb[2]) in cubes]:
                is_air_cube = False
            elif not [1 for y in range(min_y, cb[1]) if (cb[0], y, cb[2]) in cubes]:
                is_air_cube = False
            elif not [1 for z in range(cb[2], max_z+1) if (cb[0], cb[1], z) in cubes]:
                is_air_cube = False
            elif not [1 for z in range(min_z, cb[2]) if (cb[0], cb[1], z) in cubes]:
                is_air_cube = False

            if is_air_cube:
                air_cubes[cb] = 6

    for ac in air_cubes:
        for n in neighbors(ac):
            if n in air_cubes:
                air_cubes[ac] -= 1
    return surface - sum(air_cubes.values())


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 58


def test_real():
    assert solve(import_data(False)) == 4320
