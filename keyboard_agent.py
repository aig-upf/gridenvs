#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.keyboard_controller import Controls, KeyboardController

def run_env(env_name, controls={**Controls.Arrows, **Controls.KeyPad}, frameskip=1, obs_fn = lambda x:None):
    import gym
    env = gym.make(env_name)

    if not hasattr(env.action_space, 'n'):
        raise Exception('Keyboard agent only supports discrete action spaces')

    controller = KeyboardController(env, controls=controls, frameskip=frameskip, obs_fn=obs_fn)
    controller.run()
    env.close()

if __name__ == "__main__":

    import sys
    import gridenvs.examples  # load example gridworld environments

    env_name = 'GE_MazeOptions-v0' if len(sys.argv)<2 else sys.argv[1] #default environment or input from command line
    run_env(env_name)
