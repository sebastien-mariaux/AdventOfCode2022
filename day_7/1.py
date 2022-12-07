from collections import defaultdict


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def set_nested_keys(dirs, keys, value):
    for key in keys + [value]:
        dirs = dirs.setdefault(key, {})


def set_file(dirs, keys, value):
    for key in keys:
        dirs = dirs.setdefault(key, {})
        # dirs.setdefault('files', []).append(int(value))
        dirs.setdefault('size', 0)
        # dirs['size'] = sum(dirs['files'])
        dirs['size'] += int(value)


def get_size(dirs, acc):
    dirs.setdefault('size', 0)
    for k, v in dirs.items():
        if isinstance(v, dict):
            if v['size'] < 100000:
                acc.append(v['size'])
            get_size(v, acc)
    return acc


def solve(data):
    dirs = defaultdict(list)
    nav = []
    for row in data.splitlines():
        row = row.split(' ')
        if row[0] == '$':
            if row[1] == 'cd':
                if row[2] == '/':
                    nav = ['/']
                elif row[2] == '..':
                    nav.pop()
                else:
                    nav.append(row[2])
        else:
            if row[0] == 'dir':
                pass
                set_nested_keys(dirs, nav, row[1])
            else:
                set_file(dirs, nav, row[0])

    print(sum(get_size(dirs, [])))


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
