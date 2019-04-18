from gridenvs.utils import Color, Direction
from gridenvs.hero import HeroEnv, create_world_from_string_map


class KeyDoorEnv(HeroEnv):
    def __init__(self, str_map, key_reward=False, blocking_walls=False, **kwargs):
        self.str_map = str_map
        self.blocks = {'W'} if blocking_walls else {}
        self.key_reward = 1.0 if key_reward else 0.0
        super(KeyDoorEnv, self).__init__(**kwargs)

    def _state(self):
        colors = {'W': Color.gray, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black}
        gridworld, hero = create_world_from_string_map(self.str_map, colors, hero_mark='H')
        return {"world": gridworld,
                "hero": hero,
                "blocks": self.blocks,
                "has_key" : False}

    def _update(self):
        collisions = self.state["world"].collision(self.state['hero'], direction=None)  # check superposition of objs
        if len(collisions) > 0:
            assert len(collisions) == 1
            o = collisions[0]

            if o.name == 'W':
                return -1.0, True, {}
            elif o.name == 'D' and self.state["has_key"]:
                return 1.0, True, {}
            elif o.name == 'K':
                self.state["has_key"] = True
                self.state["world"].remove_object(o)
                return self.key_reward, False, {}
        return 0.0, False, {}


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
