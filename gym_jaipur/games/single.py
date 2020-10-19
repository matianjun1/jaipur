import numpy as np

from gym_jaipur.games.consts import DEFAULT_DECK

# 宝石 金 银 丝绸 香料 布 骆驼
# 0, 0, 0, 0, 0, 0, 0


TOTAL = np.array(
    [52]  # 剩余牌数 0: 1
    + [7, 7, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 宝石token 1: 17
    + [6, 6, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 金子token 17: 33
    + [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 银token 33: 49
    + [5, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 丝绸token 49: 65
    + [5, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 香料token 65: 81
    + [4, 3, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]  # 布token 81: 97
    + [8, 8, 8, 9, 9, 9, 10, 10, 10, 0]  # 5张token 97: 107
    + [4, 4, 4, 5, 5, 5, 6, 6, 6, 0]  # 4张token 107: 117
    + [3, 3, 3, 2, 2, 2, 1, 1, 1, 0]  # 3张token 117: 127
    + [0, 0, 0, 0, 0, 0, 3]  # 市场牌型 127: 134
    + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 当前玩家 手牌 + 骆驼, 分, 额外token数, 额外分 134: 144
    + [0, 0, 0, 0],  # 对手: 手牌数, 骆驼, 分, 额外token数 144: 148
    dtype=np.int8,
)
PLAYER = np.array(
    [0, 0, 0, 0, 0, 0, 0] + [0, 0, 0], dtype=np.int8
)  # 手牌 + 骆驼, 分, 额外token数, 额外分


def bc(cards, market):
    total = []
    for x in range(-cards[0], market[0] + 1):
        for y in range(-cards[1], market[1] + 1):
            for z in range(-cards[2], market[2] + 1):
                for l in range(-cards[3], market[3] + 1):
                    for m in range(-cards[4], market[4] + 1):
                        for n in range(-cards[5], market[5] + 1):
                            for o in range(max(sum(cards[:6]) - 7, -cards[6]), 1):
                                t = [x, y, z, l, m, n, o]
                                if (
                                    sum(t) == 0
                                    and 2 <= sum([i for i in t if i > 0]) <= 5
                                ):
                                    total.append(t)
    return total


action_set = [
    # 拿取 动作
    [1, 0, 0, 0, 0, 0, 0],  # 拿 宝石
    [0, 1, 0, 0, 0, 0, 0],  # 拿 金子
    [0, 0, 1, 0, 0, 0, 0],  # 拿 银
    [0, 0, 0, 1, 0, 0, 0],  # 拿 丝绸
    [0, 0, 0, 0, 1, 0, 0],  # 拿 香料
    [0, 0, 0, 0, 0, 1, 0],  # 拿 布
    [0, 0, 0, 0, 0, 0, 1],  # 拿 骆驼
    # 卖 动作
    *[[-i, 0, 0, 0, 0, 0, 0] for i in range(2, 8)],  # 卖 宝石
    *[[0, -i, 0, 0, 0, 0, 0] for i in range(2, 8)],  # 卖 金子
    *[[0, 0, -i, 0, 0, 0, 0] for i in range(2, 8)],  # 卖 银
    *[[0, 0, 0, -i, 0, 0, 0] for i in range(1, 8)],  # 卖 丝绸
    *[[0, 0, 0, 0, -i, 0, 0] for i in range(1, 8)],  # 卖 香料
    *[[0, 0, 0, 0, 0, -i, 0] for i in range(1, 8)],  # 卖 布
    # 交换 动作
    # *bc([1, 1, 1, 1, 1, 1, 1], [1, 0, 1, 2, 0, 1, 0]),
]

action_set = {
    i: np.array(
        v,
        dtype=np.int8,
    )
    for i, v in enumerate(action_set)
}


class GameManager:
    __game_over = False

    def __init__(self):
        self.__act_set = {
            0: self.get,
            1: self.get_camels,
            2: self.exchange,
            3: self.sell,
        }
        # 初始化
        self.total = np.copy(TOTAL)
        self.deck = np.copy(DEFAULT_DECK)
        self.player = np.copy(PLAYER)
        self.player2 = np.copy(PLAYER)

        # 打乱牌堆
        np.random.default_rng().shuffle(self.deck)

        # 打乱额外token
        np.random.default_rng().shuffle(self.total[97:106])
        np.random.default_rng().shuffle(self.total[107:116])
        np.random.default_rng().shuffle(self.total[117:126])

        # 发牌
        self.total[127:134] += self._get_cards(2)
        self.player[:7] = self._get_cards(5)
        self.player2[:7] = self._get_cards(5)

    def reverse(self):
        self.player, self.player2 = self.player2, self.player
        self.score[0], self.score[1] = self.score[1], self.score[0]

    def get_obs(self):
        self.total[134:144] = self.player
        self.total[144] = np.sum(self.player2[:6], axis=0)
        self.total[145:148] = self.player2[6:9]
        # print(self.total)
        return self.total

    def pprint(self):
        t = self.total
        return f"""
        剩余牌数 {t[0]}
        宝石token {t[1: 17]}
        金子token {t[17: 33]}
        银token {t[33: 49]}
        丝绸token {t[49: 65]}
        香料token {t[65: 81]}
        布token {t[81: 97]}
        5张token {t[97: 107]}
        4张token {t[107: 117]}
        3张token {t[117: 127]}
        市场牌型 {t[127: 134]}
        当前玩家 手牌 + 骆驼, 分, 额外token数, 额外分 {t[134: 144]}
        对手: 手牌数, 骆驼, 分, 额外token数 {t[144: 148]}
        """

    def _get_cards(self, nums):
        self.total[0] -= nums
        ans = np.sum(self.deck[:nums], axis=0)
        self.deck = self.deck[nums:]
        return ans

    def get(self, cards):
        # 只拿1种, 且只拿1张
        if np.sum(cards != 0, axis=0) != 1 or np.sum(cards, axis=0) != 1:
            return -5

        # 已经7张手牌上限
        if np.sum(self.player[:6], axis=0) == 7:
            return -5

        new_market = self.total[127:134] - cards
        # 不能拿没有的
        if np.sum(new_market < 0, axis=0) != 0:
            return -5

        self.player[:7] += cards
        self.total[127:134] = new_market
        self.total[127:134] += self._get_cards(1)
        return -0.01

    def get_camels(self, cards):
        # 只拿1种, 且只拿骆驼
        if np.sum(cards != 0, axis=0) != 1 or cards[6] != 1 or self.total[133] == 0:
            return -5

        # 一次性拿取所有骆驼
        camels = self.total[133]
        self.player[6] += camels
        self.total[133] = 0
        self.total[127:134] += self._get_cards(camels)
        return -0.01

    def exchange(self, cards):
        # 不能去交换场上的骆驼
        if cards[6] > 0:
            return -5

        gets = np.sum(cards > 0, axis=0)
        drops = np.sum(cards < 0, axis=0)
        # 必须2张起换, 且拿的和丢的个数一样
        if gets < 2 or gets + drops != 0:
            return -5

        new_player = self.player[:7] + cards
        # 不能弃没有的
        if np.sum(new_player < 0, axis=0) != 0:
            return -5

        # 超过7张手牌上限
        if np.sum(new_player[:6], axis=0) > 7:
            return -5

        self.player[:7] = new_player

        new_market = self.total[127:134] - cards
        # 不能拿没有的
        if np.sum(new_market < 0, axis=0) != 0:
            return -5

        self.total[127:134] = new_market
        return 0.1

    def sell(self, cards):
        # 只卖1种, 贵重物2张起卖, 其他1张起
        if np.sum(cards != 0, axis=0) != 1 or (
            np.sum(cards[:3], axis=0) > -2 and np.sum(cards[3:6], axis=0) > -1
        ):
            return -5

        new_player = self.player[:7] + cards

        # 不能卖没有的
        if np.sum(new_player < 0, axis=0) != 0:
            return -5

        self.player[:7] = new_player

        token = 0
        score = 0
        for i, card in enumerate(-cards):
            if card > 0:
                x = 16 * i + 1
                score += np.sum(self.total[x : x + card], axis=0)
                self.total[x : x + 16 - card] = self.total[x + card : x + 16]

                if card == 3:
                    token += self.total[117]
                    self.total[117:126] = self.total[118:127]
                elif card == 4:
                    token += self.total[107]
                    self.total[107:116] = self.total[108:117]
                elif card >= 5:
                    token += self.total[97]
                    self.total[97:106] = self.total[98:107]

                break

        self.player[7] += score
        if token > 0:
            self.player[8] += 1
            self.player[9] += token

        return token + score

    def _game_over(self):
        if self.total[0] < 0:
            self.__game_over = True
            return True

        zeros = 0
        for i in range(6):
            if np.sum(self.total[i * 16 + 1 : i * 16 + 17], axis=0) == 0:
                zeros += 1

        if zeros >= 3:
            self.__game_over = True

        return zeros >= 3

    def game_over(self):
        return self.__game_over

    def act(self, a):
        act = action_set[a]
        total = np.sum(act, axis=0)
        if total == 0:
            reward = self.exchange(act)
        elif total == 1:
            if act[6] == 1:
                reward = self.get_camels(act)
            else:
                reward = self.get(act)
        elif total < 0:
            reward = self.sell(act)

        # 是否游戏结束
        if self._game_over():
            # 骆驼判定
            if self.total[140] > self.total[145]:
                reward += 5
                self.total[141] += 5
            elif self.total[140] < self.total[145]:
                self.total[146] += 5

        return reward


if __name__ == "__main__":
    mm = 0
    for x in range(0, 8):
        for y in range(0, 8 - x):
            for z in range(0, 8 - x - y):
                for l in range(0, 8 - x - y - z):
                    for m in range(0, 8 - x - y - z - l):
                        for n in range(0, 8 - x - y - z - l - m):
                            for o in range(0, 6):
                                t = [x, y, z, l, m, n, o]
                                if sum(t) < 1 or sum(t[:6]) > 7:
                                    continue
                                for _x in range(0, 6):
                                    for _y in range(0, 6 - _x):
                                        for _z in range(0, 6 - _x - _y):
                                            for _l in range(0, 6 - _x - _y - _z):
                                                for _m in range(
                                                    0, 6 - _x - _y - _z - _l
                                                ):
                                                    for _n in range(
                                                        0, 6 - _x - _y - _z - _l - _m
                                                    ):
                                                        for _o in range(0, 6 - _x - _y - _z - _l - _m - _n):
                                                            _t = [
                                                                _x,
                                                                _y,
                                                                _z,
                                                                _l,
                                                                _m,
                                                                _n,
                                                                _o,
                                                            ]
                                                            mmm = len(bc(t, _t))
                                                            if mmm >= mm:
                                                                print(mmm, t, _t)
                                                                mm = mmm
