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
        q_function_options = {current_zone : {Option_1 : reward_1, Option_2 : reward_2,...}, ...} 
        Option_1, Option_2 are numbers. Actual options are stored in list_options[Option_1], list_options[Option_2]
        TODO make a list of q_function_options when the agent has to pick up the key to enter the door
        """
        #self.game_state_id = 0
        self.zone = zone
        self.position = position
        self.list_options = [OptionExplore(reward_end_option = 1, zone = self.zone), OptionKey(reward_end_option = 1, zone = self.zone)] # two special options : 0 = explore, 1 = key
        self.q_function_options = {str(self.zone) : {}}
        self.executing_option = None # the option's number currently being executed.

    def choose_option(self):
        """
        TODO : find_key option
        """
        time.sleep(1.5)
        if self.executing_option != None: # One option execution is ongoing
            print('agent : continue')
            return self.list_options[self.executing_option]
        elif self.q_function_options[str(self.zone)] == {}: # No option available : explore
            print('agent : explore')
            self.executing_option = 0
            return self.list_options[self.executing_option]
        else: # options are available : find the best and execute
            print('agent : change option')
            best_option_number = self.find_best_option(self.q_function_options[str(self.zone)])
            self.executing_option = best_option_number
            return self.list_options[self.executing_option]

    def find_best_option(self, dict_option_reward):
        best_option_number = None
        best_reward = - float('inf')
        for option_number in dict_option_reward:
            reward = dict_option_reward[option_number]
            if reward > best_reward:
                best_reward = reward
                best_option_number = option_number
        return int(best_option_number)

    def option_update(self, ends, locations):
        if ends[0] and not(ends[1]): # in this case the option ended and the episode did not
            self.executing_option = None
            print("option ends. New zone :" + str(locations[1]))
            # if a new zone is discovered, create a new option and give it a reward_end_option
            # if not, done
            # if the state has a new id, we just got the key and so on

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
