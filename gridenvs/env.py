
from copy import deepcopy
import gym
import numpy as np
from gym.spaces import Discrete, Box

class GridEnv(gym.Env):
    """
        This class should not be instantiated
        It models a game based on colored squares/rectangles in a 2D space
    """

    def __init__(self, actions, pixel_size=(84,84), reset_to_new_state=False):
        self.actions = actions
        self.pixel_size = tuple(pixel_size)
        self.reset_to_new_state = reset_to_new_state
        self.action_space = Discrete(len(actions))
        self.observation_space = Box(0, 255, shape=self.pixel_size+(3,), dtype=np.uint8)
        self.state = self.new_state()
        self.state["done"] = True
        self.init_state = deepcopy(self.state)
        assert "world" in self.state.keys(), "State should contain a GridWorld object"

    def seed(self, seed):
        np.random.seed(seed) #TODO: use own random state instead of global one
        return seed

    def step(self, action):
        assert not self.state["done"], "The environment needs to be reset."

        if np.issubdtype(type(action), np.integer):
            assert action < len(self.actions), "Action index %i exceeds the number of actions (%i)." % (action, len(self.actions))
            action = self.actions[action]
        else:
            assert action in self.actions, "Action %s not in actions list. Possible actions: %s" % (action, str(self.actions))

        r, done, info = self.update_environment(action)
        self._obs = self.state["world"].render()
        self.state["done"] = done
        return (self._obs, r, done, info)

    def reset(self):
        if self.reset_to_new_state:
            self.state = self.new_state()
        else:
            self.state = deepcopy(self.init_state)
        self._obs = self.state["world"].render()
        self.state["done"] = False
        return self._obs

    def render(self, size=None):
        import cv2
        img = self._obs
        if size: img = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
        if len(img.shape) == 2: img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        try:
            self.viewer.imshow(img)
        except AttributeError:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
        return self.viewer.isopen

    def clone_state(self):
        return deepcopy(self.state)

    def restore_state(self, internal_state):
        self.state = deepcopy(internal_state)

    def get_char_matrix(self):
        return self.state["world"].get_char_matrix().view(np.uint32) # TODO: check

    def new_state(self):
        """
        To be implemented by child classes. Returns a dictionary with at least the gridworld object.
        """
        raise NotImplementedError

    def update_environment(self, action):
        """
        To be implemented by child classes. Returns a tuple: reward, episode_done, info_dict
        """
        raise NotImplementedError()

    def __del__(self):
        try:
            self.viewer.close()
        except AttributeError:
            pass
