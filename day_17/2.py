
import itertools
from pprint import pprint


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def appears_at(rock, top):
    rock = rock % 5
    if rock == 0:
        return [(3, top + 4), (4, top + 4),
                (5, top + 4), (6, top + 4)]
    if rock == 1:
        return [(4, top + 4), (3, top + 5),
                (4, top + 5), (5, top + 5), (4, top + 6)]
    if rock == 2:
        return [(3, top + 4), (4, top + 4), (5, top + 4),
                (5, top+5), (5, top+6)]
    if rock == 3:
        return [(3, top + 4), (3, top + 5), (3, top + 6), (3, top + 7)]
    if rock == 4:
        return [(3, top+4), (4, top+4), (3, top+5), (4, top+5)]


def get_next_pos(direction, pos, blocks):
    if direction == 'R':
        next_pos = [(x+1, y) for x, y in pos]
    elif direction == 'L':
        next_pos = [(x-1, y) for x, y in pos]
    elif direction == 'D':
        next_pos = [(x, y-1) for x, y in pos]
    intersect = [x for x in next_pos if x in blocks]
    if len(intersect) == 0:
        return next_pos, True
    return pos, False


def solve(data, is_sample):
    jets = iter(data)
    rock = 0
    top = 0
    blocks = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (7, 0)]
    pos = appears_at(rock, top)
    cycles = []
    inner_count = 0

    # This is used only to find parameters of the final operation
    while rock < (1707+168):
        inner_count += 1
        try:
            jet = next(jets)
        except:
            jets = iter(data)
            jet = next(jets)
            cycles.append([rock, rock % 5, inner_count, top])

        # activate the jets!!!
        if jet == '>':
            # block is close to right wall
            if not [x for x in pos if x[0] == 7]:
                pos, _ = get_next_pos('R', pos, blocks)
        elif jet == '<':
            # block is close to left wall
            if not [x for x in pos if x[0] == 1]:
                pos, _ = get_next_pos('L', pos, blocks)
        # block falls if it can
        pos, moved = get_next_pos('D', pos, blocks)
        if not moved:
            blocks += pos
            rock += 1
            top = max([y for _, y in blocks])
            pos = appears_at(rock, top)
            inner_count = 0
    pprint(cycles)

    # round 1 to 36 : top = 61
    # then cycles of 35 => top + 53
    if is_sample:
        # Height resulting from N cycles + height of first rocks before cycle  starts + remaing rock to fall after last full cycle ends
        # At the end, it remains 14 cycles (1000000000000 -36) % 35
        # We know that 14 cycles after the end of a cycle, the height increases by (78-61)
        return int((1000000000000 -36)  /35)*53 + 61 + (78-61)
    # round 1 to 1707 : top = 2569
    # then cycles of (3442-1707) => top + (5280-2569)
    return int((1000000000000 -1707)  /(3442-1707))*(5280-2569) + 2569 + (2841-2569)


def main():
    print(solve(import_data(True), is_sample=True))
    print(solve(import_data(False), is_sample=False))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True), True) == 1514285714288


def test_real():
    assert solve(import_data(False), False) == 1562536022966
