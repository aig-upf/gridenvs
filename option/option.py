"""
This class is for making options
For the moment we only implement the "exploring option"
(depth first)
"""
from gridenvs.utils import Direction
import time
import numpy as np

class Option(object):

    """
    TODO
    """
    def __init__(self, env, terminal_zone = None, go_explore = False, get_key = False):
        # terminal_zone is None when go_explore is True. Any zone different from initial_zone is a terminal zone

        self.env = env
        self.go_explore = go_explore
        self.get_key = get_key
        self.terminal_zone = terminal_zone
        self.q_function = {}
        self.set_initial_position()
        
    def set_initial_position(self):
        self.initial_zone = self.env.get_hero_zone()
        self.current_state = self.env.get_hero_position()

    def explore(self):
        # TODO.
        # For the moment we do a stupid thing (go random)
        k = 0
        new_zone = []
        while k < 150 and len(new_zone) < 4:
            k += 1
            done = False
            self.env.reset()
            while not(done):
                hero_current_zone = self.env.get_hero_zone()
                if hero_current_zone != self.initial_zone:
                    #just look around THE CLOSEST zones
                    done = True
                    if hero_current_zone not in new_zone:
                        new_zone.append(hero_current_zone)
                        print('find a new zone' + str(new_zone))
                direction_number = np.random.randint(4)
                cardinal = Direction.cardinal()
                _, _, done, _ = self.env.step(cardinal[direction_number])
        return new_zone

    def get_key(self):
        obs, r, done, info = env.step()
        if info["state_id"]:
            # I have the key
    
    def act(self):
        self.set_initial_position()
        # explore option is a special option to discover new zones
        # it is activated with the bool go_explore
        if self.go_explore:
            return self.explore()
        if self.get_key:
            self.get_key()
        

        
        


        # direction_number = np.random.randint(4)
        # cardinal = Direction.cardinal()
        # return cardinal[direction_number]
