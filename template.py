import re


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    pass


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
