
from gridenvs.env import GridEnv
from gridenvs.world import GridWorld, GridObject
from gridenvs.utils import Direction, Point


class HeroEnv(GridEnv):
    """
    Abstract class for environments with a single agent (hero) that can be moved around the grid
    """
    def __init__(self, actions=[None,]+Direction.cardinal(), max_moves=None, **kwargs):
        super(HeroEnv, self).__init__(actions, **kwargs)
        self.max_moves = max_moves
        assert self.max_moves is None or self.max_moves > 0

    def new_state(self):
        state = self._state()
        assert all(k in state.keys() for k in ['world', 'hero'])
        state.update({'moves': 0})
        return state

    def update_environment(self, action):
        self.move_hero(action)
        r, done, info = self._update()
        self.state['moves'] += 1
        if self.max_moves is not None and self.state['moves'] >= self.max_moves:
            done = True
        info.update({'position': self.state['hero'].pos})
        return r, done, info

    def move(self, obj, direction):
        if direction:
            dx, dy = direction.value
            bb = obj.bounding_box
            if bb[0].x + dx >= 0 and bb[1].x + dx <= self.state["world"].grid_size.x \
                    and bb[0].y + dy >= 0 and bb[1].y + dy <= self.state["world"].grid_size.y:  # TODO: change to point operations
                others = self.state["world"].collision(obj, direction)
                if dx != 0 and dy != 0:
                    # diagonal move, also check cardinal positions before trying to move diagonally
                    others.extend(self.state["world"].collision(obj, Direction(Point(dx, 0))))
                    others.extend(self.state["world"].collision(obj, Direction(Point(0, dy))))  # we may have repeated objects

                if "blocks" in self.state.keys():
                    for other in others:
                        if other in self.state["blocks"]:
                            return False
                obj.pos += (dx, dy)
            else:
                return False
        return True

    def move_hero(self, direction):
        return self.move(self.state['hero'], direction)

    def _state(self):
        raise NotImplementedError

    def _update(self):
        raise NotImplementedError


def create_world_from_string_map(str_map, colors, hero_mark):
    world = GridWorld((len(str_map[0]), len(str_map)))

    hero = None
    for y, string in enumerate(str_map):
        for x, point in enumerate(string):
            if point == '.':
                continue
            else:
                obj_name = str_map[y][x]
                assert obj_name in colors.keys(), "Please define a color for object %s"%obj_name
                color = colors[obj_name]

                o = GridObject(name=point, pos=(x, y), rgb=color)
                if point == hero_mark:
                    o.render_preference = 1
                    hero = o
                world.add_object(o)

    assert hero is not None, "Hero could not be loaded. Hero mark not in string map?"
    return world, hero


class StrHeroEnv(HeroEnv):
    def __init__(self, str_map, colors, hero_mark, actions=[None,]+Direction.cardinal(), block_marks={}, max_moves=200, pixel_size=(84,84)):
        self.str_map = str_map
        self.colors = colors
        self.hero_mark = hero_mark
        self.block_marks = block_marks
        super(StrHeroEnv, self).__init__(actions, max_moves, pixel_size)

    def _state(self):
        gridworld, hero = create_world_from_string_map(self.str_map, self.colors, self.hero_mark)
        blocks = gridworld.get_objects_by_names(list(self.block_marks))
        return {"world": gridworld, "hero": hero, "blocks": blocks }