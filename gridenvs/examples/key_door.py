from gridenvs.utils import Color, Direction
from gridenvs.hero import HeroEnv, create_world_from_string_map


class KeyDoorEnv(HeroEnv):
    color1 = {'W': Color.gray, 'D': Color.green, 'K': Color.yellow, 'H': Color.blue, '.': Color.black, 'L': Color.red}
    color2 = {'W': Color.gray, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black, 'T': Color.yellow, 'L': Color.red}
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

    def move_hero(self, direction):
        collisions = self.state["world"].collision(self.state['hero'], direction=direction)
        if len(collisions) > 0:
            o = collisions[0]
            if 'D' == o.name and not self.state["has_key"]:
                return False

        return self.move(self.state['hero'], direction)

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


def Treasure16x16keyDoor0(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......WW......W",
                "W.K....WW.D....W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "WWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWW.WWW",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W..............W",
                "W.H....WW......W",
                "W......WW......W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure16x16keyDoor1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......WW......W",
                "W.K....WW.T....W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "WWW.WWWWWWWW.WWW",
                "WWW.WWWWWWWWDWWW",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W..............W",
                "W.H....WW......W",
                "W......WW......W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure16x16keyDoor2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......WW......W",
                "W....T.WW....K.W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "WWW.WWWWWWWW.WWW",
                "WWWDWWWWWWWW.WWW",
                "W......WW......W",
                "W......WW......W",
                "W......WW......W",
                "W..............W",
                "W......WW....H.W",
                "W......WW......W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure16x16keyDoorLava0(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......LL......W",
                "W.K....LL.T....W",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "WLL.LLLLLLLL.LLW",
                "WLL.LLLLLLLL.LLW",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "W..............W",
                "W.H....LL......W",
                "W......LL......W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure16x16keyDoorLava1(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......LL......W",
                "W.K....LL.T....W",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "WLL.LLLLLLLL.LLW",
                "WLL.LLLLLLLLDLLW",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "W..............W",
                "W.H....LL......W",
                "W......LL......W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure16x16keyDoorLava2(**kwargs):
    init_map = ["WWWWWWWWWWWWWWWW",
                "W......LL......W",
                "W....T.LL....K.W",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "WLL.LLLLLLLL.LLW",
                "WLLDLLLLLLLL.LLW",
                "W......LL......W",
                "W......LL......W",
                "W......LL......W",
                "W..............W",
                "W......LL....H.W",
                "W......LL......W",
                "WWWWWWWWWWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure16x16keyDoorOriginal(**kwargs):
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

def Treasure8x16keyDoorLava0(**kwargs):
    init_map = ["WWWWWWWW",
                "W......W",
                "W.D....W",
                "W......W",
                "W......W",
                "W......W",
                "W......W",
                "WWW.WWWW",
                "WWW.WWWW",
                "W......W",
                "W.K....W",
                "W......W",
                "W......W",
                "W....H.W",
                "W......W",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure8x16keyDoorLava1(**kwargs):
    init_map = ["WWWWWWWW",
                "W......W",
                "W....H.W",
                "W......W",
                "W......W",
                "W.K....W",
                "W......W",
                "WWW.WWWW",
                "WWW.WWWW",
                "W......W",
                "W......W",
                "W......W",
                "W......W",
                "W.D....W",
                "W......W",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

def Treasure8x16keyDoorLava2(**kwargs):
    init_map = ["WWWWWWWW",
                "W......W",
                "W....D.W",
                "W......W",
                "W......W",
                "W......W",
                "W......W",
                "WWW.WWWW",
                "WWW.WWWW",
                "W......W",
                "W....K.W",
                "W......W",
                "W......W",
                "W.H....W",
                "W......W",
                "WWWWWWWW"]
    return KeyDoorEnv(init_map, color = KeyDoorEnv.color2, **kwargs)

