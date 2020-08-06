import random
from enum import Enum, unique


@unique
class Card(Enum):
    宝石 = 1
    金 = 2
    银 = 3
    丝绸 = 4
    香料 = 5
    布 = 6
    骆驼 = 7

    @staticmethod
    def NewCards(seller) -> list:
        ans = []
        for card, item in seller.goods.items():
            ans.extend([card] * (len(item) + 1))
        ans.extend([Card.骆驼] * 8)

        random.shuffle(ans)
        return ans


class Seller:
    def __init__(self):
        self.goods = {
            Card.宝石: [5, 5, 5, 7, 7],
            Card.金: [5, 5, 5, 6, 6],
            Card.银: [5, 5, 5, 5, 5],
            Card.丝绸: [1, 1, 2, 2, 3, 3, 5],
            Card.香料: [1, 1, 2, 2, 3, 3, 5],
            Card.布: [1, 1, 1, 1, 1, 1, 2, 3, 4],
        }
        self.tokens = {
            5: 9,
            4: 5,
            3: 2,
        }
        self.limits = {
            Card.宝石: 2,
            Card.金: 2,
            Card.银: 2,
            Card.丝绸: 1,
            Card.香料: 1,
            Card.布: 1,
        }

    def sell(self, card: Card, num: int) -> (int, bool):
        if num >= 6 or card not in self.goods:
            return 0, False

        if not num >= self.limits[card]:
            return 0, False

        total = self.tokens.get(num, 0)
        total += sum(self.goods[card][-num:])
        self.goods[card] = self.goods[card][:-num]
        return total, True


class Market:
    __market = None
    __deck = None

    def __init__(self, deck: list):
        self.__deck = deck
        self.__market = [
            Card.骆驼,
            Card.骆驼,
            Card.骆驼,
            self.__deck.pop(),
            self.__deck.pop(),
        ]

    def public(self):
        print("市场:", self.__market)
        print("牌库:", len(self.__deck))

    def get(self, card: Card) -> (int, bool):
        if card == Card.骆驼:
            self.__market = [good for good in self.__market if good != Card.骆驼]
            camels = 5 - len(self.__market)
            for _ in range(camels):
                self.__market.append(self.__deck.pop())
            return camels, True
        else:
            self.__market.remove(card)
            self.__market.append(self.__deck.pop())
            return 1, True

    def exchange(self, goods: list, camels: int, market: list) -> bool:
        for good in market:
            self.__market.remove(good)
        for good in goods:
            self.__market.append(good)
        for _ in range(camels):
            self.__market.append(Card.骆驼)
        return True
