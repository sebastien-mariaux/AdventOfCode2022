from pprint import pprint
import re
import itertools


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def turn(current,  letter):
    return {
        '>': {
            'L': '^',
            'R': 'v'
        },
        '<': {
            'L': 'v',
            'R': '^'
        },
        '^': {
            'L': '<',
            'R': '>'
        },
        'v': {
            'L': '>',
            'R': '<'
        }
    }[current][letter]


def solve(data):
    M, I = data.split('\n\n')
    M = [list(row) for row in M.splitlines()]

    width = max([len(row) for row in M])
    for row in M:
        if len(row) < width:
            row += [' '] * (width - len(row))
    start = M[0].index('.')
    M[0][start] = '>'
    position = (0, start)
    facing = '>'

    J = ''
    for i in I:
        if i.isnumeric():
            J += i
        else:
            J += f" {i} "
    J = J.split(' ')
    for j in J:
        if j.isnumeric():
            for i in range(int(j)):
                if facing == '>':
                    new_position = (position[0], position[1] + 1)
                    # On dépasse à droite
                    if new_position[1] >= len(M[new_position[0]]) or M[new_position[0]][new_position[1]] == ' ':
                        start_row = next(i for i, v in enumerate(
                            M[position[0]]) if v in ['.', '#', '>', '<', '^', 'v'])
                        new_position = [position[0], start_row]
                    if M[new_position[0]][new_position[1]] in ['.', '>', '<', '^', 'v']:
                        M[new_position[0]][new_position[1]] = '>'
                        position = new_position
                    elif M[new_position[0]][new_position[1]] == '#':
                        break
                if facing == '<':
                    new_position = (position[0], position[1] - 1)
                    # on dépasse à gauche
                    if new_position[1] < 0 or M[new_position[0]][new_position[1]] == ' ':
                        row = M[new_position[0]]
                        next_valid = max(
                            [j for j, v in enumerate(row) if v in [
                                '.', '>', '<', '^', 'v', '#']]
                        )
                        new_position = [position[0], next_valid]
                    if M[new_position[0]][new_position[1]] in ['.', '>', '<', '^', 'v']:
                        M[new_position[0]][new_position[1]] = '<'
                        position = new_position
                    elif M[new_position[0]][new_position[1]] == '#':
                        break
                if facing == '^':
                    new_position = (position[0] - 1, position[1])
                    if new_position[0] < 0 or M[new_position[0]][new_position[1]] == ' ':
                        column = [row[new_position[1]] for row in M]
                        next_valid = next(
                            i for i, v in enumerate(itertools.cycle(reversed(column)))
                            if v in ['.', '#', '>', '<', '^', 'v']
                            and i > len(M) - position[0]
                        )
                        new_position = ((len(M) - next_valid - 1) %
                                        len(M), position[1])
                    if M[new_position[0]][new_position[1]] in ['.', '>', '<', '^', 'v']:
                        M[new_position[0]][new_position[1]] = '^'
                        position = new_position
                    elif M[new_position[0]][new_position[1]] == '#':
                        break
                if facing == 'v':
                    new_position = (position[0] + 1, position[1])
                    if new_position[0] >= len(M) or M[new_position[0]][new_position[1]] == ' ':
                        column = [row[new_position[1]] for row in M]
                        next_valid = next(
                            i for i, v in enumerate(itertools.cycle(column))
                            if v in ['.', '#', '>', '<', '^', 'v']
                            and i > position[0])
                        new_position = [next_valid % len(M), position[1]]
                    if M[new_position[0]][new_position[1]] in ['.', '>', '<', '^', 'v']:
                        M[new_position[0]][new_position[1]] = 'v'
                        position = new_position
                    elif M[new_position[0]][new_position[1]] == '#':
                        break
        else:
            facing = turn(facing, j)
            M[position[0]][position[1]] = facing

        # for row in M:
        #     print(''.join(row))
        # print('last rule', j)

    facing_score = {
        '>': 0,
        'v': 1,
        '<': 2,
        '^': 3
    }[facing]

    final_row = position[0] + 1
    final_column = position[1] + 1

    return 1000*final_row + 4*final_column+facing_score


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 6032


def test_real():
    assert solve(import_data(False)) == 66292
