
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    data = [[int(e) for e in list(row)] for row in data.split("\n")]
    max_score = 0
    row_count = len(data)
    col_count = len(data[0])
    for y in range(row_count):
        for x in range(col_count):
            tree = data[y][x]
            # Visible right trees
            right_count = 0
            for i in range(x + 1, col_count):
                right_count += 1
                if data[y][i] >= tree:
                    break
            # visible left trees
            left_count = 0
            for i in range(x - 1, -1, -1):
                left_count += 1
                if data[y][i] >= tree:
                    break

            # visible top trees
            top_count = 0
            for i in range(y - 1, -1, -1):
                top_count += 1
                if data[i][x] >= tree:
                    break
            # visible botoom trees
            bottom_count = 0
            for i in range(y + 1, row_count):
                bottom_count += 1
                if data[i][x] >= tree:
                    break

            max_score = max(max_score, left_count *
                            right_count * top_count * bottom_count)

    print(max_score)


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
