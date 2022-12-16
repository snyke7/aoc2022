from typing import List, Callable
from itertools import product

from attrs import define


@define
class Monkey:
    op: Callable[[int], int]
    divider: int
    target_divisible: int
    target_non_divisible: int
    items: List[int] = []
    inspections: int = 0

    def throw_first(self, monkeys: List['Monkey'], bound_op: Callable[[int], int]):
        item = bound_op(self.op(self.items.pop(0)))
        monkeys[
            self.target_divisible if item % self.divider == 0 else self.target_non_divisible
        ].items.append(item)
        self.inspections += 1

    def do_turn(self, monkeys: List['Monkey'], bound_op: Callable[[int], int]):
        while self.items:
            self.throw_first(monkeys, bound_op)


def do_round(monkeys: List[Monkey], bound_op: Callable[[int], int] = lambda x: x // 3):
    for monkey in monkeys:
        monkey.do_turn(monkeys, bound_op)


def monkey_business(monkeys: List[Monkey]):
    inspections = list(reversed(sorted((monkey.inspections for monkey in monkeys))))
    return inspections[0] * inspections[1]


def gen_test_monkeys() -> List[Monkey]:
    return [
        Monkey(lambda o: o * 19, 23, 2, 3, [79, 98]),
        Monkey(lambda o: o + 6, 19, 2, 0, [54, 65, 75, 74]),
        Monkey(lambda o: o * o, 13, 1, 3, [79, 60, 97]),
        Monkey(lambda o: o + 3, 17, 0, 1, [74]),
    ]


def gen_input_monkeys() -> List[Monkey]:
    return [
        Monkey(lambda o: o * 19, 3, 2, 3, [76, 88, 96, 97, 58, 61, 67]),
        Monkey(lambda o: o + 8, 11, 5, 6, [93, 71, 79, 83, 69, 70, 94, 98]),
        Monkey(lambda o: o * 13, 19, 3, 1, [50, 74, 67, 92, 61, 76]),
        Monkey(lambda o: o + 6, 5, 1, 6, [76, 92]),
        Monkey(lambda o: o + 5, 2, 2, 0, [74, 94, 55, 87, 62]),
        Monkey(lambda o: o * o, 7, 4, 7, [59, 62, 53, 62]),
        Monkey(lambda o: o + 2, 17, 5, 7, [62]),
        Monkey(lambda o: o + 3, 13, 4, 0, [85, 54, 53]),
    ]


def main():
    test_monks = gen_input_monkeys()
    divider_prod = 1
    for monkey in test_monks:
        divider_prod *= monkey.divider
    for i in range(10000):
        do_round(test_monks, lambda x: x % divider_prod)
    print(monkey_business(test_monks))


if __name__ == '__main__':
    main()
