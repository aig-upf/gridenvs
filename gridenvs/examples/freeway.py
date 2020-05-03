
import numpy as np
from gridenvs.hero import HeroEnv
from gridenvs.utils import Direction, Colors, Point
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

        super(FreewayEnv, self).__init__(actions=[None, Direction.N, Direction.S],
                                         max_moves=max_moves,
                                         reset_to_new_state=True,
                                         **kwargs)

    def reset_frog(self):
        self.state["hero"].pos = Point(int(self.size_x / 2), self.size_y - 1)

    def _state(self):
        world = GridWorld((self.size_x, self.size_y))
        frog = GridObject('F', (int(self.size_x / 2), self.size_y - 1), rgb=Colors.green)
        world.add_object(frog)

        for i in range(self.size_x):
            world.add_object(GridObject('G', (i, 0), rgb=Colors.blue)) #goal

        step_next_car = [None]*(self.size_y - 2)
        for i in range(self.size_y - 2):
            current_car_pos = 0
            #fill grid with cars
            while True:
                current_car_pos += self.get_relative_time() + 1
                if current_car_pos < self.size_x:
                    world.add_object(GridObject('C', (current_car_pos, i + 1), rgb=Colors.red))
                else:
                    break
            #get step at which a new car will be generated, for each row i
            step_next_car[i] = self.get_relative_time() + 1

        return {"world": world,
                "hero": frog,
                "step_next_car": step_next_car}

    def move_cars(self):
        # Move cars
        cars_to_remove = []
        for o in self.state["world"].objects:
            if o.name == 'C':
                if not self.move(o, Direction.E): #if we cannot move, it's because we reached the right edge
                    cars_to_remove.append(o)

        # Remove the ones that were getting out of the grid
        for car in cars_to_remove:
            self.state["world"].objects.remove(car)

        # Add new cars
        for i in range(self.size_y - 2):
            if self.state["step_next_car"][i] == self.state["moves"]:
                self.state["world"].add_object(GridObject('C', (0, i + 1), rgb=Colors.red))
                self.state["step_next_car"][i] = self.get_relative_time() + self.state["moves"] + 1

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

    def _update(self):
        self.move_cars()
        collisions = self.state["world"].collision(self.state['hero'], direction=None)
        if len(collisions) > 0:
            assert len(collisions) == 1
            o = collisions[0]
            assert o.name in ('C', 'G')

            r = -1.0 if o.name == 'C' else 1.0
            self.reset_frog()
            return r, self.end_episode == "collision", {}
        return 0.0, False, {}

    def reset_world(self):
        self.state["world"], self.state["hero"], self.state["step_next_car"] = self.create_world()