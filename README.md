# Gridenvs

Gridenvs is an open-source library that allows to easily create [gym](https://github.com/openai/gym) gridworld environments. To test some [examples](gridenvs/examples), run `keyboard_agent.py`.

## Creating your own environments

Most environments consist of a single agent that moves in a grid (i.e. action affect a single object). If this is your case, consider inheriting from the [HeroEnv](gridenvs/hero.py) class. There are two functions that need to be implemented:
* _state(): returns a dictionary containing the internal state of the environment. The state dict will contain all the necessary information of the game, and has to come with at least two elements: "world" (the GridWorld object) and "hero" (the agent GridObject). 
* _update(): implements the logic of the environment, and returns a tuple `(reward, end_of_episode, info)` just as gym's env.step() function, except for the observation.

To easily create a grid map, we provide a function that takes as input a list of strings, such as:
    
    ["WWWWWWWWWW",
     "WD.W....KW",
     "W..W.....W",
     "W..W..WWWW",
     "W........W",
     "W........W",
     "W..WWWW..W",
     "W........W",
     "WH.......W",
     "WWWWWWWWWW"]
      
and returns a GridWorld object. See some given [examples](gridenvs/examples).

To be able to create your environment with gym.make() you will need to register it. See gym's [creating environments guide](https://github.com/openai/gym/blob/master/docs/creating-environments.md) or check `examples/__init__.py`.

For other types of games, consider deriving directly from the [Env](gridenvs/env.py) class.

## Installation

Clone the repository:

    git clone https://github.com/aig-upf/gridenvs.git
    cd gridenvs 
    
(Optional) If you want to create a virtual environment, you can do it by:

    python3 -m venv my_venv
    source my_venv/bin/activate

Install it:

    pip3 install -r requirements.txt
    
When using it in other projects, make sure gridenvs is in your `$PYTHONPATH` (e.g. by adding it with `export PYTHONPATH=\my\path\to\gridenvs`).

If you are using an environment from the examples package, import it so that environments get registered to gym (i.e. `import gridenvs.examples`).