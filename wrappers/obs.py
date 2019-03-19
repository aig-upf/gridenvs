import sys
import gym
import numpy as np
import time
import cv2
from gym.envs.classic_control import rendering
sys.path.append('gridenvs')
import gridenvs.examples  # load example gridworld environments
from gym.envs.classic_control import rendering

class ObservationZoneWrapper(gym.ObservationWrapper):
    def __init__(self, env, zone_size_x, zone_size_y, zone_size_master_x, zone_size_master_y, blurred, number_gray_colors, gray_scale = False, cut_off = False):
        super(gym.ObservationWrapper, self).__init__(env)
        self.zone_size_x = zone_size_x
        self.zone_size_y = zone_size_y
        self.zone_size_master_x = zone_size_master_x
        self.zone_size_master_y = zone_size_master_y
        self.blurred = blurred
        self.gray_scale = gray_scale
        self.cut_off = cut_off
        self.number_gray_colors = number_gray_colors
        
    def render(self, size = (512, 512), mode = 'human', close = False, blurred_render = False, gray_scale_render = False):
        if hasattr(self.env.__class__, 'render_scaled'): # we call render_scaled function from gridenvs
            return self.env.render_scaled(size, mode, close)
         
        else: # we scale the image from other environment (like Atari)
            img = self.env.env.ale.getScreenRGB2()
            if self.cut_off:
                #cut-off of the image
                img = img[50:180] #size: 130
                
            if blurred_render:
                img = self.make_downsampled_image(img, self.zone_size_x, self.zone_size_y)
                img = self.make_downsampled_image(img, self.zone_size_master_x, self.zone_size_master_y)

            if gray_scale_render:
                img = self.make_gray_scale(img)

            img = np.array([[[color]*3 for color in lig] for lig in img])
            img_resized = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
            
            if mode == 'rgb_array':
                return img
            
            elif mode == 'human':
                if self.env.env.viewer is None:
                    self.env.env.viewer = rendering.SimpleImageViewer()
                    
                self.env.env.viewer.imshow(img_resized)
                return self.env.env.viewer.isopen

    def make_downsampled_image(self, image, zone_size_x, zone_size_y):
        len_y = len(image) # with MontezumaRevenge-v4 : 160
        len_x = len(image[0]) # with MontezumaRevenge-v4 : 210
        if (len_x % zone_size_x == 0) and (len_y % zone_size_y == 0):
            downsampled_size = (len_x // zone_size_x , len_y // zone_size_y)
            img_blurred = cv2.resize(image, downsampled_size, interpolation=cv2.INTER_AREA) # vector of size "downsampled_size"
            return img_blurred

        else:
            raise Exception("The gridworld " + str(len_x) + "x" + str(len_y) +  " can not be fragmented into zones " + str(zone_size_x) + "x" + str(zone_size_y))

    def observation(self, observation):
        #instead of returning a nested array, returns a *blurred*, *nested* *tuple* : img_blurred_tuple. Returns also the hashed obersvation.
        #img = observation.copy()
        img = observation
        if self.cut_off:
            #cut-off of the image
            img = img[50:180] #size: 130
            observation = observation[50:180]
    
        img = self.make_gray_scale(img)
        img = self.make_downsampled_image(img, self.zone_size_x, self.zone_size_y)
        
        img_blurred_more = img.copy()
        img_blurred_more = self.make_downsampled_image(img_blurred_more, self.zone_size_master_x, self.zone_size_master_y) 

        # transform the observation in tuple
        img_tuple = tuple(tuple(tuple([color]*3) for color in lig) for lig in img)
        img_blurred_more_tuple = tuple(tuple(tuple([color]*3) for color in lig) for lig in img_blurred_more)

        #img_tuple = tuple(tuple(lig) for lig in img)
        #img_blurred_more_tuple = tuple(tuple(lig) for lig in img_blurred_more)

        # observation_tuple = tuple(tuple(tuple(color) for color in lig) for lig in observation)
        
        
        return {"state" : hash(img_tuple), "blurred_state" : hash(img_blurred_more_tuple)}

    def make_gray_scale(self, image):    
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        #return cv2.medianBlur(image,7)
        #img = cv2.medianBlur(image,7)    
        #return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        #print(img)
        #return cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        #return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray_levels = np.linspace(0, 255, self.number_gray_colors)
        # for i in range(len(image)):
        #     for j in range(len(image[0])):
        #         sum_rgb = np.mean(image[i][j])
        #         # find the nearest
        #         idx_nearest = (np.abs(gray_levels - sum_rgb)).argmin()
        #         image[i][j] = [gray_levels[idx_nearest]] * 3
                
        # return image

