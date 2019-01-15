from gridenvs.utils import Point, Direction

class Q(object):
    """ 
    Contains the q value function which maps a state and an action to a value
    q_dict is a dictionary q_dict = {state_* : {action_* : value}}
    """
    def __init__(self, state):
        self.q_dict = {state.__hash__() : {}}
        self.hash_state = {}
        self.hash_action = {}

    def __str__(self):
        message = ""
        for state in self.q_dict:
            for action in self.q_dict[state]:
                message += str(self.hash_action[action]) + " value : " + str(self.q_dict[state][action]) + "\n"
        return message
        
    def add_state(self, state):
        """
        If state does not exist, we create it.
        Otherwise, we do nothing.
        returns True iif state already existed
        """
        state_hashed = state.__hash__()
        try:
            self.hash_state[state_hashed]
        except:
            self.hash_state.update({state_hashed : state})
            self.q_dict.update({state_hashed : {}})
            return False
        return True
            
    def add_action_to_state(self, state, action):
        """
        If state does not exist, we do not create it.
        If corresponding action does not exist, create it.
        Otherwise, we do nothing.
        returns True iif action already existed
        """
        self.add_state(state)
        state_hashed = state.__hash__()
        action_hashed = action.__hash__()
        self.hash_state.update({state_hashed : state})
        self.hash_action.update({action_hashed : action})
        
        total_actions_hashed = self.q_dict[state_hashed]
        if total_actions_hashed == {}:
            self.q_dict[state_hashed].update({action_hashed : 0})
            return False
        else:
            for act_hashed in total_actions_hashed:
                if act_hashed == action_hashed:
                    return True
            self.q_dict[state_hashed].update({action_hashed : 0})
            return False
        
    def update_q_dict(self, state, new_state, action, reward, t):
        """
        Q learning procedure :
        Q_{t+1}(current_position, action) =
        (1- learning_rate) * Q_t(current_position, action)
        + learning_rate * [reward + max_{actions} Q_(new_position, action)]
        """
        state_hashed = state.__hash__()
        new_state_hashed = new_state.__hash__()
        action_hashed = action.__hash__()
        
        learning_rate = 1 / t
        if self.q_dict[new_state_hashed] == {}:
            max_value_action = 0
        else:
            max_value_action, _ = self.find_best_action(new_state)
        # print("best_action = " + str(action_hashed))
        # print("current_state " + str(state_hashed))
        # print("corresponding q[state] : " + str(self.q_dict[state_hashed]) + "\n")
        # print("corresponding q : " + str(self.q_dict) + "\n")
        
        self.q_dict[state_hashed][action_hashed] *= (1 - learning_rate)
        self.q_dict[state_hashed][action_hashed] += learning_rate * (reward + max_value_action)
        
    def find_best_action(self, state):
        best_action_hashed = None
        best_reward = - float('inf')
        state_hashed = state.__hash__()
        exist_state = self.add_state(state)
        if exist_state:
            #print("current state " + str(state) + " q dictionary : " + str(self.q_dict))
            total_actions_hashed = self.q_dict[state_hashed]
            for action_hashed in total_actions_hashed:
                reward = total_actions_hashed[action_hashed]
                if reward > best_reward:
                    best_reward = reward
                    best_action_hashed = action_hashed
                    #print("best_reward = " + str(best_reward))
                    #print("best_action = " + str(best_action))
            return best_reward, self.hash_action[best_action_hashed]
        else:
            raise Exception('state does not exists')
                

    def is_actions(self, zone):
        return self.q_dict[zone.__hash__()] != {}
