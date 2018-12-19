""" This is an abstract class for agents"""

from gridenvs.keyboard_controller import Controls, Key

class Agent(object):
    """ This is an abstract class"""
    def __init__(self, env):
        self.env = env
        self.env.render_scaled()
        self.human_wants_shut_down = False
        self.env.unwrapped.viewer.window.on_key_press = self.key_press
        self.env.unwrapped.viewer.window.on_key_release = self.key_release

    def key_press(self, key, mod):
        if key==Key.esc:
            self.human_wants_shut_down = True
            self.env.close()

    def key_release(self, key, mod):
        pass

    def act(self, obs):
        raise NotImplementedError()

