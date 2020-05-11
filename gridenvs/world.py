import numpy as np
import cv2
from collections import defaultdict
from gridenvs.utils import Direction, Colors


check_collision = {
    #direction is taken from the point of reference of the first parameter (e.g. second parameter is South/North/... of first parameter)
    #direction = None checks superposition
    None: lambda p1, p2: p1[0] == p2[0] and p1[1] == p2[1],
    Direction.N: lambda p1, p2: p1[0] == p2[0] and p1[1]-1 == p2[1],
    Direction.S: lambda p1, p2: p1[0] == p2[0] and p1[1]+1 == p2[1],
    Direction.E: lambda p1, p2: p1[0]+1 == p2[0] and p1[1] == p2[1],
    Direction.W: lambda p1, p2: p1[0]-1 == p2[0] and p1[1] == p2[1],
    Direction.NE: lambda p1, p2: p1[0]+1 == p2[0] and p1[1]-1 == p2[1],
    Direction.SE: lambda p1, p2: p1[0]+1 == p2[0] and p1[1]+1 == p2[1],
    Direction.NW: lambda p1, p2: p1[0]-1 == p2[0] and p1[1]-1 == p2[1],
    Direction.SW: lambda p1, p2: p1[0]-1 == p2[0] and p1[1]+1 == p2[1],
}

from collections import namedtuple
GridObject = namedtuple("GridObject", ['name', 'pos', 'rgb', 'render_preference'])
GridObject.__new__.__defaults__ = (0,)  # namedtuple can handle defaults from Python 3.7, this is for backwards compatibility


def get_render_ordered_objects(objects):
    return sorted(objects, key=lambda a: a.render_preference)


class GridWorld:
    def __init__(self, size):
        try:
            size_x, size_y = size
        except TypeError:
            size_x = size_y = size
        self.size = (size_x, size_y)

    def get_colors(self, objects):
        grid = np.array([["0x000000"] * self.size[0]] * self.size[1])
        for obj in get_render_ordered_objects(objects):
            grid[obj.pos[1]][obj.pos[0]] = Colors.rgb_to_hex(obj.rgb)
        return grid

    def get_char_matrix(self, objects):
        grid = np.array([['·'] * self.size[0]] * self.size[1])
        for obj in get_render_ordered_objects(objects):
            grid[obj.pos[1]][obj.pos[0]] = obj.name[0].capitalize()
        return grid

    def get_objects_by_position(self, objects):
        res = defaultdict(list)
        for obj in objects:
            res[obj.pos].append(obj)
        return dict(res)

    def get_objects_by_names(self, objects, name_or_names):
        if type(name_or_names) is str:
            name_or_names = (name_or_names,)
        return [o for o in objects if o.name in name_or_names]

    def collision(self, obj, objects, direction=None):
        # if direction is None, it checks superposition of objects
        return [o for o in objects if obj is not o and check_collision[direction](obj.pos, o.pos)]

    def render(self, objects, size=None):
        grid = np.zeros([self.size[1], self.size[0], 3], dtype=np.uint8)
        for obj in get_render_ordered_objects(objects):
            grid[obj.pos[1]][obj.pos[0]] = obj.rgb

        if size: grid = cv2.resize(grid, size, interpolation=cv2.INTER_AREA)
        return grid
