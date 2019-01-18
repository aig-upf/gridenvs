""" This is an abstract class for agents"""

from gridenvs.keyboard_controller import Controls, Key
from gridenvs.utils import Direction, Point
import numpy as np
import time
from option.option import Option, OptionExplore
from q.q import Q
from variables import *

class AgentOption(): 

    def __init__(self, position, state, play = False):
        """
        TODO : replace state by a dictionary : self.state = {'zone' : zone, 'state_id' = 0}
        """
        self.play = play
        self.state = state
        self.q = Q(self.state)
        self.position = position
        if not(play):
            self.explore_option = OptionExplore(initial_state = self.state) # special options

    def reset_explore_option(self):
        self.explore_option.initial_state = self.state
        
    def reset(self, initial_agent_position, initial_agent_state):
        """
        Same as __init__ but the q function is preserved 
        """
        self.position = initial_agent_position
        self.state = initial_agent_state
        self.reset_explore_option()

    def choose_option(self):
        """
        if no option : explore
        else flip a coin, then take the best or explore
        """
        if self.play: # in this case we do not learn anymore
            _, best_option = self.q.find_best_action(self.state)
            best_option.play = True
            best_option.set_position_update_q(self.position)
            return best_option
        
        else:
            if not(self.q.is_actions(self.state)): # No option available : explore, and do not count the number of explorations
                print('empty_explore')
                self.reset_explore_option()
                self.explore_option.reset_number_explore()
                return self.explore_option
            
            else: # action are available : find the best and execute or explore
                if self.explore_option.number_explore(self.state) < MAXIMUM_EXPLORATION and np.random.rand() < PROBABILTY_EXPLORE: # in this case go explore
                    print('rand_explore')
                    self.reset_explore_option()
                    self.explore_option.add_number_explore()
                    return self.explore_option
                else: # in this case find the best option
                    best_reward, best_option = self.q.find_best_action(self.state)
                    if best_reward == 0:
                        print("best option chosen : " + str(best_option) +" \n")
                        best_option = np.random.choice(list(self.q.q_dict[self.state].keys()))
                        best_option.set_position_update_q(self.position)
                        return best_option
                    else:
                        print("best option chosen : " + str(best_option) +" \n")
                        best_option.set_position_update_q(self.position)
                        return best_option
                        
    def compute_total_reward(self, new_state_id):
        total_reward = 0
        if self.state[1] < new_state_id: # we get an item of the world
            total_reward += REWARD_KEY # extra reward for having the key !
        # if new_zone not in self.q.q_dict:
        #     total_reward += 1
        #     time.sleep(4)
        return total_reward
        
    def update_agent(self, new_position, new_state, option):
        if self.play:
            self.state = new_state
            self.position = new_position
        else:
            total_reward = self.compute_total_reward(new_state[1])
            self.update_q_function_options(new_state, option, total_reward)
            
            self.state = new_state
            self.position = new_position
            
    def update_q_function_options(self, new_state, option, reward):
        if self.q.is_state(new_state):
            if option != self.explore_option:
                print('update q : reward = ' + str(reward) + '\n' + str(self.q) + "\n")
                self.q.update_q_dict(self.state, new_state, option, reward)
        else:
            self.q.add_state(new_state)
            self.q.add_action_to_state(self.state, Option(position = self.position, initial_state = self.state, terminal_state = new_state))
            

class KeyboardAgent():
    def __init__(self, env, controls={**Controls.Arrows, **Controls.KeyPad}):
        self.env = env
        self.env.render_scaled()
        self.human_wants_shut_down = False
        self.controls = controls
        self.human_agent_action = None
        self.env.unwrapped.viewer.window.on_key_press = self.key_press
        self.env.unwrapped.viewer.window.on_key_release = self.key_release

    def key_press(self, key, mod):
        if key==Key.esc:
            self.human_wants_shut_down = True
        elif key in self.controls.keys():
            self.human_agent_action = self.controls[key]
        else:
            raise Exception("Key %d not in controls map %s"%(key, self.controls))
    
    def key_release(self, key, mod):
        pass
    
    def act(self):
        action = self.human_agent_action
        self.human_agent_action = None
        return action
