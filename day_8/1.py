
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    data = [[int(e) for e in list(row)] for row in data.split("\n")]
    count = 0
    row_count = len(data)
    col_count = len(data[0])
    for y in range(row_count):
        for x in range(col_count):
            tree = data[y][x]
            left_trees = [data[y][i] for i in range(x)]
            if tree > max(left_trees, default=-1):
                count += 1
                continue
            right_trees = [data[y][i] for i in range(x + 1, col_count)]
            if tree > max(right_trees, default=-1):
                count += 1
                continue
            top_trees = [data[i][x] for i in range(y)]
            if tree > max(top_trees, default=-1):
                count += 1
                continue
            bottom_trees = [data[i][x] for i in range(y + 1, row_count)]
            if tree > max(bottom_trees, default=-1):
                count += 1
                continue
    print(count)


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
