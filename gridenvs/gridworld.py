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
    import PIL
    resize = lambda a, size: np.array(Image.fromarray(a).resize(size, Image.NEAREST))

class GridworldEnv(gym.Env):
    """
        This class should not be instantiated
        Models a game based on colored squares/rectangles in a 2D space
    TODO : for the moment we leave 'blurred' as a special attribute... TOREMOVE
    """
    GAME_NAME = "Gridworld environment"
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, n_actions, pixel_size=(84,84), obs_type="image", zone_size_x = 2, zone_size_y = 2, blurred = False):
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
        #The world is the grid which directly comes from the matrix representation of init_map (examples of gridenvs)
        self.world = self.create_world()
        # The grid is cut into several zones of size zone_size_x X zone_size_y
        self.zone_size = {'x' : zone_size_x, 'y' : zone_size_y}
        # Is the world blurred ?
        self.blurred = blurred

    def create_world(self):
        raise NotImplementedError()

    def get_colors(self):
        return self.world.get_colors()

    def render_env(self, size, grid_state):
        a = grid_state.render()
        a = cv2.resize(a, size, interpolation=cv2.INTER_NEAREST)
        return a

    def render_env_low_quality(self, size, grid_state):
        """
        here we are making an average of the colors in the grid
        TODO size argument ?
        TODO gray_scale bool in argument
        """
        # a is a matrix which each entry is an array of 3 integers (RGB)
        # it is just the translation in terms of color of the grid writen in examples.
        grid_colors = grid_state.render()
        # a = self.average_colors(a)
        if (len(grid_colors[0]) % self.zone_size['x'] == 0) and (len(grid_colors) % self.zone_size['y'] == 0):
            size_x_image_blurred = int(len(grid_colors[0]) // self.zone_size['x'])
            size_y_image_blurred = int(len(grid_colors) // self.zone_size['y'])
            image_blurred = cv2.resize(grid_colors, (size_x_image_blurred, size_y_image_blurred), interpolation=cv2.INTER_AREA)
            gray_scale = True
            # gray scale ?
            if gray_scale:

                black_rgb = [0, 0, 0]
                black = 90 * 3
                gray_1_rgb = [80, 80, 80]
                gray_1 = 120 * 3
                gray_2_rgb = [160, 160, 160]
                gray_2 = 150 * 3
                white_rgb = [255, 255, 255]
                for i in range(size_x_image_blurred):
                    for j in range(size_y_image_blurred):
                        rgb = image_blurred[i][j]
                        sum_rgb = sum(rgb)
                        if sum_rgb<black:
                            image_blurred[i][j] = black_rgb
                        elif sum_rgb<gray_1:
                            image_blurred[i][j] = gray_1_rgb
                        elif sum_rgb<gray_2:
                            image_blurred[i][j] = gray_2_rgb
                        else:
                            image_blurred[i][j] = white_rgb


            image_blurred_resized = cv2.resize(image_blurred, (512,512), interpolation=cv2.INTER_NEAREST)
            return image_blurred_resized
        else:
            raise Exception("The gridworld can not be fragmented into zones")

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
        if self.blurred:
            img = self.render_env_low_quality(size, self.world)
        else:
            img = self.render_env(size, self.world)
        self.render_gym(img, mode, close)

    def _seed(self, seed):
        np.random.seed(seed)
        return seed
