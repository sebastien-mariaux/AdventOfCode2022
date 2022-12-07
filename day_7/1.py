
def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data

class Dir:
    def __init__(self, name):
        self.name = name
        self.subdirs = []
        self.files= []

    def add_subdir(self, subdir):
        self.subdirs.append(subdir)

    def add_file(self, file):
        self.files.append(file)

    def get_subdirs(self):
        return self.subdirs

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} : {self.size()} - subdirs: {self.subdirs}"

    def size(self):
        return sum([file.get_size() for file in self.files]) + sum([dir.size() for dir in self.subdirs])

class File:
    def __init__(self, size):
        self.size = size

    def get_size(self):
        return self.size

    def __str__(self):
        return self.size

    def __repr__(self):
        return self.size


def find_or_create_dir(objects, name):
    for dir in objects:
        if dir.get_name() == name:
            return dir
    new_dir = Dir(name)
    objects.append(new_dir)
    return new_dir

def solve(data):
    objects = []
    dirs = []
    current_dir = None
    for row in data.split("\n"):
        row = row.split(' ')
        if row[0] == '$':
            if row[1] == 'cd':
                if row[2] ==  '..':
                    dirs.pop()
                    current_dir = dirs[-1]
                elif row[2] == '/':
                    dirs.append(row[2])
                    current_dir = find_or_create_dir(objects, row[2])
                else:
                    dirs.append(row[2])
                    current_dir = find_or_create_dir(objects, row[2])
        else:
            if row[0] == 'dir':
                new_dir = find_or_create_dir(objects, row[1])
                current_dir.add_subdir(new_dir)
            else:
                new_file = File(int(row[0]))
                current_dir.add_file(new_file)

    result = 0
    for dir in objects:
        if (s:= dir.size()) < 100000:
            result += s
    print(result)

def main():
    solve(import_data(True))
    solve(import_data(False))


if __name__ == '__main__':
    main()


