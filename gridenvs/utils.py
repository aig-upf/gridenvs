import numpy as np
from enum import Enum
from collections import OrderedDict


class Point(np.ndarray):
    def __new__(cls, x, y=None):
        if y is None:
            a = np.array(x, dtype=np.int)
            assert a.shape == (2,), "Create a Point with either two integers or a tuple-like structure of size 2 e.g. (1,2)"
        else:
            a = np.array([x, y], dtype=np.int)
        return super(Point, cls).__new__(cls, shape=(2,), dtype=np.int, buffer=a.data)

    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        return np.array_equal(self, other)

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    
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

    def opposite(self):
        return Direction(-self.value)

class Colors:
    # MORE COLORS IN https://web.njit.edu/~kevin/rgb.txt.html
    black = (0, 0, 0)
    white = (255, 255, 255)
    gray = (155, 155, 155)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    darkOrange = (255, 140, 0)
    blueViolet = (138, 43, 226)
    darkTurquoise = (0, 206, 209)

    # Colors from https://en.wikipedia.org/wiki/Help:Distinguishable_colors
    distinguishable = OrderedDict([("Amethyst", (240, 163, 255)),
                                   ("Blue", (0, 117, 220)),
                                   ("Caramel", (153, 63, 0)),
                                   ("Damson", (76, 0, 92)),
                                   ("Ebony", (25, 25, 25)),
                                   ("Forest", (0, 92, 49)),
                                   ("Green", (43, 206, 72)),
                                   ("Honeydew", (255, 204, 153)),
                                   ("Iron", (128, 128, 128)),
                                   ("Jade", (148, 255, 181)),
                                   ("Khaki", (143, 124, 0)),
                                   ("Lime", (157, 204, 0)),
                                   ("Mallow", (194, 0, 136)),
                                   ("Navy", (0, 51, 128)),
                                   ("Orpiment", (255, 164, 5)),
                                   ("Pink", (255, 168, 187)),
                                   ("Quagmire", (66, 102, 0)),
                                   ("Red", (255, 0, 16)),
                                   ("Sky", (94, 241, 242)),
                                   ("Turquoise", (0, 153, 143)),
                                   ("Uranium", (224, 255, 102)),
                                   ("Violet", (116, 10, 255)),
                                   ("Wine", (153, 0, 0)),
                                   ("Xanthin", (255, 255, 128)),
                                   ("Yellow", (255, 255, 0)),
                                   ("Zinnia", (255, 80, 5))])
