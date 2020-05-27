from gridenvs.utils import Color, Direction
from gridenvs.hero import HeroEnv, create_world_from_string_map


class KeyDoorEnv(HeroEnv):
    color1 = {'W': Color.gray, 'D': Color.green, 'K': Color.yellow, 'H': Color.blue, '.': Color.black, 'L': Color.red}
    color2 = {'W': Color.gray, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black, 'T': Color.yellow}
    color3 = {'W': Color.blue, 'D': Color.red, 'K': Color.green, 'H': Color.gray, '.': Color.green}

    def __init__(self, str_map, key_reward=False, blocking_walls=False, color = color1, total_number_of_keys=None, **kwargs):
        self.str_map = str_map
        self.blocking_walls = blocking_walls
        self.key_reward = 1.0 if key_reward else 0.0
        self.colors = color
        self.total_number_of_keys = total_number_of_keys
        self.number_of_keys_collected = 0
        self.collect_keys_env_option = False
        super(KeyDoorEnv, self).__init__(**kwargs)

    def _state(self):
        gridworld, hero = create_world_from_string_map(self.str_map, self.colors, hero_mark='H')
        if self.blocking_walls:
            blocks = gridworld.get_objects_by_names(['W'])
        else:
            blocks = []
        return {"world": gridworld,
                "hero": hero,
                "blocks": blocks,
                "has_key" : False}

    def _update(self):
        collisions = self.state["world"].collision(self.state['hero'], direction=None)  # check superposition of objs
        if len(collisions) > 0:
            assert len(collisions) == 1
            o = collisions[0]

            if o.name == 'W':
                self.number_of_keys_collected = 0
                return 0, True, {}

            elif o.name == 'L':
                self.number_of_keys_collected = 0
                return 0, True, {}

            elif o.name == 'D' and self.state["has_key"] and self.total_number_of_keys is None:
                self.number_of_keys_collected = 0
                self.state["world"].remove_object(o)
                return 1.0, False, {}

            elif o.name == 'T':
                return 1.0, True, {}

            elif o.name == 'K':
                self.state["has_key"] = True
                self.state["world"].remove_object(o)
                self.number_of_keys_collected += 1

                if self.total_number_of_keys is not None:
                    if self.number_of_keys_collected == self.total_number_of_keys:
                        self.number_of_keys_collected = 0
                        return self.key_reward, True, {}
                    else:
                        return self.key_reward, False, {}

                else:
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


