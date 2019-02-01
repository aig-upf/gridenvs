#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero import get_StrHeroEnv
from gridenvs.utils import Color, Direction

def path_key_door_env(die, **kwargs):
    state_map = {(0, 'K'): (1, 0.0, False, lambda w,c: w.remove_object(c)), #getting the key, state: 0->1
                 (1, 'D'): (1, 1.0, True, None)} #reaching the goal
    if die:
        state_map.update({(0, 'W'): (0, -1.0, True, None), #hitting a wall at state 0
                               (1, 'W'): (1, -1.0, True, None)}) #hitting a wall at state 1

    colors = {'W': Color.white, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black}
    blocks = {'W'}
    map = ["..........",
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

    return get_StrHeroEnv(str_map=map,
                          colors=colors,
                          hero_mark='H',
                          state_map=state_map,
                          action_map=action_map,
                          blocks=blocks)(**kwargs)
