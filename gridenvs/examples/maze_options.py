#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero_gridworld import StrMapHeroGridEnv
import numpy as np

def key_door_env(init_map, key_reward, kwargs):
    # a dictionary of the states.
    # {(state, collision): (new_state, reward, end,?)}
    state_dict = {(1, 'D'): (1, 1.0, True, None)}
    for s in [0,1]: #possible states
        state_dict[(s, 'W')] = (0, -1.0, True, None)

    state_dict[0,'K'] = (1, 0, True, lambda w,c: w.remove_object(c))

    from gridenvs.utils import Color
    # A CLASS IN A FUNCTION ?!
    class KeyDoorEnv(StrMapHeroGridEnv):
        MAP = init_map
        STATE_MAP = state_dict
        MAP_DESC = {
            'COLORS': {'W': Color.white, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black}
        }
        BLOCKS = {}

    return KeyDoorEnv(**kwargs)

def key_door_walls(key_reward = False, **kwargs):
    """
    init_map = ["WWWWWWWW",
                "WD....KW",
                "W.W....W",
                "W.W..WWW",
                "W.W....W",
                "W.WWW..W",
                "WH.....W",
                "WWWWWWWW"]
    """
    init_map = ["WWWWWWWWWWWWWWWW",
                "WWWWWWWWWWWWWWWW",
                "WW.....WW......W",
                "WW.....WW......W",
                "WW..H..........W",
                "WW.....WW......W",
                "WW.....WW......W",
                "WW.....WW......W",
                "WWWKWWWWW......W",
                "WWW.WWWWWWW.WWWW",
                "WW.....WWWW.WWWW",
                "WW.....WW......W",
                "WW.....WW......W",
                "WW.............W",
                "WWD....WW......W",
                "WWWWWWWWWWWWWWWW"]
    init_map = np.array([list(init_map[i]) for i in range(len(init_map))])

    init_map=["".join(row) for row in init_map]
    return key_door_env(init_map, key_reward, kwargs)
