from copy import deepcopy
import gym
import numpy as np
from gym.spaces import Discrete, Box
from gridenvs.world import GridWorld


class GridEnv(gym.Env):
    """
        This class should not be instantiated
        It models a game based on colored squares/rectangles in a 2D space
    """

    def __init__(self, size, n_actions, max_moves=None, pixel_size=(84, 84), using_immutable_states=False, fixed_init_state=False):
        self.max_moves = max_moves
        assert self.max_moves is None or self.max_moves > 0
        self.pixel_size = tuple(pixel_size)
        self.fixed_init_state = fixed_init_state
        self.using_immutable_states = using_immutable_states
        self.action_space = Discrete(n_actions)
        self.observation_space = Box(0, 255, shape=self.pixel_size + (3,), dtype=np.uint8)
        self.world = GridWorld(size)
        self._state = {"done": True}  # We are forced to reset

    def seed(self, seed):
        np.random.seed(seed)  # TODO: use own random state instead of global one, allow seed=None
        return seed

    def step(self, action):
        assert not self._state["done"], "The environment needs to be reset."
        next_state, r, done, info = self.get_next_state(self._state, action)
        next_state['moves'] = self._state["moves"] + 1
        if self.max_moves is not None and next_state['moves'] >= self.max_moves:
            done = True
        obs = self.world.render(self.get_objects_to_render(next_state), size=self.pixel_size)
        next_state["done"] = done
        self._state = next_state
        return (obs, r, done, info)

    def reset(self):
        if self.fixed_init_state:
            try:
                self.restore_state(self.init_state)
            except AttributeError:
                self.init_state = self.get_init_state()
                self.restore_state(self.init_state)
        else:
            self._state = self.get_init_state()

        self._state["moves"] = 0
        obs = self.world.render(self.get_objects_to_render(self._state), size=self.pixel_size)
        self._state["done"] = False
        return obs

    def render(self, size=None):
        if size is None:
            size = self.pixel_size
        img = self.world.render(self.get_objects_to_render(self._state), size=size)
        try:
            self.viewer.imshow(img)
        except AttributeError:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
        return self.viewer.isopen

    def clone_state(self):
        if self.using_immutable_states:
            return self._state
        return deepcopy(self._state)

    def restore_state(self, internal_state):
        if self.using_immutable_states:
            self._state = internal_state
        else:
            self._state = deepcopy(internal_state)

    def get_char_matrix(self):
        return self.world.get_char_matrix(self.get_objects_to_render(self._state)) #.view(np.uint32)

    def get_init_state(self):
        """
        To be implemented by child classes. It will be called at each environment reset if fixed_init_state is False,
        or only once at initialization otherwise.
        """
        raise NotImplementedError

    def get_next_state(self, state, action):
        """
        To be implemented by child classes. Returns a tuple: reward, episode_done, info_dict
        """
        raise NotImplementedError()

    def get_objects_to_render(self, state):
        """
        To be implemented by child classes.
        :return: iterable of grid objects
        """
        raise NotImplementedError()

    def __repr__(self):
        return "\n".join([" ".join(row) for row in self.get_char_matrix()])

    def __del__(self):
        try:
            self.viewer.close()
        except AttributeError:
            pass
