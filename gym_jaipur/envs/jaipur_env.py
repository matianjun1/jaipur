import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

from gym_jaipur.games.single import GameManager, action_set


class JaipurEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        self.g = GameManager()
        self.observation_space = spaces.Box(
            low=0, high=52, dtype=np.int8, shape=(self.g.total.shape[0],)
        )
        self.action_space = spaces.Discrete(len(action_set))

    def _get_obs(self):
        return self.g.get_obs()

    def step(self, a):
        reward = self.g.act(a)
        ob = self._get_obs()
        # if reward != -1000:
        #     print(a, reward)

        return ob, reward, self.g.game_over(), {}

    def reset(self):
        self.g = GameManager()
        return self._get_obs()

    def render(self, mode="human"):
        print(self.g.pprint())

    def close(self):
        pass
