""" This agent will find his way through the maze but using hierarchy """
from gridenvs.utils import Direction
from gridenvs.keyboard_controller import Controls, Key
import numpy as np
import time
from agent.agent import Agent
from option.option import Option

class AgentOption(Agent):

    def __init__(self, env):
        super().__init__(env)
        self.option_explore = Option(env = env, go_explore = True)
        self.option_get_key = Option(env = env, get_key = True)
        self.option_set = []

    def key_press(self, key, mod):
        self.human_wants_shut_down = key==Key.esc

    def key_release(self, key, mod):
        pass

    def act(self, obs):
        # Explore option is the first option in the option_set
        new_zone = self.option_explore.act()
        # Then, make new options
        for zone in new_zone:
            self.option_set.append(Option(env = self.env, terminal_zone = zone, go_explore = False))
