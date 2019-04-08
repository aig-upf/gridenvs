import sys
import gym
import cv2
from gym.envs.classic_control import rendering
sys.path.append('gridenvs')


class ObservationZoneWrapper(gym.ObservationWrapper):
    def __init__(self,
                 env,
                 zone_size_option_x,
                 zone_size_option_y,
                 zone_size_agent_x,
                 zone_size_agent_y,
                 blurred,
                 thresh_binary_option,
                 thresh_binary_agent,
                 gray_scale=False,
                 cut_off=False):

        super().__init__(env)
        self.zone_size_option_x = zone_size_option_x
        self.zone_size_option_y = zone_size_option_y
        self.zone_size_agent_x = zone_size_agent_x
        self.zone_size_agent_y = zone_size_agent_y
        self.blurred = blurred
        self.gray_scale = gray_scale
        self.cut_off = cut_off
        self.thresh_binary_option = thresh_binary_option
        self.thresh_binary_agent = thresh_binary_agent

    def render(self,
               size=(512, 512),
               mode='human',
               agent_render=True,
               close=False,
               blurred_render=False,
               gray_scale_render=False):

        if hasattr(self.env.__class__, 'render_scaled'):  # we call render_scaled function from gridenvs
            return self.env.render_scaled(size, mode, close)
         
        else:  # we scale the image from other environment (like Atari)
            env_unwrapped = self.env.unwrapped
            img = env_unwrapped.ale.getScreenRGB2()
            if self.cut_off:
                # cut-off of the image
                img = img[50:180]  # size: 130
                
            if blurred_render:
                if agent_render:
                    img = ObservationZoneWrapper.make_downsampled_image(img,
                                                                        self.zone_size_agent_x,
                                                                        self.zone_size_agent_y)
                else:
                    img = ObservationZoneWrapper.make_downsampled_image(img,
                                                                        self.zone_size_option_x,
                                                                        self.zone_size_option_y)

            if gray_scale_render:
                if agent_render:
                    img = ObservationZoneWrapper.make_gray_scale(img, self.thresh_binary_agent)
                else:
                    img = ObservationZoneWrapper.make_gray_scale(img, self.thresh_binary_option)

            img_resized = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
            
            if mode == 'rgb_array':
                return img
            
            elif mode == 'human':
                if env_unwrapped.viewer is None:
                    env_unwrapped.viewer = rendering.SimpleImageViewer()

                env_unwrapped.viewer.imshow(img_resized)
                return env_unwrapped.viewer.isopen

    @staticmethod
    def make_downsampled_image(image, zone_size_x, zone_size_y):
        len_y = len(image)  # with MontezumaRevenge-v4 : 160
        len_x = len(image[0])  # with MontezumaRevenge-v4 : 210
        if (len_x % zone_size_x == 0) and (len_y % zone_size_y == 0):
            downsampled_size = (len_x // zone_size_x , len_y // zone_size_y)
            # vector of size "downsampled_size"
            img_blurred = cv2.resize(image, downsampled_size, interpolation=cv2.INTER_AREA)
            return img_blurred

        else:
            raise Exception("The gridworld " + str(len_x) + "x" + str(len_y) +
                            " can not be fragmented into zones " + str(zone_size_x) + "x" + str(zone_size_y))

    def observation(self, observation):
        img_option = observation
        img_agent = img_option.copy()
        if self.cut_off:
            raise NotImplementedError()
            #  cut-off of the image
            #  img = img[50:180] #size: 130
            #  observation = observation[50:180]
    
        img_option = ObservationZoneWrapper.make_downsampled_image(img_option,
                                                                   self.zone_size_option_x,
                                                                   self.zone_size_option_y)

        img_option = ObservationZoneWrapper.make_gray_scale(img_option,
                                                            self.thresh_binary_option)

        img_agent = ObservationZoneWrapper.make_downsampled_image(img_agent,
                                                                  self.zone_size_agent_x,
                                                                  self.zone_size_agent_y)

        img_agent = ObservationZoneWrapper.make_gray_scale(img_agent, self.thresh_binary_agent)

        img_option_tuple = tuple(tuple(tuple(color) for color in lig) for lig in img_option)
        img_agent_tuple = tuple(tuple(tuple(color) for color in lig) for lig in img_agent)    
        
        return {"state": hash(img_option_tuple), "blurred_state": hash(img_agent_tuple)}

    @staticmethod
    def make_gray_scale(image, threshold):
        img = cv2.medianBlur(image,1)
        _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        return img
