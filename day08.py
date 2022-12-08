from typing import List, Tuple
from math import prod


def get_visible_trees(i, j, grid: List[List[int]]) -> Tuple[List[int], List[int], List[int], List[int]]:
    above = list(reversed([grid[k][j] for k in range(i)]))
    below = [grid[k][j] for k in range(i+1, len(grid))]
    left = list(reversed([grid[i][k] for k in range(j)]))
    right = [grid[i][k] for k in range(j+1, len(grid[i]))]
    return above, below, left, right


def is_visible_in(i, j, grid: List[List[int]]):
    if i == 0 or j == 0 or i == len(grid) - 1 or j == len(grid[i]) - 1:
        return True
    height = grid[i][j]
    min_view_dist = min(map(max, list(get_visible_trees(i, j, grid))))
    return min_view_dist < height


def calc_view_dist(height, trees: List[int]):
    view_dist = 0
    for tree in trees:
        view_dist += 1
        if tree >= height:
            break
    return view_dist


def calc_scenic_score(i, j, grid: List[List[int]]):
    height = grid[i][j]
    return prod((calc_view_dist(height, trees) for trees in get_visible_trees(i, j, grid)))


def main():
    with open('input/day08_input.txt') as f:
        grid = [list(map(int, line.strip())) for line in f.readlines()]
    print(grid)
    print(len(grid))
    print(len(grid[0]))
    print(sum((1 for i in range(len(grid)) for j in range(len(grid[0])) if is_visible_in(i, j, grid))))
    print(max((calc_scenic_score(i, j, grid) for i in range(len(grid)) for j in range(len(grid[0])))))


if __name__ == '__main__':
    main()
