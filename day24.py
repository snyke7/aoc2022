from typing import Set, Tuple, List, Dict

from day12 import dijkstra

Coord = Tuple[int, int]


test_input = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''


def read_map(input_str: str) -> Set[Coord]:
    return {
        (i - 1, j - 1)
        for i, line in enumerate(input_str.splitlines(False))
        for j, el in enumerate(line)
        if el != '#'
    }


DIR_MAP = {
    '>': 0,
    'v': 1,
    '<': 2,
    '^': 3
}

DIR_STEP_MAP = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0)
}


def read_tornadoes(input_str: str) -> Set[Tuple[Coord, int]]:
    return {
        ((i - 1, j - 1), DIR_MAP[el])
        for i, line in enumerate(input_str.splitlines(False))
        for j, el in enumerate(line)
        if el in DIR_MAP
    }


def get_map_size(the_map: Set[Coord]) -> Tuple[int, int]:
    xlen = (max((x for x, _ in the_map)) - 1) - (min((x for x, _ in the_map)) + 1) + 1
    ylen = max((y for _, y in the_map)) - min((y for _, y in the_map)) + 1
    return xlen, ylen


def get_gcd(a: int, b: int) -> int:
    if b > a:
        return get_gcd(b, a)
    if a % b == 0:
        return b
    return get_gcd(b, a % b)


def get_scm(a: int, b: int) -> int:
    return (a * b) // get_gcd(a, b)


def tornado_step(coord: Coord, the_dir: int, xlen: int, ylen: int) -> Coord:
    x, y = coord
    dx, dy = DIR_STEP_MAP[the_dir]
    return (x + dx) % xlen, (y + dy) % ylen


def tornadoes_step(tornadoes: Set[Tuple[Coord, int]], xlen: int, ylen: int) -> Set[Tuple[Coord, int]]:
    return {
        (tornado_step(coord, the_dir, xlen, ylen), the_dir)
        for coord, the_dir in tornadoes
    }


def gen_map_sequence(the_map: Set[Coord], tornadoes: Set[Tuple[Coord, int]]) -> List[Set[Coord]]:
    xlen, ylen = get_map_size(the_map)
    list_len = get_scm(xlen, ylen)
    result = []
    for i in range(list_len):
        result.append(the_map - {tornado_coord for tornado_coord, _ in tornadoes})
        tornadoes = tornadoes_step(tornadoes, xlen, ylen)
    return result


def get_neighbors(coord: Coord) -> List[Coord]:
    x, y = coord
    return [
        (x + DIR_STEP_MAP[the_dir][0], y + DIR_STEP_MAP[the_dir][1])
        for the_dir in range(4)
    ] + [(x, y)]


def to_regular_map(map_sequence: List[Set[Coord]]) -> Dict[Tuple[int, Coord], List[Tuple[int, Coord]]]:
    result = {}
    for i, cur_map in enumerate(map_sequence):
        next_idx = (i + 1) % len(map_sequence)
        next_map = map_sequence[next_idx]
        for coord in cur_map:
            result[i, coord] = [(next_idx, neighbor) for neighbor in get_neighbors(coord) if neighbor in next_map]
    return result


def find_first_at(path_len_dict: Dict[Tuple[int, Coord], int], coord: Coord, map_len: int) -> Tuple[int, int]:
    shortest = min((
        path_len_dict[i, coord]
        for i in range(map_len)
        if (i, coord) in path_len_dict
    ))
    return shortest, (shortest % map_len)


def find_path_len(the_map: Set[Coord], tornadoes: Set[Tuple[Coord, int]]) -> Tuple[int, int]:
    map_seq = gen_map_sequence(the_map, tornadoes)
    reg_map = to_regular_map(map_seq)
    start = (-1, 0)
    path_len_dict1 = dijkstra(reg_map, (0, start))
    xlen, ylen = get_map_size(the_map)
    dest = (xlen, ylen - 1)
    pt1, idx = find_first_at(path_len_dict1, dest, len(map_seq))
    path_len_dict2 = dijkstra(reg_map, (idx, dest))
    pt2_1, idx1 = find_first_at(path_len_dict2, start, len(map_seq))
    path_len_dict3 = dijkstra(reg_map, ((idx + idx1)% len(map_seq), start))
    pt2_2, _ = find_first_at(path_len_dict3, dest, len(map_seq))
    return pt1, (pt1 + pt2_1 + pt2_2)


def main():
    with open('input/day24_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    the_map = read_map(the_input)
    tornadoes = read_tornadoes(the_input)
    print(find_path_len(the_map, tornadoes))


if __name__ == '__main__':
    main()
