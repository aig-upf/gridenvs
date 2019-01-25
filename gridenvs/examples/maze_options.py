#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero_gridworld import StrMapHeroGridEnv
import numpy as np

def key_door_env(init_map, key_reward, kwargs):
    # a dictionary of the states.
    # {(state, collision): (new_state, reward, end,?)}
    state_dict = {(1, 'D'): (2, 100.0, True, None)}
    for s in [0,1]: #possible states
        state_dict[(s, 'W')] = (0, - 100, True, None)

    state_dict[0,'K'] = (1, 100.0, False, lambda w,c: w.remove_object(c))


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
    """
    init_map = ["WWWWWWWWWWWWWWWW",
                "WWWWWWWWWWWWWWWW",
                "WW............WW",
                "WW.......W....WW",
                "WW..H....W....WW",
                "WW.......W....WW",
                "WW.......W....WW",
                "WW.......W....WW",
                "WW.WWWWWWWWWW.WW",
                "WW.DW.........WW",
                "WW..W.........WW",
                "WW..W.........WW",
                "WW..WWWWWW.K..WW",
                "WW..W.........WW",
                "WW.....WW.....WW",
                "WWWWWWWWWWWWWWWW"]
    """
    
    init_map = ["WWWWWWWWWWWWWWWW",
                "WWWWWWWWWWWWWWWW",
                "WW.....W......WW",
                "WW.....W......WW",
                "WW..H.........WW",
                "WW..D.........WW",
                "WW.....W......WW",
                "WW.....W......WW",
                "WWW..WWWWW..WWWW",
                "WW.....W......WW",
                "WW.....W......WW",
                "WW.....W......WW",
                "WW.........K..WW",
                "WW............WW",
                "WW.....W......WW",
                "WWWWWWWWWWWWWWWW"]
    """
    init_map = ["WWWWWWWW",
                "W..H...W",
                "WD.....W",
                "W......W",
                "W......W",
                "W......W",
                "W...K..W",
                "WWWWWWWW"]
   
    """
    init_map = np.array([list(init_map[i]) for i in range(len(init_map))])

    init_map=["".join(row) for row in init_map]
    return key_door_env(init_map, key_reward, kwargs)
