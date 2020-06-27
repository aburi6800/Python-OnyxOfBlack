# -*- coding: utf-8 -*-
import random
from module.singleton import Singleton

'''
 Characterクラス
 - キャラクタの基本属性を持つクラス
'''
class Character(object):

    #
    # クラス初期化
    #
    def __init__(self):
        self.name = ""
        self.level = 0
        self.life = 0
        self.str = 0
        self.dex = 0
        self.exp = 0
        self.gold = 0


'''
 Human
 - 人間のクラス
'''
class Human(Character):

    #
    # クラス初期化
    #
    def __init__(self):
        super(Human, self).__init__()
        self.head = None
        self.helmet = None
        self.armor = None
        self.shield = None
        self.weapon = None
        self.potion = -1


'''
 Partyクラス
 - パーティーを管理するクラス
'''
class Party():

    #
    # クラス初期化
    #
    def __init__(self):
        print("[Party]initialized.")
        self.memberList = []

    #
    # メンバー追加
    #
    def addMember(self, chr: Character):
        if len(self.memberList) < 5:
            self.memberList.append(chr)
        else:
            raise Exception("can't add a member.")

    #
    # メンバー削除
    #
    def removeMember(self, idx):
        try:
            del self.memberList[idx]
        except:
            raise Exception("specified a member who doesn't exist.：" + str(idx))

    #
    # メンバー取得
    #
    def getMember(self, idx):
        try:
            return self.memberList[idx]
        except:
            raise Exception("specified a member who doesn't exist.：" + str(idx))

    #
    # メンバーリスト取得
    #
    def getMemberList(self):
        return self.memberList


'''
 PlayerPartyクラス
 - プレイヤーパーティーを管理するクラス
 - Singletonとする
'''
class PlayerParty(Singleton):

    memberList = []

    #
    # クラス初期化
    #
    def __init__(self):
        self.memberList = []

    #
    # メンバー追加
    #
    def addMember(self, chr: Human):
        if len(self.memberList) < 5:
            self.memberList.append(chr)
        else:
            raise Exception("can't add a member.")

    #
    # メンバー削除
    #
    def removeMember(self, idx):
        try:
            del self.memberList[idx]
        except:
            raise Exception("specified a member who doesn't exist.：" + str(idx))

    #
    # メンバー取得
    #
    def getMember(self, idx):
        try:
            return self.memberList[idx]
        except:
            raise Exception("specified a member who doesn't exist.：" + str(idx))

    #
    # 平均レベルを算出
    #
    def getAvarageLevel(self):
        avr = 0

        if len(self.memberList) > 0:
            for idx in range(len(self.memberList)):
                if self.memberList[idx] is not None:
                    avr = avr + self.memberList[idx]._level
            avr = avr // len(self.memberList)
        
        return avr


'''
 HumanPartyGeneratorクラス
 - 人間のパーティーを自動作成するクラス
 - Singletonとする
'''
class HumanPartyGenerator():

    @staticmethod
    def generate():

        # 人数
        count = random.randint(1, 4)
        print("[HumanPartyGenerator]COUNT:" + str(count))

        # レベル
        level = random.randint(1, PlayerParty.getAvarageLevel(PlayerParty) + 2)
        print("[HumanPartyGenerator]LEVEL:" + str(level))

        # パーティー生成
        party = Party()
        for _ in range(count):
            party.addMember(HumanGenerator.generate(level))

        return party


'''
 HumanGeneratorクラス
 - 人間のキャラクターを自動作成するクラス
'''
class HumanGenerator():

    @staticmethod
    def generate(__level):
        print("[HumanGenerator]generate target level=" + str(__level))
        human = Human()
        human.level = __level
        human.life = random.randint(1, __level * 10)
        human.exp = random.randint(1, 50)
        human.name = "DUMMYNAME"
        print("[HumanGenerator]generated.")
        print(id(human))
        return human

'''
 MonsterPartyGeneratorクラス
 - モンスターのパーティーを自動作成するクラス
 - Singletonとする
'''
class MonsterPartyGenerator(Singleton):

    @staticmethod
    def generate(self):

        pass
