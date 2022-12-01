def main():
    with open('input/day01_input.txt') as f:
        lines = ''.join(f.readlines())
        elves = [[int(el.strip()) for el in group.split('\n') if el.strip()] for group in lines.split('\n\n')]
        print(max(map(sum, elves)))
        print(sum(sorted(map(sum, elves))[-3:]))


if __name__ == '__main__':
    main()