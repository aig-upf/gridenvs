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
from q.q import Q

class AgentOption(): 

    def __init__(self, position, zone, play = False):
        """
        TODO make a list of q_function_options when the agent has to pick up the key to enter the door
        """
        self.play = play
        self.q = Q(zone)
        self.state_id = 0
        self.zone = zone
        self.position = position
        self.explore_option = OptionExplore(position = position, zone = zone) # special options

    def reset(self, initial_agent_position, initial_agent_zone):
        """
        Same as __init__ but the q function is preserved 
        """
        self.position = initial_agent_position
        self.zone = initial_agent_zone
        self.state_id = 0

    def choose_option(self):
        """
        if no option : explore
        else flip a coin, then take the best or explore
        """
        if self.play: # in this case we do not learn anymore
            _, best_option = self.q.find_best_action(self.zone)
            best_option.play = True
        else:
            if not(self.q.is_actions(self.zone)): # No option available : explore
                return self.explore_option
            else: # action are available : find the best and execute or explore
                if np.random.rand() < 0.5: # in this case go explore
                    return self.explore_option
                else: # in this case find the best option
                    _, best_option = self.q.find_best_action(self.zone)

        best_option.set_position(self.position)
        return best_option

    def option_update(self, new_position, new_zone, new_state_id, option, t = None):
        """
        """
        if self.play:
            self.zone = new_zone
            self.position = new_position
        else:
            reward = -1
            if self.state_id != new_state_id: # we get an item of the world
                reward += 10 # extra reward for having the key !
                self.state_id = new_state_id
        
            self.update_q_function_options(self.position, self.zone, new_position, new_zone, option, reward, t)

            self.zone = new_zone
            self.position = new_position
        
    def update_q_function_options(self, position, zone, new_position, new_zone, option, reward, t):
        if self.explore_option == option:
            self.q.add_state(new_zone)
            self.q.add_action_to_state(zone, Option(zone = zone, position = position, terminal_state = new_zone))
        elif self.q.is_actions(zone):
            self.q.update_q_dict(zone, new_zone, option, reward, t)


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
            raise Exception("Key %d not in controls map %s"%(key, self.controls))
    
    def key_release(self, key, mod):
        pass
    
    def act(self):
        action = self.human_agent_action
        self.human_agent_action = None
        return action
