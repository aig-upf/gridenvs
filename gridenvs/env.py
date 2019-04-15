
from copy import deepcopy
import gym
import numpy as np
from gym.spaces import Discrete, Box


class GridEnv(gym.Env):
    """
        This class should not be instantiated
        It models a game based on colored squares/rectangles in a 2D space
    """

    def __init__(self, n_actions, pixel_size):
        self.pixel_size = pixel_size
        self.action_space = Discrete(n_actions)
        self.observation_space = Box(0, 255, shape=self.pixel_size+(3,), dtype=np.uint8)
        self.state = {"world": self.create_world()}

    def get_char_matrix(self):
        return self.state["world"].get_char_matrix().view(np.uint32)

    def create_world(self):
        """
        Child classes should implement this method.
        :return: A GridWorld object
        """
        raise NotImplementedError()

    def generate_observation(self, grid_state):
        return grid_state.render()

    def update_environment(self, action):
        raise NotImplementedError()

    def step(self, action):
        update_info = self.update_environment(action)
        obs = self.generate_observation(self.state["world"])
        return (obs, *update_info)

    def clone_state(self):
        return deepcopy(self.state)

    def restore_state(self, internal_state):
        self.state = deepcopy(internal_state)

    def reset(self):
        raise Exception ("Child class should implement this.")

    def render(self, size=None):
        import cv2
        img = self.generate_observation(self.state["world"])
        if size: img = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
        if len(img.shape) == 2: img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        try:
            self.viewer.imshow(img)
        except AttributeError:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
        return self.viewer.isopen

    def __del__(self):
        try:
            self.viewer.close()
        except AttributeError:
            pass

    def seed(self, seed):
        np.random.seed(seed) #TODO: use own random state instead of global one
        return seed
