
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def add_value(C,  values, X):
    if C in [20, 60, 100, 140, 180, 220]:
        values.append(C*X)
    return values


def solve(data):
    data = data.splitlines()
    X = 1
    values = []
    C = 1
    for ins in data:
        values = add_value(C, values, X)
        if ins == 'noop':
            C += 1
        else:
            C += 1
            values = add_value(C, values, X)
            X += int(ins.split(' ')[1])
            C += 1
    return sum(values)


def main():
    solve(import_data(True))
    solve(import_data(False))


def test_sample():
    assert solve(import_data(True)) == 13140


def test_data():
    assert solve(import_data(False)) == 13480


if __name__ == '__main__':
    main()
