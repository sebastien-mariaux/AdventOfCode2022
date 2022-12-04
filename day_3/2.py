import re


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


ITEMS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
prios = {item: i+1 for i, item in enumerate(ITEMS)}


def solve(data):
    stacks = data.split("\n")
    sum = 0
    for i in range(0, len(stacks), 3):
        stack = stacks[i:i+3]
        common = [el for el in stack[0] if el in stack[1] and el in stack[2]]
        sum += prios[common[0]]
    print(sum)


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()

