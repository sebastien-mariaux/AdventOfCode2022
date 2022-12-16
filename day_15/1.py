import re
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def exclusion(S, md, B, target_row):
    E = set()
    for i in range(S[0]-md, S[0]+md+1):
        j = target_row
        if manhattan_distance(S, (i,j)) <= md and (i,j) != B:
            E.add((i,j))
    return E


def solve(data, target_row):
    regex = r"^Sensor at x=(-*\d*), y=(-*\d*): closest beacon is at x=(-*\d*), y=(-*\d*)"
    exclusion_zone = set()
    for ix, row in enumerate(data.splitlines()):
        print('row', ix)
        m = re.search(regex, row)
        s = (int(m.group(1)), int(m.group(2)))
        b = (int(m.group(3)), int(m.group(4)))
        md = manhattan_distance(s, b)
        e = exclusion(s, md, b, target_row)
        exclusion_zone.update(e)
    return len([x for x in exclusion_zone if x[1] == target_row])


# compute manhantan distance
def manhattan_distance(A, B):
    x1, y1 = A
    x2, y2 = B
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    print(solve(import_data(True), 10))
    print(solve(import_data(False), 2000000))

def test_sample():
    assert solve(import_data(True), 10) == 26

def test_real():
    assert solve(import_data(False), 2000000) == 4793062


# def test_exclusion():
#     print(exclusion((8,7), 9, (0,0)))
#     assert False


if __name__ == '__main__':
    main()
