#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gridenvs.utils import Direction

class Key:
    arrow_left = 65361
    arrow_up = 65362
    arrow_right = 65363
    arrow_down = 65364

    keypad0 = 65456
    keypad1 = 65457
    keypad2 = 65458
    keypad3 = 65459
    keypad4 = 65460
    keypad5 = 65461
    keypad6 = 65462
    keypad7 = 65463
    keypad8 = 65464
    keypad9 = 65465

    enter = 65293
    esc = 65307
    space = 32

class Controls:
    #Provides maps key->action
    Arrows = {
        Key.arrow_left: Direction.W,
        Key.arrow_right: Direction.E,
        Key.arrow_down: Direction.S,
        Key.arrow_up: Direction.N,
        Key.space: None #Noop
    }
    KeyPad = {
        Key.keypad0: None, #Noop
        Key.keypad1: Direction.SW,
        Key.keypad2: Direction.S,
        Key.keypad3: Direction.SE,
        Key.keypad4: Direction.W,
        Key.keypad5: None, #Noop
        Key.keypad6: Direction.E,
        Key.keypad7: Direction.NW,
        Key.keypad8: Direction.N,
        Key.keypad9: Direction.NE
    }

class KeyboardController:
    def __init__(self, env, controls={**Controls.Arrows, **Controls.KeyPad}, render_size=(512, 512), frameskip=1, obs_fn=lambda x:None):
        self.env = env
        self.controls = controls
        self.render_size = render_size
        assert frameskip >= 1
        self.frameskip = frameskip  # Use previous control decision for these many steps
        self.obs_fn = obs_fn
        self.action_space = self.env.action_space
        self.env.reset()
        self.env.render(render_size)
        self.env.unwrapped.viewer.window.on_key_press = self.key_press
        self.env.unwrapped.viewer.window.on_key_release = self.key_release
        self.human_agent_action = -1
        self.human_wants_restart = False

    def key_press(self, key, mod):
        if key==Key.esc: self.human_wants_restart = True
        elif key in self.controls.keys():
            self.human_agent_action = self.controls[key]
        else:
            raise Exception("Key %d not in controls map %s"%(key, str(self.controls)))

    def key_release(self, key, mod):
        pass

    def run(self):
        while True:
            self.human_wants_restart = False
            done = False
            self.env.reset()
            while True:
                if self.human_wants_restart: break
                if self.human_agent_action != -1:
                    #print("taking action {}".format(self.human_agent_action))
                    r = 0
                    for _ in range(self.frameskip):
                        obs, reward, done, info = self.env.step(self.human_agent_action)
                        r += reward
                        if done:
                            break
                    self.human_agent_action = -1

                    self.obs_fn(obs)
                    print("r =", r)
                    if done:
                        print("End of episode", flush=True)
                        break

                self.env.render(self.render_size)


if __name__ == "__main__":
    import sys
    import gridenvs.examples  # load example gridworld environments

    env_name = 'GE_Montezuma-v0' if len(sys.argv)<2 else sys.argv[1] #default environment or input from command line

    import gym
    env = gym.make(env_name)
    controller = KeyboardController(env)
    controller.run()
