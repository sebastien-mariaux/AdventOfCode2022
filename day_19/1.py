from pprint import pprint
import re
import itertools
from collections import deque, defaultdict
import time
from multiprocessing import Pool


def import_data(sample=False):
    dataset = 'sample_data.txt' if sample else 'data.txt'
    f = open(dataset, "r")
    data = f.read()
    return data


def run_blueprint(bprint):
    geodes_at_time = defaultdict(lambda: 0)
    best = 0
    states = deque([{
        'ore': 0,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
        'ore_robots': 1,
        'clay_robots': 0,
        'obsidian_robots': 0,
        'geode_robots': 0,
        'time': 0
    }])
    expr = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    m = re.search(expr, bprint)
    bp_id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = map(
        int, m.groups())
    print('==== Running blueprint', bp_id, '====')
    # clay_ore_ratio = (geode_obsidian * obsidian_clay) / (geode_ore + geode_obsidian*obsidian_ore)
    seen = []
    max_ore_robots = max(clay_ore, obsidian_ore, ore_ore)
    max_clay_robots = obsidian_clay
    max_obsidian_robots = geode_obsidian

    while states:
        state = states.pop()
        # # Check if exists a state with more geode at this time
        # if geodes_at_time[state['time']] > state['geode']:
        #     continue
        # geodes_at_time[state['time']] = state['geode']

        if state['time'] == 24:
            if state['geode'] > best:
                best = state['geode']
                # print('best', best)
            continue

        # Check if we have a better state at this time already
        better_seen_at_time = next((
            s for s in seen
            if s['time'] == state['time']
            and s['ore'] >= state['ore']
            and s['clay'] >= state['clay']
            and s['obsidian'] >= state['obsidian']
            and s['geode'] >= state['geode']
            and s['ore_robots'] >= state['ore_robots']
            and s['clay_robots'] >= state['clay_robots']
            and s['obsidian_robots'] >= state['obsidian_robots']
            and s['geode_robots'] >= state['geode_robots']
        ), None)
        if better_seen_at_time:
            continue
        if state not in seen:
            seen.append(state)

        time_left = 24 - state['time']
        max_potential_geodes = state['geode'] + state['geode_robots']*time_left + sum([i for i in range(time_left)])
        if max_potential_geodes <= best:
            continue
        can_build_geode_robot = (
            state['ore'] >= geode_ore and state['obsidian'] >= geode_obsidian and state['time'] < 23 )
        can_build_obsidian_robot = (
            state['ore'] >= obsidian_ore
            and state['clay'] >= obsidian_clay
            and state['obsidian_robots'] <= max_obsidian_robots and state['time'] < 22)
        can_build_clay_robot = (
            state['ore'] >= clay_ore and state['clay_robots'] <= max_clay_robots  and state['time'] < 21)
        can_build_ore_robot = (
            state['ore'] >= ore_ore and state['ore_robots'] <= max_ore_robots and state['time'] < 22)

        if can_build_geode_robot:
            states.append({
                'ore': state['ore'] + state['ore_robots'] - geode_ore,
                'clay': state['clay'] + state['clay_robots'],
                'obsidian': state['obsidian'] + state['obsidian_robots'] - geode_obsidian,
                'geode': state['geode'] + state['geode_robots'],
                'ore_robots': state['ore_robots'],
                'clay_robots': state['clay_robots'],
                'obsidian_robots': state['obsidian_robots'],
                'geode_robots': state['geode_robots'] + 1,
                'time': state['time'] + 1
            })
            continue
        # build no robot
        states.append({
            'ore': state['ore'] + state['ore_robots'],
            'clay': state['clay'] + state['clay_robots'],
            'obsidian': state['obsidian'] + state['obsidian_robots'],
            'geode': state['geode'] + state['geode_robots'],
            'ore_robots': state['ore_robots'],
            'clay_robots': state['clay_robots'],
            'obsidian_robots': state['obsidian_robots'],
            'geode_robots': state['geode_robots'],
            'time': state['time'] + 1
        })
        if can_build_ore_robot:
            states.append({
                'ore': state['ore'] + state['ore_robots'] - ore_ore,
                'clay': state['clay'] + state['clay_robots'],
                'obsidian': state['obsidian'] + state['obsidian_robots'],
                'geode': state['geode'] + state['geode_robots'],
                'ore_robots': state['ore_robots'] + 1,
                'clay_robots': state['clay_robots'],
                'obsidian_robots': state['obsidian_robots'],
                'geode_robots': state['geode_robots'],
                'time': state['time'] + 1
            })
        if can_build_clay_robot:
            states.append({
                'ore': state['ore'] + state['ore_robots'] - clay_ore,
                'clay': state['clay'] + state['clay_robots'],
                'obsidian': state['obsidian'] + state['obsidian_robots'],
                'geode': state['geode'] + state['geode_robots'],
                'ore_robots': state['ore_robots'],
                'clay_robots': state['clay_robots'] + 1,
                'obsidian_robots': state['obsidian_robots'],
                'geode_robots': state['geode_robots'],
                'time': state['time'] + 1
            })
        if can_build_obsidian_robot:
            states.append({
                'ore': state['ore'] + state['ore_robots'] - obsidian_ore,
                'clay': state['clay'] + state['clay_robots'] - obsidian_clay,
                'obsidian': state['obsidian'] + state['obsidian_robots'],
                'geode': state['geode'] + state['geode_robots'],
                'ore_robots': state['ore_robots'],
                'clay_robots': state['clay_robots'],
                'obsidian_robots': state['obsidian_robots']+1,
                'geode_robots': state['geode_robots'],
                'time': state['time'] + 1
            })

    print('==== Completed blueprint', bp_id, '====')

    return bp_id * best


def solve(data):
    bprints = data.splitlines()
    quality_level = 0
    with Pool() as p:
        quality_level = sum(p.map(run_blueprint, bprints))
    # quality_level= run_blueprint(bprints[0])
    return quality_level


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 33


def test_real():
    assert solve(import_data(False)) == 0

# not 2275
