import re
from collections import defaultdict


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    stack, moves = data.split("\n\n")
    mapping = {v: i+1 for (i, v) in enumerate(range(2, 50, 4))}
    initial = defaultdict(list)
    for row in stack.split("\n")[:-1]:
        for (pos, char) in enumerate(row):
            pos += 1
            if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                initial[mapping[pos]].insert(0, char)

    regex = r"move ([\d]*) from ([\d]*) to ([\d]*)"
    for row in moves.split("\n"):
        r = re.search(regex, row)
        n = int(r.group(1))
        f = int(r.group(2))
        t = int(r.group(3))

        s = initial[f][-n:]
        initial[f] = initial[f][:-n]
        initial[t] = initial[t] + s

    print(''.join([initial[key][-1] for key in sorted(initial.keys())]))


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
