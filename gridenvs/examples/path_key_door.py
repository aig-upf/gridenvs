#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero_gridworld import StrMapHeroGridEnv
from gridenvs.utils import Color, Direction

class PathKeyDoorEnv(StrMapHeroGridEnv):

    STATE_MAP = {(0, 'K'): (1, 0.0, False, lambda w,c: w.remove_object(c)), #getting the key, state: 0->1
                 (1, 'D'): (1, 1.0, True, None)} #reaching the goal
    
    
#    MAP_DESC = {'COLORS': {'W': Color.blue,
#                           'D': Color.yellow,
#                           'H': Color.green,
#                           'K': Color.darkOrange}}
    MAP_DESC = {'COLORS': {'W': Color.white, 'D': Color.green, 'K': Color.red, 'H': Color.blue, '.': Color.black}}

    BLOCKS = {'W'}

    MAP = ["..........",
           "..........",
           "..........",
           "WWWWWWWWWW",
           "WDH.....KW",
           "WWWWWWWWWW",
           "..........",
           "..........",
           "..........",
           ".........."]

    ACTION_MAP = [Direction.W, Direction.E]

    def __init__(self, die=True, *args, **kwargs):
        if die:
            self.STATE_MAP.update({(0, 'W'): (0, -1.0, True, None), #hitting a wall at state 0
                                   (1, 'W'): (1, -1.0, True, None)}) #hitting a wall at state 1
        StrMapHeroGridEnv.__init__(self, *args, **kwargs)