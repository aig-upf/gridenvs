from gym.envs.registration import register

# =============================================================================
# FREEWAY
# =============================================================================
register(id='GE_Freeway-v0',
         entry_point='gridenvs.examples.freeway:FreewayEnv',
         kwargs={'size': 10, "avg_cars": 0.1, "episode_end": "moves"},
         nondeterministic=False)

# =============================================================================
# MONTEZUMA
# =============================================================================
register(id='GE_Montezuma-v0',
         entry_point='gridenvs.examples.montezuma:MontezumaEnv',
         nondeterministic=False)

# =============================================================================
# KEY-DOOR
# =============================================================================
for i in range(4):
    register(id='GE_MazeKeyDoor-v%i'%i,
             entry_point='gridenvs.examples.key_door:maze%i'%i,
             kwargs={'max_moves': 200, 'key_reward': True},
             nondeterministic=False)

for d in ['R', 'L']:
    register(id='GE_MazeKeyDoor%c-v0'%d,
             entry_point='gridenvs.examples.key_door:maze%c'%d,
             kwargs={'max_moves': 200},
             nondeterministic=False)

register(id='GE_PathKeyDoor-v0',
        entry_point='gridenvs.examples.key_door:corridor',
        kwargs={'max_moves': 200},
        nondeterministic=False)

for i in range(2):
    register(id='GE_MazeKeyDoorXL-v%i'%i,
             entry_point='gridenvs.examples.key_door:mazeXL%i'%i,
             kwargs={'max_moves': 10000, 'key_reward': True},
             nondeterministic=False)

for i in (10,18,30):
    register(id='GE_MazeKeyDoor-v%i'%i,
         entry_point='gridenvs.examples.key_door:maze%ix%i'%(i, i),
         kwargs={'max_moves': 1000, 'key_reward': True},
         nondeterministic=False)

for i in (10,18,30):
    for j in (1,2,3):
        register(id='GE_MazeKeyDoor%ikey%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:maze%ix%ikey%i'%(i, i, j),
             kwargs={'max_moves': 1000, 'key_reward': True},
             nondeterministic=False)

for i in (8,16):
    for j in (1,2,3):
        register(id='GE_MazeKeyDoor%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:maze%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 1000, 'key_reward': True},
             nondeterministic=False)

for i in (10,18,30):
    for j in (1,2,3):
        register(id='GE_MazeKeyDoor%ikey%icolor%i-v0'%(i, j, j),
             entry_point='gridenvs.examples.key_door:maze%ix%ikey%icolor%i'%(i, i, j, j),
             kwargs={'max_moves': 1000, 'key_reward': True},
             nondeterministic=False)

for i in [10, 18]:
    for j in (1,2,3):
        register(id='GE_MazeKeyDoor%ipick_up_objects1color%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:maze%ix%ipick_up_objects1color%i'%(i, i, j),
             kwargs={'max_moves': 1000, 'key_reward': True},
             nondeterministic=False)

for i in [8, 16]:
    for j in (1,2,3):
        register(id='GE_MazeFourRoom%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:FourRoom%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 1000, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [32]:
    for j in (1,2,3):
        register(id='GE_MazeEightRoom%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:EightRoom%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 1000, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [16]:
    for j in (1,2,3):
        register(id='GE_MazeLava%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Lava%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 1000, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [16]:
    for j in [0,1,2,3,4,5,6]:
        register(id='GE_MazeTreasure%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Treasure%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [16]:
    for j in [0,1,2,3,4,5,6]:
        register(id='GE_MazeTreasure%ikey%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Treasure%ix%ikey%i'%(i, i, j),
             kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [15]:
    for j in [0,1,2]:
        register(id='GE_MazeTreasure%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Treasure%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [15, 16]:
    for j in [0,1,2]:
        register(id='GE_MazeTreasure%ikeyDoorLava%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Treasure%ix%ikeyDoorLava%i'%(i, i, j),
             kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

register(id='GE_MazeTreasure15keyDoorOriginal-v0',
     entry_point='gridenvs.examples.key_door:Treasure15x15keyDoorOriginal',
     kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
     nondeterministic=False)



# =============================================================================
# NAVIGATE TO BEACON
# =============================================================================
register(id='GE_MoveToBeacon-v0',
         entry_point='gridenvs.examples.beacon:MoveToBeaconEnv',
         kwargs={'size' : (10,10), 'max_moves': 200},
         nondeterministic=False)
