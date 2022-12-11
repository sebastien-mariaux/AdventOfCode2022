from functools import reduce


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


class Monkey:
    def __init__(self,  id, items, operation, test, if_true, if_false):
        self.id = id
        self.items = [int(i) for i in items]
        self.operation = operation
        self.test = int(test)
        self.if_true = int(if_true)
        self.if_false = int(if_false)
        self.inspect_count = 0

    def __str__(self) -> str:
        return f'{self.id} | {self.items} | {self.operation} | {self.test} | {self.if_true} | {self.if_false}'

    def inspect(self, item):
        assert item in self.items
        self.inspect_count += 1

    def compute(self, old, mod):
        new = eval(self.operation)
        return new % mod

    def run_test(self, item):
        mod = item % self.test
        if mod == 0:
            return self.if_true
        return self.if_false

    def add_item(self, item):
        self.items.append(item)

    def clear_items(self):
        self.items = []


def solve(data):
    monkeys = data.split('\n\n')
    M = []
    # Initialisation: create the monkeys
    for monkey in monkeys:
        infos = iter(monkey.split('\n'))
        id = next(infos)[-2]
        items = next(infos).split(': ')[1].split(', ')
        ope = next(infos).split('= ')[1]
        test = next(infos).split('by ')[1]
        if_true = next(infos)[-1]
        if_false = next(infos)[-1]
        M.append(Monkey(id, items, ope, test, if_true, if_false))

    # get product of all divisers used in test
    mod = reduce(lambda x, y: x*y, [m.test for m in M])

    # Loop over rounds
    for _ in range(10000):
        print('round', _ + 1)
        for m in M:
            # for each monkey, play as described
            for item in m.items:
                m.inspect(item)
                item = m.compute(item, mod)
                next_m = m.run_test(item)
                M[next_m].add_item(item)
            m.clear_items()
    return (reduce(lambda x, y: x*y, sorted([m.inspect_count for m in M])[-2:]))


def test_sample():
    assert solve(import_data(True)) == 2713310158


def test_real():
    assert solve(import_data(False)) == 14081365540


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()
