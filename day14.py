from typing import Dict, Tuple, List
from collections import defaultdict


Coord = Tuple[int, int]

# populate a dictionary with rock monoliths. no need to store whether sand or rock
# get lowest rock monolith
# simulate sand falling until stopped or lower than lowest rock monolith


def add_from_to(start: Coord, end: Coord, grid: Dict[Coord, bool]):
    xdiff = end[0] - start[0]
    ydiff = end[1] - start[1]
    xstep = xdiff // abs(xdiff) if xdiff else 0
    ystep = ydiff // abs(ydiff) if ydiff else 0
    for i in range(max(abs(xdiff), abs(ydiff)) + 1):
        res = start[0] + i * xstep, start[1] + i * ystep
        grid[res] = True


def parse_input(the_input) -> List[List[Coord]]:
    return [
        [
            tuple((
                int(el) for el in coord.split(',')
            ))
            for coord in line.split(' -> ')
        ]
        for line in the_input.splitlines()
    ]


def add_regolith(coords: List[Coord], grid: Dict[Coord, bool]):
    for start, end in zip(coords[:-1], coords[1:]):
        add_from_to(start, end, grid)


def get_initial_grid(regos: List[List[Coord]]):
    grid = defaultdict(lambda: False)
    for rego in regos:
        add_regolith(rego, grid)
    return grid


def get_pt2_grid(regos: List[List[Coord]]):
    grid = get_initial_grid(regos)
    lowest = max((y for _, y in grid.keys()))
    for x in range(500 - lowest - 2, 500 + lowest + 2 + 1):
        grid[x, lowest + 2] = True
    return grid


def add_sand(grid: Dict[Coord, bool], lowest: int) -> bool:
    sandx = 500
    sandy = 0
    while sandy <= lowest:
        if not grid[sandx, sandy + 1]:
            sandy += 1
        elif not grid[sandx - 1, sandy + 1]:
            sandx -= 1
            sandy += 1
        elif not grid[sandx + 1, sandy + 1]:
            sandx += 1
            sandy += 1
        else:
            taken = grid[sandx, sandy]
            grid[sandx, sandy] = True
            return not taken
    return False


def fill_grid(grid: Dict[Coord, bool]):
    added_sand = 0
    lowest = max((y for _, y in grid.keys()))
    while True:
        if add_sand(grid, lowest):
            added_sand += 1
        else:
            break
    return added_sand


def main():
    test_input = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
    with open('input/day14_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    parsed = parse_input(the_input)
    grid = get_initial_grid(parsed)
    print(fill_grid(grid))
    print(fill_grid(get_pt2_grid(parsed)))


if __name__ == '__main__':
    main()
