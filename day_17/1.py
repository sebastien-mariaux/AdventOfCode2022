
import itertools


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
    raise RuntimeError('not possible')

def get_next_pos(direction, pos, blocks):
    if direction == 'R':
        next_pos = [(x+1, y) for x, y in pos]
    elif  direction == 'L':
        next_pos = [(x-1, y) for x, y in pos]
    elif direction == 'D':
        next_pos = [(x, y-1) for x, y in pos]
    intersect = [x for x in next_pos if x in blocks]
    if len(intersect) == 0:
        print('moves 1 ', direction)
        return next_pos, True
    print('dont move')
    return pos, False

def solve(data):
    jets = itertools.cycle(data)
    rock = 0
    top = 0
    blocks = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (7, 0)]
    pos = appears_at(rock, top)
    while rock < 2022:
        jet = next(jets)

        # activate the jets!!!
        if jet == '>':
            # block is close to right wall
            if [x for x in pos if x[0] == 7]:
                print('dont moves right')
            else:
                pos, _ = get_next_pos('R', pos, blocks)
        elif jet == '<':
            # block is close to left wall
            if [x for x in pos if x[0] == 1]:
                print('dont moves left')
                pass
            else:
                pos, _ = get_next_pos('L', pos, blocks)
        # block falls if it can
        pos, moved = get_next_pos('D', pos, blocks)
        if moved:
            print('falls 1')
        else:
            print('rocks settles at', pos)
            blocks += pos
            rock += 1
            top = max([y for _, y in  blocks])
            pos = appears_at(rock, top)
            print('rock appears at position', pos)
    return top


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 3068

def test_real():
    assert solve(import_data(False)) == 3065
