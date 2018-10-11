#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero_gridworld import StrMapHeroGridEnv
from gridenvs.utils import Color, Direction

class PathKeyDoorEnv(StrMapHeroGridEnv):
    STATE_MAP = {(0, 'K'): (1, 0.0, False, lambda w,c: w.remove_object(c)), #getting the key, state: 0->1
                 (1, 'D'): (1, 1.0, True, None)} #reaching the goal
                 # (0, 'W'): (0, -1.0, True, None), #hitting a wall at state 0
                 # (1, 'W'): (1, -1.0, True, None)} #hitting a wall at state 1

    MAP_DESC = {'COLORS': {'W': Color.blue,
                           'D': Color.yellow,
                           'H': Color.green,
                           'K': Color.darkOrange}}
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
