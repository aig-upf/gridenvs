from gridenvs.hero import HeroEnv
from gridenvs.utils import Point
import cv2

class ZonesEnv(HeroEnv):
    def __init__(self, zone_size_x=1, zone_size_y=1, blurred=False, number_gray_colors=0):
        HeroEnv.__init__(self, max_moves=None, obs_type="image")
        # Is the world blurred ?
        self.blurred = blurred
        self.number_gray_colors = number_gray_colors
        # The grid is cut into several zones of size zone_size_x X zone_size_y
        self.set_zone_size(zone_size_x, zone_size_y)
        HeroEnv._reset(self)
        # The zone is a region of the state space. For the moment we take squares of size zone_size.
        # The location of the zones are given by a Point, which contains its coordinates.
        self.update_zone(self.game_state['hero'].pos)


    def set_zone_size(self, x, y):
        self.zone_size = Point(x, y)

    def get_hero_position(self):
        return self.game_state['hero'].pos

    def get_hero_zone(self):
        self.update_zone(self.get_hero_position())
        return self.game_state['zone']

    def render_scaled(self, size=(512, 512), mode='human', close=False):
        # img = self.render_env_low_quality(size, self.world)
        img = self.render_env(size, self.world)
        self.render_gym(img, mode, close)

    def render_env(self, size, grid_state):
        """
        here we are making an average of the colors in the grid
        TODO : make sure that if zone_size_x = zone_size_y = 1 then the environement is not blurred
        """
        # a is a matrix which each entry is an array of 3 integers (RGB)
        # it is just the translation in terms of color of the grid writen in examples.
        grid_colors = grid_state.render()
        # a = self.average_colors(a)
        if (len(grid_colors[0]) % self.zone_size.x == 0) and (len(grid_colors) % self.zone_size.y == 0):
            size_x_image_blurred = int(len(grid_colors[0]) // self.zone_size.x)
            size_y_image_blurred = int(len(grid_colors) // self.zone_size.y)
            image_blurred = cv2.resize(grid_colors, (size_x_image_blurred, size_y_image_blurred),
                                       interpolation=cv2.INTER_AREA)
            # gray scale ?
            if self.number_gray_colors:
                for j in range(size_x_image_blurred):
                    for i in range(size_y_image_blurred):
                        rgb = image_blurred[i][j]
                        gray_level = (255 * 3) // self.number_gray_colors
                        sum_rgb = (sum(rgb) // gray_level) * gray_level
                        image_blurred[i][j] = [sum_rgb] * 3

            image_blurred_resized = cv2.resize(image_blurred, size, interpolation=cv2.INTER_NEAREST)
            return image_blurred_resized
        else:
            raise Exception("The gridworld can not be fragmented into zones")

    def update_world(self):
        reward, end_episode, info = HeroEnv.update_world(self)
        info.update({'zone': self.game_state['zone']})
        info.update({'position': self.game_state['hero'].pos})
        self.update_zone(self.game_state['hero'].pos)
        return reward, end_episode, info

    def update_zone(self, position):
        """
        gives the current zone for the position
        """
        self.game_state['zone'] = position // self.zone_size