
from gridenvs.hero import HeroEnv
from gridenvs.world import GridObject
from gridenvs.utils import Colors, Direction
import numpy as np

class MoveToBeaconEnv(HeroEnv):
    def __init__(self, size, **kwargs):
        super(MoveToBeaconEnv, self).__init__(size=size, actions=Direction.cardinal(), fixed_init_state=False, **kwargs)

    def _state(self):
        hero_pos = self.generate_random_position()
        beacon_pos = self.generate_random_position()
        while beacon_pos == hero_pos:
            beacon_pos = self.generate_random_position()
        other_objects = []
        hero = GridObject('H', hero_pos, Colors.green, render_preference=1)
        other_objects.append(GridObject('B', beacon_pos, Colors.darkOrange))
        return {"other_objects": other_objects,
                "hero": hero}

    def _update(self):
        collisions = self.world.collision(self.state["hero"], self.state["other_objects"], direction=None)
        if len(collisions) > 0:
            assert len(collisions) == 1 and collisions[0].name == 'B'
            return 1.0, True, {}
        return 0.0, False, {}

    def generate_random_position(self):
        x = np.random.randint(0, self.world.size[0])
        y = np.random.randint(0, self.world.size[1])
        return (x,y)
