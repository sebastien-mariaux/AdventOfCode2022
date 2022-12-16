import re
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def exclusion(S, md, inclusion_zone):
    E = set()
    targets = [(i,j) for i in range(S[0]-md, S[0]+md+1) for j in range(S[1]-md, S[1]+md+1) if (i,j) in inclusion_zone]
    for t in targets:
        if manhattan_distance(S, t) <= md :
            E.add(t)
    return E

def is_winner(S, el, maxi):
    if el[0] >= 0 and el[0] <= maxi and el[1] >= 0 and el[1] <= maxi:
        for s, md in S.items():
            if manhattan_distance(s, el) <= md:
                return False
        return True
    return False


def solve(data, maxi):
    regex = r"^Sensor at x=(-*\d*), y=(-*\d*): closest beacon is at x=(-*\d*), y=(-*\d*)"
    inclusion_zone = ( (x,y) for x in range(0, maxi+1) for y in range(0, maxi+1))
    S={}
    for ix, row in enumerate(data.splitlines()):
        print('row', ix)
        m = re.search(regex, row)
        s = (int(m.group(1)), int(m.group(2)))
        b = (int(m.group(3)), int(m.group(4)))
        md = manhattan_distance(s, b)
        S[s] = md

    for s, md in S.items():
        top = (s[0], s[1]-md-1)
        bottom = (s[0], s[1]+md+1)
        left = (s[0] - md - 1, s[1])
        right = (s[0] + md + 1, s[1])

        # top right side
        current = top
        while current != right:
            if is_winner(S, current, maxi):
                return current[0] * 4000000 + current[1]
            current = (current[0]+1, current[1]+1)
        # top left side
        current = top
        while current != left:
            if is_winner(S, current, maxi):
                return current[0] * 4000000 + current[1]
            current = (current[0]-1, current[1]+1)
        #bottom right side
        current=bottom
        while current != right:
            if is_winner(S, current, maxi):
                return current[0] * 4000000 + current[1]
            current = (current[0]+1, current[1]-1)
        #bottom left side
        current=bottom
        while current != left:
            if is_winner(S, current, maxi):
                return current[0] * 4000000 + current[1]
            current = (current[0]-1, current[1]-1)



# compute manhantan distance
def manhattan_distance(A, B):
    x1, y1 = A
    x2, y2 = B
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    print(solve(import_data(True), 20))
    print(solve(import_data(False), 4000000))

def test_sample():
    assert solve(import_data(True), 20) == 56000011

def test_real():
    assert solve(import_data(False), 4000000) == 10826395253551


if __name__ == '__main__':
    main()
