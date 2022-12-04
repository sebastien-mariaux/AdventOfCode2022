def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    sum = 0
    for pair in data.split('\n'):
        first, second = pair.split(',')
        first = [int(el) for el in first.split('-')]
        second = [int(el) for el in second.split('-')]
        first = range(first[0], first[-1] + 1)
        second = range(second[0], second[-1] + 1)
        if issubset(first, second):
            sum += 1
    print(sum)


def main():
    solve(import_data(True))
    solve(import_data(False))


def issubset(range1, range2):
    return range1.start in range2 and range1[-1] in range2 or range2.start in range1 and range2[-1] in range1


if __name__ == '__main__':
    main()
