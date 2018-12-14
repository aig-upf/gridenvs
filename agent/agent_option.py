""" This agent will find his way through the maze but using hierarchy """
from gridenvs.utils import Direction
from gridenvs.keyboard_controller import Controls, Key
import numpy as np
import time
from agent.agent import Agent

class AgentOption(Agent):

    def key_press(self, key, mod):
        self.human_wants_shut_down = key==Key.esc

    def key_release(self, key, mod):
        pass

    def act(self, obs):
        time.sleep(0.3)
        direction_number = np.random.randint(4)
        cardinal = Direction.cardinal()
        return cardinal[direction_number]
