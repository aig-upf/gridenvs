import sys, time
import gridenvs.examples  # load example gridworld environments
import gym
import numpy as np
import time
from tqdm import tqdm
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
    agent_position = env.get_hero_position()
    agent_zone = env.get_hero_zone()
    
    if not hasattr(env.action_space, 'n'):
        raise Exception('Keyboard agent only supports discrete action spaces')

    if type_agent == "keyboard_controller":
        from gridenvs.keyboard_controller import Controls
        agent = KeyboardAgent(env, controls={**Controls.Arrows, **Controls.KeyPad})

    elif type_agent == "agent_option":
        agent = AgentOption(agent_position, agent_zone)
    else:
        raise Exception("agent name does not exist")
    return env, agent

def learn(env, agent):
    initial_agent_position = agent.position
    initial_agent_zone = agent.zone
    iteration_learning = 500
    for t in tqdm(range(1, iteration_learning + 1)):
        current_position = env.get_hero_position()
        done = False
        print("starting new episode")
        while not(done):
            env.render_scaled()
#            time.sleep(1)
            option = agent.choose_option() # The agent chooses an option and set its parameter
            action = option.act() # The option makes the action
            # TOFIX : I change the info in the env render.
            # UGLY : info contains observations for the moment : zone and position of the agent
            _, reward, done, info = env.step(action) # The environment gives the feedback
            end_option, new_position, new_zone = option.update(reward, done, info, action, t) # We update the option's parameters.
            agent.option_update(end_option, new_position, new_zone, info['state_id'], done) # The agent update his info about the option
        
        env.reset()
        agent.reset(initial_agent_position, initial_agent_zone)
    env.close()

def play_keyboard(env, agent):
    """
    play with the Keyboard agent
    """
    
    #env_blurred, agent_blurred = make_environment_agent(env_name, type_agent = type_agent, blurred_bool = True)
    done = False
    total_reward = 0
    shut_down = agent.human_wants_shut_down
        
    while(not(done) and not(shut_down)):
        shut_down = agent.human_wants_shut_down
        #env_blurred.render_scaled()
        env.render_scaled()
        action = agent.act()
        if action != None:
            _, reward, done, info = env.step(action)
            total_reward += reward
            print('zone = ' + repr(info['zone']))
            #env_blurred.close()
    env.close()
    print('End of the episode')
    print('reward = ' + str(total_reward))

type_agent_list = ["keyboard_controller", "agent_option"]
env_name = 'GE_MazeOptions-v0' if len(sys.argv)<2 else sys.argv[1] #default environment or input from command line 'GE_Montezuma-v1'
type_agent = type_agent_list[1]
env, agent = make_environment_agent(env_name, blurred_bool = False, type_agent = type_agent)

learn(env, agent)
#play_keyboard(env, agent)
