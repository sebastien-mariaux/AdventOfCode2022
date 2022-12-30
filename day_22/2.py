from pprint import pprint
import re
import itertools
import time

def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def print_face(face):
    print(f"==== FACE { face['name'] } ====")
    for row in face['map']:
        print(''.join(row))


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


def switch_from_face(face, ii, jj, facing, faces):
    top, right, front, left, bot, back = faces
    if face['name'] == 'top':
        if facing == '>':
            return right, ii, 0, '>'
        elif facing == 'v':
            return front, 0, jj, 'v'
        elif facing == '<':
            return left, 50-ii-1, 0, '>'
        elif facing == '^':
            return back, jj, 0, '>'
    if face['name'] == 'left':
        if facing == '>':
            return bot, ii, 0, '>'
        elif facing == 'v':
            return back, 0, jj, 'v'
        elif facing == '<':
            return top, 50-ii-1, 0, '>'
        elif facing == '^':
            return front, jj, 0, '>'
    if face['name'] == 'back':
        if facing == '>':
            return bot, 49, ii, '^'
        elif facing == 'v':
            return right, 0, jj, 'v'
        elif facing == '<':
            return top, 0, ii, 'v'
        elif facing == '^':
            return left, 49, jj, '^'
    if face['name'] == 'right':
        if facing == '>':
            return bot, 50-ii-1, 49, '<'
        elif facing == 'v':
            return front, jj, 49, '<'
        elif facing == '<':
            return top, ii, 49, '<'
        elif facing == '^':
            return back, 49, jj, '^'
    if face['name'] == 'front':
        if facing == '>':
            return right, 49, ii, '^'
        elif facing == 'v':
            return bot, 0, jj, 'v'
        elif facing == '<':
            return left, 0, ii, 'v'
        elif facing == '^':
            return top, 49, jj, '^'
    if face['name'] == 'bot':
        if facing == '>':
            return right, 50-ii-1, 49, '<'
        elif facing == 'v':
            return back, jj, 49, '<'
        elif facing == '<':
            return left, ii, 49, '<'
        elif facing == '^':
            return front, 49, jj, '^'

def solve(data):
    M, I = data.split('\n\n')
    M = [list(row) for row in M.splitlines()]
    top = {'name': 'top', 'map': [x[50:100] for x in M[0:50]]}
    right = {'name': 'right', 'map': [x[100:150] for x in M[0:50]]}
    front = {'name': 'front', 'map': [x[50:100] for x in M[50:100]]}
    left = {'name': 'left', 'map':  [x[0:50] for x in M[100:150]]}
    bot = {'name': 'bot', 'map': [x[50:100] for x in M[100:150]]}
    back = {'name': 'back', 'map':  [x[0:50] for x in M[150:200]]}

    faces = [top, right, front, left, bot, back]
    face = top
    top['map'][0][0] = '>'
    ii = 0
    jj = 0
    facing = '>'

    J = ''
    for i in I:
        if i.isnumeric():
            J += i
        else:
            J += f" {i} "
    J = J.split(' ')
    for j in J:
        print("Instruction", j)
        if j.isnumeric():
            for i in range(int(j)):
                new_face =  face
                new_facing = facing
                new_ii = ii
                new_jj = jj
                if facing == '>':
                    new_jj = jj+1
                    if new_jj == 50:
                        new_face, new_ii,  new_jj, new_facing = switch_from_face(
                            face, ii, jj, facing, faces)
                    if new_face['map'][new_ii][new_jj] == '#':
                        break
                if facing == 'v':
                    new_ii = ii+1
                    if new_ii == 50:
                        new_face, new_ii,  new_jj, new_facing = switch_from_face(
                            face, ii, jj, facing, faces)
                    if new_face['map'][new_ii][new_jj] == '#':
                        break
                if facing == '<':
                    new_jj = jj-1
                    if new_jj == -1:
                        new_face, new_ii,  new_jj, new_facing = switch_from_face(
                            face, ii, jj, facing, faces)
                    if new_face['map'][new_ii][new_jj] == '#':
                        break
                if facing == '^':
                    new_ii = ii-1
                    if new_ii == -1:
                        new_face, new_ii,  new_jj, new_facing = switch_from_face(
                            face, ii, jj, facing, faces)
                    if new_face['map'][new_ii][new_jj] == '#':
                        break


                face, ii, jj, facing = new_face, new_ii, new_jj, new_facing
                face['map'][ii][jj] = facing

        else:
            facing = turn(facing, j)
            face['map'][ii][jj] = facing
        print_face(face)
        # time.sleep(2)

        # for row in M:
        #     print(''.join(row))
        # print('last rule', j)

    facing_score = {
        '>': 0,
        'v': 1,
        '<': 2,
        '^': 3
    }[facing]


    if face['name'] == 'right':
        ii += 1
        jj += 100 + 1
    elif face['name'] == 'front':
        ii += 50 + 1
        jj += 50 + 1
    elif face['name'] == 'left':
        ii += 100 + 1
        jj += 1
    elif face['name'] == 'bot':
        ii += 100 + 1
        jj += 50 + 1
    elif face['name'] == 'back':
        ii += 150 + 1
        jj += 1
    elif face['name'] == 'top':
        ii += 1
        jj += 50 + 1
    print(face['name'], ii, jj, facing)
    return 1000*ii + 4*jj+facing_score



def main():
    # print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_real():
    assert solve(import_data(False)) == 66292


# not 39158
# not 26008
# not 27012