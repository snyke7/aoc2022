from typing import Tuple, List


Cost = Tuple[int, int, int]
Robots = List[int]

test_input = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''

Blueprint = Tuple[Cost, Cost, Cost, Cost]


def parse_blueprint(line: str) -> Blueprint:
    ore_cost_o, clay_cost_o, obs_cost_o, obs_cost_c, geo_cost_o, geo_cost_d = tuple(
        int(el) for el in line.split(' ')[1:]
        if el.isnumeric()
    )
    return (ore_cost_o, 0, 0), (clay_cost_o, 0, 0), (obs_cost_o, obs_cost_c, 0), (geo_cost_o, 0, geo_cost_d)


def increase_inv_with(inventory: Cost, robot_count: Robots) -> Cost:
    return tuple((i + r) for i, r in zip(inventory, robot_count))


def max_geodes(blueprint: Blueprint, minutes: int, inventory: Cost, robot_count: Robots) -> int:
    if minutes == 0:
        return 0
    # given any situation, the best one can do is produce a geode-cracker every minute
    # this would produce cur_geocrackers * minutes + minutes * (minutes - 1) // 2
    # but this assumes that one has enough resources, and geode-crackers are expensive

    # an additional heuristic: never produce a robot which is already producing more ore than we can consume
    result = 0
    am_poor = False
    for robot, robot_cost in enumerate(blueprint):
        reduced_inv: Cost = tuple((i - c for i, c in zip(inventory, robot_cost)))
        if all((i >= 0 for i in reduced_inv)) and (
            robot == len(blueprint) - 1 or
            robot_count[robot] + 1 <= max((cost[robot] for cost in blueprint))
        ):
            # we can construct one, and its ores are possibly useful
            reduced_inv = increase_inv_with(reduced_inv, robot_count)
            robot_count[robot] += 1
            that_result = max_geodes(blueprint, minutes - 1, reduced_inv, robot_count)
            if minutes >= 10:
                print(f'Built robot {robot} (total: {robot_count}, inv: {inventory}) with {minutes} minutes left: {that_result}')
            robot_count[robot] -= 1
            if that_result > result:
                result = that_result
        else:
            am_poor = True
    if am_poor:
        # base case: construct no robots. this is only a good option if there is a robot we cannot build
        wait_result = max_geodes(blueprint, minutes - 1, increase_inv_with(inventory, robot_count), robot_count) + robot_count[-1]  # geode-crackers
        if wait_result > result:
            result = wait_result
    return result


def estimate_v1(minutes: int, geocrackers: int, obs_miners: int, cur_obs: int, obs_cost: int) -> int:
    # so suppose ore is abundant, and we only need to deal with clay and obsidian
    # then the best thing would be: produce geode-cracker if enough obsidian is around
    # produce obsidian-robot if enough clay is around
    # suppose we have enough clay: then best thing would be to produce obsidian robot if we cannot build a geode cracker
    # estimation becomes:
    # cur_geocrackers * minutes + _
    # where _ is:
    result = geocrackers * minutes
    extra_geocrackers = 0
    for i in range(minutes):
        result += extra_geocrackers
        if cur_obs >= obs_cost:
            cur_obs -= obs_cost
            extra_geocrackers += 1
            cur_obs += obs_miners
        else:
            cur_obs += obs_miners
            obs_miners += 1
    return result


def estimate_v2(minutes: int,
                geocrackers: int, cur_obs: int, obs_cost: int,
                obs_miners: int, cur_clay: int, clay_cost: int,
                clay_miners: int) -> int:
    # so suppose ore is abundant, and we only need to deal with clay and obsidian
    # then the best thing would be: produce geode-cracker if enough obsidian is around
    # produce obsidian-robot if enough clay is around
    # otherwise produce clay-robot, this is fine since we have enough ore
    # suppose we have enough clay: then best thing would be to produce obsidian robot if we cannot build a geode cracker
    # estimation becomes:
    # cur_geocrackers * minutes + _
    # where _ is:
    result = geocrackers * minutes
    extra_geocrackers = 0
    for i in range(minutes):
        result += extra_geocrackers
        if cur_obs >= obs_cost:
            cur_obs += obs_miners
            cur_clay += clay_miners

            cur_obs -= obs_cost
            extra_geocrackers += 1
        elif cur_clay >= clay_cost:
            cur_obs += obs_miners
            cur_clay += clay_miners

            cur_clay -= clay_cost
            obs_miners += 1
        else:
            cur_obs += obs_miners
            cur_clay += clay_miners

            clay_miners += 1
    return result


def estimate_v3(minutes: int,
                geocrackers: int, cur_obs: int, obs_cost: int,
                obs_miners: int, cur_clay: int, clay_cost: int,
                clay_miners: int, cur_ore: int, ore_cost: int,
                ore_miners: int) -> int:
    # suppose geocrackers and obs_miners do not cost ore
    # then the best thing would be: produce geode-cracker if enough obsidian is around
    # otherwise produce obsidian-robot if enough clay is around
    # otherwise produce clay-robot if enough ore is around
    # otherwise produce ore-robot, these are free
    # estimation becomes:
    result = geocrackers * minutes
    extra_geocrackers = 0
    for i in range(minutes):
        result += extra_geocrackers
        if cur_obs >= obs_cost:
            cur_obs += obs_miners
            cur_clay += clay_miners
            cur_ore += ore_miners

            cur_obs -= obs_cost
            extra_geocrackers += 1
        elif cur_clay >= clay_cost:
            cur_obs += obs_miners
            cur_clay += clay_miners
            cur_ore += ore_miners

            cur_clay -= clay_cost
            obs_miners += 1
        elif cur_ore >= ore_cost:
            cur_obs += obs_miners
            cur_clay += clay_miners
            cur_ore += ore_miners

            cur_ore -= ore_cost
            clay_miners += 1
        else:
            cur_obs += obs_miners
            cur_clay += clay_miners
            cur_ore += ore_miners

            ore_miners += 1
    return result


def main():
    the_input = test_input
    blueprints = [parse_blueprint(line.strip()) for line in the_input.splitlines()]
    print(blueprints)
    # print(max_geodes(blueprints[0], 24, (0, 0, 0), [1, 0, 0, 0]))
    print(estimate_v1(11, 0, 0, 0, 7))
    print(estimate_v2(10, 0, 0, 7, 0, 33, 14, 6))
    print(estimate_v3(10, 0, 0, 7, 0, 32, 14, 6, 4, 2, 2))


if __name__ == '__main__':
    main()
