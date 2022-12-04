def sum_priorities(char_list):
    return sum([ord(c) - (ord('a') - 1 if c.islower() else ord('A') - 27) for c in char_list])


def main():
    with open('input/day03_input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    duplicates = [list(set(line[:len(line) // 2]).intersection(set(line[len(line) // 2:])))[0] for line in lines]
    print(sum_priorities(duplicates))
    elf_groups = [list(set(lines[i * 3]).intersection(*map(set, lines[i * 3 + 1:i * 3 + 3])))[0] for i in range(len(lines) // 3)]
    print(sum_priorities(elf_groups))


if __name__ == '__main__':
    main()
