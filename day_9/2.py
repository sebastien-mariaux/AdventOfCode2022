
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def euclid_distance(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5


def solve(data):
    visited = set()
    positions = [(0, 0) for i in range(10)]
    visited.add(positions[-1])
    for row in data.split("\n"):
        print(row)
        direction, distance = row.split(" ")
        distance = int(distance)
        for i in range(distance):
            H = positions[0]
            if direction == 'R':
                H = (H[0]+1, H[1])
                positions[0] = H
                next_move = None
                for i in range(9):
                    H = positions[i]
                    T = positions[i+1]
                    if euclid_distance(H, T) >= 2:
                        if  T[0] != H[0] and T[1] != H[1]:
                            delta = 1 if H[1] > T[1] else -1
                            T_new = (T[0]+1, T[1]+delta)
                        else:
                            T_new = (H[0]-1, H[1])
                        positions[i+1] = T_new

            if direction == 'L':
                H = (H[0]-1, H[1])
                positions[0] = H
                next_move = None
                for i in range(9):
                    H = positions[i]
                    T = positions[i+1]
                    if euclid_distance(H, T) >= 2:
                        if  T[0] != H[0] and T[1] != H[1]:
                            delta = 1 if H[1] > T[1] else -1
                            T_new = (T[0]-1, T[1]+delta)
                        else:
                            T_new = (H[0]+1, H[1])
                        positions[i+1] = T_new
            if direction == 'U':
                H = (H[0], H[1]+1)
                positions[0] = H
                next_move = None
                for i in range(9):
                    H = positions[i]
                    T = positions[i+1]
                    if euclid_distance(H, T) >= 2:
                        if  T[0] != H[0] and T[1] != H[1]:
                            delta = 1 if H[1] > T[0] else -1
                            T_new = (T[0]+delta, T[1]+1)
                        else:
                            T_new = (H[0], H[1]-1)
                        positions[i+1] = T_new
            if direction == 'D':
                H = (H[0], H[1]-1)
                positions[0] = H
                next_move = None
                for i in range(9):
                    H = positions[i]
                    T = positions[i+1]
                    if euclid_distance(H, T) >= 2:
                        if  T[0] != H[0] and T[1] != H[1]:
                            delta = 1 if H[1] > T[0] else -1
                            T_new = (T[0]+delta, T[1]-1)
                        else:
                            T_new = (H[0], H[1]+1)
                        positions[i+1] = T_new
            visited.add(positions[-1])
            print(positions)
    print('result', len(visited))


def main():
    solve(import_data(True))
    # solve(import_data(False))


if __name__ == '__main__':
    main()
