from pprint  import pprint

def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


VALUES = {v: k for k, v in enumerate('abcdefghijklmnopqrstuvwxyz')}
VALUES['E'] = VALUES['z']
VALUES['S'] = VALUES['a']


def get_value(letter):
    return letter, VALUES[letter]


def adjacents(point, data, nb_col, nb_row):
    x, y, _, value = point
    return [(i, j, data[i][j], VALUES[data[i][j]])
            for (i,j) in [(x-1, y), (x+1, y), (x, y-1), (x,  y+1)]
            if  i >= 0 and j >=  0 and i < nb_row and j < nb_col
            and VALUES[data[i][j]] <= value + 1
            ]

def solve(data):
    data = [list(el) for el in data.split('\n')]
    nb_col = len(data[0])
    nb_row = len(data)
    count = 0
    S = [(i, j, 'S', 0) for j in range(nb_col)
         for i in range(nb_row) if data[i][j] == 'S'][0]
    found = False
    routes = [[S]]
    visited = [S]
    while not found:
        count += 1
        print(count)
        new_routes = []
        for route in routes:
            for adj in adjacents(route[-1], data, nb_col, nb_row):
                if adj[2] == 'E':
                    found = True
                    break
                if adj not in visited:
                    visited.append(adj)
                    new_route = route
                    new_routes.append(new_route + [adj])
        routes = new_routes
    print(count)


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
