from const import Card, Seller, Market


class Player:
    __point = 0
    __goods = None
    __camels = 0

    def __init__(self, init_goods: list, gm):
        self.gm = gm
        self.__goods = init_goods
        self.arrange()

    def arrange(self):
        nums = len(self.__goods)
        self.__goods = [good for good in self.__goods if good != Card.骆驼]
        self.__camels += nums - len(self.__goods)

    def see(self):
        print("卡:", self.__goods)
        print("骆驼:", self.__camels)
        print("分:", self.__point)
        self.gm.public()

    def public(self):
        print("卡数:", len(self.__goods))
        print("骆驼:", self.__camels)

    def sell(self, card: Card, nums: int) -> bool:
        for _ in range(nums):
            self.__goods.remove(card)
        point, _ = self.gm.seller.sell(card, nums)
        self.__point += point
        self.see()
        return True

    def get(self, card) -> bool:
        num, _ = self.gm.market.get(card)
        if card == Card.骆驼:
            self.__camels += num
        else:
            self.__goods.append(card)
        self.see()
        return True

    def exchange(self, goods, camels, market) -> bool:
        ok = self.gm.market.exchange(goods, camels, market)
        if ok:
            for good in goods:
                self.__goods.remove(good)
            self.__camels -= camels
            self.__goods.extend(market)
        self.see()
        return ok


class GameManager:
    __deck = None
    seller = None
    __player_A = None
    __player_B = None
    market = None
    __round = None

    def __init__(self):
        self.seller = Seller()
        self.__deck = Card.NewCards(self.seller)
        self.market = Market(self.__deck)

    def start(self) -> (Player, Player):
        self.__player_A = Player(self.__deck[-5:], self)
        self.__deck = self.__deck[:-5]
        self.__player_B = Player(self.__deck[-5:], self)
        self.__deck = self.__deck[:-5]
        self.__round = self.__player_A
        return self.__player_A, self.__player_B

    def public(self):
        self.market.public()
        print("玩家A公开信息:")
        self.__player_A.public()
        print("玩家B公开信息:")
        self.__player_B.public()

    @staticmethod
    def NewGame() -> (Player, Player):
        manager = GameManager()
        return manager.start()


if __name__ == "__main__":
    player_A, player_B = GameManager.NewGame()
    print("玩家A视角~~")
    player_A.see()
    print()
    print("玩家B视角~~")
    player_B.see()
    print()
