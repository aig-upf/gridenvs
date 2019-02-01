#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.hero_gridworld import HeroEnv, create_world_from_string_map
from gridenvs.utils import Direction, Color
from copy import deepcopy

class MontezumaEnv(HeroEnv):
    MAP = [
        "..................................",
        ".................RH...............",
        "..............FFFRFF..............",
        ".................R......R.........",
        ".G...............R......R.........",
        "....R............R......R..R......",
        ".FFFRFFF.....FFFFFFF....FFFRFFFF..",
        "....R......................R......",
        "....R......................R......",
        "....R......................R......",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
    ]
    HERO_MARK = 'H'
    COLORS = {'F': Color.blue,
              'H': Color.yellow,
              'G': Color.green,
              'R': Color.darkOrange}
    BLOCKS = {'F'}
    STATE_MAP = {(0, 'G'): (0, 1.0, True, None)}
    ACTION_MAP = Direction.all() + [None]

    def _reset(self):
        self.falling_direction = None
        self.going_to_die = False
        self.last_direction = None
        return super(MontezumaEnv, self)._reset()

    def update_world(self):
        collisions = self.world.all_collisions(self.game_state["hero"], return_names=True)
        if self.going_to_die and 'F' in collisions[Direction.S] and not 'R' in collisions[None]:
            return 0, True, {}

        return super(MontezumaEnv, self).update_world()

    def move_hero(self, direction):
        collisions = self.world.all_collisions(self.game_state["hero"], return_names=True)

        #Are we falling?
        if not 'F' in collisions[Direction.S] and not 'R' in collisions[None]:
            if self.falling_direction:
                self.going_to_die = True
            else:
                if self.last_direction in Direction.all_west(): self.falling_direction = Direction.SW
                elif self.last_direction in Direction.all_east(): self.falling_direction = Direction.SE
                else: self.falling_direction = Direction.S
            res = super(MontezumaEnv, self).move_hero(self.falling_direction)
            if not res:
                #couldn't move! probably because of an horizontal collision with floor (colliding with a corner while falling). Try going down:
                self.falling_direction = Direction.S
                res = super(MontezumaEnv, self).move_hero(self.falling_direction)
                return res
        else:
            self.falling_direction = None
            self.going_to_die = False

        #ILEGAL ACTIONS:
        #To move we need to touch the floor
        if not 'R' in collisions[None] and not 'F' in collisions[Direction.S]:
            #Do not allow going up or down if not touching the floor or not on a rope
            direction = None

        #If we are in a rope, we cannot move right or left (but we can jump right or left)
        if direction in [Direction.E, Direction.W]:
            if 'R' in collisions[None] and not 'F' in collisions[Direction.SE]+collisions[Direction.SW]:
                direction = None

        self.last_direction = direction
        return super(MontezumaEnv, self).move_hero(direction)

    def create_world(self):
        _, self.init_state_world = create_world_from_string_map(self.MAP, self.COLORS, self.HERO_MARK)
        return deepcopy(self.init_state_world)

    def reset_world(self):
        self.world = deepcopy(self.init_state_world)
        hero = self.world.get_objects_by_names(self.HERO_MARK)[0]
        return hero