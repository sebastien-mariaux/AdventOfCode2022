from pprint import pprint
import re
import itertools


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def solve(data):
    bprints = data.splitlines()
    scores = []
    for bprint in bprints:
        ore = 0
        clay = 0
        obsidian = 0
        geode = 0
        ore_robots = 1
        clay_robots = 0
        obsidian_robots = 0
        geode_robots = 0
        expr = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
        m = re.search(expr, bprint)
        bp_id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = map(int, m.groups())

        clay_ore_ratio = (geode_obsidian * obsidian_clay) / (geode_ore + geode_obsidian*obsidian_ore)
        for m in range(24):
            # collect resources
            extra_ore = ore_robots
            extra_clay = clay_robots
            extra_obsidian = obsidian_robots
            extra_geode = geode_robots
            print('minute ', m+1)

            # build geode robot
            if ore >= geode_ore and obsidian >= geode_obsidian:
                ore -= geode_ore
                obsidian -= geode_obsidian
                geode_robots += 1
                print('geode robot built')
            # build obsidian robot
            if ore >= obsidian_ore and clay >= obsidian_clay:
                ore -= obsidian_ore
                clay -= obsidian_clay
                obsidian_robots += 1
                print('obsidian robot built')
            # build clay robot
            if ore >= clay_ore and clay / ore < clay_ore_ratio:
                ore -= clay_ore
                clay_robots += 1
                print('clay robot built')
            # build ore robot
            if ore >= ore_ore:
                ore -= ore_ore
                ore_robots += 1
                print('ore robot built')

            ore += extra_ore
            print('we have ore ', ore)
            clay += extra_clay
            print('we have clay ', clay)
            obsidian += extra_obsidian
            print('we have obsidian ', obsidian)
            geode += extra_geode
            print('we have geode ', geode)
        scores.append(geode)
    return scores


def main():
    print(solve(import_data(True)))
    # print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 0


def test_real():
    assert solve(import_data(False)) == 0
