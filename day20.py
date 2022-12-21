from typing import List, Optional, Generator, Tuple

from attrs import define


test_input = '''7
2
-3
3
-2
0
4
'''


@define
class CircularListNode:
    val: int
    prev: 'CircularListNode'
    next: 'CircularListNode'

    def detach(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = None
        self.next = None

    def insert_between(self, newprev: 'CircularListNode', newnext: 'CircularListNode'):
        self.prev = newprev
        self.next = newnext
        newprev.next = self
        newnext.prev = self

    def move(self, amt):
        while amt > 0:
            amt -= 1
            old_prev = self.prev
            old_next = self.next
            old_prev.next = old_next
            old_next.prev = old_prev
            self.prev = old_next
            self.next = old_next.next
            old_next.next = self
            self.next.prev = self

        while amt < 0:
            amt += 1
            old_prev = self.prev
            old_next = self.next
            old_prev.next = old_next
            old_next.prev = old_prev
            self.prev = old_prev.prev
            self.next = old_prev
            old_prev.prev = self
            self.prev.next = self


@define
class CircularList:
    first: CircularListNode
    length: int

    def __getitem__(self, item) -> CircularListNode:
        item = item % self.length
        node = self.first
        while item > 0:
            node = node.next
            item -= 1
        return node

    def __iter__(self) -> Generator[CircularListNode, None, None]:
        idx = 0
        node = self.first
        while idx < self.length:
            yield node
            idx += 1
            node = node.next

    def find(self, item: int) -> Optional[Tuple[int, CircularListNode]]:
        for i, node in enumerate(self):
            if node.val == item:
                return i, node
        return None

    def move_value(self, value: int):
        _, node = self.find(value)
        to_move = node.val % (self.length - 1)  # now always in positive direction!
        # but -1 =%= self.length - 1 - 1
        if abs(to_move) > abs(to_move - (self.length - 1)):
            to_move -= self.length - 1
        node.move(to_move)

    def move_value_fast(self, value: int):
        idx, node = self.find(value)
        if idx == 0:
            self.first = node.next
        node.detach()
        self.length -= 1
        # idx now points to oldnext
        # so idx + value now points to newnext
        new_next = self[idx + value]
        node.insert_between(new_next.prev, new_next)
        self.length += 1

    def as_val_list(self):
        return [node.val for node in self]

    def as_val_list_from(self, head: int):
        result = self.as_val_list()
        head_idx = result.index(head)
        return result[head_idx:] + result[:head_idx]

    def copy(self) -> 'CircularList':
        return to_circular_list(self.as_val_list())


def to_circular_list(array: List[int]) -> Optional[CircularList]:
    # temporarily break types :)
    nodes = [CircularListNode(val=v, prev=None, next=None) for v in array]
    # now fix them
    for i, node in enumerate(nodes):
        node.prev = nodes[(i - 1) % len(nodes)]
        node.next = nodes[(i + 1) % len(nodes)]
    if nodes:
        return CircularList(nodes[0], len(nodes))
    else:
        return None


def mix(clist: CircularList):
    for v in clist.as_val_list():
        clist.move_value_fast(v)
        # print(clist.as_val_list())
    return clist


def mix_both(clist: CircularList):
    clist2 = clist.copy()
    to_rep = list(enumerate(clist.as_val_list()))
    for i, v in to_rep:
        list1 = clist.as_val_list_from(0)
        list2 = clist2.as_val_list_from(0)
        print(list1)
        if list1 != list2:
            print()
            print(list2)
            print()
            raise ValueError(f'bad code after {i}: {v}')
        clist.move_value(v)
        clist2.move_value_fast(v)
    return clist


def get_coord_sum(clist: CircularList) -> int:
    z_ind, _ = clist.find(0)
    num1 = clist[z_ind + 1000].val
    num2 = clist[z_ind + 2000].val
    num3 = clist[z_ind + 3000].val
    print(num1, num2, num3)
    return num1 + num2 + num3


def main():
    with open('input/day20_input.txt') as f:
        file_input = f.read()
    the_input = file_input
    array = list(map(int, the_input.splitlines(False)))
    array = array[0:200]
    array[-2] = 0
    clist = to_circular_list(array)
    mix_both(clist)
    print('done mixing')
    print(get_coord_sum(clist))


if __name__ == '__main__':
    main()
