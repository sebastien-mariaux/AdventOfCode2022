
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def euclid_distance(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5


def solve(data):
    visited = set()
    H = (0, 0)
    T = (0, 0)
    visited.add(T)
    for row in data.split("\n"):
        direction, distance = row.split(" ")
        distance = int(distance)
        for i in range(distance):
            if direction == 'R':
                H = (H[0]+1, H[1])
                if euclid_distance(H, T) >= 2:
                    T = (H[0]-1, H[1])
            if direction == 'L':
                H = (H[0]-1, H[1])
                if euclid_distance(H, T) >= 2:
                    T = (H[0]+1, H[1])
            if direction == 'U':
                H = (H[0], H[1]+1)
                if euclid_distance(H, T) >= 2:
                    T = (H[0], H[1]-1)
            if direction == 'D':
                H = (H[0], H[1]-1)
                if euclid_distance(H, T) >= 2:
                    T = (H[0], H[1]+1)
            visited.add(T)
    print('result', len(visited))


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
