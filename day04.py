class Range:
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

    def is_superset(self, other):
        return (self.lb <= other.lb) and (other.ub <= self.ub)

    def overlap(self, other):
        return (self.lb <= other.ub) and (other.lb <= self.ub)

    def __repr__(self):
        return f'Range(lb={self.lb}, ub={self.ub})'

    def __str__(self):
        return f'{self.lb}-{self.ub}'


def range_from_str(rangestr):
    return Range(*map(int,rangestr.split('-')))


def main():
    with open('input/day04_input.txt') as f:
        rangepairs = [tuple(map(range_from_str, line.strip().split(','))) for line in f.readlines()]
    full_contains_count = sum((1 for left, right in rangepairs
                               if left.is_superset(right) or right.is_superset(left)))
    print(full_contains_count)
    overlap_count = sum((1 for left, right in rangepairs
                         if left.overlap(right)))
    print(overlap_count)


if __name__ == '__main__':
    main()
