
from gridenvs.hero import HeroEnv
from gridenvs.world import GridWorld, GridObject
from gridenvs.utils import Color, Direction
import numpy as np

class MoveToBeaconEnv(HeroEnv):
    STATE_MAP = {(0, 'B'): (0, 1.0, True, None)}
    ACTION_MAP = Direction.cardinal()

    def create_world(self):
        self.game_state['hero'] = self.reset_world()
        return self.world

    def reset_world(self):
        self.world = GridWorld((10, 10))
        quadrant_hero = np.random.randint(4)
        quadrant_beacon = np.random.choice(list(set(range(4)) - {quadrant_hero}))
        hero_pos = self.generate_random_position()
        beacon_pos = self.generate_random_position()
        while beacon_pos == hero_pos:
            beacon_pos = self.generate_random_position()
        hero = self.world.add_object(GridObject('H', hero_pos, Color.green, render_preference=1))
        beacon = self.world.add_object(GridObject('B', beacon_pos, Color.darkOrange))
        return hero

    def generate_random_position(self):
        x = np.random.randint(0, self.world.grid_size.x)
        y = np.random.randint(0, self.world.grid_size.y)
        return (x,y)


"""
Implementation of the 1D world in which the agent moves right to the goal.
Different instances change the position of the goal (which is always at the
right of our agent), adding walls to the right of the goal.
"""
def beacon_1D(level=0, **kwargs):
    assert level in range(9)

    class Beacon1DEnv(HeroEnv):
        STATE_MAP = {(0, 'B'): (0, 1.0, True, None)}
        ACTION_MAP = [Direction.E, Direction.W]

        def create_world(self):
            self.game_state['hero'] = self.reset_world()
            return self.world

        def reset_world(self):
            self.world = GridWorld((10, 1))
            locations = self.generate_instance_positions(instance=level)
            hero_pos = (0, 0)
            hero = self.world.add_object(GridObject('H', hero_pos, Color.green, render_preference=1))
            beacon = self.world.add_object(GridObject('B', locations[-1], Color.darkOrange))
            locations.remove(locations[-1])
            # Add walls to the right of the goal
            while len(locations):
                wall = self.world.add_object(GridObject('W', locations[-1], Color.white))
                # wall.collides_with(hero) #Make it block the hero's way (not really needed rightnow since ends at goal, no transitions added)
                locations.remove(locations[-1])

            return hero

        def generate_instance_positions(self, instance=0):
            # Add object positions
            positions = []
            for t in range(instance + 1):
                positions.append((self.world.grid_size.x - (t + 1), 0))
            return positions

    return Beacon1DEnv(**kwargs)