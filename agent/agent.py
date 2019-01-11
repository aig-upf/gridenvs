""" This is an abstract class for agents"""
""" TODO : je pense que dans la variable self.executing_option il faut mettre l'option en question en train d'être exécutée.
La chaine d'action est la suivante : 
action -> environnment -> environment_feedback.
Dans cette dernière étape, on doit mettre à None la variable executing_option si besoin.
 """

from gridenvs.keyboard_controller import Controls, Key
from gridenvs.utils import Direction, Point
import numpy as np
import time
from option.option import Option, OptionExplore

class AgentOption(): 

    def __init__(self, position, zone):
        """
        TODO make a list of q_function_options when the agent has to pick up the key to enter the door
        """
        self.q = Q(zone)
        self.state_id = 0
        self.t = 0
        self.zone = zone
        self.position = position
        self.explore_option = OptionExplore(position = self.position, zone = self.zone) # special options

    def reset(self, initial_agent_position, initial_agent_zone):
        """
        Same as __init__ but the q function is preserved 
        """
        self.position = initial_agent_position
        self.zone = initial_agent_zone
        self.t = 0
        self.state_id = 0

    def choose_option(self):
        """
        if no option : explore
        else flip a coin, then take the best or explore
        """
        if self.q_function_options[str(self.zone)] == {}: # No option available : explore
            return self.explore_option
        else: # action are available : find the best and execute or explore
            if np.random.rand() < 0.1: # in this case go explore
                return self.explore_option
            else: # in this case find the best option
                _, best_option = self.q.q_dict.find_best_action(self.zone)

        best_option.set_position_zone(self.position, self.zone)        
        return best_option

    def option_update(self, new_position, new_zone, new_state_id):
        """
        key
        """
        reward = -1
        if self.id != new_state_id: # we get an item of the world
            reward += 1
            self.state_id = new_state_id
        self.t += 1
        
        self.q.q_dict.add_state(new_zone)
        self.q.q_dict.add_action_to_state(new_zone, Option(zone = self.zone, position = self.position, terminal_state = new_zone))


        if str(new_zone) != str(self.zone):
            if str(new_zone) not in self.q_function_options[str(self.zone)].keys(): #exploration found a new zone
                self.q_function_options[str(self.zone)].update({str(new_zone) : [), 0]}) # we have created a new option starting ending in new_zone
                if str(new_zone) not in self.q_function_options.keys():
                    self.q_function_options.update({str(new_zone) : {}})# we create also a new option starting from self.zone
            else:
                self.update_q_function_options(new_zone, reward, self.t)

        self.zone = new_zone
        self.position = new_position
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
