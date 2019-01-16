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
    def __init__(self, initial_state, terminal_state, position, play = False):
        self.play = play
        self.q = Q(position)
        self.initial_state = initial_state
        self.set_position_update_q(position)
        self.terminal_state = terminal_state

    def __repr__(self):
        return "".join(["Option(", str(self.initial_state), ",", str(self.terminal_state), ")"])
    
    def __str__(self):
        return "option from " + str(self.initial_state) + " to " + str(self.terminal_state)

    def __eq__(self, other_option):
        if type(other_option).__name__ == "Option":
            return (self.initial_state == other_option.initial_state) and (self.terminal_state == other_option.terminal_state)
        else:
            return False

    def __hash__(self):
        return hash((self.initial_state, self.terminal_state))

    def check_end_option(self, new_zone):
        return new_zone != self.initial_state

    def set_position_update_q(self, position):
        """
        Everytime the option updates its position, it adds in his q_function this position and the corresponding actions (N, S, E, W)
        """
        self.position = position
        self.q.add_state(position)
        self.add_primitive_actions(position)

    def add_primitive_actions(self, position):
        """
        add the actions N, S, E, W at this position
        """
        try:
            self.q.q_dict[position]
        except:
            raise Exception("cannot add primitive actions because position does not exist")

        if not(self.q.is_actions(position)):
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
            total_reward = reward - 1
            end_option = self.check_end_option(new_zone)
            if end_option:
                if new_zone == self.terminal_state:
                    total_reward += REWARD_END_OPTION
                    print("got a reward for ending option in a correct manner")
                else:
                    total_reward -= 2*REWARD_END_OPTION
                    print("got a penalty for ending option in a wrong manner")
                    
            self.q.update_q_dict(self.position, new_position, action, total_reward)    
            self.set_position_update_q(new_position)
            return end_option

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

class OptionExplore(object):
    """
    This is a special option to explore. No q_function is needed here.
    """
    def __init__(self, initial_state):
        self.initial_state = initial_state

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

    def update_option(self, reward, new_position, new_zone, action):
        return self.check_end_option(new_zone)
