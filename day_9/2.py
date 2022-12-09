def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def euclid_distance(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5


def head_position(H, direction):
    return {
        'R': (H[0]+1, H[1]),
        'L': (H[0]-1, H[1]),
        'U':  (H[0], H[1]+1),
        'D': (H[0], H[1]-1),
    }[direction]


def follow_head(H, T):
    if H[0] == T[0] and H[1] > T[1]:
        return (T[0], T[1]+1)
    if H[0] == T[0] and H[1] < T[1]:
        return (T[0], T[1]-1)
    if H[0] > T[0] and H[1] == T[1]:
        return (T[0]+1, T[1])
    if H[0] < T[0] and H[1] == T[1]:
        return (T[0]-1, T[1])

    if H[0] > T[0] and H[1] > T[1]:
        return (T[0]+1, T[1]+1)
    if H[0] < T[0] and H[1] < T[1]:
        return (T[0]-1, T[1]-1)
    if H[0] < T[0] and H[1] > T[1]:
        return (T[0]-1, T[1]+1)
    if H[0] > T[0] and H[1] < T[1]:
        return (T[0]+1, T[1]-1)


def solve(data):
    rope_len = 10
    visited = set()
    positions = [(0, 0) for i in range(rope_len)]
    visited.add(positions[-1])

    for row in data.split("\n"):
        direction, distance = row.split(" ")
        distance = int(distance)
        for i in range(distance):
            H = positions[0]
            H = head_position(H, direction)
            positions[0] = H
            for i in range(rope_len-1):
                H = positions[i]
                T = positions[i+1]
                if euclid_distance(H, T) >= 2:
                    T = follow_head(H, T)
                positions[i+1] = T
            visited.add(positions[-1])
    print('result', len(visited))
    return len(visited)


def main():
    solve(import_data(True))
    solve(import_data(False))


def test_solve_sample():
    data = import_data(sample=True)
    assert solve(data) == 36


def test_solve_real():
    data = import_data(sample=False)
    assert solve(data) == 2419


if __name__ == '__main__':
    main()
