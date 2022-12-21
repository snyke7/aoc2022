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

    def partial_yell(self, monkeys: Dict[str, Any]) -> 'NumberMonkey':
        return self


OPS = {
    '+': lambda l, r: l + r,
    '-': lambda l, r: l - r,
    '*': lambda l, r: l * r,
    '/': lambda l, r: l // r,
    '=': lambda l, r: l == r
}


@define
class OpMonkey:
    left_monkey: str
    right_monkey: str
    op: str
    result: Optional[int] = None
    partial_result: Optional[Any] = None

    def yell(self, monkeys: Dict[str, Any]) -> int:
        if self.result is None:
            self.result = OPS[self.op](monkeys[self.left_monkey].yell(monkeys), monkeys[self.right_monkey].yell(monkeys))
        return self.result

    def partial_yell(self, monkeys: Dict[str, Any]):
        if self.partial_result is None:
            left = monkeys[self.left_monkey].partial_yell(monkeys)
            right = monkeys[self.right_monkey].partial_yell(monkeys)
            if isinstance(left, NumberMonkey) and isinstance(right, NumberMonkey):
                self.partial_result = NumberMonkey(OPS[self.op](left.yell(monkeys), right.yell(monkeys)))
            else:
                self.partial_result = self
        return self.partial_result


@define
class Human:
    name: str
    to_yell: Optional[int] = None

    def yell(self, monkeys: Dict[str, Any]) -> int:
        if self.to_yell is None:
            raise ValueError('Dont know what to yell yet!')
        else:
            return self.to_yell

    def partial_yell(self, monkeys: Dict[str, Any]) -> Any:
        return self


def parse_monkey(monkey_op: str):
    if monkey_op.isnumeric():
        return NumberMonkey(int(monkey_op))
    else:
        left, op, right = monkey_op.split(' ')
        return OpMonkey(left, right, op)


def to_partial_yell_str(monkeys: Dict[str, Any], monkey: Any):
    if isinstance(monkey, NumberMonkey):
        return str(monkey.value)
    elif isinstance(monkey, OpMonkey):
        if monkey.partial_result != monkey:
            return to_partial_yell_str(monkeys, monkey.partial_result)
        else:
            return f'({to_partial_yell_str(monkeys, monkeys[monkey.left_monkey])} {monkey.op} ' \
                   f'{to_partial_yell_str(monkeys, monkeys[monkey.right_monkey])})'
    elif isinstance(monkey, Human):
        return f'{monkey.name}'
    else:
        raise ValueError(monkey)


def main():
    with open('input/day21_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    monkeys = {line[:4]: parse_monkey(line[5:].strip()) for line in the_input.splitlines()}
    # print(monkeys['root'].yell(monkeys))
    monkeys['humn'] = Human('x')
    monkeys['root'].op = '='
    # monkeys['root'].partial_yell(monkeys)
    # print(to_partial_yell_str(monkeys, monkeys['root']))
    # input into wolframalpha
    # win
    # x = 3876907167495
    # to check the result:
    monkeys['humn'] = NumberMonkey(3876907167495)
    print(monkeys['root'].yell(monkeys))


if __name__ == '__main__':
    main()
