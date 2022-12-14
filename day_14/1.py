
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    P = data.splitlines()
    rocks = set()
    for p in P:
        boundaries = [(int(x), int(y)) for x, y in [b.split(',') for b in p.split(' -> ')]]
        for ix in range(len(boundaries) -1):
            start, end = boundaries[ix], boundaries[ix+1]
            # vertical path
            if start[0] == end[0]:
                top = start if start[1] < end[1] else end
                bottom = start if start[1] > end[1] else end
                for i in range(top[1], bottom[1] + 1):
                    rocks.add((start[0], i))
            # horizontal path
            else:
                left = start if start[0] < end[0] else end
                right = start if start[0] > end[0] else end
                for i in range(left[0], right[0] + 1):
                    rocks.add((i, start[1]))
    lower_rock = max([y for x, y in rocks])

    abyss = False
    sand_count = 0
    while not abyss:
        x, y  = (500,0)
        while True:
            if (x, y+1) not in rocks:
                y = y+1
            elif (x-1, y+1) not in rocks:
                x, y = x-1, y+1
            elif (x+1, y+1) not in rocks:
                x, y = x+1, y+1
            else:
                rocks.add((x, y))
                sand_count +=1
                break
            if y >=lower_rock:
                abyss =True
                break
    print(sand_count)

def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
