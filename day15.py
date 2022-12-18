from typing import Tuple, List, Set

from parsy import string, decimal_digit, seq
from attrs import define, Factory


Coord = Tuple[int, int]

number = seq(
    string('-').at_most(1).map(
        lambda s: -1 if s else 1
    ),
    decimal_digit.at_least(1).concat().map(int)
).combine(lambda s, n: s * n)

coord = seq(
    string('x=') >> number,
    string(', y=') >> number
).map(tuple)

sensor_line = seq(
    string('Sensor at ') >> coord,
    string(': closest beacon is at ') >> coord << string('\n')
).map(tuple)

sensor_parse = sensor_line.many()


def get_exclusion_in(sensor: Coord, beacon: Coord, y: int) -> Tuple[int, int]:
    dist = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
    remxdist = dist - abs(sensor[1] - y)
    if remxdist < 0:
        return sensor[0], sensor[0]
    else:
        return sensor[0] - remxdist, sensor[0] + remxdist + 1


def get_exclusion_set_in(conns: List[Tuple[Coord, Coord]], y: int) -> Set[int]:
    result = set()
    for sensor, beacon in conns:
        new_excls = set(range(*get_exclusion_in(sensor, beacon, y)))
        result.update(new_excls)
    # now remove all beacons from the result
    for _, beacon in conns:
        if beacon[1] == y and beacon[0] in result:
            result.remove(beacon[0])
    return result


@define
class Ranges:
    ranges: List[Tuple[int, int]] = Factory(list)

    def add_range(self, rangex, rangey):
        idx = 0
        while idx < len(self.ranges) and self.ranges[idx][0] < rangex:
            idx += 1
        if 0 < idx:  # maybe merge with predecessor?
            if rangex <= self.ranges[idx - 1][1]:  # yes, merge
                # merge is: remove overlapping preceder
                # change rangex to start of preceder
                rangex = self.ranges[idx - 1][0]
                rangey = max(rangey, self.ranges[idx - 1][1])
                self.ranges.pop(idx - 1)
                idx -= 1
        # no overlap with preceder, merge with all overlapping postceders
        del_idx = idx
        while del_idx < len(self.ranges) and self.ranges[del_idx][0] <= rangey:
            del_idx += 1
        # everything between idx and del_idx gets gobbled up
        # enlarge rangey to that of del_idx if there is overlap
        if 0 < del_idx and idx < del_idx:  # maybe overlap?
            if rangey >= self.ranges[del_idx - 1][0]:  # yes, overlap
                rangey = max(self.ranges[del_idx - 1][1], rangey)
                self.ranges.pop(del_idx - 1)
                del_idx -= 1
        for to_del in range(idx, del_idx):
            self.ranges.pop(to_del)
        self.ranges.insert(idx, (rangex, rangey))

    def remove_el(self, el):
        idx = 0
        while idx < len(self.ranges):
            x, y = self.ranges[idx]
            if x <= el < y:  # then split
                if x == el:
                    self.ranges[idx] = x + 1, y
                elif y - 1 == el:
                    self.ranges[idx] = x, y - 1
                else:
                    self.ranges[idx] = x, el
                    self.ranges.insert(idx + 1, (el + 1, y))
                break
            if el < x:
                break
            idx += 1

    def __len__(self):
        return sum((y - x for x, y in self.ranges))

    def __contains__(self, el):
        idx = 0
        while idx < len(self.ranges):
            x, y = self.ranges[idx]
            if x <= el < y:
                return True
            if el < x:
                return False
            idx += 1
        return False

    def truncated_complement(self, lb: int, ub: int) -> 'Ranges':
        new_ranges = []
        for rx, ry in zip((y for _, y in self.ranges[:-1]), (x for x, _ in self.ranges[1:])):
            if ry < lb:
                continue
            if rx >= ub:
                break
            new_ranges.append((max(rx, lb), min(ry, ub)))
        # now possibly prepend or postpend edge cases
        if not self.ranges:
            new_ranges.append((lb, ub))
        else:
            if self.ranges[-1][1] < ub:
                new_ranges.append((self.ranges[-1][1], ub))
            if self.ranges[0][0] >= lb:
                new_ranges.insert(0, (lb, self.ranges[0][0]))
        return Ranges(new_ranges)


def get_exclusion_ranges_in(conns: List[Tuple[Coord, Coord]], y: int, remove_beacons=True) -> Ranges:
    result = Ranges()
    for sensor, beacon in conns:
        rangex, rangey = get_exclusion_in(sensor, beacon, y)
        if rangex != rangey:
            result.add_range(rangex, rangey)
    if remove_beacons:
        for _, beacon in conns:
            if beacon[1] == y and beacon[0] in result:
                result.remove_el(beacon[0])
    return result


def find_beacon(conns: List[Tuple[Coord, Coord]], lb: int, ub: int):
    # slow but it works in about a minute or two
    # better would be to not do it row by row but all at once. but the ranges are
    # diamonds instead of squares, so that is annoying. maybe you could do heuristics for sensors that are far off
    # beacons but writing that takes longer than two minutes
    for row in range(lb, ub):
        excluded = get_exclusion_ranges_in(conns, row, False)
        compl = excluded.truncated_complement(lb, ub)
        if row % 10000 == 0:
            print(row)
        if len(compl) > 0:
            print(f'y={row}', excluded, compl)
            break


def main():
    test_input = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
    with open('input/day15_input.txt') as f:
        file_input = f.read()
    TEST = False
    if TEST:
        the_input = test_input
        the_row = 10
        the_bound = 20
    else:
        the_input = file_input
        the_row = 2000000
        the_bound = 4000000
    sensors = sensor_parse.parse(the_input)
    result_range = get_exclusion_ranges_in(sensors, the_row)
    print(len(result_range))
    find_beacon(sensors, 0, the_bound)


if __name__ == '__main__':
    main()
