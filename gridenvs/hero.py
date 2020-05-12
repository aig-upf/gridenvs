import numpy as np
from gridenvs.env import GridEnv
from gridenvs.world import GridWorld, GridObject
from gridenvs.utils import Direction


class HeroEnv(GridEnv):
    """
    Abstract class for environments with a single agent (hero) that moves around the grid
    """
    def __init__(self, size, actions=[None,]+Direction.cardinal(), block_names=[], max_moves=None, **kwargs):
        super(HeroEnv, self).__init__(size=size, n_actions=len(actions), max_moves=max_moves, **kwargs)
        self.actions = actions
        self.block_names = block_names

    def get_init_state(self):
        state = self._init_state()
        assert all(k in state.keys() for k in ['hero', 'other_objects'])
        return state

    def get_next_state(self, state, action):
        if np.issubdtype(type(action), np.integer):
            assert action < len(self.actions), f"Action index {action} exceeds the number of actions ({len(self.actions)})."
            action = self.actions[action]
        else:
            assert action in self.actions, f"Action {action} not in actions list. Possible actions: {self.actions}"

        next_state, r, done, info = self._next_state(state, action)
        info.update({'position': next_state['hero'].pos})
        return next_state, r, done, info

    def get_objects_to_render(self, state):
        return [state["hero"]] + list(state["other_objects"])

    def move(self, obj, direction, check_collision_objects):
        if direction is not None:
            dx, dy = direction.value
            if obj.pos[0] + dx >= 0 and obj.pos[0] + dx < self.world.size[0] \
                    and obj.pos[1] + dy >= 0 and obj.pos[1] + dy < self.world.size[1]:
                others = self.world.collision(obj, check_collision_objects, direction)
                if dx != 0 and dy != 0:
                    # diagonal move, also check cardinal positions before trying to move diagonally
                    others.extend(self.world.collision(obj, check_collision_objects, Direction((dx, 0))))
                    others.extend(self.world.collision(obj, check_collision_objects, Direction((0, dy))))  # we may have repeated objects

                for other in others:
                    if other.name in self.block_names:
                        return obj
                return obj._replace(pos=(obj.pos[0]+dx, obj.pos[1]+dy))
        return obj

    def _init_state(self):
        raise NotImplementedError

    def _next_state(self, state, action):
        raise NotImplementedError


def create_world_from_string_map(str_map, colors, hero_mark):
    hero = None
    other_objects = []
    for y, string in enumerate(str_map):
        for x, point in enumerate(string):
            if point == '.':
                continue
            else:
                obj_name = str_map[y][x]
                assert obj_name in colors.keys(), "Please define a color for object %s"%obj_name
                color = colors[obj_name]

                render_preference = 1 if point == hero_mark else 0
                o = GridObject(name=point, pos=(x, y), rgb=color, render_preference=render_preference)
                if point == hero_mark:
                    assert hero is None
                    hero = o
                else:
                    other_objects.append(o)

    assert hero is not None, "Hero could not be loaded. Hero mark not in string map?"
    return hero, tuple(other_objects)


class StrHeroEnv(HeroEnv):
    def __init__(self, str_map, colors, hero_mark, actions=[None,]+Direction.cardinal(), block_marks={}, max_moves=200, pixel_size=(84,84)):
        self.str_map = str_map
        self.colors = colors
        self.hero_mark = hero_mark
        self.block_marks = block_marks
        super(StrHeroEnv, self).__init__(size=(len(str_map[0]), len(str_map)),
                                         actions=actions,
                                         max_moves=max_moves,
                                         pixel_size=pixel_size)

    def _init_state(self):
        hero, other_objects = create_world_from_string_map(self.str_map, self.colors, self.hero_mark)
        return {"hero": hero, "other_objects": other_objects}

    def _next_state(self, state, action):
        hero = self.move(state["hero"], action, check_collision_objects=state["other_objects"])
        return {"hero": hero, "other_objects": state["other_objects"]}