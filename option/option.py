"""
This class is for making options
For the moment we only implement the "exploring option"
(depth first)
"""
from gridenvs.utils import Direction
from q.q import Q
import time
import numpy as np
from variables import *

class Option(object):
    """
    This is the general option which allows the agent to go to zone to zone.
    It can be activate in the initial_zone and it ends in the terminal_state.
    """
    def __init__(self, initial_state, terminal_state = None, position = None, play = False):
        self.play = play
        self.q = Q(position)
        self.initial_state = initial_state
        self.set_position(position)
        self.terminal_state = terminal_state
        self.reward_end_option = REWARD_END_OPTION

    def __repr__(self):
        return "".join(["Option(", str(self.initial_state), ",", str(self.terminal_state), ")"])
    
    def __str__(self):
        return "option from " + str(self.initial_state) + " to " + str(self.terminal_state)

    def __eq__(self, other_option):
        return (self.initial_state == other_option.initial_state) and (self.terminal_state == other_option.terminal_state)

    def __hash__(self):
        return hash((self.initial_state, self.terminal_state))

    def check_end_option(self, new_zone):
        return new_zone == self.terminal_state

    def set_position(self, position):
        self.position = position
        self.add_primitive_actions(position)

    def add_primitive_actions(self, position):
        """
        add the actions N, S, E, W at this position
        """
        cardinal = Direction.cardinal()
        for k in range(4):
            self.q.add_action_to_state(position, cardinal[k])
            
    def update_option(self, reward, new_position, new_zone, action):
        """
        option gets an extra reward if it finishes.
        returns True iff the option ends, i.e. if check_end_option returns True
        """
        if self.play:
            self.position = new_position
            return self.check_end_option(new_zone)
        else:
            total_reward = reward
            end_option = self.check_end_option(new_zone)
            if end_option:
                total_reward = reward + self.reward_end_option
            self.update_q_function(self.position, new_position, action, total_reward)
            self.position = new_position
            return end_option

    def update_q_function(self, position, new_position, action, total_reward):
        self.add_primitive_actions(new_position)
        self.q.update_q_dict(position, new_position, action, total_reward)
    
    def act(self):
        if self.play:
            _, best_action = self.q.find_best_action(self.position)
            return best_action
        else:
            if np.random.rand() < PROBABILTY_EXPLORE_IN_OPTION:
                cardinal = Direction.cardinal()
                return cardinal[np.random.randint(4)]
            else:
                best_reward, best_action = self.q.find_best_action(self.position)
                return best_action

class OptionExplore(Option):
    """
    This is a special option to explore. No q_function is needed here.
    """
    
    def __str__(self):
        return "explore option from " + str(self.initial_state)

    def __eq__(self, other):
        return type(other).__name__ == "OptionExplore"

    def __hash__(self):
        return hash("explore")

    def act(self):
        # For the moment we do a stupid thing: go random, until it finds a new zone
        direction_number = np.random.randint(4)
        cardinal = Direction.cardinal()
        return cardinal[direction_number]
    
    def check_end_option(self, new_zone):
        """
        option ends iff it has found a new zone
        """
        return new_zone != self.initial_state

    def update_q_function(self, position, new_position, action, reward):
        """
        There is no q_function for this special option
        """
        pass
