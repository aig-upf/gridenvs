from gridenvs.utils import Color, Direction
from gridenvs.hero import get_StrHeroEnv


def key_door_env(init_map, key_reward=0.0, door_reward=1.0, wall_reward=-1.0, blocking_walls=False, action_map=None, **kwargs):
    state_dict = {(0, 'K'): (1, key_reward, False, lambda w, c: w.remove_object(c)),  # pick key
                  (1, 'D'): (1, door_reward, True, None),  # open door with key
                  (0, 'W'): (0, wall_reward, True, None),  # wall collision
                  (1, 'W'): (0, wall_reward, True, None)}
    colors = {'W': Color.gray, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black}
    return get_StrHeroEnv(str_map=init_map,
                          colors=colors,
                          hero_mark='H',
                          state_map=state_dict,
                          action_map=action_map,
                          blocks={'W'} if blocking_walls else None)(**kwargs)


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
    return key_door_env(init_map, **kwargs)


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
    return key_door_env(init_map, **kwargs)


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
    return key_door_env(init_map, **kwargs)


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
    return key_door_env(init_map, **kwargs)


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
    return key_door_env(init_map, **kwargs)


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
    return key_door_env(init_map, **kwargs)


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
    action_map = [Direction.W, Direction.E]
    return key_door_env(init_map,
                        blocking_walls=True,
                        action_map=action_map,
                        **kwargs)
