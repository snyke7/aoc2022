from parsy import seq, string, decimal_digit, letter

from day12 import dijkstra


test_input = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''


valve_name = letter.times(2, 2).concat()
valve_names = seq(
    valve_name,
    (string(', ') >> valve_name).many()
).combine(lambda h, tl: [h] + tl)

conn_line = seq(
    string('Valve ') >> valve_name,
    string(' has flow rate=') >> decimal_digit.at_least(1).concat().map(int),
    string('; tunnel') >> (string('s lead to valves ') | string(' leads to valve ')) >> valve_names << string('\n')
).combine(lambda name, flow, conns: (name, (flow, conns)))

input_parser = conn_line.many().map(dict)


def pt1_base_case(valve_dict, action_valves, to_beat=0):
    return 0, ''


def max_estimator_pt1(valve_dict, action_valves, minutes):
    return sum((
        valve_dict[v][0] * (minutes - 2 - 2 * i)
        for i, v in enumerate(sorted(action_valves, key=lambda v: -valve_dict[v][0]))
        if i < (minutes - 2) // 2
        # visit all remaining valves, one by one, best ones first, supposing they are all next to eachother
    ))


def most_released_pressure(valve_dict, minutes, action_valves, cur_valve, to_beat=0,
                           base=pt1_base_case, estimator=max_estimator_pt1):
    # the best we are possibly able to do to beat to_beat, is open all remaining action_valves for the remaining
    # minutes
    if minutes <= 0:
        return base(valve_dict, action_valves, to_beat=to_beat)
    if estimator(valve_dict, action_valves, minutes) < to_beat:
        # then recursing is pointless
        return 0, ''
    most_pressure, best_valve = base(valve_dict, action_valves, to_beat=to_beat)
    if to_beat > most_pressure:
        most_pressure = to_beat
        best_valve = None
    dists = dijkstra({valve: conns for valve, (_, conns) in valve_dict.items()}, cur_valve)
    for i, v in enumerate(action_valves.copy()):  # copy since we are mutating action_valves below
        dist = dists[v]
        if dist < minutes:
            action_valves.remove(v)
            res, tail = most_released_pressure(
                valve_dict, minutes - dist - 1, action_valves, v,
                to_beat=max(to_beat - (minutes - dist - 1) * valve_dict[v][0], 0),
                base=base, estimator=estimator
            )
            that_pressure = (minutes - dist - 1) * valve_dict[v][0] + res
            if minutes == 26 and base != pt1_base_case:
                print(v, that_pressure, tail, base)
            action_valves.append(v)
            if that_pressure > most_pressure:
                most_pressure = that_pressure
                best_valve = v + '-' + str(tail)
            to_beat = max(to_beat, most_pressure)
    return most_pressure, best_valve


def pt2_base_case(valve_dict, action_valves, to_beat=0):
    res, tail = most_released_pressure(valve_dict, 26, action_valves, 'AA', to_beat=to_beat)
    return res, f' E: {tail}'


def max_estimator_pt2(valve_dict, action_valves, minutes):
    rev_av = list(sorted(action_valves, key=lambda v: -valve_dict[v][0]))
    # have elefant do the top priority ones until he is at same time as we
    partial = sum((
        # what Elefant will do
        valve_dict[v][0] * (26 - 2 - 2 * i)
        for i, v in enumerate(rev_av)
        if 2 + 2 * i <= 26 - minutes
    ))  # sums until 2 + 2 * i > 26 - minutes
    idx_lb = (24 - minutes) // 2 + 1
    if minutes % 2 == 1:
        minutes += 1
    if len(rev_av) >= idx_lb:
        # there are action_valves left to do together
        partial += sum((
            valve_dict[v][0] * (minutes - 2 - (2 * (i // 2)))
            for i, v in enumerate(rev_av[idx_lb:])
            if (minutes - (2 * (i // 2))) >= 0
        ))
    return partial


def calc_best(valve_dict):
    action_valves = [v for v, (flow, _) in valve_dict.items() if flow != 0]
    return most_released_pressure(valve_dict, 30, action_valves, 'AA')


def calc_best_pt2(valve_dict):
    action_valves = [v for v, (flow, _) in valve_dict.items() if flow != 0]
    return most_released_pressure(valve_dict, 26, action_valves, 'AA',
                                  base=pt2_base_case, estimator=max_estimator_pt2)


def main():
    with open('input/day16_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    parsed = input_parser.parse(the_input)
    # print(calc_best(parsed))
    print(calc_best_pt2(parsed))
    # print(max_estimator_pt2(parsed, ['BB', 'CC', 'DD', 'HH', 'EE'], 23))


if __name__ == '__main__':
    main()
