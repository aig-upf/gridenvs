import sys, time
import gridenvs.examples  # load example gridworld environments
import gym
import numpy as np
import time
from agent.keyboard_agent import KeyboardAgent
from agent.agent_option import AgentOption

"""
TODO : duplicate of blurred and not blurred environment.
TODO : instead of doing zone_size, let's do : number of zones x and y
TODO : problem with escape
"""
# First choose your environment
env_name = 'GE_MazeKeyDoor-v1' if len(sys.argv)<2 else sys.argv[1] #default environment or input from command line 'GE_Montezuma-v1'
env_blurred = gym.make(env_name)
env_blurred.blurred = True
env_not_blurred = gym.make(env_name)
env_not_blurred.blurred = False
if not hasattr(env_blurred.action_space, 'n') and hasattr(env_not_blurred.action_space, 'n') :
    raise Exception('Keyboard agent only supports discrete action spaces')

# Second, choose your agent among the type_agent_list
type_agent_list = ["keyboard_controller","agent_option"]
agent_chosen = type_agent_list[0]

if agent_chosen == type_agent_list[0]:
    from gridenvs.keyboard_controller import Controls
    agent_blurred = KeyboardAgent(env_blurred, controls={**Controls.Arrows, **Controls.KeyPad})
    agent_not_blurred = KeyboardAgent(env_not_blurred, controls={**Controls.Arrows, **Controls.KeyPad})

elif agent_chosen == type_agent_list[1]:
    from agent.agent_option import AgentOption
    agent_blurred = AgentOption(env_blurred)
    agent_not_blurred = AgentOption(env_not_blurred)

done = False
total_reward = 0
env_blurred.reset()
env_not_blurred.reset()
while(not(done) and not(agent_blurred.human_wants_shut_down)):
    obs = 0
    #TODO TOFIX obs = 0
    env_blurred.render_scaled()
    env_not_blurred.render_scaled()
    action = agent_not_blurred.act(obs)
    if action != None:
        obs, reward, done, info = env_not_blurred.step(action)
        obs, reward, done, info = env_blurred.step(action)
        total_reward += reward
        print('zone = ' + repr(info['zone']))

print('End of the episode')
print('reward = ' + str(total_reward))
print('zone = ' + repr(info['zone']))
env_blurred.close()
env_not_blurred.close()
