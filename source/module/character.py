# -*- coding: utf-8 -*-
import random
from .singleton import Singleton
from .item import WeaponParams
from .item import ArmorParams
from .item import ShieldParams
from .item import HelmParams

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
 Monster
 - モンスターのクラス
'''
class Monster(Character):

    #
    # クラス初期化
    #
    def __init__(self):
        super(Monster, self).__init__()
        self.item = None


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
    # メンバーリスト取得
    #
    def getMemberList(self):
        return self.memberList

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
class HumanPartyGenerator(Singleton):

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
class HumanGenerator(Singleton):

    @staticmethod
    def generate(_level):
        print("[HumanGenerator]generate target level=" + str(_level))
        human = Human()

        human.level = _level
        human.life = random.randint(1, _level * 8)
        human.exp = random.randint(1, 50)
        human.str = random.randint(1, _level * 5)
        human.dex = random.randint(1, _level * 5)
        human.gold = random.randint(1, _level * 100)
        human.weapon = WeaponParams().weaponList[random.randint(0, 3)]
        human.armor = ArmorParams().armorList[random.randint(0, 1)]
        human.name = HumanGenerator().generateName()
        human.head = random.randint(0, 128)
        print("[HumanGenerator]generated.")
        print(id(human))

        return human

    @staticmethod
    def generateName():
        __name1 = [
            "ANNA", "ARES", "ALEY", "ADAL",
            "BEBY", "BORD", "BEAN", "BOYO",
            "CHRY", "CHAC", "CIEL", "CALM",
            "DALD", "DORY", "DEOL", "DWAF",
            "ENNE", "ELAC", "EYAR", "ERAC",
            "FARD", "FISH", "FEEN", "FOYA",
            "GEAR", "GINN", "GORY", "GANG",
            "HEAR", "HACK", "HIYA", "HIRO",
            "INO", "IYAN", "IELA", "IONC",
            "JOE", "JACK", "JOHN", "JEIB",
            "KARL", "KIM", "KALK", "KORE",
            "LARY", "LESY", "LOKA", "LYCK",
            "MICH", "MARY", "MOMO", "MEAR",
            "NU", "NOE", "NACK", "NICK",
            "OTTO", "ORA", "OMNY", "OWAR",
            "PYCKY", "PACK", "PARY", "PONY",
            "QUER", "QUCK", "QUA", "QUNE",
            "ROBY", "RABI", "RENY", "ROSA",
            "SHERY", "SACK", "SOYA", "SEAN",
            "TERL", "TONY", "TORA", "TANY",
            "UAE", "UNO", "UNIY", "UES",
            "VARY", "VOCK", "VELY", "VYLO",
            "WICK", "WOOD", "WAGO", "WENN",
            "XECK", "XALY", "XYAS", "XORA",
            "YEAN", "YONA", "YOHA", "YACK",
            "ZALY", "ZOE", "ZEE", "ZERA"]
        __name2 = ["", "SON", "A", "RY", "N", "NA", "NIA", "PU", "PO", "ON", "Y", "K", "S", "EL", "ER", "CS", "FA", "PI", "C", "CK", "DA", "ON", "B"]

        __idx1 = random.randint(0, len(__name1))
        __idx2 = random.randint(0, len(__name2))
        print("idx1=" + str(__idx1) + "/idx2=" + str(__idx2))

        return __name1[random.randint(0, __idx1)] + __name2[random.randint(0, __idx2)]


'''
 MonsterPartyGeneratorクラス
 - モンスターのパーティーを自動作成するクラス
 - Singletonとする
'''
class MonsterPartyGenerator(Singleton):

    @staticmethod
    def generate(self):

        pass
