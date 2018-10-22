from gym.envs.registration import register

# =============================================================================
# FREEWAY
# =============================================================================
register(id='GE_Freeway-v0',
         entry_point='gridenvs.examples.freeway:FreewayEnv',
         kwargs={'size': 10, "obs_type": "image", "avg_cars": 0.1, "episode_end": "moves"},
         nondeterministic=False)

# =============================================================================
# MONTEZUMA
# =============================================================================
register(id='GE_Montezuma-v0',
         entry_point='gridenvs.examples.montezuma:MontezumaEnv',
         kwargs={"obs_type": "image"},
         nondeterministic=False)

# =============================================================================
# MAZE KEY-DOOR
# =============================================================================
for i in range(5):
    register(id='GE_MazeKeyDoor-v%i' % i,
             entry_point='gridenvs.examples.maze_key_door:key_door_walls',
             kwargs={"obs_type": "image", "level": i, "key_reward": False, 'max_moves': 200},
             nondeterministic=False)

for entrance in ('R', 'L'):
    register(id='GE_MazeKeyDoor%s-v0' % entrance,
             entry_point='gridenvs.examples.maze_key_door:key_door_entrance',
             kwargs={"obs_type": "image", "entrance": entrance, "key_reward": False, 'max_moves': 200},
             nondeterministic=False)

# =============================================================================
# PATH KEY-DOOR
# =============================================================================
register(id='GE_PathKeyDoor-v0',
         entry_point='gridenvs.examples.path_key_door:PathKeyDoorEnv',
         kwargs={"obs_type": "image", 'max_moves': 200},
         nondeterministic=False)

# =============================================================================
# NAVIGATE TO BEACON
# =============================================================================
register(id='GE_MoveToBeacon-v0',
         entry_point='gridenvs.examples.beacon:MoveToBeaconEnv',
         kwargs={"obs_type": "image", 'max_moves': 200},
         nondeterministic=False)