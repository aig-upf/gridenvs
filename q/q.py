from gridenvs.utils import Point, Direction

class Q(object):
    """ 
    Contains the q value function which maps a state and an action to a value
    q_dict is a dictionary q_dict = {state_* : {action_* : value}}
    """
    def __init__(self, state):
        self.q_dict = {str(state) : {}}

    def add_state(self, state):
        """
        If state does not exist, we create it.
        Otherwise, we do nothing.
        returns True iif state already existed
        """
        try:
            self.q_dict[str(state)]
        except:
            self.q_dict.update({str(state) : {}})
            return False
        return True
            
    def add_action_to_state(self, state, action):
        """
        If state does not exist, we do not create it.
        If corresponding action does not exist, create it.
        Otherwise, we do nothing.
        returns True iif action already existed
        """
        actions = self.q_dict[str(state)]
        if actions == {}:
            self.q_dict[str(state)].update({str(action) : 0})
            return False
        else:
            for act in actions:
                if eval(act) == action:
                    return True
            self.q_dict[str(state)].update({str(action) : 0})
            return False
        
    def update_q_dict(self, state, new_state, action, reward, t):
        """
        Q learning procedure :
        Q_{t+1}(current_position, action) =
        (1- learning_rate) * Q_t(current_position, action)
        + learning_rate * [reward + max_{actions} Q_(new_position, action)]
        """
        learning_rate = 1 / t
        max_value_action = self.find_best_action(new_state)
        self.q_dict[state][action] *= (1 - learning_rate)
        self.q_dict[state][action] += learning_rate * (reward + max_value_action)
        
    def find_best_action(self, state):
        best_action = None
        best_reward = - float('inf')
        exist_state = self.add_state(state)
        if exist_state:
            if self.q_dict[str(state)] == {}:
                raise Exception('no action found for this state')
            else:
                actions = self.q_dict[str(state)]
                for action in actions:
                    reward = actions[action]
                    if reward > best_reward:
                        best_reward = reward
                        best_action = action
                return best_reward, eval(best_action)            
        else:
            raise Exception('state does not exists')
                
