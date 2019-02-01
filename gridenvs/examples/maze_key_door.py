#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero_gridworld import StrMapHeroEnv
import numpy as np

def key_door_env(init_map, key_reward, kwargs):
    state_dict = {(1, 'D'): (1, 1.0, True, None)}
    for s in [0,1]: #possible states
        state_dict[(s, 'W')] = (0, -1.0, True, None)
    
    kr = 1.0 if key_reward else 0.0
    state_dict[0,'K'] = (1, kr, False, lambda w,c: w.remove_object(c))
        
    from gridenvs.utils import Color
    class KeyDoorEnv(StrMapHeroEnv):
        MAP = init_map
        STATE_MAP = state_dict
        MAP_DESC = {
            'COLORS': {'W': Color.white, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black}
        }
        BLOCKS = {}

    return KeyDoorEnv(**kwargs)

def key_door_walls(level = 2, key_reward = False, **kwargs):
    assert level in range(5)
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
    init_map = np.array([list(init_map[i]) for i in range(len(init_map))])

    if level >= 1:
        init_map[6, 3:7] = 'W'
    if level >= 2:
        init_map[3, 6:] = 'W'
    if level >= 3:
        init_map[:4, 3] = 'W'
    if level >= 4:
        init_map[3, 3:] = 'W' #close entrance
        init_map[3, 6] = '.' #open 1 square in the middle
        
    init_map=["".join(row) for row in init_map]
    return key_door_env(init_map, key_reward, kwargs)

        
def key_door_entrance(entrance = 'R', key_reward = False, **kwargs):
    assert entrance in ('R', 'L')
    init_map = ["WWWWWWWWWW",
                "WD.......W",
                "W........W",
                "W..WWWW..W",
                "W........W",
                "W........W",
                "W..WWWW..W",
                "W........W",
                "WH.......W",
                "WWWWWWWWWW"]
    init_map = np.array([list(init_map[i]) for i in range(len(init_map))])

    if entrance == 'R':
        init_map[4:6, 3] = 'W'
        init_map[5, 4] = 'K'
    else:
        init_map[4:6, 6] = 'W'
        init_map[5, 5] = 'K'
    
    init_map=["".join(row) for row in init_map]
    return key_door_env(init_map, key_reward, kwargs)