from typing import Tuple, Set, List, Dict

from collections import defaultdict


Coord = Tuple[int, int]

test_input = '''....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
'''

test_input_small = '''.....
..##.
..#..
.....
..##.
.....
'''


def parse_input(input_str: str) -> Set[Coord]:
    return {
        (i, j)
        for i, line in enumerate(input_str.splitlines(False))
        for j, el in enumerate(line)
        if el == '#'
    }


def add_step(coord: Coord, step: Coord):
    x, y = coord
    i, j = step
    return x + i, y + j


def get_neigbors(coord: Coord):
    for i in range(-1, 1 + 1):
        for j in range(-1, 1 + 1):
            if i == 0 and j == 0:
                continue
            yield add_step(coord, (i, j))


def propose_move(coord: Coord, elfs: Set[Coord], dirs: List[List[Coord]]):
    present_neighbors = {
        neighbor for neighbor in get_neigbors(coord)
        if neighbor in elfs
    }
    if not present_neighbors:
        return coord
    for dir_neighbors in dirs:
        if all((add_step(coord, dir_neighbor) not in present_neighbors for dir_neighbor in dir_neighbors)):
            return add_step(coord, dir_neighbors[1])


def do_move(elfs: Set[Coord], dirs: List[List[Coord]]):
    proposed: Dict[Coord, List[Coord]] = defaultdict(lambda: list())
    dups = []
    for elf in elfs:
        dest = propose_move(elf, elfs, dirs)
        proposed[dest].append(elf)
        if len(proposed[dest]) > 1 or dest is None:
            dups.append(dest)
    return {
        dest for dest in proposed.keys()
        if dest not in dups
    } | {
        orig for dup in dups
        for orig in proposed[dup]
    }


DIR_LIST = [
    [(-1, -1), (-1, 0), (-1, 1)],
    [(1, -1), (1, 0), (1, 1)],
    [(-1, -1), (0, -1), (1, -1)],
    [(-1, 1), (0, 1), (1, 1)],
]


def do_moves(elfs: Set[Coord], amt: int):
    the_dirs = DIR_LIST.copy()
    for i in range(amt):
        elfs = do_move(elfs, the_dirs)
        the_dirs = the_dirs[1:] + the_dirs[:1]
    return elfs


def find_fixpoint(elfs: Set[Coord]):
    the_dirs = DIR_LIST.copy()
    moves = 0
    while True:
        new_elfs = do_move(elfs, the_dirs)
        the_dirs = the_dirs[1:] + the_dirs[:1]
        moves += 1
        if new_elfs == elfs:
            return moves
        elfs = new_elfs


def get_elfs_dimensions(elfs: Set[Coord]) -> Tuple[int, int, int, int]:
    mini, minj = next(iter(elfs))
    maxi = mini
    maxj = minj
    for i, j in elfs:
        if i < mini:
            mini = i
        if i > maxi:
            maxi = i
        if j < minj:
            minj = j
        if j > maxj:
            maxj = j
    return mini, maxi, minj, maxj


def elf_map_str(elfs: Set[Coord]) -> str:
    mini, maxi, minj, maxj = get_elfs_dimensions(elfs)
    return '\n'.join((
        ''.join(
            '#' if (i, j) in elfs else '.'
            for j in range(minj, maxj + 1)
        ) for i in range(mini, maxi + 1)
    ))


def empty_ground_tiles(elfs: Set[Coord]) -> int:
    mini, maxi, minj, maxj = get_elfs_dimensions(elfs)
    return (maxi + 1 - mini) * (maxj + 1 - minj) - len(elfs)


def main():
    with open('input/day23_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    parsed = parse_input(the_input)
    after_10 = do_moves(parsed, 10)
    print(empty_ground_tiles(after_10))
    # could be made more efficient by keeping track of non-moving elves. but this is okay
    print(find_fixpoint(parsed))


if __name__ == '__main__':
    main()
