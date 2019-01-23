"""
This class is for making options
For the moment we only implement the "exploring option"
(depth first)
"""
from gridenvs.utils import Direction, Point
from q.q import Q
import time
import numpy as np
from variables import *
verb = False
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
        self.number_state = 2 * grid_size_option.x * grid_size_option.y + 1
        self.number_actions = len(Direction.cardinal())
        self.q = np.zeros((self.number_state, self.number_actions))
        self.cardinal = Direction.cardinal()
        self.position = self.set_position_update_q((position, 0))
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
    
    def set_position_update_q(self, point_state_id):
        """
        this function encodes the state from a point to a number
        point is the current position on the whole grid.
        point is projected into the zone
        """
        point = point_state_id[0]
        
        projected_point = Point(point.x % self.grid_size_option.x, point.y % self.grid_size_option.x)
        # TODO : put a function modulo in class Point
        
        return projected_point.x + self.grid_size_option.x * projected_point.y 
        
    def encode_direction(self, direction):
        """
        this function encodes a direction Direction.N/S/E/W into a number, 1/2/3/4
        """
        return self.cardinal.index(direction)
        
    def update_option(self, reward, new_position, new_state, action):
        encoded_new_position = self.set_position_update_q(new_state)
        if self.play:
            self.position = encoded_new_position
            return self.check_end_option(new_state)

        else:
            print("q value " + str(self.q[self.position]))
            encoded_action = self.encode_direction(action)
            max_value_action = np.max(self.q[encoded_new_position])
            total_reward = reward - 1
            end_option = self.check_end_option(new_state)
            if end_option:
                if new_state == self.terminal_state:
                    total_reward += REWARD_END_OPTION
                    print("got a reward for ending option in a CORRECT manner. total reward = " + str(total_reward))
                    
                else:
                    total_reward -= PENALTY_END_OPTION
                    print("got a penalty for ending option in a WRONG manner")
            print("q(s,a) = " + str(self.q[self.position, encoded_action]))
            print("max_value_action " + str(max_value_action))
            self.q[self.position, encoded_action] *= (1 - LEARNING_RATE)
            print("s = " + str(self.position))
            print("inter q(s,a) " + str(self.q[self.position, encoded_action]))
            print("total reward " + str(total_reward))
            self.q[self.position, encoded_action] += LEARNING_RATE * (total_reward + max_value_action)
            print("new q(s,a) " + str(self.q[self.position, encoded_action]))
            print("q value updated " + str(self.q[self.position]))
            self.position = encoded_new_position
            return end_option
        
    def act(self):
        if self.play:
            best_action = np.argmax(self.q[self.position])

        else:
            if np.random.rand() < PROBABILTY_EXPLORE_IN_OPTION:
                if verb:
                    a = print("random explore")
                best_action = np.random.randint(self.number_actions)
            
            else:
                best_action = np.argmax(self.q[self.position])
            
        return self.cardinal[best_action]
        
class Option_dict(object):
    """
    This is the general option which allows the agent to go to zone to zone.
    It can be activate in the initial_zone and it ends in the terminal_state.
    The q function is a dictionary (in case we don't have access to the number of actions and states)
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
        if type(other_option).__name__ == "Option_dict":
            return (self.initial_state == other_option.initial_state) and (self.terminal_state == other_option.terminal_state)
        
        else:
            return False

    def __hash__(self):
        return hash((self.initial_state, self.terminal_state))

    def check_end_option(self, new_state):
        return new_state != self.initial_state

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
            
    def update_option(self, reward, new_position, new_state, action):
        """
        option gets an extra reward if it finishes.
        returns True iff the option ends, i.e. if check_end_option returns True
        """
        if self.play:
            self.position = new_position
            return self.check_end_option(new_state)
        
        else:
            total_reward = reward - 1
            end_option = self.check_end_option(new_state)
            if end_option:
                if new_state == self.terminal_state:
                    total_reward += REWARD_END_OPTION
                    print("got a reward for ending option in a correct manner")
                    
                else:
                    total_reward -= PENALTY_END_OPTION
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
        self.count_explore = {initial_state : 0}

    def __str__(self):
        return "explore option from " + str(self.initial_state)

    def __eq__(self, other):
        return type(other).__name__ == "OptionExplore"

    def __hash__(self):
        return hash("explore")

    def number_explore(self, state):
        if state in self.count_explore:
            return self.count_explore[state]
        
        else:
            self.count_explore.update({state : 0})
            return 0

    def reset_number_explore(self):
        if self.initial_state in self.count_explore:
            self.count_explore[self.initial_state] = 0
            
        else:
            self.count_explore.update({self.initial_state : 0})
            return 0
        
    def add_number_explore(self):
        if self.initial_state in self.count_explore:
            self.count_explore[self.initial_state] += 1
            
        else:
            self.count_explore.update({self.initial_state : 1})
            
    def act(self):
        print('state : ' + str(self.initial_state) + ' number of explorations : ' + str(self.count_explore[self.initial_state]))
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
