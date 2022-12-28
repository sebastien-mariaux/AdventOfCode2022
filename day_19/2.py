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
    best = 0
    max_time = 32
    states = deque([{
        'ore': 0,
        'clay': 0,
        'obsidian': 0,
        'geode': 0,
        'ore_robots': 1,
        'clay_robots': 0,
        'obsidian_robots': 0,
        'geode_robots': 0,
        'time': 0,
        'skip_ore': False,
        'skip_clay': False,
        'skip_obsidian': False,
    }])
    expr = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    m = re.search(expr, bprint)
    bp_id, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = map(
        int, m.groups())
    print('==== Running blueprint', bp_id, '====')
    seen = []
    max_ore_robots = max(clay_ore, obsidian_ore, ore_ore)
    max_clay_robots = obsidian_clay
    max_obsidian_robots = geode_obsidian

    while states:
        state = states.pop()
        if state['time'] == max_time:
            if state['geode'] > best:
                best = state['geode']
                print(f"best for {bp_id} :", best)
                # print('best', best)
            # branches_completed += 1
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

        # if state in seen:
        #     continue
        # seen.append(state)

        time_left = max_time - state['time']
        max_potential_geodes = state['geode'] + state['geode_robots'] * \
            time_left + sum([i for i in range(time_left)])
        if max_potential_geodes <= best:
            continue

        can_build_geode_robot = (
            state['ore'] >= geode_ore and state['obsidian'] >= geode_obsidian and state['time'] < max_time-1)
        can_build_obsidian_robot = (
            state['ore'] >= obsidian_ore
            and state['clay'] >= obsidian_clay
            and state['obsidian_robots'] <= max_obsidian_robots
            and not state['skip_obsidian']
            and state['time'] < max_time-2)
        can_build_clay_robot = (
            state['ore'] >= clay_ore and state['clay_robots'] <= max_clay_robots
            and not state['skip_clay'] and state['time'] < max_time-3)
        can_build_ore_robot = (
            state['ore'] >= ore_ore and state['ore_robots'] <= max_ore_robots
            and not state['skip_ore'] and state['time'] < max_time-2)

        geode_state ={
            'ore': state['ore'] + state['ore_robots'] - geode_ore,
            'clay': state['clay'] + state['clay_robots'],
            'obsidian': state['obsidian'] + state['obsidian_robots'] - geode_obsidian,
            'geode': state['geode'] + state['geode_robots'],
            'ore_robots': state['ore_robots'],
            'clay_robots': state['clay_robots'],
            'obsidian_robots': state['obsidian_robots'],
            'geode_robots': state['geode_robots'] + 1,
            'time': state['time'] + 1,
            'skip_ore': False,
            'skip_clay': False,
            'skip_obsidian': False,
        }

        # build no robot
        no_state ={
            'ore': state['ore'] + state['ore_robots'],
            'clay': state['clay'] + state['clay_robots'],
            'obsidian': state['obsidian'] + state['obsidian_robots'],
            'geode': state['geode'] + state['geode_robots'],
            'ore_robots': state['ore_robots'],
            'clay_robots': state['clay_robots'],
            'obsidian_robots': state['obsidian_robots'],
            'geode_robots': state['geode_robots'],
            'time': state['time'] + 1,
            'skip_ore': can_build_ore_robot,
            'skip_clay': can_build_clay_robot,
            'skip_obsidian': can_build_obsidian_robot,
        }
        clay_state ={
            'ore': state['ore'] + state['ore_robots'] - clay_ore,
            'clay': state['clay'] + state['clay_robots'],
            'obsidian': state['obsidian'] + state['obsidian_robots'],
            'geode': state['geode'] + state['geode_robots'],
            'ore_robots': state['ore_robots'],
            'clay_robots': state['clay_robots'] + 1,
            'obsidian_robots': state['obsidian_robots'],
            'geode_robots': state['geode_robots'],
            'time': state['time'] + 1,
            'skip_ore': False,
            'skip_clay': False,
            'skip_obsidian': False,
        }
        ore_state ={
            'ore': state['ore'] + state['ore_robots'] - ore_ore,
            'clay': state['clay'] + state['clay_robots'],
            'obsidian': state['obsidian'] + state['obsidian_robots'],
            'geode': state['geode'] + state['geode_robots'],
            'ore_robots': state['ore_robots'] + 1,
            'clay_robots': state['clay_robots'],
            'obsidian_robots': state['obsidian_robots'],
            'geode_robots': state['geode_robots'],
            'time': state['time'] + 1,
            'skip_ore': False,
            'skip_clay': False,
            'skip_obsidian': False,
        }
        obsidian_state ={
            'ore': state['ore'] + state['ore_robots'] - obsidian_ore,
            'clay': state['clay'] + state['clay_robots'] - obsidian_clay,
            'obsidian': state['obsidian'] + state['obsidian_robots'],
            'geode': state['geode'] + state['geode_robots'],
            'ore_robots': state['ore_robots'],
            'clay_robots': state['clay_robots'],
            'obsidian_robots': state['obsidian_robots']+1,
            'geode_robots': state['geode_robots'],
            'time': state['time'] + 1,
            'skip_ore': False,
            'skip_clay': False,
            'skip_obsidian': False,
        }

        # Maybe order matters?
        if can_build_geode_robot:
            states.append(geode_state)
            # assume building a geode robot  is always the best option
            continue
        states.append(no_state)
        if can_build_obsidian_robot:
            states.append(obsidian_state)
        if ore_ore >= clay_ore:
            if can_build_ore_robot:
                states.append(ore_state)
            if can_build_clay_robot:
                states.append(clay_state)
        else:
            if can_build_clay_robot:
                states.append(clay_state)
            if can_build_ore_robot:
                states.append(ore_state)

    print('==== Completed blueprint', bp_id, '====')
    return bp_id * best


def solve(data):
    bprints = data.splitlines()[:3]
    quality_level = 0
    with Pool(8) as p:
        quality_level = sum(p.map(run_blueprint, bprints))
    # quality_level= run_blueprint(bprints[0])
    return quality_level


def main():
    print(solve(import_data(True)))
    print(solve(import_data(False)))


if __name__ == '__main__':
    main()


def test_sample():
    assert solve(import_data(True)) == 180


def test_real():
    assert solve(import_data(False)) == 0

