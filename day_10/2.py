from pprint import pprint


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def start_next_cycle(i, j, C):
    C += 1
    if C in [41, 81, 121, 161, 201, 241]:
        j = 0
        i += 1
    else:
        j += 1
    return i, j, C


class CRT:
    def __init__(self):
        self.screen = [['.' for i in range(40)] for j in range(6)]

    def draw(self, i, j, X):
        if j in self.get_sprite(X):
            self.screen[i][j] = '#'
        else:
            self.screen[i][j] = '.'

    def get_sprite(self, X):
        return [X - 1, X, X + 1]

    def show(self):
        print('\n'.join([''.join(row) for row in self.screen]))
        print('\n')


def solve(data):
    crt = CRT()
    i = 0
    j = 0
    data = data.splitlines()
    X = 1
    C = 1
    for ins in data:
        if ins == 'noop':
            crt.draw(i, j, X)
            i, j, C = start_next_cycle(i, j, C)
        else:
            crt.draw(i, j, X)
            i, j, C = start_next_cycle(i, j, C)
            crt.draw(i, j, X)
            X += int(ins.split(' ')[1])
            i, j, C = start_next_cycle(i, j, C)

    crt.show()


def main():
    solve(import_data(True))
    solve(import_data(False))



if __name__ == '__main__':
    main()
