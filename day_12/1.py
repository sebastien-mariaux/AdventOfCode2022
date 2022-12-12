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

# def get_counts(point, counts, data, current_count, nb_col, nb_row, visited):
#     visited.append(point)
#     for adj in [a for a in adjacents(point, data, nb_col, nb_row) if a not in visited]:
#         next_count = current_count
#         next_visited = visited
#         if adj[2] == 'E':
#             # print(adj)
#             next_count += 1
#             counts.append(next_count)
#         else:
#             next_count += 1
#             next_count += get_counts(adj, counts, data, next_count, nb_col, nb_row, next_visited)[1]
#         return counts, next_count


def solve(data):
    data = [list(el) for el in data.split('\n')]
    nb_col = len(data[0])
    nb_row = len(data)
    count = 0
    S = [(i, j, 'S', 0) for j in range(nb_col)
         for i in range(nb_row) if data[i][j] == 'S'][0]
    found = False
    routes = [[S]]
    while not found:
        count += 1
        print(count)
        new_routes = []
        for route in routes:
            for adj in adjacents(route[-1], data, nb_col, nb_row):
                if adj[2] == 'E':
                    found = True
                    break
                if adj not in route:
                    new_route  = route
                    new_routes.append(new_route + [adj])
        routes = new_routes
    print(count)


def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
