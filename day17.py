from typing import Tuple, Set, Generator

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
    print(stack_to_str(filled.union(rock.as_filled(dx, dy))))
    while True:
        ddy = next(jets)
        if not rock.overlaps(filled, dx, dy + ddy):
            dy += ddy
        print(stack_to_str(filled.union(rock.as_filled(dx, dy))))
        if rock.overlaps(filled, dx + 1, dy):  # stop at current position
            print(f'breaking at {dx, dy}')
            break
        dx += 1
        print(stack_to_str(filled.union(rock.as_filled(dx, dy))))
    print()
    filled.update(rock.as_filled(dx, dy))


def drop_rocks(jets: Generator[int, None, None], amt: int):
    stack = set()
    for i in range(amt):
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
    the_input = test_input
    jets = input_to_jets(the_input)
    interm = drop_rocks(jets, 9)
    print(stack_to_str(interm))
    print()
    tenth = interm.copy()
    add_rock(jets, rocks[-1], tenth)
    print(stack_to_str(tenth))
    pass


if __name__ == '__main__':
    main()
