#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero_gridworld import HeroEnv
from gridenvs.gridworld_map import GridWorld, GridObject
from gridenvs.utils import Color, Direction, Point
import numpy as np

class MoveToBeaconEnv(HeroEnv):
    STATE_MAP = {(0, 'B'): (0, 1.0, True, None)}
    ACTION_MAP = Direction.cardinal()

    def create_world(self):
        self.game_state['hero'] = self.reset_world()
        return self.world

    def reset_world(self):
        self.world = GridWorld((10, 10))
        quadrant_hero = np.random.randint(4)
        quadrant_beacon = np.random.choice(list(set(range(4)) - {quadrant_hero}))
        hero_pos = self.generate_random_position()
        beacon_pos = self.generate_random_position()
        while beacon_pos == hero_pos:
            beacon_pos = self.generate_random_position()
        hero = self.world.add_object(GridObject('H', hero_pos, Color.green, render_preference=1))
        beacon = self.world.add_object(GridObject('B', beacon_pos, Color.darkOrange))
        return hero

    def generate_random_position(self):
        x = np.random.randint(0, self.world.grid_size.x)
        y = np.random.randint(0, self.world.grid_size.y)
        return (x,y)