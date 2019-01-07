import sys, time
import gridenvs.examples  # load example gridworld environments
import gym
import numpy as np
import time
from agent.keyboard_agent import KeyboardAgent
from agent.agent_option import AgentOption

"""
Maybe : instead of doing zone_size, let's do : number of zones x and y
TODO : duplicate of blurred and not blurred environment.
TODO : problem with escape, problem with close() actually.
(Look at the stashed version :
stash@{0}: WIP on branch_options: 3f712e7 some small changes
to change the agent files in order to delete environment in their list of attributes.)
"""
# First choose your environment

def make_environment_agent(env_name, blurred_bool = False, type_agent = "keyboard_controller", number_gray_colors = 1):
    env = gym.make(env_name)
    env.blurred = blurred_bool
    env.number_gray_colors = number_gray_colors
    if not hasattr(env.action_space, 'n'):
        raise Exception('Keyboard agent only supports discrete action spaces')

    # Second, choose your agent among ["keyboard_controller","agent_option"]
    if type_agent == "keyboard_controller":
        from gridenvs.keyboard_controller import Controls
        agent = KeyboardAgent(env, controls={**Controls.Arrows, **Controls.KeyPad})

    elif type_agent == "agent_option":
        from agent.agent_option import AgentOption
        agent = AgentOption(env)
    else:
        raise Exception("agent name does not exist")
    return env, agent

env_name = 'GE_MazeOptions-v0' if len(sys.argv)<2 else sys.argv[1] #default environment or input from command line 'GE_Montezuma-v1'
env_blurred, agent_blurred = make_environment_agent(env_name, blurred_bool = True)
env_not_blurred, agent_not_blurred = make_environment_agent(env_name, blurred_bool = False)
done = False
total_reward = 0
env_blurred.reset()
env_not_blurred.reset()
while(not(done) and not(agent_blurred.human_wants_shut_down) and not(agent_not_blurred.human_wants_shut_down)):
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
