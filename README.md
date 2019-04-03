# Grid world environment

This environment is developed in Python 3.6 and uses the library gym.

You can design a new map by editing/adding a file in the folder `gridenvs/examples`.

The variable `init_map` allows you to create a map with characters `W`, `.`, `H`, `K`, `D` which design respectively Wall, empty space, Hero, Key and Door.

You can change the parameters of variable `state_dict` which:

* first parameter is an integer which refers to the state of the world (for example : 0 -> The agent has not the key and 1 -> The agent has the key),
* second parameter is an integer which corresponds to the reward the agent gets when hitting the object,
* third parameter is a boolean. When it is True the episode ends when the agent gets the object and does not otherwise.

Also, you can just run the file `keyboard_agent.py` located in the root of the folder to generate the environment and move an agent with the arrows of your keyboard (press Escape to exit).
