from typing import Dict, Any, Optional

from attrs import define


test_input = '''root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''


@define
class NumberMonkey:
    value: int

    def yell(self, monkeys: Dict[str, Any]) -> int:
        return self.value


OPS = {
    '+': lambda l, r: l + r,
    '-': lambda l, r: l - r,
    '*': lambda l, r: l * r,
    '/': lambda l, r: l // r,
}


@define
class OpMonkey:
    left_monkey: str
    right_monkey: str
    op: str
    result: Optional[int] = None

    def yell(self, monkeys: Dict[str, Any]) -> int:
        if self.result is None:
            self.result = OPS[self.op](monkeys[self.left_monkey].yell(monkeys), monkeys[self.right_monkey].yell(monkeys))
        return self.result


def parse_monkey(monkey_op: str):
    if monkey_op.isnumeric():
        return NumberMonkey(int(monkey_op))
    else:
        left, op, right = monkey_op.split(' ')
        return OpMonkey(left, right, op)


def main():
    with open('input/day21_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    monkeys = {line[:4]: parse_monkey(line[5:].strip()) for line in the_input.splitlines()}
    print(monkeys['root'].yell(monkeys))


if __name__ == '__main__':
    main()
