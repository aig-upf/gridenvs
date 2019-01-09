import sys, time
import gridenvs.examples  # load example gridworld environments
import gym
import numpy as np
import time
from agent.agent import KeyboardAgent, AgentOption

"""
TODO : problem with escape for closing the environment, problem with close().
(Look at the stashed version :
stash@{0}: WIP on branch_options: 3f712e7 some small changes
to change the agent files in order to delete environment in their list of attributes.)
"""

def make_environment_agent(env_name, blurred_bool = False, type_agent = "keyboard_controller", number_gray_colors = 10, zone_size_x = 4, zone_size_y = 4):
    env = gym.make(env_name)
    env.reset()
    env.blurred = blurred_bool
    env.number_gray_colors = number_gray_colors
    env.set_zone_size(zone_size_x, zone_size_y)
    if not hasattr(env.action_space, 'n'):
        raise Exception('Keyboard agent only supports discrete action spaces')

    if type_agent == "keyboard_controller":
        from gridenvs.keyboard_controller import Controls
        agent = KeyboardAgent(env, controls={**Controls.Arrows, **Controls.KeyPad})

    elif type_agent == "agent_option":
        agent = AgentOption()
    else:
        raise Exception("agent name does not exist")
    return env, agent


def learn(env, agent):
    # The agent learns a good policy
    print("Learning phase...")
    iteration_learning = 200
    for t in tqdm(range(1, iteration_learning + 1)):
        current_position = env.get_hero_position()
        done = False
        while not(done):
            # Only one task for the moment
            action = agent.act()
            reward, done, info = env.update(action)
            #agent.task.updateQ(current_position, action, new_position, reward, t)
            #current_position = new_position
            #end_episode ??
        env.reset()

def play(env_name, type_agent):
    env_blurred, agent_blurred = make_environment_agent(env_name, type_agent = type_agent, blurred_bool = True)
    env_not_blurred, agent_not_blurred = make_environment_agent(env_name, type_agent = type_agent, blurred_bool = False)

    done = False
    total_reward = 0
    shut_down = False
        
    while(not(done) and not(shut_down)):
        if type_agent ==  "keyboard_controller":
            shut_down = agent_blurred.human_wants_shut_down or agent_not_blurred.human_wants_shut_down
    
        obs = 0
        #TODO TOFIX obs = 0
        env_blurred.render_scaled()
        env_not_blurred.render_scaled()
        action = agent_not_blurred.act(obs)
        if action != None:
            obs, reward, done, info = env_not_blurred.step(action)
            obs, reward, done, info = env_blurred.step(action)
            total_reward += reward
    print('End of the episode')
    #print('reward = ' + str(total_reward))
    #print('zone = ' + repr(info['zone']))
    env_blurred.close()
    env_not_blurred.close()

            #        print('zone = ' + repr(info['zone']))
#        if done:
#            env_not_blurred.reset()
#            env_blurred.reset()


type_agent_list = ["keyboard_controller","agent_option"]
env_name = 'GE_MazeOptions-v0' if len(sys.argv)<2 else sys.argv[1] #default environment or input from command line 'GE_Montezuma-v1'
play(env_name, type_agent_list[0])
