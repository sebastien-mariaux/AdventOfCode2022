from pprint import pprint
import re
import itertools
from collections import deque
import time


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def dijkstra(G, start):
    nodes = G.keys()
    N = len(nodes)
    previous = {node: None for node in nodes}
    used = {node: False for node in nodes}
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0
    remaining = [(0, start)]
    while remaining:
        remaining.sort(reverse=True)
        dist_parent, parent = remaining.pop()
        if used[parent]:
            continue
        used[parent] = True
        for child in G[parent]['next']:
            dist_child = dist_parent + 1  # in this case, all ponderation = 1
            if dist_child < distances[child]:
                distances[child] = dist_child
                previous[child] = parent
                remaining.append((dist_child, child))
    return distances, previous


def distance(G, start, end):
    distances, previous = dijkstra(G, start)
    return distances[end]


def solve(data):
    # Création du graphe
    expr = r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels* leads* to valves* (.+)"
    G = {}
    for row in data.splitlines():
        m = re.search(expr, row)
        G[m.group(1)] = {'rate': int(m.group(2)),
                         'next': m.group(3).split(', ')}
    print(G)

    # calcul des distances entre les points intéressants
    flowing = [node for node in G.keys() if G[node]['rate'] > 0]
    distance_computed = []
    distances = {}
    for start in ['AA'] + flowing:
        distance_computed.append(start)
        for end in [x for x in flowing if x not in distance_computed]:
            distances[tuple(sorted([start, end]))] = distance(G, start, end)
    print(distances)

    state = {
        'current': 'AA',
        'opened': [],
        'elapsed': 0,
        'relieved': 0
    }

    finished = []
    states = [state]
    seen = [state]
    while states:
        parent = states.pop()
        flow = sum([v['rate'] for k, v in G.items() if k in parent['opened']])
        if len(parent['opened']) == len(flowing):
            parent['relieved'] = parent['relieved'] + (30-parent['elapsed'])*flow
            finished.append(parent)
            continue
        if parent['elapsed'] >= 30:
            continue
        for node in [n for n in flowing if n != parent['current'] and n not in parent['opened']]:
            d = distances[tuple(sorted([parent['current'], node]))]
            next_state = {
                'current': node,
                'opened': parent['opened'] + [node],
                'elapsed': parent['elapsed'] + d + 1,
                'relieved': parent['relieved'] + flow * (d+1)
            }
            if  next_state not in seen:
                states.append(next_state)
            seen.append(next_state)
    return max([el['relieved']  for el in finished])


def main():
    print(solve(import_data(True)))
    # print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 1651


def test_real():
    assert solve(import_data(False)) == 0
