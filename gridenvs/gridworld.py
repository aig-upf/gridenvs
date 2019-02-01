#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
import gym
import numpy as np
from gym.spaces import Discrete, Box

try:
    import cv2
    resize = lambda a, size: cv2.resize(a, size, interpolation=cv2.INTER_NEAREST)
except ImportError:
    from PIL import Image
    resize = lambda a, size: np.array(Image.fromarray(a).resize(size, Image.NEAREST))

class GridEnv(gym.Env):
    """
        This class should not be instantiated
        Models a game based on colored squares/rectangles in a 2D space
    """
    GAME_NAME = "Gridworld environment"
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, n_actions, pixel_size=(84,84), obs_type="image"):
        self.pixel_size = pixel_size
        self.viewer = None

        if obs_type == "image":
            self.generate_observation = lambda grid_state: self.render_env(self.pixel_size, grid_state)
        elif obs_type == "matrix":
            self.generate_observation = lambda grid_state: grid_state.get_char_matrix().view(np.uint32)
        else:
            raise NotImplementedError("Bad observation type.")

        self.action_space = Discrete(n_actions)
        self.observation_space = Box(0, 255, shape=self.pixel_size+(3,))
        self.world = self.create_world()

    def create_world(self):
        """
        Child classes should implement this method.
        :return: A GridWorld object
        """
        raise NotImplementedError()

    def render_env(self, size, grid_state):
        a = grid_state.render()
        a = cv2.resize(a, size, interpolation=cv2.INTER_NEAREST)
        return a

    def update_environment(self, action):
        raise NotImplementedError()

    def _step(self, action):
        update_info = self.update_environment(action)
        obs = self.generate_observation(self.world)
        return (obs, *update_info)

    def clone_state(self):
        return deepcopy(self._clone()) #It is important to use deepcopy, that's why this wrapper function is needed

    def restore_state(self, internal_state):
        self._restore(deepcopy(internal_state)) #It is important to use deepcopy, that's why this wrapper function is needed

    def _clone(self):
        """
        To be overriden by child classes.
        """
        return self.world
    
    def _restore(self, internal_state):
        """
        To be overriden by child classes.
        """
        assert self.world.grid_size == internal_state.grid_size
        self.world = internal_state
        
    def _reset(self):
        raise Exception ("Child class should implement this.")

    def render_gym(self, img, mode='human', close=False):
        # Source: https://github.com/openai/gym/blob/master/gym/envs/atari/atari_env.py
        if close: #TODO: Sometimes the environment is closed just after being created (gym does that?) and raises an exception after calling _render(close=True). Check it out!
            if hasattr(self, 'viewer') and self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)

    def _render(self, mode='human', close=False):
        img = self.generate_observation(self.world)
        self.render_gym(img, mode, close)

    def render_scaled(self, size=(512, 512), mode='human', close=False):
        img = self.render_env(size, self.world)
        self.render_gym(img, mode, close)

    def _seed(self, seed):
        np.random.seed(seed)
        return seed

