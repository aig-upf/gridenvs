"""
This class is for making options
For the moment we only implement the "exploring option"
(depth first)
"""
from gridenvs.utils import Direction, Point
from agent.q import Q
import time
import numpy as np
from variables import *
class Option(object):
    """
    This class is doing Q learning, where Q is a matrix (we know the number of states and actions)
    """
    def __init__(self, position, initial_state, terminal_state, grid_size_option, play):
        """
        here grid_size_option is the size of the zone ! 
        """
        self.play = play
        self.grid_size_option = grid_size_option
        self.number_state = 2 * grid_size_option.x * grid_size_option.y + 1 # we add 1 for state 2 (agent got the door)
        self.number_actions = len(Direction.cardinal())
        self.q = np.zeros((self.number_state, self.number_actions))
        self.cardinal = Direction.cardinal()
        self.position = self.get_position((position, 0))
        self.initial_state = initial_state
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

    def check_end_option(self, new_state):
        return new_state != self.initial_state
    
    def get_position(self, point_state_id):
        """
        this function encodes the state from a point to a number
        point is the current position on the whole grid.
        point is projected into the zone
        """
        point = point_state_id[0]
        print("point : " + str(point))
        projected_point = point % self.grid_size_option
        print("projected point : " + str(projected_point))
        if point_state_id[1] == 2:
            return (self.number_state - 1)
        
        else:
            print("resulting position : " + str(projected_point.x + self.grid_size_option.x * projected_point.y + point_state_id[1] * self.grid_size_option.x * self.grid_size_option.y))
            return projected_point.x + self.grid_size_option.x * projected_point.y + point_state_id[1] * self.grid_size_option.x * self.grid_size_option.y
        
    def encode_direction(self, direction):
        """
        this function encodes a direction Direction.N/S/E/W into a number, 1/2/3/4
        """
        return self.cardinal.index(direction)
        
    def update_option(self, reward, new_position, new_state, action):
        encoded_new_position = self.get_position((new_position, new_state[1]))
        if self.play:
            self.position = encoded_new_position
            return self.check_end_option(new_state)

        else:
            encoded_action = self.encode_direction(action)
            max_value_action = np.max(self.q[encoded_new_position])
            total_reward = reward - REWARD_OPTION_ACTION
            end_option = self.check_end_option(new_state)
            if end_option:
                if new_state == self.terminal_state:
                    total_reward += REWARD_END_OPTION
                    
                else:
                    total_reward -= PENALTY_END_OPTION
            print("position : " + str(self.position))
            print("q not updated " + str(self.q[self.position]))
            self.q[self.position, encoded_action] *= (1 - LEARNING_RATE)
            self.q[self.position, encoded_action] += LEARNING_RATE * (total_reward + max_value_action)
            print("total_reward " + str(total_reward))
            print("q updated " + str(self.q[self.position]))
            self.position = encoded_new_position
            print("new position : " + str(self.position))
            return end_option
        
    def act(self):
        if self.play:
            best_action = np.argmax(self.q[self.position])

        else:
            if np.random.rand() < PROBABILTY_EXPLORE_IN_OPTION:
                best_action = np.random.randint(self.number_actions)
            
            else:
                best_action = np.argmax(self.q[self.position])
            
        return self.cardinal[best_action]

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
    
    def check_end_option(self, new_state):
        """
        option ends iff it has found a new zone
        """
        return new_state != self.initial_state

    def update_option(self, reward, new_position, new_state, action):
        return self.check_end_option(new_state)
