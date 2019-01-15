from gridenvs.utils import Point, Direction
from variables import *
class Q(object):
    """ 
    Contains the q value function which maps a state and an action to a value
    q_dict is a dictionary q_dict = {state_* : {action_* : value}}
    """
    def __init__(self, state):
        self.q_dict = {state : {}}

    def __str__(self):
        message = ""
        for state in self.q_dict:
            for action in self.q_dict[state]:
                message += "state " +str(state) + "action " + str(action) + " value : " + str(self.q_dict[state][action]) + "\n"
        return message

    def add_state(self, state):
        """
        If state does not exist, we create it.
        Otherwise, we do nothing.
        returns True iif state already existed
        """
        try:
            self.q_dict[state]
        except:
            self.q_dict.update({state : {}})

            
    def add_action_to_state(self, state, action):
        try:
            self.q_dict[state]
        except:
            raise Exception("action cannot be added since state does not exist")
        total_actions = self.q_dict[state]
        if total_actions == {}:
            self.q_dict[state].update({action : 0})
        else:
            if action not in total_actions:
                self.q_dict[state].update({action : 0})
        
    def find_best_action(self, state):
        try:
            self.q_dict[state]
        except:
            raise Exception('cannot find best action since there is no state')
        if not(self.is_actions(state)):
            raise Exception('cannot find best action since there is no action in state')
        
        best_action = None
        best_reward = - float('inf')
        total_actions = self.q_dict[state]
        for action in total_actions:
            reward = total_actions[action]
            if reward > best_reward:
                best_reward = reward
                best_action = action
        return best_reward, best_action

    def is_actions(self, zone):
        return self.q_dict[zone] != {}

    def update_q_dict(self, state, new_state, action, reward):
        """
        Q learning procedure :
        Q_{t+1}(current_position, action) =
        (1- learning_rate) * Q_t(current_position, action)
        + learning_rate * [reward + max_{actions} Q_(new_position, action)]
        """
        try:
            self.q_dict[state]
        except:
            raise Exception('state cannot be updated since it does not exist')

        self.add_action_to_state(state, action)
        self.add_state(new_state)
        if self.q_dict[new_state] == {}:
            max_value_action = 0
        else:
            max_value_action, _ = self.find_best_action(new_state)
        self.q_dict[state][action] *= (1 - LEARNING_RATE)
        self.q_dict[state][action] += LEARNING_RATE * (reward + max_value_action)
        
