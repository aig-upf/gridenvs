
from gridenvs.env import GridEnv
from gridenvs.world import GridWorld, GridObject
from gridenvs.utils import Direction, Point
import numpy as np

class HeroEnv(GridEnv):
    """
    Abstract class for environments with a single agent (hero) that can be moved around the grid
    """
    ACTION_MAP = [None, ] + Direction.cardinal() # Default actions: Noop, north, east, south west.
    STATE_MAP = dict()       # Description of the state machine. TODO: describe
    BLOCKS = set()           # Names of objects that cannot be trespassed by the hero

    def __init__(self, max_moves=None, pixel_size=(84,84)):
        GridEnv.__init__(self, len(self.ACTION_MAP), pixel_size)
        self.state['done'] = True
        self.max_moves = max_moves
        assert self.max_moves is None or self.max_moves > 0

    def reset(self):
        self.state['hero'] = self.reset_world()
        assert self.state['hero'] is not None, "Reset world should return hero object."
        self.state['state_id'] = 0
        self.state['moves'] = 0
        self.state['done'] = False
        return self.generate_observation(self.state["world"])

    def move(self, obj, direction):
        if direction:
            dx, dy = direction.value
            bb = obj.bounding_box
            if bb[0].x + dx >= 0 and bb[1].x + dx <= self.state["world"].grid_size.x and bb[0].y + dy >= 0 and bb[1].y + dy <= self.state["world"].grid_size.y:
                others = self.state["world"].collisions(obj, direction)
                if dx != 0 and dy != 0:
                    # diagonal move, also check cardinal positions before trying to move diagonally
                    others.extend(self.state["world"].collisions(obj, Direction(Point(dx, 0))))
                    others.extend(self.state["world"].collisions(obj, Direction(Point(0, dy)))) #we may have repeated objects

                for other in others:
                    if other.name in self.BLOCKS:
                        return False
                obj.pos += (dx, dy)
            else:
                return False
        return True

    def move_hero(self, direction):
        return self.move(self.state['hero'], direction)

    def update_environment(self, action):
        assert not self.state['done'], "The environment needs to be reset."
        if np.issubdtype(type(action), np.integer):
            if action >= len(self.ACTION_MAP):
                raise Exception("Action index %s not in ACTION_MAP." % action)
            else:
                action = self.ACTION_MAP[action]
        else:
            if action not in self.ACTION_MAP:
                raise Exception("Action %s not in ACTION_MAP. ACTION_MAP: %s" % (action, str(self.ACTION_MAP)))

        self.move_hero(action)
        self.state['moves'] += 1
        r, self.state['done'], info_dict = self.update_world()
        return r, self.state['done'], info_dict

    def update_world(self):
        reward = 0.
        end_episode = False
        collisions = self.state["world"].collisions(self.state['hero'])
        for collision in collisions:
            try:
                # TODO: use neighbors instead of collisions
                # state, collision_name -> new_state, reward, end_of_episode, collision_fn
                self.state['state_id'], reward, end_episode, state_change_fn = self.STATE_MAP[(self.state['state_id'], collision.name)]
                if state_change_fn: state_change_fn(self.state["world"], collision)
            except KeyError:
                # if the pair (state, collision_name) does not exist -> new_state = state, reward = 0, end_of_episode = False, fn world, collision_obj = lambda:None
                pass

        if self.max_moves is not None and self.state['moves'] >= self.max_moves:
            end_episode = True
        info = {
            'state_id': self.state['state_id']
        }
        info.update({'position': self.state['hero'].pos}) # This position information should only be used by the QAgent
        return reward, end_episode, info

    def create_world(self):
        """
        Called at init.
        :return: the world (GridworldMap object)
        """
        raise NotImplementedError()

    def reset_world(self):
        """
        Called at every reset().
        :return: the hero (GameObject).
        """
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
    return hero, world

def get_StrHeroEnv(str_map, colors, hero_mark, state_map=None, action_map=None, blocks=None, cls=HeroEnv):
    """
    Will define functions create_world and reset_world so that the string map is read only once
    """
    from copy import deepcopy
    assert issubclass(cls, HeroEnv)
    class StrHeroEnv(cls):
        if state_map: STATE_MAP = state_map
        if blocks: BLOCKS = blocks
        if action_map: ACTION_MAP = action_map

        def create_world(self):
            _, self.init_state_world = create_world_from_string_map(str_map, colors, hero_mark)
            return deepcopy(self.init_state_world)

        def reset_world(self):
            self.state["world"] = deepcopy(self.init_state_world)
            hero = self.state["world"].get_objects_by_names(hero_mark)[0]
            return hero
    return StrHeroEnv
