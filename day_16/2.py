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


def two_partitions(S):
    for l in range(0, int(len(S)/2)+1):
        combis = set(itertools.combinations(S, l))
        for c in combis:
            yield (sorted(list(c)), sorted(list(S-set(c))))


def walk_the_graph(MAX_TIME, G, flowing, distances):
    state = {
        'current': 'AA',
        'opened': [],
        'elapsed': 0,
        'relieved': 0
    }
    relieved = 0
    states = deque([state])
    seen = [state]
    while states:
        parent = states.popleft()
        flow = sum([v['rate'] for k, v in G.items() if k in parent['opened']])
        if len(parent['opened']) == len(flowing):
            parent['relieved'] = parent['relieved'] + \
                (MAX_TIME-parent['elapsed'])*flow
            if parent['relieved'] > relieved:
                relieved = parent['relieved']
            continue
        if parent['elapsed'] >= MAX_TIME:
            continue
        for node in [n for n in flowing if n != parent['current'] and n not in parent['opened']]:
            d = distances[tuple(sorted([parent['current'], node]))]
            next_state = {
                'current': node,
                'opened': parent['opened'] + [node],
                'elapsed': parent['elapsed'] + d + 1,
                'relieved': parent['relieved'] + flow * (d+1)
            }
            if next_state['elapsed'] >= MAX_TIME:
                next_state['relieved'] -= (next_state['elapsed'] -
                                           MAX_TIME) * flow
                if next_state['relieved'] > relieved:
                    relieved = next_state['relieved']
                continue
            similar_states = [s for s in seen if s['current'] ==
                              next_state['current'] and s['elapsed'] == next_state['elapsed']]
            similar_states_relieved = [s['relieved'] for s in similar_states]
            if not similar_states or next_state['relieved'] > max(similar_states_relieved):
                states.append(next_state)
            seen.append(next_state)
    return relieved


def solve(data):
    MAX_TIME = 26
    # Création du graphe
    expr = r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels* leads* to valves* (.+)"
    G = {}
    for row in data.splitlines():
        m = re.search(expr, row)
        G[m.group(1)] = {'rate': int(m.group(2)),
                         'next': m.group(3).split(', ')}

    # calcul des distances entre les points intéressants
    flowing = [node for node in G.keys() if G[node]['rate'] > 0]
    distance_computed = []
    distances = {}
    for start in ['AA'] + flowing:
        distance_computed.append(start)
        for end in [x for x in flowing if x not in distance_computed]:
            distances[tuple(sorted([start, end]))] = distance(G, start, end)

    # Run algorithm after spliting flowing list in 2
    maxi = 0
    for elephant_job, elf_job in two_partitions(set(flowing)):
        print(maxi)
        elephant_result = walk_the_graph(MAX_TIME, G, elephant_job, distances)
        elf_result = walk_the_graph(MAX_TIME, G, elf_job, distances)
        if (tot := elephant_result + elf_result) > maxi:
            maxi = tot

    return maxi


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 1707


def test_real():
    assert solve(import_data(False)) == 1999
