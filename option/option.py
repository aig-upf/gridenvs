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
    def __init__(self, zone, position, reward_end_option = 1, terminal_state = None):
        self.position = position
        self.zone = zone
        self.terminal_state = terminal_state
        self.q_function = {}
        self.first_visit_q(self.position)
        self.reward_end_option = reward_end_option

    def __repr__(self):
        return "option"
    #    if terminal_state != None:
    #        return "terminal zone: " + str(self.terminal_state)

    def first_visit_q(self, position):
        known_state_action = True
        # If q_function(current_position,action) does not exist, initialize.
        try:
            self.q_function[str(position)]
        except:
            self.q_function.update({str(position) : {str(Direction.N) : 0, str(Direction.E) : 0, str(Direction.S) : 0, str(Direction.W) : 0}})
            known_state_action = False
        return known_state_action


    def update_q_function(self, action, new_position, reward, t):
        """
        Q learning procedure :
        Q_{t+1}(current_position, action) =
        (1- learning_rate) * Q_t(current_position, action)
        + learning_rate * [reward + max_{actions} Q_(new_position, action)
        """
        q_knows_current_position = self.first_visit_q(self.position)
        q_knows_new_position =  self.first_visit_q(new_position)
        if q_knows_current_position:
            learning_rate = 1 / t
            # TOFIX
            if q_knows_new_position:
                dict_actions_reward = self.q_function[str(new_position)]
                max_action = self.find_max_action(dict_actions_reward)
                max_value_action = dict_actions_reward[str(max_action)]
            else:
                max_value_action = 0
            # update the Q function with Q Learning algorithme
            self.q_function[str(self.position)][str(action)] *= (1 - learning_rate)
            self.q_function[str(self.position)][str(action)] += learning_rate * (reward + max_value_action)
    
    def update(self, reward, new_position, new_zone, action, t):
        """
        TODO
        returns e, E, P, Z where:
        e is True if the option is done
        E is True if episode is done
        P is the new position
        Z is the new zone
        """
        total_reward = reward
        end_option = self.check_end_option(new_zone)
        if end_option:
            total_reward = reward + self.reward_end_option

        self.update_q_function(action, new_position, total_reward, t)
        self.position = new_position
        self.zone = new_zone
        return end_option

    def act(self):
        if np.random.rand() < 0.1:
            cardinal = Direction.cardinal()
            return cardinal[np.random.randint(4)]
        else:
            print("q function : " + str(self.q_function))
            dict_actions_reward = self.q_function[str(self.position)]
            max_action = self.find_max_action(dict_actions_reward)
            return max_action

    def find_max_action(self, dict_actions_reward):
        """
        Take the maximum over all dictionnary's actions dict_actions.
        return argmax_{action} dict_actions
        """
        best_reward = -float('inf')
        best_action = None
        for action in dict_actions_reward:
            reward = dict_actions_reward[action]
            if reward > best_reward:
                best_action = action
                best_reward = reward
        return eval(best_action)

    def check_end_option(self, new_zone):
        return self.zone == self.terminal_state
        
class OptionExplore(Option):
    """
    This is a special option to explore. No q_function is needed here.
    """
    def act(self):
        # For the moment we do a stupid thing: go random, until it finds a new zone
        direction_number = np.random.randint(4)
        cardinal = Direction.cardinal()
        return cardinal[direction_number]
    
    def check_end_option(self, new_zone):
        return new_zone != self.zone

    def update_q_function(self, action, position, reward, t):
        pass










    
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

    def check_end_option(self):
        """TODO"""
        pass
    
