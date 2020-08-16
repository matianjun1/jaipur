import numpy as np

from consts import DEFAULT_DECK

# 宝石 金 银 丝绸 香料 布 骆驼
# 0, 0, 0, 0, 0, 0, 0


TOTAL = np.array(
    [52]  # 剩余牌数 0: 1
    + [7, 7, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 宝石token 1: 17
    + [6, 6, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 金子token 17: 33
    + [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 银token 33: 49
    + [5, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 丝绸token 49: 65
    + [5, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 香料token 65: 81
    + [4, 3, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]  # 香料token 81: 97
    + [8, 8, 8, 9, 9, 9, 10, 10, 10, 0]  # 5张token 97: 107
    + [4, 4, 4, 5, 5, 5, 6, 6, 6, 0]  # 4张token 107: 117
    + [3, 3, 3, 2, 2, 2, 1, 1, 1, 0]  # 3张token 117: 127
    + [0, 0, 0, 0, 0, 0, 3]  # 市场牌型 127: 134
    + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 当前玩家 手牌 + 骆驼, 分, 额外token数, 额外分 134: 144
    + [0, 0, 0, 0]  # 对手: 手牌数, 骆驼, 分, 额外token数 144: 148
)
PLAYER = np.array([0, 0, 0, 0, 0, 0, 0] + [0, 0, 0])  # 手牌 + 骆驼, 分, 额外token数, 额外分


class GameManager:
    def __init__(self):
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
        self.total[127:134] += self.get_cards(2)
        self.player[:7] = self.get_cards(5)
        self.player2[:7] = self.get_cards(5)

    def reverse(self):
        self.player, self.player2 = self.player2, self.player
        self.score[0], self.score[1] = self.score[1], self.score[0]

    def pprint(self):
        self.total[134:144] = self.player
        self.total[144] = np.sum(self.player2[:6], axis=0)
        self.total[145:148] = self.player2[6:9]
        print(self.total)
        return self.player

    def get_cards(self, nums):
        self.total[0] -= nums
        ans = np.sum(self.deck[:nums], axis=0)
        self.deck = self.deck[nums:]
        return ans

    def get(self, card):
        self.player[:7] += card
        self.total[127:134] += self.get_cards(1)
        return 0

    def get_camels(self):
        camels = self.total[133]
        self.player[6] += camels
        self.total[133] = 0
        self.total[127:134] += self.get_cards(camels)

    def exchange(self, cards):
        self.player[:7] += cards
        self.total[127:134] -= cards

    def sell(self, cards):
        self.player[:7] -= cards

        token = 0
        score = 0
        for i, card in enumerate(cards):
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


if __name__ == "__main__":
    g = GameManager()
    g.pprint()
