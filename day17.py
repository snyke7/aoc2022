from typing import Tuple, Set, Generator, List

from attrs import define


Coord = Tuple[int, int]


@define
class Rock:
    overlay: Set[Coord]

    def as_filled(self, dx: int, dy: int):
        return {
            (cx + dx, cy + dy)
            for cx, cy in self.overlay
        }

    def overlaps(self, filled: Set[Coord], dx: int, dy: int):
        for cx, cy in self.as_filled(dx, dy):
            if (cx, cy) in filled:
                return True
            if cy < 0 or cy >= 7:
                return True
            if cx >= 0:
                return True
        return False


rocks = [  # (0,0) is left-bottom
    Rock({(0, 0), (0, 1), (0, 2), (0, 3)}),  # --
    Rock({(-1, 0), (-1, 1), (-1, 2), (-2, 1), (0, 1)}),  # +
    Rock({(0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2)}),  # _|
    Rock({(-3, 0), (-2, 0), (-1, 0), (0, 0)}),  # |
    Rock({(-1, 0), (-1, 1), (0, 0), (0, 1)}),  # ⊠
]


def get_highest(filled: Set[Coord]):
    return min((x for x, y in filled) if filled else [0])


def add_rock(jets: Generator[int, None, None], rock: Rock, filled: Set[Coord]):
    highest = get_highest(filled)
    dx = highest - 4
    dy = 2
    while True:
        ddy = next(jets)
        if not rock.overlaps(filled, dx, dy + ddy):
            dy += ddy
        if rock.overlaps(filled, dx + 1, dy):  # stop at current position
            break
        dx += 1
    filled.update(rock.as_filled(dx, dy))
    return dx


def has_tetris_at(stack: Set[Coord], x: int):
    return all((
            (x, y) in stack
            for y in range(7)
        ))


def read_jet_rep(jets: Generator[int, None, None], jet_len: int):
    return tuple([next(jets) for _ in range(jet_len)])


def gen_tetris_hash(stack: Set[Coord], rock, jets: Generator[int, None, None], jet_len: int):
    cur_jet = read_jet_rep(jets, jet_len)
    min_height = max((x for x, _ in stack)) if stack else 0
    return hash((frozenset({
        (x - min_height, y)
        for x, y in stack
    }), rock % 5, cur_jet))


def gen_bounded_hash(stack: Set[Coord], rock, jets: Generator[int, None, None], jet_len: int, bound: int):
    cur_jet = read_jet_rep(jets, jet_len)
    max_height = get_highest(stack)
    return hash((frozenset({
        (x - max_height, y)
        for x, y in stack
        if abs(x - max_height) <= bound
    }), rock % 5, cur_jet))


def jet_to_str(jet_cmds: List[int]):
    return ''.join((
        '<' if cmd == -1 else '>'
        for cmd in jet_cmds
    ))


def find_jet_index(jet_str: str, cur_jet: Tuple[int]):
    half_index = len(cur_jet) // 2
    cur_left, cur_right = jet_to_str(list(cur_jet)[:half_index]), jet_to_str(list(cur_jet)[half_index:])
    idx = jet_str.find(cur_left)
    if idx == -1:
        idx = jet_str.find(cur_right)
        rem_left_len = len(cur_jet) - len(cur_right) - idx
        assert(cur_left[rem_left_len:] + cur_right + cur_left[:rem_left_len] == jet_str)
        return idx + len(cur_right)
    else:
        rem_right_len = len(cur_jet) - len(cur_left) - idx
        assert(cur_right[rem_right_len:] + cur_left + cur_right[:rem_right_len] == jet_str)
        return idx


def drop_rocks(jet_str: str, amt: int, repetition_size_bound=None):
    stack = set()
    num_tetris = 0
    tetris_dict = {}
    last_n_dict = {}
    jet_str = jet_str.strip()
    jets = input_to_jets(jet_str)
    jet_rep = len(jet_str)
    period = None
    last_rock = 0
    height_period = 0

    for i in range(amt):
        destx = add_rock(jets, rocks[i % len(rocks)], stack)
        for maybe_tetris in range(destx - 3, destx + 1):
            if has_tetris_at(stack, maybe_tetris):
                stack = {
                    (cx, cy)
                    for cx, cy in stack
                    if cx <= maybe_tetris
                }
                num_tetris += 1
                the_hash = gen_tetris_hash(stack, i % 5, jets, jet_rep)
                if the_hash in tetris_dict:
                    print(f'Found repetition at {i}! Same post-tetris state as after {tetris_dict[the_hash]}')
                    print(f' that is: {i, find_jet_index(jet_str, read_jet_rep(jets, jet_rep)), get_highest(stack)}')
                    period = i - tetris_dict[the_hash][0]
                    last_rock = i
                    height_period = get_highest(stack) - tetris_dict[the_hash][2]
                else:
                    tetris_dict[the_hash] = i, find_jet_index(jet_str, read_jet_rep(jets, jet_rep)), get_highest(stack)
                    print(f'Turn {i}, tetris at line {maybe_tetris}')
        if repetition_size_bound is not None:
            cur_hash = gen_bounded_hash(stack, i % 5, jets, jet_rep, repetition_size_bound)
            if cur_hash in last_n_dict:
                print(f'Found repetition at {i}! Same state as after {last_n_dict[cur_hash]}')
                print(f' that is: {i, find_jet_index(jet_str, read_jet_rep(jets, jet_rep)), get_highest(stack)}')
                period = i - last_n_dict[cur_hash][0]
                last_rock = i
                height_period = get_highest(stack) - last_n_dict[cur_hash][2]
            else:
                last_n_dict[cur_hash] = i, find_jet_index(jet_str, read_jet_rep(jets, jet_rep)), get_highest(stack)
        if period is not None:
            break
    if period is None:
        return stack
    # otherwise: loop was broken since repeating period was found before reaching simulation depth
    # we can take the current stack, and increase the height by the precisely sufficient amount of repetitions
    num_rep = (amt - last_rock - 1) // period
    cur_rock = last_rock + num_rep * period + 1
    print(f'Skipping from {last_rock} to {cur_rock}')
    stack = {
        (x + num_rep * height_period, y)
        for x, y in stack
    }
    for i in range(cur_rock, amt):
        add_rock(jets, rocks[i % len(rocks)], stack)
    return stack


def input_to_jets(input_str: str) -> Generator[int, None, None]:
    i = 0
    while True:
        yield 1 if input_str[i] == '>' else -1
        i += 1
        i = i % len(input_str)


def stack_to_str(filled: Set[Coord]):
    result = []
    for i in range(get_highest(filled), 0):
        the_str = '|' + ''.join(
            '#' if (i, j) in filled else '.'
            for j in range(7)
        ) + '|'
        result.append(the_str)
    result.append('+-------+')
    return '\n'.join(result)


def main():
    test_input = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>\n'
    with open('input/day17_input.txt') as f:
        file_input = f.read()
    the_input = file_input

    pt1 = 2022
    pt2 = 1000000000000

    print(get_highest(drop_rocks(the_input, pt1)))
    print(get_highest(drop_rocks(the_input, pt2)))
    pass


if __name__ == '__main__':
    main()
