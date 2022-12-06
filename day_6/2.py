
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    for i in range(len(data)):
        chain = data[i:i+14]
        if len(set(chain)) == len(chain):
            print(i+14)
            break

def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()
