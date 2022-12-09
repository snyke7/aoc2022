from typing import Tuple, Dict, List
from collections import defaultdict

from attrs import define


@define
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __mul__(self, other: int):
        return Position(self.x * other, self.y * other)


Left = Position(-1, 0)
Right = Position(1, 0)
Up = Position(0, 1)
Down = Position(0, -1)


def compute_new_tail_pos(new_head_pos: Position, old_tail_pos: Position) -> Position:
    tail_move = Position(0, 0)
    x_diff = new_head_pos.x - old_tail_pos.x
    y_diff = new_head_pos.y - old_tail_pos.y
    if abs(x_diff) > 1 or abs(y_diff) > 1:
        tail_move.x += x_diff / abs(x_diff) if x_diff else 0
        tail_move.y += y_diff / abs(y_diff) if y_diff else 0
    return old_tail_pos + tail_move


def propagate_rope_move(head: Position, tail: List[Position]) -> List[Position]:
    if not tail:
        return tail
    else:
        tail_move = Position(0, 0)
        old_tail_pos = tail[0]
        x_diff = head.x - old_tail_pos.x
        y_diff = head.y - old_tail_pos.y
        if abs(x_diff) > 1 or abs(y_diff) > 1:
            tail_move.x += x_diff / abs(x_diff) if x_diff else 0
            tail_move.y += y_diff / abs(y_diff) if y_diff else 0
        new_tail_pos = old_tail_pos + tail_move
        return [new_tail_pos] + propagate_rope_move(new_tail_pos, tail[1:])


def move_rope(rope: List[Position], direction: Position) -> List[Position]:
    new_head = rope[0] + direction
    return [new_head] + propagate_rope_move(new_head, rope[1:])


def register_move(visit_dict: Dict[Position, bool], rope: List[Position], direction: Position)\
        -> Tuple[Position, Position]:
    new_rope = move_rope(rope, direction)
    visit_dict[new_rope[-1]] = True
    return new_rope


def parse_move(move_line: str) -> Tuple[Position, int]:
    move_str, amt_str = tuple(move_line.strip().split(' '))
    amt = int(amt_str)
    if move_str == 'L':
        return Left, amt
    elif move_str == 'R':
        return Right, amt
    elif move_str == 'U':
        return Up, amt
    elif move_str == 'D':
        return Down, amt


def parse_moves(move_lines: str) -> List[Tuple[Position, int]]:
    return [parse_move(line) for line in move_lines.splitlines()]


TEST_MOVES1 = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''

TEST_MOVES2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''


def make_rope(rope_len):
    return [Position(0, 0) for _ in range(rope_len)]


def main():
    with open('input/day09_input.txt') as f:
        moves_str = ''.join(f.readlines())
    # moves_str = TEST_MOVES2
    moves = parse_moves(moves_str)
    visit_dict = defaultdict(lambda _: False)
    rope_pt1 = make_rope(2)
    for move, amt in moves:
        for i in range(amt):
            rope_pt1 = register_move(visit_dict, rope_pt1, move)
    visit_dict = defaultdict(lambda _: False)
    rope_pt2 = make_rope(10)
    for move, amt in moves:
        for i in range(amt):
            rope_pt2 = register_move(visit_dict, rope_pt2, move)
    print(sum((1 for val in visit_dict.values() if val)))


if __name__ == '__main__':
    main()
