from parsy import string, decimal_digit, seq


def to_instr_tuple(*, amt, from_idx, to_idx):
    return amt, from_idx, to_idx


instruction = seq(
    __tag1=string('move '),
    amt=decimal_digit.at_least(1).concat().map(int),
    __tag2=string(' from '),
    from_idx=decimal_digit.map(int),
    __tag3=string(' to '),
    to_idx=decimal_digit.map(int)
).combine_dict(to_instr_tuple) << string('\n')


def apply_instruction(cargo, instr, reverse=True):
    amt, from_idx, to_idx = instr
    to_take, new_from = cargo[from_idx][:amt], cargo[from_idx][amt:]
    new_to = (list(reversed(to_take)) if reverse else to_take) + cargo[to_idx]
    cargo[from_idx] = new_from
    cargo[to_idx] = new_to


def main():
    with open('input/day05_input.txt') as f:
        lines = f.readlines()
    cargo_lines = lines[:9]
    instruction_lines = lines[10:]
    cargo = {
        i: list(''.join([cargo_lines[j][4 * (i - 1) + 1] for j in range(8)]).strip())
        for i in range(1, 10)
    }
    cargo_9001 = cargo.copy()
    instructions = [instruction.parse(line) for line in instruction_lines]
    for instr in instructions:
        apply_instruction(cargo, instr)
    print(''.join((stack[0] for stack in cargo.values())))
    for instr in instructions:
        apply_instruction(cargo_9001, instr, reverse=False)
    print(''.join((stack[0] for stack in cargo_9001.values())))


if __name__ == '__main__':
    main()
