""" This is an abstract class for agents"""

from gridenvs.keyboard_controller import Controls, Key
from gridenvs.utils import Direction
import numpy as np
import time
from option.option import Option, OptionExplore, OptionKey


class Agent(object):
    """ This is an abstract class
    not sure this will be useful
    """
    def __init__(self):
        pass
    
    def act(self):
        raise NotImplementedError()

    def environment_update(self, info):
        pass


class AgentOption(Agent):

    def __init__(self, position, zone):
        self.game_state_id = 0
        self.zone = zone
        self.position = position
        self.option_explore = OptionExplore()
        self.option_get_key = OptionKey()
        self.q_function_options = {str(self.zone) : {}}
        self.executing_option = None # the terminal zone of the option

    def environment_update(self, info):
        self.game_state_id = info['state_id']
        self.position = info['position']
        if self.zone != info['zone']:
            # first update the current zone : The new zone is a connected zone
            # we create here the terminal state of a new option
            self.q_function_options[str(self.zone)].update
            ({
                str(info['zone']) :
                Option(zone = self.zone, terminal_zone = info['zone'])
            })
            # then add a new zone in the dictionary (we create its initial state)
            if str(info['zone']) not in self.q_function_options:
                self.q_function_options.update({str(info['zone']) : {}})
        # Finally update the current zone of the agent
        self.zone = info['zone']

    def learn(self):
        """
           This functions does:
        0. If an option is being executed, then continue
        1. Whatever the zone you are in: try to find the key (TODO)
        2. Explore and find a new zone if your q_function is empty for this zone.
        3. Learn the best option to change the zone
        """
        if self.executing_option != None:
            self.execute_option(self.q_function_options[str(self.zone)][str(self.executing_option)])
        # go explore
        elif self.q_function_options[str(self.zone)] == {}:
            return self.option_explore.act()
        else:
            # take the best option
            best_terminal_zone = self.find_best_terminal_zone(self.q_function_options[str(self.zone)])
            self.executing_option = best_terminal_zone
            self.execute_option(self.q_function_options[str(self.zone)][str(best_terminal_zone)])

    def execute_option(self, option):
        """
        Execute the option. Remember that it is always better to do the interrupting option strategy.
        Must ends with an update of self.executing_option
        """
        option_done, action = option.act(self.zone)
        if option_done: # option is done
            self.executing_option = None
            self.learn() # go back to choose a new option to learn 
        else:
            pass
        

    def find_best_terminal_zone(self, dict_options):
        """
        This function returns the best option possible, i.e. the one with the best cost_of_option
        """
        best_zone = None
        best_reward = - float('inf')
        for zone in dict_options:
            option = dict_options[zone]
            if option.reward_of_option > best_reward:
                best_reward = option.reward_of_option
                best_zone = zone
        return best_zone
        
    def act(self):
        """
        Here act means: select the best option
        """
        time.sleep(0.3)
        # go explore
#        if self.q_function_options[str(self.zone)] == {}:
#            return self.option_explore.act()
        return self.option_explore.act()        
        
        #self.option_get_key.act()
        # Then, make new options
#        new_zone = self.option_explore.act()
#        for zone in new_zone:
#            self.option_set.append(Option(env = self.env, terminal_zone = zone, go_explore = False))



class KeyboardAgent(Agent):
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
            raise Exception("Key %d not in controls map %s"%(key, str(self.controls)))
    
    def key_release(self, key, mod):
        pass
    
    def act(self):
        action = self.human_agent_action
        self.human_agent_action = None
        return action
