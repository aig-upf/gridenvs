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
    This is the general option which allows the agent to go to zone to zone.
    It can be activate in the initial_zone and it ends in the terminal_zone.
    """
    def __init__(self, initial_zone = None, terminal_zone = None):
        self.terminal_zone = terminal_zone
        self.intial_zone = initial_zone
        self.q_function = {}
        self.reward = 0
#        self.set_initial_position()
        
#    def set_initial_position(self):
#        self.initial_zone = self.env.get_hero_zone()
#        self.current_state = self.env.get_hero_position()
    
    def act(self, terminal_state = None):
        pass
 #       self.set_initial_position()
        #TODO
 
        


        # direction_number = np.random.randint(4)
        # cardinal = Direction.cardinal()
        # return cardinal[direction_number]


class OptionKey(Option):
    """
    This is a special option to get the key
    """
    def act(self):
        """ 
        TODO this is not good at all
        """
        pass
    """
        self.set_initial_position()
        for k in range(1000):
            direction_number = np.random.randint(4)
            cardinal = Direction.cardinal()
            obs, r, done, info = self.env.step(cardinal[direction_number])
            if info["state_id"]:
                print('I have the key, here is my position ' + str(self.env.get_hero_position()))
                self.env.reset()
            if done:
                self.env.reset()
    """     

class OptionExplore(Option):
    """
    This is a special option to explore
    """
    def act(self):
        # For the moment we do a stupid thing (go random)
        direction_number = np.random.randint(4)
        cardinal = Direction.cardinal()
        return cardinal[direction_number]

