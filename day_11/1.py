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
        self.inspect_count +=1

    def compute(self, old):
        new = eval(self.operation)
        return int(new / 3)

    def run_test(self, item):
        if item % self.test == 0:
            return self.if_true
        return self.if_false

    def add_item(self, item):
        self.items.append(item)

    def clear_items(self):
        self.items = []


def solve(data):
    monkeys = data.split('\n\n')
    M = []
    for monkey in monkeys:
        infos = iter(monkey.split('\n'))
        id = next(infos)[-2]
        items = next(infos).split(': ')[1].split(', ')
        ope =  next(infos).split('= ')[1]
        test = next(infos).split('by ')[1]
        if_true = next(infos)[-1]
        if_false = next(infos)[-1]
        M.append(Monkey(id, items, ope, test, if_true, if_false))

    for _ in range(20):
        print('round', _ + 1)
        for m in M:
            for item in m.items:
                m.inspect(item)
                item = m.compute(item)
                next_m = m.run_test(item)
                M[next_m].add_item(item)
            m.clear_items()
    print(reduce(lambda x, y: x*y, sorted([m.inspect_count for m in M])[-2:]))


def main():
    solve(import_data(True))
    solve(import_data(False))

if __name__ == '__main__':
    main()
