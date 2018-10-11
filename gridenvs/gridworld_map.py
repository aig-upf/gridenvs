"""
    This file captures all the map logic and representation.
"""
import numpy as np
from collections import defaultdict
from gridenvs.utils import Point, Direction

check_collision = {
    #direction is taken from the point of reference of the first parameter (e.g. second parameter is South/North/... of first parameter)
    #direction = None checks superposition
    None: lambda obj_bb, other_bb: obj_bb[0].x < other_bb[1].x and obj_bb[1].x > other_bb[0].x and obj_bb[0].y < other_bb[1].y and obj_bb[1].y > other_bb[0].y,
    Direction.N: lambda obj_bb, other_bb: obj_bb[0].y == other_bb[1].y and obj_bb[0].x < other_bb[1].x and obj_bb[1].x > other_bb[0].x,
    Direction.S: lambda obj_bb, other_bb: obj_bb[1].y == other_bb[0].y and obj_bb[0].x < other_bb[1].x and obj_bb[1].x > other_bb[0].x,
    Direction.E: lambda obj_bb, other_bb: obj_bb[1].x == other_bb[0].x and obj_bb[0].y < other_bb[1].y and obj_bb[1].y > other_bb[0].y,
    Direction.W: lambda obj_bb, other_bb: obj_bb[0].x == other_bb[1].x and obj_bb[0].y < other_bb[1].y and obj_bb[1].y > other_bb[0].y,
    Direction.NE: lambda obj_bb, other_bb: obj_bb[0].y <= other_bb[1].y and obj_bb[1].x >= other_bb[0].x and obj_bb[0].y > other_bb[0].y and obj_bb[1].x < other_bb[1].x,
    Direction.SE: lambda obj_bb, other_bb: obj_bb[1].y >= other_bb[0].y and obj_bb[1].x >= other_bb[0].x and obj_bb[1].y < other_bb[1].y and obj_bb[1].x < other_bb[1].x,
    Direction.NW: lambda obj_bb, other_bb: obj_bb[0].y <= other_bb[1].y and obj_bb[0].x <= other_bb[1].x and obj_bb[0].y > other_bb[0].y and obj_bb[0].x > other_bb[0].x,
    Direction.SW: lambda obj_bb, other_bb: obj_bb[1].y >= other_bb[0].y and obj_bb[0].x <= other_bb[1].x and obj_bb[1].y < other_bb[1].y and obj_bb[0].x > other_bb[0].x,
}

class GameObject:
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

class GameObjectGroup(GameObject):
    def __init__(self, name, objects, pos, render_preference=0):
        """
        It takes a list of objects and groups them together. The position of the group object is given by the pos
        parameter. The positions of all objects of the groupneed to be relative to this position: e.g. if group obj has
        position (1,3), an object of this group with position (2,4) will be rendered at grid position (3,7). Render
        preferences of objects of a group will only be taken into account if two objects are at the same position.
        :param name:
        :param objects:
        :param pos:
        :param render_preference:
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

class GridworldMap:
    def __init__(self, grid_size):
        try:
            size_x, size_y = grid_size
        except TypeError:
            size_x = size_y = grid_size
        self.grid_size = Point(size_x, size_y)
        self.reset()

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
        """
        :return: reference to object
        """
        self.objects.append(game_object)
        return game_object

    def remove_object(self, obj):
        self.objects.remove(obj)

    def reset(self):
        self.objects = []

    def get_objects_by_position(self):
        res = defaultdict(list)
        for obj in self.objects:
            res[obj.pos].append(obj)
        return dict(res)

    def get_objects_by_names(name_or_names, objects):
        """
        :param names: Single name or list / tuple
        :return:
        """
        if type(name_or_names) is str:
            name_or_names = (name_or_names,)
        return [o for o in objects if o.name in name_or_names]

    def collisions(self, obj:GameObject, direction=None, objects=None, return_names=False):
        """

        :param obj:
        :param direction: None (check superposition of objects) or Direction
        :param objects: None (all objects) or iterable of GameObjects or their names (strings)
        :return: list of objects that are neighbors with obj at the specified direction
        """
        if objects is None:
            objects = self.objects # With all objects

        neighbor_objs = []
        if len(objects) > 0:
            if type(objects[0]) is str:
                objects = self.get_objects_by_names(objects, self.objects)
            for other in objects:
                if obj.collides_with(other, direction):
                    neighbor_objs.append(other)

        if return_names:
            neighbor_objs = list(set([obj.name for obj in neighbor_objs]))
        return neighbor_objs

    def all_collisions(self, obj:GameObject, objects=None, return_names=False):
        if objects is None:
            objects = self.objects # With all objects

        neighbor_objs = dict([(d, []) for d in Direction.all() + [None]])
        if len(objects) > 0:
            if type(objects[0]) is str:
                objects = self.get_objects_by_names(objects, self.objects)

            for direction in Direction.all()+[None]:
                for other in objects:
                    if obj.collides_with(other, direction):
                        neighbor_objs[direction].append(other)

        if return_names:
            for d in neighbor_objs.keys():
                neighbor_objs[d] = list(set([obj.name for obj in neighbor_objs[d]]))
        return neighbor_objs

    def render(self):
        grid = np.zeros([self.grid_size.y, self.grid_size.x, 3], dtype=np.uint8)
        for obj in get_render_ordered_objects(self.objects):
            grid = obj.render_rgb(grid)
        return grid