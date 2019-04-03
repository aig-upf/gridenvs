#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero import HeroEnv
from gridenvs.world import GridWorld, GridObject
from gridenvs.utils import Color, Direction

"""
Implementation of the 1D world in which the agent moves right to the goal.
Different instances change the position of the goal (which is always at the
right of our agent), adding walls to the right of the goal.
"""

def beacon_1D(level = 0, **kwargs):
    assert level in range(9)
    class Beacon1DEnv(HeroEnv):
        STATE_MAP = {(0, 'B'): (0, 1.0, True, None)}
        ACTION_MAP = Direction.left_right()

        def create_world(self):
            self.game_state['hero'] = self.reset_world()
            return self.world

        def reset_world(self):
            self.world = GridWorld((10, 1))
            locations = self.generate_instance_positions(instance=level)
            hero_pos = (0, 0)
            hero = self.world.add_object(GridObject('H', hero_pos, Color.green, render_preference=1))
            beacon = self.world.add_object(GridObject('B', locations[-1], Color.darkOrange))
            locations.remove(locations[-1])
            # Add walls to the right of the goal
            while len(locations): 
                wall = self.world.add_object(GridObject('W', locations[-1], Color.white))
                # wall.collides_with(hero) #Make it block the hero's way (not really needed rightnow since ends at goal, no transitions added)
                locations.remove(locations[-1])

            return hero

        def generate_instance_positions(self, instance = 0):
            # Add object positions
            positions = []
            for t in range(instance + 1):
                positions.append((self.world.grid_size.x - (t + 1), 0))
            return positions
    
    return Beacon1DEnv(**kwargs)