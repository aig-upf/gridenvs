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
    """
    GAME_NAME = "Gridworld environment"
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, n_actions, pixel_size=(84,84), obs_type="image", zone_size_x = 3, zone_size_y = 3):
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
        TODO : test this function
        """
        # a is a matrix which each entry is an array of 3 integers (RGB)
        a = grid_state.render()
#        a = self.average_colors(a)
        a = cv2.resize(a, (3,3), interpolation=cv2.INTER_AREA)
        a = cv2.resize(a, (512,512), interpolation=cv2.INTER_NEAREST)
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

    def render_scaled(self, size=(512, 512), mode='human', close=False, blurred = False):
        if blurred:
            size_divide_by_two = (size[0] // 2, size[1] // 2)
            img = self.render_env_low_quality(size_divide_by_two, self.world)
        else:
            img = self.render_env(size, self.world)
        self.render_gym(img, mode, close)

    def _seed(self, seed):
        np.random.seed(seed)
        return seed

    @staticmethod
    def average_colors_zone(matrix):
        """
        input : a list of list object
        output : a np.matrix objec

        matrix's entries are arrays of 3 integers.
        """
        number_rows = len(matrix)
        number_columns = len(matrix[0])
        matrix_average = np.zeros((number_rows, number_columns), dtype = object)
        number_elements = number_rows * number_columns
        has_same_number_elements = True
        has_three_elements = True
        for i in range(0,number_rows):
             has_same_number_elements *= (number_columns == len(matrix[i]))
             for j in matrix[i]:
                 has_three_elements *= (len(j) == 3)
        if not(has_same_number_elements):
            raise Exception ("The matrix rows have not all the same number of elements !")
        elif not(has_three_elements):
            raise Exception ("The matrix entries are not lists of 3 elements")
        else:
            r, g, b = 0, 0, 0
            for i in range(number_rows):
                for RGB in matrix[i]:
                    r += RGB[0]
                    g += RGB[1]
                    b += RGB[2]
            r /= number_elements
            g /= number_elements
            b /= number_elements
        matrix_average.fill([r, g, b])
        return matrix_average

    def average_colors(self, matrix):
        """
        call average_colors_zone in every zone of the matrix
        """
        m = np.array(matrix, object)
        if not((len(m) % self.zone_size['y'] == 0) and (len(m[0]) % self.zone_size['x'] == 0)):
            raise Exception ("The map can not be divided with these zones")
        else:
            for j in range(0, len(m[0]), self.zone_size['x']):
                for i in range(0, len(m), self.zone_size['y']):
                    i_min = i
                    i_max = i + self.zone_size['y']
                    j_min = j
                    j_max = j + self.zone_size['x']
                    m[i_min:i_max, j_min:j_max]  = self.average_colors_zone(m[i_min:i_max, j_min:j_max])
            return m.tolist()
