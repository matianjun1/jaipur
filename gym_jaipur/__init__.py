from gym.envs.registration import register

register(
    id='jaipur-v1',
    entry_point='gym_jaipur.envs:JaipurEnv',
)
