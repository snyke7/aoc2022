from typing import Tuple, Dict, Optional, List, Set

from parsy import string, decimal_digit, seq
from attrs import define

Coord = Tuple[int, int]


test_input = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
''', 4, 5031


test_input3 = '''   ...#..
   ...#..
   ...#.#
   ...
   ...
   ...
###...
......
#.....
#..
..#
..#

4R7R4
''', 3, 8011

test_input4 = '''   ......
   ......
   ......
   ...
   ...
   ...
......
......
......
...
...
...

6R1R12R1R6
''', 3, 1016

test_input5 = '''   ......
   ......
   ......
   ...
   ...
   ...
......
......
......
...
...
...

1R6R1R12R1R6
''', 3, 1021

test_input6 = '''   ......
   ......
   ......
   ...
   ...
   ...
......
......
......
...
...
...

1R4R6R1R12R1R6
''', 3, 5022


DIR_STEP_COORDS = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0)
}


@define
class Map:
    map_dict: Dict[Coord, bool]
    map_size: int

    def get_step_dest(self, coord: Coord, step_dir: int) -> Optional[Coord]:
        x, y = coord
        dx, dy = DIR_STEP_COORDS[step_dir]
        while True:
            x = (x + dx - 1) % self.map_size + 1
            y = (y + dy - 1) % self.map_size + 1
            if (x, y) in self.map_dict:
                return (x, y) if self.map_dict[(x, y)] else None

    def __str__(self):
        return '\n'.join((
            ''.join((
                ' ' if (i, j) not in self.map_dict else (
                    '.' if self.map_dict[(i, j)] else '#'
                )
                for j in range(self.map_size + 1)
            ))
            for i in range(self.map_size + 1)
        ))


# Prototypical cube layout:
#    4
#   301     (1 is right of zero since you reach it by stepping right, which is represented as zero, the first option)
#    2
#    5


COORD_FACE_MAP = {
    (0, 1): 4,
    (1, 0): 3,
    (1, 1): 0,
    (1, 2): 1,
    (2, 1): 2,
    (3, 1): 5
}
TOP_LEFT_MAP = {
    4: (0, 1),
    3: (1, 0),
    0: (1, 1),
    1: (1, 2),
    2: (2, 1),
    5: (3, 1)
}


def get_top_left_dict(side_len):
    return {
        f: (x * side_len + 1, y * side_len + 1)
        for f, (x, y) in TOP_LEFT_MAP.items()
    }


@define
class CubeMap:
    map_dict: Dict[Coord, bool]
    side_len: int
    orig_coords: Dict[Coord, Coord]

    def get_face(self, coord: Coord) -> Optional[int]:
        x, y = coord
        fx, fy = (x - 1) // self.side_len, (y - 1) // self.side_len
        return COORD_FACE_MAP[(fx, fy)] if (fx, fy) in COORD_FACE_MAP else None

    def get_step_dest(self, coord: Coord, step_dir: int) -> Tuple[Coord, int]:
        x, y = coord
        dx, dy = DIR_STEP_COORDS[step_dir]
        on_face = self.get_face(coord)
        new_face = self.get_face((x + dx, y + dy))
        if on_face == new_face:
            return (x + dx, y + dy), step_dir
        # changed face!
        dest_face, new_dir, flip = face_connections[on_face][step_dir]
        # print(f'Swapping face! from {on_face} (to {new_face}) to {dest_face}')
        top_left_dict = get_top_left_dict(self.side_len)
        top_left = top_left_dict[dest_face]
        old_top_left = top_left_dict[on_face]
        odx, ody = x - old_top_left[0], y - old_top_left[1]
        # new direction indicates side of face we are on
        # only unknown is where on this row/column
        if new_dir % 2 == 0:  # now going left or right, so y coordinate can be determined
            cy = top_left[1] + (self.side_len - 1 if new_dir == 2 else 0)
            if (step_dir - new_dir) % 2 == 1:  # y offset becomes x offset
                cx = top_left[0] + (ody if not flip else self.side_len - 1 - ody)
            else:  # x offset becomes x offset
                cx = top_left[0] + (odx if not flip else self.side_len - 1 - odx)
            # print(f'Face1 swapped from {coord} to {(cx, cy)}: {top_left[0], flip, odx, ody}')
            return (cx, cy), new_dir
        else:  # now going up or down, so x coordinate can be deterimned
            cx = top_left[0] + (self.side_len - 1 if new_dir == 3 else 0)
            if (step_dir - new_dir) % 2 == 1:  # x offset becomes y offset
                cy = top_left[1] + (odx if not flip else self.side_len - 1 - odx)
            else:  # y offset becomes y offset
                cy = top_left[1] + (ody if not flip else self.side_len - 1 - ody)
            # print(f'Face2 swapped from {coord} to {(cx, cy)}: {top_left[1], flip, odx, ody}')
            return (cx, cy), new_dir

    def get_password(self, coord: Coord, step_dir: int):
        orig_coord = self.orig_coords[coord]
        # this will badly compute step_dir!
        print(f'On face {self.get_face(coord)}, might change direction {step_dir}?')
        return get_password(orig_coord, step_dir)

    def __str__(self):
        return str(map_from_dict(self.map_dict))


#                      face      step_dir  face' dir' flip_side_index?
face_connections: Dict[int, Dict[int, Tuple[int, int, bool]]] = {
    0: {
        0: (1, 0, False),  # step right on face 0: now on face 1, still right facing
        1: (2, 1, False),
        2: (3, 2, False),
        3: (4, 3, False)
    },
    1: {
        0: (5, 2, True),  # step right on face 1: now on face 5, facing left now!  high x becomes low x
        1: (2, 2, False),
        2: (0, 2, False),
        3: (4, 2, True),  # high y becomes low x
    },
    2: {
        0: (1, 3, False),
        1: (5, 1, False),
        2: (3, 3, True),
        3: (0, 3, False)
    },
    3: {
        0: (0, 0, False),
        1: (2, 0, True),
        2: (5, 0, True),
        3: (4, 0, False)
    },
    4: {
        0: (1, 1, True),
        1: (0, 1, False),
        2: (3, 1, False),
        3: (5, 3, False)
    },
    5: {
        0: (1, 2, True),
        1: (4, 1, False),
        2: (3, 0, True),
        3: (2, 3, False)
    }
}


def map_from_dict(map_dict: Dict[Coord, bool]):
    return Map(map_dict, max((max(i, j) for i, j in map_dict.keys())))


def gen_map(map_str: str) -> Map:
    return map_from_dict({
        (i + 1, j + 1): char == '.'
        for i, line in enumerate(map_str.splitlines(False))
        for j, char in enumerate(line)
        if char != ' '
    })


def rotate(base: Coord, coord: Coord, rotation: int, side_len: int):
    rotation = rotation % 4
    if rotation == 0:
        return coord
    bx, by = base
    cx, cy = coord
    dx, dy = cx - bx, cy - by
    if rotation == 1:
        return bx + dy, by + side_len - dx - 1
    elif rotation == 2:
        return bx + side_len - dx - 1, by + side_len - dy - 1
    elif rotation == 3:
        return bx + side_len - dy - 1, by + dx


def morph_cube_map(map_dict: Dict[Coord, bool], side_len: int) -> CubeMap:
    # morph to shape:
    #   4
    #  301
    #   2
    #   5
    top_left_dict = get_top_left_dict(side_len)
    result = {}
    coord_map = {}
    # initialize faces down from 3
    face_queue = [(4, next(iter(map_dict.keys())), 0)]
    rem_faces = {0, 1, 2, 3, 5}
    while rem_faces or face_queue:
        cur_face, top_left, rotation = face_queue.pop()
        dest_top_left = top_left_dict[cur_face]
        for i in range(side_len):
            for j in range(side_len):
                orig_loc = (top_left[0] + i, top_left[1] + j)
                changed_loc = rotate(top_left, orig_loc, -rotation, side_len)
                new_loc = (dest_top_left[0] + i, dest_top_left[1] + j)
                result[new_loc] = map_dict[changed_loc]
                coord_map[new_loc] = changed_loc
        for d in range(4):
            d_step = DIR_STEP_COORDS[(d - rotation) % 4]
            new_top_left = (top_left[0] + side_len * d_step[0], top_left[1] + side_len * d_step[1])
            next_face, new_d, flip = face_connections[cur_face][d]
            if new_top_left in map_dict and next_face in rem_faces:
                next_rotation = (new_d - d + rotation) % 4
                # print(f'Stepping from {cur_face} to {next_face} (which will have rotation {next_rotation})')
                rem_faces.remove(next_face)
                face_queue.append((next_face, new_top_left, next_rotation))
    return CubeMap(result, side_len, coord_map)


number = decimal_digit.many().concat().map(int)
direction = string('R').result(1) | string('L').result(-1)
route_el = seq(direction, number).map(tuple)
route_parse = route_el.many()


def parse_input(input_str: str):
    map_str, route = tuple(input_str.split('\n\n'))
    map_obj = gen_map(map_str)
    return map_obj, route_parse.parse('R' + route.strip())


def walk_route_el(map_obj: Map, coord: Coord, facing: int, steps: int, dir_change: int) \
        -> Tuple[Coord, int]:
    facing = (facing + dir_change) % 4
    for i in range(steps):
        dest = map_obj.get_step_dest(coord, facing)
        if dest is None:
            break
        coord = dest
    return coord, facing


def walk_route(map_obj: Map, route: List[Tuple[int, int]]) -> Tuple[Coord, int]:
    coord = map_obj.get_step_dest((1, 1), 0)
    facing = 3
    for dir_change, steps in route:
        coord, facing = walk_route_el(map_obj, coord, facing, steps, dir_change)
    return coord, facing


def walk_cube_route_el(map_obj: CubeMap, coord: Coord, facing: int, steps: int, dir_change: int) \
        -> Tuple[Coord, int]:
    facing = (facing + dir_change) % 4
    for i in range(steps):
        new_coord, new_facing = map_obj.get_step_dest(coord, facing)
        if not map_obj.map_dict[new_coord]:  # there is a wall there
            break
        coord, facing = new_coord, new_facing
    return coord, facing


def walk_cube_route(map_obj: CubeMap, route: List[Tuple[int, int]]) -> Tuple[Coord, int]:
    coord = get_top_left_dict(map_obj.side_len)[4]
    facing = 3
    for dir_change, steps in route:
        coord, facing = walk_cube_route_el(map_obj, coord, facing, steps, dir_change)
    return coord, facing


def get_password(coord: Coord, facing: int):
    return 1000 * coord[0] + 4 * coord[1] + facing


def test_cube_with(the_test_input):
    the_input, side_len, password = the_test_input
    map_obj, route = parse_input(the_input)
    cube_map = morph_cube_map(map_obj.map_dict, side_len)
    dest, facing = walk_cube_route(cube_map, route)
    assert(cube_map.get_password(dest, facing) == password)


def main():
    test_cube_with(test_input3)
    test_cube_with(test_input4)
    test_cube_with(test_input5)
    test_cube_with(test_input)
    test_cube_with(test_input6)
    with open('input/day22_input.txt') as f:
        file_input = f.read(), 50
    the_input, the_side_len = file_input
    map_obj, route = parse_input(the_input)
    print(get_password(*walk_route(map_obj, route)))
    print(str(map_obj))
    cube_map = morph_cube_map(map_obj.map_dict, the_side_len)
    print(str(cube_map))
    dest, facing = walk_cube_route(cube_map, route)
    print(cube_map.get_password(dest, facing))
    # manually correct for facing dest


if __name__ == '__main__':
    main()
