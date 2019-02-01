#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum

class Point:
    def __init__(self, x, y=None):
        if y is None:
            assert isinstance(x, (tuple, list, Point))
            self.x, self.y = x
        else:
            self.x = x
            self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return tuple.__hash__((self.x, self.y))

    def __eq__(self, p):
        return p.x == self.x and p.y == self.y

    @staticmethod
    def _get_xy_or_num(p):
        try:
            x,y = p
        except TypeError:
            x = y = p
        return x,y

    def __add__(self, p):
        x,y = self._get_xy_or_num(p)
        return Point(self.x + x, self.y + y)

    def __sub__(self, p):
        x, y = self._get_xy_or_num(p)
        return Point(self.x - x, self.y - y)

    def __truediv__(self, p):
        x, y = self._get_xy_or_num(p)
        return Point(self.x/x, self.y/y)

    def __floordiv__(self, p):
        x, y = self._get_xy_or_num(p)
        return Point(self.x // x, self.y // y)

    def __mod__(self, p):
        x, y = self._get_xy_or_num(p)
        return Point(self.x % x, self.y % y)
        

    def __mul__(self, p):
        x, y = self._get_xy_or_num(p)
        return Point(self.x*x, self.y*y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])
    
class Direction(Enum):
    #axis at top left, y is inverted
    N = Point(0,-1)
    NE = Point(1,-1)
    E = Point(1,0)
    SE = Point(1,1)
    S = Point(0,1)
    SW = Point(-1,1)
    W = Point(-1,0)
    NW = Point(-1,-1)

    @staticmethod
    def cardinal():
        return [Direction.N, Direction.E, Direction.S, Direction.W]

    @staticmethod
    def intermediate():
        return [Direction.NE, Direction.SE, Direction.SW, Direction.NW]

    @staticmethod
    def all_north():
        return [Direction.NW, Direction.N, Direction.NE]

    @staticmethod
    def all_south():
        return [Direction.SW, Direction.S, Direction.SE]

    @staticmethod
    def all_east():
        return [Direction.NE, Direction.E, Direction.SE]

    @staticmethod
    def all_west():
        return [Direction.NW, Direction.W, Direction.SW]

    @staticmethod
    def all():
        return list(Direction)

    @staticmethod
    def left_right():
        return [Direction.E, Direction.W]

    def opposite(self):
        return Direction(-self.value)

class Color:
    # MORE COLORS IN https://web.njit.edu/~kevin/rgb.txt.html
    red = (255, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    blue = (0, 0, 255)
    white = (155, 155, 155)
    darkOrange = (255, 140, 0)
    black = (0, 0, 0)
    blueViolet = (138, 43, 226)
    darkTurquoise = (0, 206, 209)
