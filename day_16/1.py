import re
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

class Node:
    def __init__(self, id, node_type, parent, time):
        self.id = id
        self.time = time
        self.node_type = node_type
        self.children = []
        self.parent = parent
        if self.parent:
            parent.children.append(self)

    def __repr__(self) -> str:
        return self.id

def get_pressures(node, V, time, pressures, pressure):
    time += 1
    if time == 5 :
         pressures.append(pressure)
         return pressures

    for t in V[node]['next']:
        pressures += get_pressures(node, V, time, pressures, pressure)
    if V[node]['rate'] > 0:
        # open
        time += 1
        pressure += (30 - time) * V[node]['rate']
        pressures += get_pressures(node, V, time, pressures, pressure )
    return pressures

# def get_tree(node, V, time):
#     print(time)
#     time += 1
#     if time >= 3:
#         return

#     for t in V[node.id]['next']:
#         n = Node(id=t, node_type='valve', parent=node, time=time)
#         get_tree(n, V, time)
#     if V[node.id]['rate'] > 0:
#         op = Node('O', node_type='open', parent=node, time=time)
#         time += 1
#         for t in V[node.id]['next']:
#             n = Node(id=t, node_type='valve', parent=op, time=time)
#             get_tree(n, V, time)


def solve(data):
    expr = r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels* leads* to valves* (.+)"
    V = {}
    O = set()
    for row in data.splitlines():
        m = re.search(expr, row)
        V[m.group(1)] = {'rate': int(m.group(2)), 'next': m.group(3).split(', ')}
    pressure = 0
    T = 1
    # node = Node(id='AA', node_type='valve', parent=None, time=0)
    pressures = get_pressures('AA', V, 0, [], 0)
    print(max(pressures))




        # print('current', current)
        # print([v for v in V[current]['next'] if v not in O])
        # #get new current
        # tunnels = V[current]['next']
        # if not_visited :=[v for v in V[current]['next'] if v not in O]:
        #     current = sorted([v for v in V[current]['next'] if v not in O], key=lambda x: V[x]['rate'])[-1]
        # else:
        #     current = V[current]['next'][0]
        # T+=1
        # O.add(current)
        # pressure += (30 - T) * V[current]['rate']
        # T+= 1




def main():
    solve(import_data(True))
    # solve(import_data(False))


if __name__ == '__main__':
    main()



def test_sample():
    assert solve(import_data(False)) == 1651