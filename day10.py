from typing import Optional, Dict, List

from attrs import define


def parse_line(line) -> Optional[int]:
    if line == 'noop':
        return None
    elif line.startswith('addx'):
        return int(line[5:])
    else:
        raise ValueError(line)


@define
class CPUState:
    cycle: int = 0
    X: int = 1

    def register(self, trace: Dict[int, int]):
        trace[self.cycle] = self.X

    def update(self):
        self.cycle += 1

    def update_and_register(self, trace: Dict[int, int]):
        self.update()
        self.register(trace)


def run_instr(state: CPUState, trace: Dict[int, int], instr: Optional[int]):
    if instr is None:
        state.update_and_register(trace)
    else:
        state.update_and_register(trace)
        state.update_and_register(trace)
        state.X += instr


def execute(state: CPUState, instrs: List[Optional[int]]):
    trace = {}
    for instr in instrs:
        run_instr(state, trace, instr)
    return trace


test_instrs = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''


def trace_to_screen(trace: Dict[int, int]) -> Dict[int, bool]:
    return {
        cycle: abs(X - ((cycle - 1) % 40)) <= 1
        for cycle, X in trace.items()
    }


def screen_to_string(screen: Dict[int, bool]) -> str:
    long_str = ''.join(('#' if lit else '.' for lit in screen.values()))
    return '\n'.join((long_str[i * 40:(i + 1) * 40] for i in range(len(long_str) // 40)))


def main():
    with open('input/day10_input.txt') as f:
        instrs = [parse_line(line.strip()) for line in f.readlines()]
    # instrs = [parse_line(line.strip()) for line in test_instrs.splitlines()]
    # print(instrs)
    trace = execute(CPUState(), instrs)
    print(sum(trace[20 + i * 40] * (20 + i * 40) for i in range(6)))
    print(trace)
    print(screen_to_string(trace_to_screen(trace)))


if __name__ == '__main__':
    main()
