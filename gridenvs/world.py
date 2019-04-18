
import numpy as np
import cv2
from collections import defaultdict
from gridenvs.utils import Point, Direction


check_collision = {
    #direction is taken from the point of reference of the first parameter (e.g. second parameter is South/North/... of first parameter)
    #direction = None checks superposition
    None: lambda bb1, bb2: bb1[0].x < bb2[1].x and bb1[1].x > bb2[0].x and bb1[0].y < bb2[1].y and bb1[1].y > bb2[0].y,
    Direction.N: lambda bb1, bb2: bb1[0].y == bb2[1].y and bb1[0].x < bb2[1].x and bb1[1].x > bb2[0].x,
    Direction.S: lambda bb1, bb2: bb1[1].y == bb2[0].y and bb1[0].x < bb2[1].x and bb1[1].x > bb2[0].x,
    Direction.E: lambda bb1, bb2: bb1[1].x == bb2[0].x and bb1[0].y < bb2[1].y and bb1[1].y > bb2[0].y,
    Direction.W: lambda bb1, bb2: bb1[0].x == bb2[1].x and bb1[0].y < bb2[1].y and bb1[1].y > bb2[0].y,
    Direction.NE: lambda bb1, bb2: bb1[0].y <= bb2[1].y and bb1[1].x >= bb2[0].x and bb1[0].y > bb2[0].y and bb1[1].x < bb2[1].x,
    Direction.SE: lambda bb1, bb2: bb1[1].y >= bb2[0].y and bb1[1].x >= bb2[0].x and bb1[1].y < bb2[1].y and bb1[1].x < bb2[1].x,
    Direction.NW: lambda bb1, bb2: bb1[0].y <= bb2[1].y and bb1[0].x <= bb2[1].x and bb1[0].y > bb2[0].y and bb1[0].x > bb2[0].x,
    Direction.SW: lambda bb1, bb2: bb1[1].y >= bb2[0].y and bb1[0].x <= bb2[1].x and bb1[1].y < bb2[1].y and bb1[0].x > bb2[0].x,
}


class GridObject:
    def __init__(self, name, pos, rgb=(255,0,0), render_preference=0):
        """
        :param name:
        :param pos: (x, y)
        :param rgb: (r, g, b) 0 to 255
        :param render_preference: Bigger number will be rendered latter than others
        """

        self.pos = Point(pos)
        self.rgb = rgb
        self.name = name
        self.render_preference = render_preference

    @property
    def bounding_box(self):
        return (self.pos, self.pos+1)

    def collides_with(self, other, direction=None):
        return other is not self and check_collision[direction](self.bounding_box, other.bounding_box)

    def render_rgb(self, grid):
        grid[self.pos.y][self.pos.x] = self.rgb
        return grid

    def render_rgb_hex(self, grid):
        grid[self.pos.y][self.pos.x] = rgb_to_hex(self.rgb)
        return grid

    def render_char(self, grid):
        grid[self.pos.y][self.pos.x] = self.name[0].capitalize()
        return grid


class GridObjectGroup(GridObject):
    def __init__(self, name, objects, pos, render_preference=0):
        """
        It takes a list of objects and groups them together. The position of the group object is given by the pos
        parameter. The positions of all objects of the group need to be relative to this position: e.g. if group obj has
        position (1,3), an object of this group with position (2,4) will be rendered at grid position (3,7). Render
        preferences of objects of a group will only be taken into account if two objects are at the same position.
        """
        self.pos = Point(pos)
        self.name = name
        self.objects = objects
        self.render_preference = render_preference
        self.compute_bounding_box()

    def compute_bounding_box(self):
        self._bb_min = Point(self.objects[0].pos)
        self._bb_max = Point(self.objects[0].pos)
        for obj in self.objects[1:]:
            if obj.pos.x > self._bb_max.x:
                self._bb_max.x = obj.pos.x
            if obj.pos.x < self._bb_min.x:
                self._bb_min.x = obj.pos.x
            if obj.pos.y > self._bb_max.y:
                self._bb_max.y = obj.pos.y
            if obj.pos.y < self._bb_min.y:
                self._bb_min.y = obj.pos.y

    @property
    def bounding_box(self):
        return (self._bb_min + self.pos, self._bb_max + self.pos + 1)

    #TODO: be able to move objects of the group (recompute bounding box)

    def render_rgb(self, grid):
        for obj in get_render_ordered_objects(self.objects):
            grid[self.pos.y + obj.pos.y][self.pos.x + obj.pos.x] = obj.rgb
        return grid

    def render_rgb_hex(self, grid):
        for obj in get_render_ordered_objects(self.objects):
            grid[self.pos.y + obj.pos.y][self.pos.x + obj.pos.x] = rgb_to_hex(obj.rgb)
        return grid

    def render_char(self, grid):
        for obj in get_render_ordered_objects(self.objects):
            grid[self.pos.y + obj.pos.y][self.pos.x + obj.pos.x] = obj.name[0].capitalize()
        return grid


def rgb_to_hex(rgb):
    return "0x" + hex(rgb[0])[2:].zfill(2) + hex(rgb[1])[2:].zfill(2) + hex(rgb[2])[2:].zfill(2)


def get_render_ordered_objects(objects):
    return sorted(objects, key=lambda a: a.render_preference)


class GridWorld:
    def __init__(self, grid_size):
        try:
            size_x, size_y = grid_size
        except TypeError:
            size_x = size_y = grid_size
        self.grid_size = Point(size_x, size_y)
        self.objects = []

    def get_colors(self):
        grid = np.array([["0x000000"] * self.grid_size.y] * self.grid_size.x)
        for obj in self.objects:
            obj.render_rgb_hex(grid)
        return grid

    def get_char_matrix(self):
        grid = np.array([['·'] * self.grid_size.y] * self.grid_size.x)
        for obj in self.objects:
            obj.render_char(grid)
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
        return [o for o in self.objects if obj.collides_with(o, direction)]

    def render(self, size=None):
        grid = np.zeros([self.grid_size.y, self.grid_size.x, 3], dtype=np.uint8)
        for obj in get_render_ordered_objects(self.objects):
            grid = obj.render_rgb(grid)
        if size: grid = cv2.resize(grid, size, interpolation=cv2.INTER_NEAREST)
        return grid
