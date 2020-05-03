
from gridenvs.hero import HeroEnv
from gridenvs.world import GridWorld, GridObject
from gridenvs.utils import Colors, Direction, Point
import numpy as np

class MoveToBeaconEnv(HeroEnv):
    def __init__(self, size, **kwargs):
        self.size = Point(size)
        super(MoveToBeaconEnv, self).__init__(actions=Direction.cardinal(), reset_to_new_state=True, **kwargs)

    def _state(self):
        world = GridWorld(self.size)
        hero_pos = self.generate_random_position()
        beacon_pos = self.generate_random_position()
        while beacon_pos == hero_pos:
            beacon_pos = self.generate_random_position()
        hero = world.add_object(GridObject('H', hero_pos, Colors.green, render_preference=1))
        beacon = world.add_object(GridObject('B', beacon_pos, Colors.darkOrange))
        return {"world": world,
                "hero": hero,
                "beacon": beacon}

    def _update(self):
        collisions = self.state["world"].collision(self.state["hero"], direction=None)
        if len(collisions) > 0:
            assert len(collisions) == 1
            if collisions[0] is self.state["beacon"]:
                return 1.0, True, {}
        return 0.0, False, {}

    def generate_random_position(self):
        x = np.random.randint(0, self.size.x)
        y = np.random.randint(0, self.size.y)
        return (x,y)
