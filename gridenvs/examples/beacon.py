from gridenvs.hero import HeroEnv
from gridenvs.world import GridObject
from gridenvs.utils import Colors, Direction
import numpy as np

class MoveToBeaconEnv(HeroEnv):
    def __init__(self, size, **kwargs):
        super(MoveToBeaconEnv, self).__init__(size=size,
                                              actions=Direction.cardinal(),
                                              using_immutable_states=True,
                                              fixed_init_state=False,
                                              **kwargs)

    def get_init_state(self):
        hero_pos = self.generate_random_position()
        beacon_pos = self.generate_random_position()
        while beacon_pos == hero_pos:
            beacon_pos = self.generate_random_position()
        other_objects = []
        hero = GridObject('H', hero_pos, Colors.green, render_preference=1)
        other_objects.append(GridObject('B', beacon_pos, Colors.darkOrange))
        return {"other_objects": other_objects,
                "hero": hero}

    def _next_state(self, state, action):
        hero = self.move(state["hero"], action, check_collision_objects=state["other_objects"])
        new_state = {"hero": hero, "other_objects": state["other_objects"]}
        collisions = self.world.collision(hero, state["other_objects"], direction=None)
        if len(collisions) > 0:
            assert len(collisions) == 1 and collisions[0].name == 'B'
            return new_state, 1.0, True, {}
        return new_state, 0.0, False, {}

    def generate_random_position(self):
        x = np.random.randint(0, self.grid_size[0])
        y = np.random.randint(0, self.grid_size[1])
        return (x,y)
