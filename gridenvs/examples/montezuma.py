
from gridenvs.hero import HeroEnv, create_world_from_string_map
from gridenvs.utils import Direction, Colors


def obj_names(objs):
    return list(set(o.name for o in objs))


class MontezumaEnv(HeroEnv):
    MAP = ["..................................",
           ".................RH...............",
           "..............FFFRFF..............",
           ".................R......R.........",
           ".G...............R......R.........",
           "....R............R......R..R......",
           ".FFFRFFF.....FFFFFFF....FFFRFFFF..",
           "....R......................R......",
           "....R......................R......",
           "....R......................R......",
           "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"]

    def __init__(self, **kwargs):
        actions = Direction.all()+[None]
        super(MontezumaEnv, self).__init__(size=(len(self.MAP[0]), len(self.MAP)), actions=actions, block_names=['F'], **kwargs)

    def _init_state(self):
        colors = {'F': Colors.blue, 'H': Colors.yellow, 'G': Colors.green, 'R': Colors.darkOrange}
        hero, other_objects = create_world_from_string_map(self.MAP, colors, 'H')
        return {"other_objects": other_objects,
                "hero": hero,
                "falling_dir": None,
                "going_to_die": False,
                "last_dir": None}

    def _next_state(self, state, direction):
        collisions = {d: obj_names(self.world.collision(state["hero"], state["other_objects"], d)) for d in [None, Direction.S, Direction.SE, Direction.SW]}

        new_state = {"hero": state["hero"],
                     "other_objects": state["other_objects"],
                     "falling_dir": state["falling_dir"],
                     "going_to_die": state["going_to_die"],
                     "last_dir": state["last_dir"]}

        #Are we falling?
        if not 'F' in collisions[Direction.S] and not 'R' in collisions[None]:
            direction = None  # We don't allow actions if not touching the floor or not on a rope
            if new_state["falling_dir"]:
                new_state["going_to_die"] = True
            else:
                if new_state["last_dir"] in Direction.all_west():
                    new_state["falling_dir"] = Direction.SW
                elif new_state["last_dir"] in Direction.all_east():
                    new_state["falling_dir"] = Direction.SE
                else:
                    new_state["falling_dir"] = Direction.S
            new_state["hero"] = self.move(state["hero"], new_state["falling_dir"], check_collision_objects=state["other_objects"])

            if state["hero"].pos == new_state["hero"].pos:  # position did not change
                # couldn't move! probably because of an horizontal collision with floor (colliding with a corner while falling). Try going down:
                new_state["falling_dir"] = Direction.S
                new_state["hero"] = self.move(new_state["hero"], new_state["falling_dir"], check_collision_objects=state["other_objects"])

        else:
            new_state["falling_dir"] = None
            new_state["going_to_die"] = False

            # If we are in a rope, we cannot move right or left (but we can jump right or left)
            if direction in [Direction.E, Direction.W]:
                if 'R' in collisions[None] and not 'F' in collisions[Direction.SE]+collisions[Direction.SW]:
                    direction = None

            new_state["hero"] = self.move(new_state["hero"], direction,
                                          check_collision_objects=state["other_objects"])

        new_state["last_dir"] = direction

        superpositions = obj_names(self.world.collision(new_state["hero"], new_state["other_objects"], direction=None))
        if 'G' in superpositions:
            return new_state, 1.0, True, {}
        elif new_state["going_to_die"]:
            collisions_south = obj_names(self.world.collision(new_state["hero"], new_state["other_objects"], direction=Direction.S))
            if 'F' in collisions_south and 'R' not in superpositions:
                return new_state, 0.0, True, {}
        return new_state, 0.0, False, {}