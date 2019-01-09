""" This is an abstract class for agents"""

from gridenvs.keyboard_controller import Controls, Key
from gridenvs.utils import Direction
import numpy as np
import time
from option.option import Option, OptionExplore, OptionKey


class Agent(object):
    """ This is an abstract class"""
    def __init__(self):
        pass
    
    def act(self, obs):
        raise NotImplementedError()

    #TODO : find max action

class KeyboardAgent(Agent):
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
    
    def act(self, obs):
        action = self.human_agent_action
        self.human_agent_action = None
        return action


class AgentOption(Agent):

    def __init__(self):
        self.option_explore = OptionExplore()
        self.option_get_key = OptionKey()
        self.q_function_options = {}

    def act(self, obs):
        pass
        # Explore option is the first option in the option_set
        #self.option_get_key.act()
        # Then, make new options
#        new_zone = self.option_explore.act()
#        for zone in new_zone:
#            self.option_set.append(Option(env = self.env, terminal_zone = zone, go_explore = False))
