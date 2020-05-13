from gridenvs.utils import Colors, Direction
from gridenvs.hero import HeroEnv, create_world_from_string_map


class KeyDoorEnv(HeroEnv):
    def __init__(self,
                 str_map,
                 colors = {'W': Colors.gray, 'D': Colors.green, 'K': Colors.red, 'H': Colors.blue, '.': Colors.black},
                 key_reward=False,
                 blocking_walls=False,
                 **kwargs):
        self.str_map = str_map
        self.colors = colors
        self.key_reward = 1.0 if key_reward else 0.0
        block_names = ['W'] if blocking_walls else []
        super(KeyDoorEnv, self).__init__(size=(len(str_map[0]), len(str_map)),
                                         block_names=block_names,
                                         using_immutable_states=True,  # To speed up clone/restore states when planning
                                         fixed_init_state=True,
                                         **kwargs)

    def get_init_state(self):
        hero, other_objects = create_world_from_string_map(self.str_map, self.colors, hero_mark='H')
        return {"hero": hero,
                "other_objects": other_objects,
                "has_key": False}

    def _next_state(self, state, direction):
        hero = self.move(state['hero'], direction, check_collision_objects=state["other_objects"])
        new_state = {'hero': hero, 'other_objects': state['other_objects'], 'has_key': state['has_key']}
        collisions = self.world.collision(hero, state["other_objects"], direction=None)  # check superposition of objs
        for o in collisions:
            if o.name == 'W':
                return new_state, -1.0, True, {}
            elif o.name == 'D' and state["has_key"]:
                return new_state, 1.0, True, {}
            elif o.name == 'K':
                new_state = {'hero': hero,
                             'has_key': True,
                             'other_objects': tuple(obj for obj in state["other_objects"] if obj.name != 'K')}
                return new_state, self.key_reward, False, {}
        return new_state, 0.0, False, {}


def maze0(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD......KW",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)


def maze1(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD......KW",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W..WWWW..W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)


def maze2(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD......KW",
                "W........W",
                "W.....WWWW",
                "W........W",
                "W........W",
                "W..WWWW..W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)


def maze3(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD.W....KW",
                "W..W.....W",
                "W..W..WWWW",
                "W........W",
                "W........W",
                "W..WWWW..W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)


def mazeR(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD.......W",
                "W........W",
                "W..WWWW..W",
                "W..W.....W",
                "W..WK....W",
                "W..WWWW..W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)


def mazeL(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD.......W",
                "W........W",
                "W..WWWW..W",
                "W.....W..W",
                "W....KW..W",
                "W..WWWW..W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)


def corridor(**kwargs):
    init_map = ["..........",
                "..........",
                "..........",
                "WWWWWWWWWW",
                "WDH.....KW",
                "WWWWWWWWWW",
                "..........",
                "..........",
                "..........",
                ".........."]
    return KeyDoorEnv(init_map,
                      blocking_walls=True,
                      actions=[Direction.W, Direction.E],
                      **kwargs)


def mazeXL0(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "W......W......W........W.......W",
                "W......W......W........W.......W",
                "W......W......W........W.......W",
                "W...H..........................W",
                "W..............................W",
                "W.............W................W",
                "W.............W........W.......W",
                "WWW..WWWW...WWWWWWWWWWWW......WW",
                "W.............W................W",
                "W.............W................W",
                "W.............W.......D........W",
                "W.............W................W",
                "W.............W................W",
                "WWWWWWWWWW...WWWWWWWWWWWWWWWWWWW",
                "W.................W............W",
                "W.................W............W",
                "W..............................W",
                "W......W.......................W",
                "W......W.......................W",
                "W.................W............W",
                "W.............WWWWWWW...WWWWWWWW",
                "W......W......W................W",
                "WWW..WWWWW..WWW................W",
                "W.............W................W",
                "W.............W................W",
                "W.............W................W",
                "W.............W.........K......W",
                "W.............W................W",
                "W.............W................W",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)


def mazeXL1(**kwargs):

    init_map = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "W......W......W........W.......W",
                "W......W......W........W.......W",
                "W......W......W........W.......W",
                "W...H..........................W",
                "W..............................W",
                "W.............W................W",
                "WWW..WWWW...WWWWWWWWWWWW......WW",
                "W.............W................W",
                "W.............W................W",
                "W.............W.......D........W",
                "W.............W................W",
                "W.............W................W",
                "W.............W................W",
                "W.............W................W",
                "WWWWWWWWWW...WWWWWWWWWWWWWWWWWWW",
                "W.................W............W",
                "W.................W............W",
                "W..............................W",
                "W......W.......................W",
                "W......W.......................W",
                "W.................W............W",
                "W..............................W",
                "WWW..WWWWW..WWWWWWWWW...WWWWWWWW",
                "W......W......W................W",
                "W.............W................W",
                "W.............W................W",
                "W.............W................W",
                "W.............W.........K......W",
                "W.............W................W",
                "W.............W................W",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]

    return KeyDoorEnv(init_map, **kwargs)
