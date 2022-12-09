
import pytest


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def euclid_distance(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5


def follow_head(H, direction):
    return {
        'R': (H[0]-1, H[1]),
        'L': (H[0]+1, H[1]),
        'U': (H[0], H[1]-1),
        'D': (H[0], H[1]+1),
    }[direction]


def head_position(H, direction):
    return {
        'R': (H[0]+1, H[1]),
        'L': (H[0]-1, H[1]),
        'U':  (H[0], H[1]+1),
        'D': (H[0], H[1]-1),
    }[direction]

def follow_diag(H, T, direction):
    if direction == 'R':
        if H[1] > T[1]:
            return (T[0]+1, T[1]+1)
        else:
            return (T[0]+1, T[1]-1)
    if direction == 'L':
        if H[1] > T[1]:
            return (T[0]-1, T[1]+1)
        else:
            return (T[0]-1, T[1]-1)
    if direction == 'U':
        if H[0] > T[0]:
            return (T[0]+1, T[1]+1)
        else:
            return (T[0]-1, T[1]+1)
    if direction == 'D':
        if H[0] > T[0]:
            return (T[0]+1, T[1]-1)
        else:
            return (T[0]-1, T[1]-1)

def solve(data):
    visited = set()
    H = (0, 0)
    T = (0, 0)
    visited.add(T)
    for row in data.split("\n"):
        direction, distance = row.split(" ")
        distance = int(distance)
        for i in range(distance):
            H = head_position(H, direction)
            if euclid_distance(H, T) < 2:
                continue
            elif euclid_distance(H, T) == 2:
                T = follow_head(H, direction)
            else:
                T = follow_diag(H, T, direction)
            visited.add(T)
    print('result', len(visited))
    return len(visited)


def main():
    solve(import_data(True))
    solve(import_data(False))


def test_solve_sample():
    data = import_data(sample=True)
    assert solve(data) == 88


def test_solve_real():
    data = import_data(sample=False)
    assert solve(data) == 6011


if __name__ == '__main__':
    main()
