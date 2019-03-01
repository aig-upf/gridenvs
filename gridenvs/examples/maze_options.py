#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero import get_StrHeroEnv
from gridenvs.utils import Direction
from gridenvs.zones import ZonesEnv
import numpy as np

def key_door_env(init_map, key_reward, kwargs):
    # Miquel: key_reward is not being used

    # a dictionary of the states.
    # {(state, collision): (new_state, reward, end,?)}
    state_dict = {(1, 'D'): (2, 100.0, True, None)}
    for s in [0,1]: #possible states
        state_dict[(s, 'W')] = (0, -100, True, None)

    state_dict[0,'K'] = (1, 100.0, False, lambda w,c: w.remove_object(c))

    from gridenvs.utils import Color
    colors = {'W': Color.white, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black}

    return get_StrHeroEnv(str_map=init_map,
                          colors=colors,
                          hero_mark='H',
                          action_map = Direction.cardinal(),
                          state_map=state_dict,
                          cls = ZonesEnv)(**kwargs)

def key_door_walls(key_reward = False, **kwargs):
    maps = []
    
    maps.append(["WWWWWWWW",
                "WD....KW",
                "W.W....W",
                "W.W..WWW",
                "W.W....W",
                "W.WWW..W",
                "WH.....W",
                "WWWWWWWW"])
    
    
    maps.append(["WWWWWWWWWWWWWWWW",
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
                "WWWWWWWWWWWWWWWW"])

    maps.append(["WWWWWWWWWWWWWWWW",
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
                "WWWWWWWWWWWWWWWW"])
    
    
    maps.append(["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
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
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"])
    
    
    maps.append(["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
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
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"])
    
    
    maps.append(["WWWWWWWW",
                "WD.....W",
                "W......W",
                "W......W",
                "W......W",
                "W......W",
                "WH....KW",
                "WWWWWWWW"])
    
    init_map = maps[-1]
    init_map = np.array([list(init_map[i]) for i in range(len(init_map))])

    init_map=["".join(row) for row in init_map]
    return key_door_env(init_map, key_reward, kwargs)
