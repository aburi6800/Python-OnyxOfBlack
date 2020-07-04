# -*- coding: utf-8 -*-
import random
from .singleton import Singleton
from .item import WeaponParams
from .item import ArmorParams
from .item import ShieldParams
from .item import HelmetParams


class Character(object):
    '''
    キャラクタの基底クラス
    '''

    def __init__(self):
        '''
        クラス初期化
        '''

        self.name = ""
        self.level = 0
        self.life = 0
        self.str = 0
        self.dex = 0
        self.exp = 0
        self.gold = 0


class Human(Character):
    '''
    人間のクラス
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super(Human, self).__init__()
        self.head = None
        self.helmet = None
        self.armor = None
        self.shield = None
        self.weapon = None
        self.potion = -1


class Monster(Character):
    '''
    モンスターのクラス
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()
        self.item = None


class Party(Singleton):
    '''
    パーティーを管理するクラス

    Characterクラスの派生クラスを格納したListを管理する
    リストに登録するCharacterの上限はない
    '''

    # パーティーメンバーのリスト
    memberList = []

    def __init__(self):
        '''
        クラス初期化
        '''
        self.memberList = []

    def addMember(self, chr: Character):
        '''
        パーティーメンバー追加
        '''
        self.memberList.append(chr)

    def removeMember(self, idx: int):
        '''
        パーティーメンバー削除

        削除したいパーティーメンバーのリストのインデックスを指定する
        リストに存在しないインデックスを指定した場合は、Exceptionが発生する
        '''
        try:
            del self.memberList[idx]
        except:
            raise Exception(
                "specified a member who doesn't exist.：" + str(idx))


class PlayerParty(Singleton):
    '''
    プレイヤーパーティーのクラス

    Singletonクラスとする
    Humanクラスを格納したListを管理する
    リストに登録するHumanの上限は5とする
    '''

    # パーティーメンバーのリスト
    memberList = []

    def __init__(self):
        '''
        クラス初期化
        '''
        self.memberList = []

    def addMember(self, chr: Human):
        '''
        パーティーメンバー追加
        '''
        if len(self.memberList) < 5:
            self.memberList.append(chr)
        else:
            raise Exception("can't add a member.")

    def removeMember(self, idx: int):
        '''
        パーティーメンバー削除
        '''
        try:
            del self.memberList[idx]
        except:
            raise Exception(
                "specified a member who doesn't exist.：" + str(idx))

    def getAvarageLevel(self):
        '''
        平均レベルを算出
        '''
        avr = 0

        if len(self.memberList) > 0:
            for idx in range(len(self.memberList)):
                if self.memberList[idx] is not None:
                    avr = avr + self.memberList[idx]._level
            avr = avr // len(self.memberList)

        return avr


class HumanPartyGenerator(Singleton):
    '''
    人間のパーティーを自動作成するクラス

    Singletonとする
    人数は1～4人でランダム
    レベルは1～プレイヤーパーティーの平均+2の範囲でランダム
    '''
    @staticmethod
    def generate():
        '''
        人間のパーティー生成
        '''
        # 人数
        count = random.randint(1, 4)

        # レベル
        level = random.randint(1, PlayerParty.getAvarageLevel(PlayerParty) + 2)

        # パーティー生成
        party = Party()
        for _ in range(count):
            party.addMember(HumanGenerator.generate(level))

        return party


class HumanGenerator(Singleton):
    '''
    人間のキャラクターを自動作成するクラス

    Singletonとする
    '''

    @staticmethod
    def generate(_level: int) -> Human:
        '''
        生成する

        Levelを与えるとランダムにパラメタが設定されたHumanクラスのインスタンスを返却する
        '''
        human = Human()

        human.level = _level
        human.life = random.randint(1, _level * 8)
        human.exp = random.randint(1, 50)
        human.str = random.randint(1, _level * 5)
        human.dex = random.randint(1, _level * 5)
        human.gold = random.randint(1, _level * 100)
        human.weapon = WeaponParams().weaponList[random.randint(0, 3)]
        human.armor = ArmorParams().armorList[random.randint(0, 1)]
        human.name = HumanGenerator()._generateName()
        human.head = random.randint(0, 128)

        return human

    @staticmethod
    def _generateName() -> str:
        '''
        名前を生成する
        '''
        _name1 = [
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
        _name2 = ["", "SON", "A", "RY", "N", "NA", "NIA", "PU", "PO", "ON", "Y",
                  "K", "S", "EL", "ER", "CS", "FA", "PI", "C", "CK", "DA", "ON", "B"]

        _idx1 = random.randint(0, len(_name1))
        _idx2 = random.randint(0, len(_name2))

        return _name1[random.randint(0, _idx1)] + _name2[random.randint(0, _idx2)]


class MonsterPartyGenerator(Singleton):
    '''
    モンスターのパーティーを自動生成するクラス

    Singletonとする
    '''

    @staticmethod
    def generate(self):
        '''
        モンスターのパーティー生成
        '''
        pass
