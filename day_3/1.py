import re


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


ITEMS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
prios = {item: i+1 for i, item in enumerate(ITEMS)}


def split_2(text):
    half = len(text) // 2
    return text[:half], text[half:]


def solve(data):
    stacks = data.split("\n")
    sum = 0
    for stack in stacks:
        c1, c2 = split_2(stack)
        common = set(c1).intersection(set(c2))
        sum += prios[list(common)[0]]
    print(sum)


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
