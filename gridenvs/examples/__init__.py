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

for i in [16]:
    for j in [0,1,2]:
        register(id='GE_MazeLava%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Lava%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 1000, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [16]:
    for j in [0,1,2]:
        register(id='GE_MazeTreasure%ikeyDoor%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Treasure%ix%ikeyDoor%i'%(i, i, j),
             kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [16]:
    for j in [0,1,2]:
        register(id='GE_MazeTreasure%ikeyDoorLava%i-v0'%(i, j),
             entry_point='gridenvs.examples.key_door:Treasure%ix%ikeyDoorLava%i'%(i, i, j),
             kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
             nondeterministic=False)

for i in [16]:
    for j in [0,1,2]:
        register(id='GE_MazeTreasure8x16keyDoorLava%i-v0'%(j),
             entry_point='gridenvs.examples.key_door:Treasure8x%ikeyDoorLava%i'%(i, j),
             kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':False},
             nondeterministic=False)

register(id='GE_MazeTreasure16keyDoorOriginal-v0',
     entry_point='gridenvs.examples.key_door:Treasure16x16keyDoorOriginal',
     kwargs={'max_moves': 300, 'key_reward': True, 'blocking_walls':True},
     nondeterministic=False)



# =============================================================================
# NAVIGATE TO BEACON
# =============================================================================
register(id='GE_MoveToBeacon-v0',
         entry_point='gridenvs.examples.beacon:MoveToBeaconEnv',
         kwargs={'size' : (10,10), 'max_moves': 200},
         nondeterministic=False)
