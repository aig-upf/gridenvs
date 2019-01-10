""" This is an abstract class for agents"""
""" TODO : je pense que dans la variable self.executing_option il faut mettre l'option en question en train d'être exécutée.
La chaine d'action est la suivante : 
action -> environnment -> environment_feedback.
Dans cette dernière étape, on doit mettre à None la variable executing_option si besoin.
 """

from gridenvs.keyboard_controller import Controls, Key
from gridenvs.utils import Direction
import numpy as np
import time
from option.option import Option, OptionExplore, OptionKey

class AgentOption():

    def __init__(self, position, zone):
        """
        Structure of the q_function_option variable
        q_function_options = {initial_zone_1 : {terminal_zone_1 : [option_1, reward_1], terminal_zone_2 : [option_2, reward_2]}, initial_zone_2 : {terminal_zone_3 : [option_3, reward_3]}}
        TODO make a list of q_function_options when the agent has to pick up the key to enter the door
        """
        # self.game_state_id = 0
        self.state_id = 0
        self.t = 0
        self.zone = zone
        self.position = position
        # two special options
        self.explore_option = OptionExplore(position = self.position, zone = self.zone)
        self.key_option = OptionKey(position = self.position, zone = self.zone) #todo : put state_id = 1 as a terminal state
        # the agent's q_function for the abstract state space
        self.q_function_options = {str(self.zone) : {}}

    def reset(self, initial_agent_position, initial_agent_zone):
        self.position = initial_agent_position
        self.zone = initial_agent_zone
        self.t = 0
        self.state_id = 0

    def choose_option(self):
        """
        TODO : find_key option
        0. If an option is ongoing, continue
        1.1 If there is no option around, go explore.
        2 If there is an option, go explore with probability epsilon.
        Take the best option otherwise.
        """
        print(self.q_function_options)
        if self.q_function_options[str(self.zone)] == {}: # No option available : explore
            print('agent : explore')
            new_option = self.explore_option
        else: # options are available : find the best and execute or explore
            if np.random.rand() < 0.1: # in this case go explore
                new_option = self.explore_option
            else: # in this case find the best option
                print('agent : take a proper option')
                print('current position' + str(self.position))
                _, new_option = self.find_best_option(self.q_function_options[str(self.zone)])

        new_option.position = self.position
        new_option.zone = self.zone
        return new_option

    def find_best_option(self, dict_zone_optionReward):
        best_option = None
        best_reward = - float('inf')
        for terminal_state in dict_zone_optionReward:
            reward = dict_zone_optionReward[terminal_state][1]
            if reward > best_reward:
                best_reward = reward
                best_option = dict_zone_optionReward[terminal_state][0]
        return best_reward, best_option

    def option_update(self, new_position, new_zone, new_state_id):
        """
        """
        reward = -1
        if self.state_id != new_state_id:
            reward += 1
            self.state_id = new_state_id

        self.t += 1
        if str(new_zone) not in self.q_function_options[str(self.zone)].keys(): #exploration found a new zone
            print("exploration found new zone :" + str(new_zone))
            self.q_function_options[str(self.zone)].update({str(new_zone) : [Option(position = self.position, zone = self.zone, terminal_state = new_zone), 0]}) # we have created a new option starting ending in new_zone
            if str(new_zone) not in self.q_function_options.keys():
                self.q_function_options.update({str(new_zone) : {}})# we create also a new option starting from self.zone
        else:
            self.update_q_function_options(new_zone, reward, self.t)

        self.zone = new_zone
        self.position = new_position
            # if the state has a new id, we just got the key
    def update_q_function_options(self, new_zone, reward, t):
        learning_rate = 1 / t
        max_value_option, _ = self.find_best_option(self.q_function_options[str(self.zone)])
        self.q_function_options[str(self.zone)][str(new_zone)][1] *= (1 - learning_rate)
        self.q_function_options[str(self.zone)][str(new_zone)][1] += learning_rate * (reward + max_value_option)

class KeyboardAgent():
    def __init__(self, env, controls={**Controls.Arrows, **Controls.KeyPad}):
        self.env = env
        self.env.render_scaled()
        self.human_wants_shut_down = False
        self.controls = controls
        self.human_agent_action = None
        self.env.unwrapped.viewer.window.on_key_press = self.key_press
        self.env.unwrapped.viewer.window.on_key_release = self.key_release

    def key_press(self, key, mod):
        if key==Key.esc:
            self.human_wants_shut_down = True
        elif key in self.controls.keys():
            self.human_agent_action = self.controls[key]
        else:
            raise Exception("Key %d not in controls map %s"%(key, str(self.controls)))
    
    def key_release(self, key, mod):
        pass
    
    def act(self):
        action = self.human_agent_action
        self.human_agent_action = None
        return action
