import sys, time
import gridenvs.examples  # load example gridworld environments
import gym
import numpy as np
import time
from agent.keyboard_agent import KeyboardAgent
from agent.agent_option import AgentOption


# First choose your environment
env_name = 'GE_MazeOptions-v1' if len(sys.argv)<2 else sys.argv[1] #default environment or input from command line
env = gym.make(env_name)
if not hasattr(env.action_space, 'n'):
    raise Exception('Keyboard agent only supports discrete action spaces')

# Second, choose your agent among the type_agent_list
type_agent_list = ["keyboard_controller","agent_option"]
agent_chosen = type_agent_list[1]

if agent_chosen == type_agent_list[0]:
    from gridenvs.keyboard_controller import Controls
    agent = KeyboardAgent(env, controls={**Controls.Arrows, **Controls.KeyPad})

elif agent_chosen == type_agent_list[1]:
    from agent.agent_option import AgentOption
    agent = AgentOption(env)

done = False
total_reward = 0
env.reset()
while(not(done) and not(agent.human_wants_shut_down)):
    obs = 0
    #TODO TOFIX obs = 0
    env.render_scaled(blurred = True)
    action = agent.act(obs)
    if action != None:
        obs, reward, done, info = env.step(action)
        total_reward += reward
        print('zone = ' + repr(info['zone']))

print('End of the episode')
print('reward = ' + str(total_reward))
print('zone = ' + repr(info['zone']))
env.close()
