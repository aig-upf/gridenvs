""" This is an abstract class for agents"""
""" TODO : je pense que dans la variable self.executing_option il faut mettre l'option en question en train d'être exécutée.
La chaine d'action est la suivante : 
action -> environnment -> environment_feedback.
Dans cette dernière étape, on doit mettre à None la variable executing_option si besoin.
 """

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
        """
        Structure of the q_function_option variable
        q_function_options = {initial_zone : {terminal_zone : [reward_of_the_option, Option]},...}
        So the agent wants to go to initial_zone_A to terminal_zone_A he executes:
        q_function_options[initial_zone_A][terminal_zone_A][1]
        """
        self.game_state_id = 0
        self.zone = zone
        self.position = position
        self.option_explore = OptionExplore()
        self.option_get_key = OptionKey()
        self.q_function_options = {str(self.zone) : {}}
        self.executing_option = None # the terminal zone of the option

    def environment_feedback(self, info):
        self.game_state_id = info['state_id']
        self.position = info['position']
        if self.zone != info['zone']:
            # first update the current zone : The new zone (info['zone']) is connected to self.zone
            # we create here the terminal dictionary corresponding to the new option
            # the key is the terminal zone.
            # the value is : the reward of the Option and the Option itself
            dict_terminal_zone = {str(info['zone']) : [0, Option(zone = self.zone, terminal_zone = info['zone'])]}
            self.q_function_options[str(self.zone)].update(dict_terminal_zone)
            # then add a new zone in the dictionary (we create the initial state of a future option)
            if str(info['zone']) not in self.q_function_options:
                self.q_function_options.update({str(info['zone']) : {}})
        # Finally update the current zone of the agent
        self.zone = info['zone']

    def act(self):
        """
           This functions does:
        0. If an option is being executed, then continue
        1. Whatever the zone you are in: try to find the key (TODO)
        2. Explore and find a new zone if your q_function is empty for this zone.
        3. Learn the best option to change the zone
        """
        time.sleep(0.3)
        print(self.q_function_options)
        if self.executing_option != None:
            print('I continue to execute the current option')
            self.execute_option(self.q_function_options[str(self.zone)][str(self.executing_option)])
        # go explore
        elif self.q_function_options[str(self.zone)] == {}:
            print('I go to explore')
            return self.option_explore.act()
        else:
            # take the best option
            print('I execute an option :')
            print('Initial zone : ' + str(self.zone))
            print('Terminal zone : ' + str(self.executing_option))
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
        
    def TODO(self):
        """
        Here act means: select the best option
        """

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
