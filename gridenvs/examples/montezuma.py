
from gridenvs.hero import HeroEnv, create_world_from_string_map
from gridenvs.utils import Direction, Color


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
        super(MontezumaEnv, self).__init__(actions=actions, **kwargs)

    def _state(self):
        colors = {'F': Color.blue, 'H': Color.yellow, 'G': Color.green, 'R': Color.darkOrange}
        gridworld, hero = create_world_from_string_map(self.MAP, colors, 'H')
        blocks = gridworld.get_objects_by_names(['F'])
        return {"world": gridworld,
                "hero": hero,
                "blocks": blocks,
                "falling_dir" : None,
                "going_to_die" : False,
                "last_dir" : None}

    def _update(self):
        superpositions = obj_names(self.state["world"].collision(self.state["hero"], direction=None))
        if 'G' in superpositions:
            return 1.0, True, {}
        elif self.state["going_to_die"]:
            collisions_south = obj_names(self.state["world"].collision(self.state["hero"], direction=Direction.S))
            if 'F' in collisions_south and 'R' not in superpositions:
                return 0, True, {}
        return 0.0, False, {}

    def move_hero(self, direction):
        collisions = {d: obj_names(self.state["world"].collision(self.state["hero"], d)) for d in [None, Direction.S, Direction.SE, Direction.SW]}

        #Are we falling?
        if not 'F' in collisions[Direction.S] and not 'R' in collisions[None]:
            if self.state["falling_dir"]:
                self.state["going_to_die"] = True
            else:
                if self.state["last_dir"] in Direction.all_west(): self.state["falling_dir"] = Direction.SW
                elif self.state["last_dir"] in Direction.all_east(): self.state["falling_dir"] = Direction.SE
                else: self.state["falling_dir"] = Direction.S
            res = super(MontezumaEnv, self).move_hero(self.state["falling_dir"])
            if not res:
                #couldn't move! probably because of an horizontal collision with floor (colliding with a corner while falling). Try going down:
                self.state["falling_dir"] = Direction.S
                res = super(MontezumaEnv, self).move_hero(self.state["falling_dir"])
                return res
        else:
            self.state["falling_dir"] = None
            self.state["going_to_die"] = False

        #ILEGAL ACTIONS:
        #To move we need to touch the floor
        if not 'R' in collisions[None] and not 'F' in collisions[Direction.S]:
            #Do not allow going up or down if not touching the floor or not on a rope
            direction = None

        #If we are in a rope, we cannot move right or left (but we can jump right or left)
        if direction in [Direction.E, Direction.W]:
            if 'R' in collisions[None] and not 'F' in collisions[Direction.SE]+collisions[Direction.SW]:
                direction = None

        self.state["last_dir"] = direction
        return super(MontezumaEnv, self).move_hero(direction)
