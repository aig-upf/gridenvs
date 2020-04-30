from copy import deepcopy
import gym
import numpy as np
from gym.spaces import Discrete, Box


class GridEnv(gym.Env):
    """
        This class should not be instantiated
        It models a game based on colored squares/rectangles in a 2D space
    """

    def __init__(self, actions, max_moves=None, pixel_size=(84, 84), fixed_init_state=True):
        self.actions = actions
        self.max_moves = max_moves
        assert self.max_moves is None or self.max_moves > 0
        self.pixel_size = tuple(pixel_size)
        self.fixed_init_state = fixed_init_state
        self.action_space = Discrete(len(actions))
        self.observation_space = Box(0, 255, shape=self.pixel_size + (3,), dtype=np.uint8)
        self.state = self.get_init_state()  # TODO: remove, only at reset
        self.state["done"] = True
        if fixed_init_state:
            self.init_state = deepcopy(self.state)
        assert "world" in self.state.keys(), "State should contain a GridWorld object"

    def seed(self, seed):
        np.random.seed(seed)  # TODO: use own random state instead of global one
        return seed

    def step(self, action):
        assert not self.state["done"], "The environment needs to be reset."
        action = self.get_env_action(action)
        r, done, info = self.update_environment(action)
        self.state['moves'] += 1
        if self.max_moves is not None and self.state['moves'] >= self.max_moves:
            done = True
        self._obs = self.state["world"].render(size=self.pixel_size)
        self.state["done"] = done
        return (self._obs, r, done, info)

    def reset(self):
        if self.fixed_init_state:
            self.state = deepcopy(self.init_state)
        else:
            self.state = self.get_init_state()
        self.state["moves"] = 0
        obs = self.state["world"].render(size=self.pixel_size)
        self.state["done"] = False
        return obs

    def render(self, size=None):
        if size is None:
            size = self.pixel_size
        img = self.state["world"].render(size=size)
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
        return self.state["world"].get_char_matrix().view(np.uint32)  # TODO: check

    def get_env_action(self, action):
        if np.issubdtype(type(action), np.integer):
            assert action < len(self.actions), "Action index %i exceeds the number of actions (%i)." % (
                action, len(self.actions))
            action = self.actions[action]
        else:
            assert action in self.actions, "Action %s not in actions list. Possible actions: %s" % (
                action, str(self.actions))
        return action

    def get_init_state(self):
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
