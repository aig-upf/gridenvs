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

# from collections import namedtuple
# GridObject = namedtuple("GridObject", ['name', 'pos', 'rgb', 'render_preference'])
# GridObject.__new__.__defaults__=((0,0,255), 0)

class GridObject:
    def __init__(self, name, pos, rgb=(255,0,0), render_preference=0):
        """
        :param name:
        :param pos: (x, y)
        :param rgb: (r, g, b) 0 to 255
        :param render_preference: Bigger number will be rendered latter than others
        """
        self.pos = pos
        self.rgb = rgb
        self.name = name
        self.render_preference = render_preference


def collides_with(obj, other, direction=None):
    return other is not obj and check_collision[direction](obj.pos, other.pos)


def get_render_ordered_objects(objects):
    return sorted(objects, key=lambda a: a.render_preference)


class GridWorld:
    def __init__(self, grid_size):
        try:
            size_x, size_y = grid_size
        except TypeError:
            size_x = size_y = grid_size
        self.grid_size = (size_x, size_y)
        self.objects = []

    def get_colors(self):
        grid = np.array([["0x000000"] * self.grid_size[0]] * self.grid_size[1])
        for obj in self.objects:
            grid[obj.pos[1]][obj.pos[0]] = Colors.rgb_to_hex(obj.rgb)
        return grid

    def get_char_matrix(self):
        grid = np.array([['·'] * self.grid_size[0]] * self.grid_size[1])
        for obj in self.objects:
            grid[obj.pos[1]][obj.pos[0]] = obj.name[0].capitalize()
        return grid

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.get_char_matrix()])

    def __repr__(self):
        return self.__str__()

    def add_object(self, game_object):
        self.objects.append(game_object)
        return game_object

    def remove_object(self, obj):
        self.objects.remove(obj)

    def get_objects_by_position(self):
        res = defaultdict(list)
        for obj in self.objects:
            res[obj.pos].append(obj)
        return dict(res)

    def get_objects_by_names(self, name_or_names):
        if type(name_or_names) is str:
            name_or_names = (name_or_names,)
        return [o for o in self.objects if o.name in name_or_names]

    def collision(self, obj:GridObject, direction=None):
        # if direction is None, it checks superposition of objects
        return [o for o in self.objects if collides_with(obj, o, direction)]

    def render(self, size=None):
        grid = np.zeros([self.grid_size[1], self.grid_size[0], 3], dtype=np.uint8)
        for obj in get_render_ordered_objects(self.objects):
            grid[obj.pos[1]][obj.pos[0]] = obj.rgb

        if size: grid = cv2.resize(grid, size, interpolation=cv2.INTER_AREA)
        return grid