def mazeXL0(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "W......W......W........W.....W",
                "W......W......W........W.....W",
                "W......W......W........W.....W",
                "W...H........................W",
                "W............................W",
                "W.............W..............W",
                "W.............W........W.....W",
                "WWW..WWWW...WWWWWWWWWWWW....WW",
                "W.............W..............W",
                "W.............W..............W",
                "W.............W.......D......W",
                "W.............W..............W",
                "W.............W..............W",
                "WWWWWWWWWW...WWWWWWWWWWWWWWWWW",
                "W.................W..........W",
                "W.................W..........W",
                "W............................W",
                "W......W.....................W",
                "W......W.....................W",
                "W.................W..........W",
                "W.............WWWWWWW...WWWWWW",
                "W......W......W..............W",
                "WWW..WWWWW..WWW..............W",
                "W.............W..............W",
                "W.............W..............W",
                "W.............W..............W",
                "W.............W.........K....W",
                "W.............W..............W",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
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

def maze8x8keyDoor1(**kwargs):
    init_map = ["WWWWWWWW",
                "WD....KW",
                "W......W",
                "W......W",
                "W......W",
                "W......W",
                "WH.....W",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze8x8keyDoor2(**kwargs):
    init_map = ["WWWWWWWW",
                "W.....DW",
                "W......W",
                "W......W",
                "W......W",
                "W......W",
                "WH....KW",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze8x8keyDoor3(**kwargs):
    init_map = ["WWWWWWWW",
                "WK.....W",
                "W......W",
                "W......W",
                "W......W",
                "W......W",
                "WH....DW",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze10x10(**kwargs):
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

def maze10x10key1(**kwargs):
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

def maze10x10key2(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD.......W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "WH......KW",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze10x10key3(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD.......W",
                "W........W",
                "W........W",
                "W.....K..W",
                "W........W",
                "W........W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze10x10keyDoor1(**kwargs):
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

def maze10x10keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWW",
                "W.......DW",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "WH......KW",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze10x10keyDoor3(**kwargs):
    init_map = ["WWWWWWWWWW",
                "W........W",
                "W........W",
                "W........W",
                "W.....K..W",
                "W........W",
                "W........W",
                "W........W",
                "WH......DW",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze10x10key1color1(**kwargs):
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

    return KeyDoorEnv(init_map, color = KeyDoorEnv.color1, **kwargs)

def maze10x10key2color2(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD.......W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "W........W",
                "WH......KW",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def maze10x10key3color3(**kwargs):
    init_map = ["WWWWWWWWWW",
                "WD.......W",
                "W........W",
                "W........W",
                "W.....K..W",
                "W........W",
                "W........W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color3, **kwargs)

def maze10x10pick_up_objects1color1(**kwargs):
    init_map = ["WWWWWWWWWW",
                "W........W",
                "W........W",
                "W.K....K.W",
                "W........W",
                "W........W",
                "W........W",
                "W.K....K.W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color1, total_number_of_keys=4, **kwargs)

def maze10x10pick_up_objects1color2(**kwargs):
    init_map = ["WWWWWWWWWW",
                "W........W",
                "W........W",
                "W.K....K.W",
                "W........W",
                "W........W",
                "W........W",
                "W.K....K.W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, total_number_of_keys=4, **kwargs)

def maze10x10pick_up_objects1color3(**kwargs):
    init_map = ["WWWWWWWWWW",
                "W........W",
                "W........W",
                "W.K....K.W",
                "W........W",
                "W........W",
                "W........W",
                "W.K....K.W",
                "WH.......W",
                "WWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color3, total_number_of_keys=4, **kwargs)

def maze18x18(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD..............KW",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze18x18key1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD..............KW",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze18x18key2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD...............W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH..............KW",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze18x18key3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD...............W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W...........K....W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze18x18keyDoor1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD..............KW",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze18x18keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "W...............DW",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH..............KW",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze18x18keyDoor3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W...........K....W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH..............DW",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze16x16keyDoor1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "WD............KW",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "WH.............W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze16x16keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W.............DW",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "WH............KW",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze16x16keyDoor3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "WK.............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "W..............W",
                "WH............DW",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def FourRoom8x8keyDoor1(**kwargs):
    init_map = ["WWWWWWWW",
                "WD.WW.KW",
                "W......W",
                "W.WWWW.W",
                "W.WWWW.W",
                "W......W",
                "WH.WW..W",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def FourRoom8x8keyDoor2(**kwargs):
    init_map = ["WWWWWWWW",
                "W..WW.DW",
                "W......W",
                "W.WWWW.W",
                "W.WWWW.W",
                "W......W",
                "WH.WW.KW",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def FourRoom8x8keyDoor3(**kwargs):
    init_map = ["WWWWWWWW",
                "WK.WW..W",
                "W......W",
                "W.WWWW.W",
                "W.WWWW.W",
                "W......W",
                "WH.WW.DW",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def FourRoom16x16keyDoor1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "WD.....WW.....KW",
                "W......WW......W",
                "W..............W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "WWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWW.WWW",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W..............W",
                "W......WW......W",
                "WH.....WW......W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def FourRoom16x16keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......WW.....DW",
                "W......WW......W",
                "W..............W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "WWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWW.WWW",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W..............W",
                "W......WW......W",
                "WH.....WW.....KW",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def FourRoom16x16keyDoor3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "WK.....WW......W",
                "W......WW......W",
                "W..............W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "WWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWW.WWW",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W..............W",
                "W......WW......W",
                "WH.....WW.....DW",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def Treasure16x16keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......WWT.....W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "WWW.WWWWWWWWWW.W",
                "WWW.WWWWWWWWWWDW",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W..............W",
                "W......WW......W",
                "WH.....WW.....KW",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Lava16x16keyDoor1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "WD............KW",
                "W..............W",
                "W......LL......W",
                "W......LL......W",
                "W.....LLLL.....W",
                "W....LLLLLL....W",
                "W..LLLLLLLLLL..W",
                "W..LLLLLLLLLL..W",
                "W....LLLLLL....W",
                "W.....LLLL.....W",
                "W......LL......W",
                "W......LL......W",
                "W..............W",
                "WH.............W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def Lava16x16keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W.............DW",
                "W..............W",
                "W......LL......W",
                "W......LL......W",
                "W.....LLLL.....W",
                "W....LLLLLL....W",
                "W..LLLLLLLLLL..W",
                "W..LLLLLLLLLL..W",
                "W....LLLLLL....W",
                "W.....LLLL.....W",
                "W......LL......W",
                "W......LL......W",
                "W..............W",
                "WH............KW",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def Lava16x16keyDoor3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "WK.............W",
                "W..............W",
                "W......LL......W",
                "W......LL......W",
                "W.....LLLL.....W",
                "W....LLLLLL....W",
                "W..LLLLLLLLLL..W",
                "W..LLLLLLLLLL..W",
                "W....LLLLLL....W",
                "W.....LLLL.....W",
                "W......LL......W",
                "W......LL......W",
                "W..............W",
                "WH............DW",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def EightRoom32x32keyDoor1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "WD.....WW......WW......WW.....KW",
                "W......WW......WW......WW......W",
                "W..............................W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "WWW.WWWWWWWW.WWWWWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWW.WWWWWW.WWWWWWWW.WWW",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W..............................W",
                "W......WW......WW......WW......W",
                "WH.....WW......WW......WW......W",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def EightRoom32x32keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "W......WW......WW......WW.....DW",
                "W......WW......WW......WW......W",
                "W..............................W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "WWW.WWWWWWWW.WWWWWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWW.WWWWWW.WWWWWWWW.WWW",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W..............................W",
                "W......WW......WW......WW......W",
                "WH.....WW......WW......WW.....KW",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def EightRoom32x32keyDoor3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "WK.....WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W..............................W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "WWW.WWWWWWWW.WWWWWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWW.WWWWWW.WWWWWWWW.WWW",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W......WW......WW......WW......W",
                "W..............................W",
                "W......WW......WW......WW......W",
                "WH.....WW......WW......WW.....DW",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)

def maze18x18key1color1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD..............KW",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color1,  **kwargs)

def maze18x18key2color2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD...............W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH..............KW",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def maze18x18key3color3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "WD...............W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W...........K....W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color3, **kwargs)

def maze18x18pick_up_objects1color1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "W................W",
                "W................W",
                "W..K..........K..W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W..K..........K..W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color1, total_number_of_keys=4, **kwargs)

def maze18x18pick_up_objects1color2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "W................W",
                "W................W",
                "W..K..........K..W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W..K..........K..W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, total_number_of_keys=4, **kwargs)

def maze18x18pick_up_objects1color3(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWW",
                "W................W",
                "W................W",
                "W..K..........K..W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W................W",
                "W..K..........K..W",
                "W................W",
                "W................W",
                "WH...............W",
                "WWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color3, total_number_of_keys=4, **kwargs)

def maze30x30(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "WD..........................KW",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "W............................W",
                "WH...........................W",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, **kwargs)
