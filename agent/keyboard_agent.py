""" Here the agent is the person who controls the keyboard !"""

from gridenvs.keyboard_controller import Controls, Key
from agent.agent import Agent

class KeyboardAgent(Agent):
    def __init__(self, env, controls={**Controls.Arrows, **Controls.KeyPad}):
        Agent.__init__(self, env)
        self.controls = controls
        self.human_agent_action = None

    def key_press(self, key, mod):
        if key==Key.esc:
            self.human_wants_shut_down = True
        elif key in self.controls.keys():
            self.human_agent_action = self.controls[key]
        else:
            raise Exception("Key %d not in controls map %s"%(key, str(self.controls)))

    def act(self, obs):
        action = self.human_agent_action
        self.human_agent_action = None
        return action

