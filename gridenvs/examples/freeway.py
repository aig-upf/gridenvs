
import numpy as np
from gridenvs.hero import HeroEnv
from gridenvs.utils import Direction, Colors
from gridenvs.world import GridWorld, GridObject

class FreewayEnv(HeroEnv):
    def __init__(self, size, avg_cars = 0.2, episode_end= "moves", **kwargs):
        assert episode_end in ("moves", "collision")
        max_moves = None if episode_end == "collision" else 100
        self.end_episode = episode_end

        assert size >= 3  # At least one row for starting point, one for goal and one for cars.
        avg_cars_per_step = avg_cars

        self.size_x = self.size_y = size
        self.mean_relative_time = 1 / avg_cars_per_step  # mean waiting steps before generating a new car, at every row.

        super(FreewayEnv, self).__init__(size=size,
                                         actions=[None, Direction.N, Direction.S],
                                         max_moves=max_moves,
                                         using_immutable_states=True,
                                         fixed_init_state=False,
                                         **kwargs)

    def reset_frog(self):
        return GridObject('F', (int(self.size_x / 2), self.size_y - 1), rgb=Colors.green)

    def _init_state(self):
        other_objects = []
        frog = self.reset_frog()

        for i in range(self.size_x):
            other_objects.append(GridObject('G', (i, 0), rgb=Colors.blue)) #goal

        step_next_car = [None]*(self.size_y - 2)
        for i in range(self.size_y - 2):
            current_car_pos = 0
            #fill grid with cars
            while True:
                current_car_pos += self.get_relative_time() + 1
                if current_car_pos < self.size_x:
                    other_objects.append(GridObject('C', (current_car_pos, i + 1), rgb=Colors.red))
                else:
                    break
            #get step at which a new car will be generated, for each row i
            step_next_car[i] = self.get_relative_time() + 1

        return {"hero": frog,
                "other_objects": tuple(other_objects),
                "step_next_car": tuple(step_next_car)}

    def move_cars(self, state):
        # Move cars
        new_objs = []
        for o in state["other_objects"]:
            if o.name == 'C':
                if o.pos[0] < self.world.size[0] - 1:  # else we remove the car
                    new_objs.append(self.move(o, Direction.E, check_collision_objects=[]))
            else:
                new_objs.append(o)

        # Add new cars
        step_next_car = list(state["step_next_car"])
        for i in range(self.size_y - 2):
            if step_next_car[i] == state["moves"]:
                new_objs.append(GridObject('C', (0, i + 1), rgb=Colors.red))
                step_next_car[i] = self.get_relative_time() + state["moves"] + 1

        return new_objs, tuple(step_next_car)

    def get_relative_time(self):
        """
        Poisson process:
        Gives the relative time at which an event is generated, sampled from
        the exponential distribution: F(x) = 1 - e^(-l*x)
        The next timestep is given by the inverse: x = -ln(U) / l, with the
        rate l=1/mean_relative_time.
        Returns: relative time
        """
        return int(round(-np.log(1.0 - np.random.rand()) * self.mean_relative_time))  # 1-rand  with lambda=rate.because random.random returns a value in [0,1) and we want a value in (0,1], to avoid log(0)

    def _next_state(self, state, action):
        frog = self.move(state["hero"], action, check_collision_objects=[])
        other_objects, step_next_car = self.move_cars(state)
        collisions = self.world.collision(frog, other_objects, direction=None)
        if len(collisions) > 0:
            assert len(collisions) == 1
            o = collisions[0]
            assert o.name in ('C', 'G')

            r = -1.0 if o.name == 'C' else 1.0
            next_state = {"hero": self.reset_frog(),
                          "other_objects": other_objects,
                          "step_next_car": step_next_car}
            return next_state, r, self.end_episode == "collision", {}

        next_state = {"hero": frog,
                      "other_objects": other_objects,
                      "step_next_car": step_next_car}
        return next_state, 0.0, False, {}
