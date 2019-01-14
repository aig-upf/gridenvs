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

def learn(env, agent, iteration_learning = 1000):
    """
    0/ The agent chooses an option
    1/ The option makes the action
    TOFIX : I change the info in the env render. Info contains observations for the moment : zone and position of the agent
    2/ The environment gives the feedback
    3/ We update the option's parameters and we get end_option which is True if only if the option is done.
    4/ The agent update his info about the option
    5/ The agent chooses an option and sets its parameter
    """
    initial_agent_position = agent.position
    initial_agent_zone = agent.zone

    for t in tqdm(range(1, iteration_learning + 1)):
        t_agent = 0
        env.reset()
        agent.reset(initial_agent_position, initial_agent_zone)
        done = False
        running_option = False
        
        while not(done):
            env.render_scaled()
            if not(running_option): # no option acting
                option = agent.choose_option()
                #print("chosen option hash code " + str(option.__hash__()))
            action = option.act()
            _, reward, done, info = env.step(action)
            new_position = info['position']
            new_zone = info['zone']
            end_option = option.update(reward, new_position, new_zone, action, t)
            if end_option:
                running_option = False
                t_agent += 1
                agent.option_update(new_position, new_zone, info['state_id'], option, t_agent)
    env.close()
    return agent

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

def play(env, agent):
    """
    """
    initial_agent_position = agent.position
    initial_agent_zone = agent.zone
    agent.play = True
    env.reset()
    agent.reset(initial_agent_position, initial_agent_zone)
    done = False
    running_option = False
    print(agent.q[initial_agent_zone.__hash__()])
    while not(done):
        time.sleep(1)
        env.render_scaled()
        if not(running_option): # no option acting
            option = agent.choose_option()
            #print("chosen option hash code " + str(option.__hash__()))
        action = option.act()
        _, reward, done, info = env.step(action)
        new_position = info['position']
        new_zone = info['zone']
        end_option = option.update(reward, new_position, new_zone, action)
        if end_option:
            running_option = False
            agent.option_update(new_position, new_zone, info['state_id'], option)
    env.close()

agent_learned = learn(env, agent, iteration_learning = 50)
play(env, agent_learned)

#play_keyboard(env, agent)
