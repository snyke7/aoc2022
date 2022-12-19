from typing import Tuple, Set, Dict, List, Generator

from day12 import dijkstra


Cube = Tuple[int, int, int]


small_test = '''1,1,1
2,1,1
'''


test_input = '''2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''


def gen_neighbors(cube: Cube):
    x, y, z = cube
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y - 1, z
    yield x, y + 1, z
    yield x, y, z - 1
    yield x, y, z + 1


def count_side(cube: Cube, cubes: Set[Cube], interior):
    return sum((1 for neighbor in gen_neighbors(cube)
                if neighbor not in cubes and (interior is None or neighbor not in interior)))


def count_sides(cubes: Set[Cube], interior=None):
    return sum((count_side(cube, cubes, interior=interior) for cube in cubes))


def get_min_bb_cube(cubes: Set[Cube]) -> Cube:
    minx = min((x for x, _, _ in cubes)) - 1
    miny = min((y for _, y, _ in cubes)) - 1
    minz = min((z for _, _, z in cubes)) - 1
    return minx, miny, minz


def get_max_bb_cube(cubes: Set[Cube]) -> Cube:
    maxx = max((x for x, _, _ in cubes)) + 1
    maxy = max((y for _, y, _ in cubes)) + 1
    maxz = max((z for _, _, z in cubes)) + 1
    return maxx, maxy, maxz


def bb_iter(cubes: Set[Cube]) -> Generator[Cube, None, None]:
    minx, miny, minz = get_min_bb_cube(cubes)
    maxx, maxy, maxz = get_max_bb_cube(cubes)
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            for z in range(minz, maxz + 1):
                yield x, y, z


def in_bound(min_cube: Cube, max_cube: Cube, the_cube: Cube) -> bool:
    minx, miny, minz = min_cube
    maxx, maxy, maxz = max_cube
    x, y, z = the_cube
    return (minx <= x <= maxx and
            miny <= y <= maxy and
            minz <= z <= maxz)


def gen_graph(cubes: Set[Cube]) -> Dict[Cube, List[Cube]]:
    conns: Dict[Cube, List[Cube]] = {}
    min_cube = get_min_bb_cube(cubes)
    max_cube = get_max_bb_cube(cubes)
    for cube in bb_iter(cubes):
        if cube not in cubes:
            conns[cube] = [
                neighbor for neighbor in gen_neighbors(cube)
                if neighbor not in cubes and in_bound(min_cube, max_cube, neighbor)
            ]
    return conns


def find_interior_air(cubes: Set[Cube]) -> Set[Cube]:
    graph = gen_graph(cubes)
    start = get_min_bb_cube(cubes)
    dists = dijkstra(graph, start)
    interior = set(bb_iter(cubes)) - set(dists.keys())
    return interior


def main():
    with open('input/day18_input.txt') as f:
        file_input = f.read()
    the_input = test_input
    cubes = {
        tuple(map(int, cube.strip().split(',')))
        for cube in the_input.splitlines()
    }
    print(count_sides(cubes))
    print(count_sides(cubes, find_interior_air(cubes)))


if __name__ == '__main__':
    main()
