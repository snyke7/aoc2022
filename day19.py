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


def max_geodes(blueprint: Blueprint, minutes: int, inventory: Cost, robot_count: Robots, at_least=0) -> int:
    if minutes == 0:
        return 0
    # given any situation, the best one can do is produce a geode-cracker every minute
    # this would produce cur_geocrackers * minutes + minutes * (minutes - 1) // 2
    # but this assumes that one has enough resources, and geode-crackers are expensive

    if not (estimate_v3_conv(minutes, robot_count, inventory, blueprint) > at_least):
        return at_least

    # an additional heuristic: never produce a robot which is already producing more ore than we can consume
    result = 0
    to_poor_for = []
    for robot, robot_cost in reversed(list(enumerate(blueprint))):
        reduced_inv: Cost = tuple((i - c for i, c in zip(inventory, robot_cost)))
        if all((i >= 0 for i in reduced_inv)) and (
                robot == len(blueprint) - 1 or
                robot_count[robot] + 1 <= max((cost[robot] for cost in blueprint[robot:]))
        ):
            # we can construct one, and its ores are possibly useful
            reduced_inv = increase_inv_with(reduced_inv, robot_count)
            additional_geodes = robot_count[-1]
            robot_count[robot] += 1
            that_result = max_geodes(blueprint, minutes - 1, reduced_inv, robot_count, at_least - additional_geodes) + additional_geodes
            # if minutes >= 12 or True:
            #     print(
            #         f'Built robot {robot} (total: {robot_count}, inv: {inventory}) with {minutes} minutes left: {that_result}')
            robot_count[robot] -= 1
            if that_result > result:
                result = that_result
            if result > at_least:
                at_least = result
        else:
            to_poor_for.append(robot)
    if to_poor_for:
        # base case: construct no robots. this is only a good option if there is a robot we cannot build
        wait_result = max_geodes(blueprint, minutes - 1, increase_inv_with(inventory, robot_count), robot_count, at_least - robot_count[-1]) + \
                      robot_count[-1]  # geode-crackers
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


def estimate_v3_conv(minutes: int,
                     robot_count: Robots,
                     inventory: Cost,
                     blueprint: Blueprint) -> int:
    ore_miners, clay_miners, obs_miners, geocrackers = robot_count
    cur_ore, cur_clay, cur_obs = inventory
    obs_cost = blueprint[3][2]
    clay_cost = blueprint[2][1]
    ore_cost = blueprint[1][0]
    return estimate_v3(minutes, geocrackers, cur_obs, obs_cost, obs_miners, cur_clay, clay_cost, clay_miners, cur_ore, ore_cost, ore_miners)


def max_geodes_init(blueprint):
    return max_geodes(blueprint, 24, (0, 0, 0), [1, 0, 0, 0])


def total_quality(blueprints: List[Blueprint]):
    return sum(((i + 1) * max_geodes_init(blueprint) for i, blueprint in enumerate(blueprints)))


def max_geodes_init_pt2(blueprint):
    return max_geodes(blueprint, 32, (0, 0, 0), [1, 0, 0, 0])


def prod_of_first_three(blueprints):
    result = 1
    for blueprint in blueprints[:3]:
        result *= max_geodes_init_pt2(blueprint)
    return result


def main():
    with open('input/day19_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    blueprints = [parse_blueprint(line.strip()) for line in the_input.splitlines()]
    print(total_quality(blueprints))
    print(prod_of_first_three(blueprints))
    # print(estimate_v1(11, 0, 0, 0, 7))
    # print(estimate_v2(10, 0, 0, 7, 0, 33, 14, 6))
    # print(estimate_v3(10, 0, 0, 7, 0, 32, 14, 6, 4, 2, 2))


if __name__ == '__main__':
    main()
