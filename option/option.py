"""
This class is for making options
For the moment we only implement the "exploring option"
(depth first)
"""
from gridenvs.utils import Direction
from q.q import Q
import time
import numpy as np

class Option(object):
    """
    This is the general option which allows the agent to go to zone to zone.
    It can be activate in the initial_zone and it ends in the terminal_zone.
    """
    def __init__(self, zone, position, reward_end_option = 0.2, terminal_state = None, play = False):
        self.play = play
        self.q = Q(position)
        self.zone = zone
        self.set_position(position)
        self.terminal_state = terminal_state
        self.reward_end_option = reward_end_option
    
    def __str__(self):
        return "option from " + str(self.zone) + " to " + str(self.terminal_state)

    def __hash__(self):
        return hash((self.zone, self.terminal_state))

    def __eq__(self, other_option):
        return (self.zone == other_option.zone) and (self.terminal_state == other_option.terminal_state)
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
            
    def update(self, reward, new_position, new_zone, action, t = None):
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
            self.update_q_function(self.position, new_position, action, total_reward, t)
            self.position = new_position
            return end_option

    def update_q_function(self, position, new_position, action, total_reward, t):
        self.add_primitive_actions(new_position)
        self.q.update_q_dict(position, new_position, action, total_reward, t)
    
    def act(self):
        if self.play:
            best_reward, best_action = self.q.find_best_action(self.position)
            return best_action
        else:
            if np.random.rand() < 0.01:
                cardinal = Direction.cardinal()
                return cardinal[np.random.randint(4)]
            else:
                best_reward, best_action = self.q.find_best_action(self.position)
                return best_action

    def check_end_option(self, new_zone):
        return new_zone == self.terminal_state
        
class OptionExplore(Option):
    """
    This is a special option to explore. No q_function is needed here.
    """
    
    def __str__(self):
        return "explore option"

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
        return new_zone != self.zone

    def update_q_function(self, position, new_position, action, reward, t):
        """
        There is no q_function for this special option
        """
        pass
