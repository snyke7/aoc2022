from typing import Tuple, Dict, List, TypeVar


test_grid = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''


def to_height_num(the_char):
    if the_char == 'S':
        return to_height_num('a')
    if the_char == 'E':
        return to_height_num('z')
    return ord(the_char) - ord('a')


def read_grid(grid_str: str) -> Dict[Tuple[int, int], int]:
    return {
        (i, j): to_height_num(char)
        for i, line in enumerate(grid_str.splitlines())
        for j, char in enumerate(line)
    }


def find_char(grid_str: str, target: str) -> Tuple[int, int]:
    for i, line in enumerate(grid_str.splitlines()):
        for j, char in enumerate(line):
            if char == target:
                return i, j


def get_visitable_neighbors(grid: Dict[Tuple[int, int], int], i: int, j: int, xlen: int, ylen: int)\
        -> List[Tuple[int, int]]:
    result = []
    height = grid[i, j]
    if i > 0 and grid[i - 1, j] <= height + 1:
        result.append((i - 1, j))
    if i < xlen - 1 and grid[i + 1, j] <= height + 1:
        result.append((i + 1, j))
    if j > 0 and grid[i, j - 1] <= height + 1:
        result.append((i, j - 1))
    if j < ylen - 1 and grid[i, j + 1] <= height + 1:
        result.append((i, j + 1))
    return result


def grid_to_graph(grid: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    xlen = max((x for x, _ in grid.keys())) + 1
    ylen = max((y for _, y in grid.keys())) + 1
    return {
        (i, j): get_visitable_neighbors(grid, i, j, xlen, ylen)
        for i, j in grid.keys()
    }


def read_graph(grid_str: str) -> Tuple[Dict[Tuple[int, int], List[Tuple[int, int]]], Tuple[int, int], Tuple[int, int]]:
    grid = read_grid(grid_str)
    start = find_char(grid_str, 'S')
    end = find_char(grid_str, 'E')
    return grid_to_graph(grid), start, end


A = TypeVar('A')


def dijkstra(graph: Dict[A, List[A]], start: A) -> Dict[A, int]:
    result = {start: 0}
    new = [start]
    while new:
        node = new.pop(0)
        cost = result[node]
        for neigbor in graph[node]:
            if neigbor not in result or result[neigbor] > cost + 1:
                result[neigbor] = cost + 1
                new.append(neigbor)
    return result


def main():
    with open('input/day12_input.txt') as f:
        input_grid = f.read()
    the_grid = input_grid
    graph, start, end = read_graph(the_grid)
    dists = dijkstra(graph, start)
    print(dists[end])
    grid = read_grid(the_grid)
    min_dists = [
        dijkstra(graph, adr)[end] if end in dijkstra(graph, adr) else 999
        # bloody inefficient but apparently fine
        for adr, height in grid.items()
        if height == 0
    ]
    print(min(min_dists))


if __name__ == '__main__':
    main()
