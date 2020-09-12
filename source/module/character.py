# -*- coding: utf-8 -*-
import random
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
        self.maxlife = 0
        self.life = 0
        self.strength = 0
        self.defend = 0
        self.dexterity = 0
        self.exp = 0
        self.gold = 0

    def levelup(self):
        '''
        レベルアップ処理
        '''
        # 増分値
        addPoint = 24
        # ライフの増分
        addLife = random.randint(1, 8)
        addPoint = addPoint - addLife
        # 強さの増分
        addStrength = random.randint(1, 8)
        addPoint = addPoint - addStrength
        # 防御力の増分
        addDefend = random.randint(1, 8)
        addPoint = addPoint - addDefend
        # 素早さの増分
        addDexterity = addPoint

        # パラメータ増加
        self.level += 1
        self.maxlife += addLife
        self.life += addLife
        self.strength += addStrength
        self.defend += addDefend
        self.dexterity += addDexterity
        self.exp = 0


class Human(Character):
    '''
    人間のクラス

    Characterクラスを継承
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super(Human, self).__init__()
        self.head = None
        self.body = None
        self.helmet = None
        self.armor = None
        self.shield = None
        self.weapon = None
        self.potion = -1
        self.x = 0
        self.y = 0


class Monster(Character):
    '''
    モンスターのクラス

    Characterクラスを継承
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()
        self.item = None
        self.x = 0
        self.y = 0


class Party(object):
    '''
    パーティーを管理するクラス

    Characterクラスの派生クラスを格納したListを管理する
    リストに登録するCharacterの上限はない
    このクラスを直接使用せず、派生クラスのplayerParty、enemyPartyを使用すること
    '''

    # パーティーメンバーのリスト
    memberList = []

    def __init__(self):
        '''
        クラス初期化
        '''
        # パーティーメンバーのリスト
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


class PlayerParty(Party):
    '''
    プレイヤーパーティーのクラス

    Partyクラスを継承
    Humanクラスを格納したListを管理する
    リストに登録するHumanの上限は5とする
    直接このクラスを使用せず、インスタンスを格納したplayerPartyをimportして使用すること
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # プレイヤーパーティーの位置と方向
        self.x = 0
        self.y = 0
        self.direction = 0

        # プレイヤーパーティーの直前の位置と方向
        self.x_save = 0
        self.y_save = 0
        self.direction_save = 0

        # 状況のフラグ
        self.isEscape = False

        if __debug__:
            print("PlayerParty : Initialized.")

    def resotreSaveData(self, playerParty):
        '''
        セーブデータの復元処理
        '''
        super().__init__()

        # メンバーリストを復元
        self.memberList = playerParty.memberList

        # プレイヤーパーティーの位置と方向
        self.x = playerParty.x
        self.y = playerParty.y
        self.direction = playerParty.direction

        # プレイヤーパーティーの直前の位置と方向
        self.x_save = playerParty.x_save
        self.y_save = playerParty.y_save
        self.direction_save = playerParty.direction_save

        # 状況のフラグ
        self.isEscape = playerParty.isEscape

        if __debug__:
            print("PlayerParty : Restored.")

    def initialize(self):
        '''
        初期化処理
        '''
        self.__init__()

    def addMember(self, chr: Human):
        '''
        パーティーメンバー追加
        '''
        if len(self.memberList) < 5:
            self.memberList.append(chr)
        else:
            raise Exception("can't add a member.")

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

    def saveCondition(self):
        '''
        状態を保存する
        '''
        self.x_save = self.x
        self.y_save = self.y
        self.direction_save = self.direction
        if __debug__:
            print("PlayerParty : Condition saved. x={:02d}".format(
                self.x_save) + ",y={:02d}".format(self.y_save) + ",direction={:01d}".format(self.direction_save))

    def restoreCondition(self):
        '''
        状態を復元する
        '''
        self.x = self.x_save
        self.y = self.y_save
        self.direction = self.direction_save
        if __debug__:
            print("PlayerParty : Condition restored. x={:02d}".format(
                self.x) + ",y={:02d}".format(self.y) + ",direction={:01d}".format(self.direction))


playerParty = PlayerParty()


class HumanPartyGenerator(object):
    '''
    人間のパーティーを自動作成するクラス

    人数は1～4人でランダム
    レベルは1～プレイヤーパーティーの平均+2の範囲でランダム
    レベルを引数とし、Humanオブジェクトを格納したリストを返却する
    '''
    @staticmethod
    def generate(level: int = 1):
        '''
        人間のパーティー生成
        '''
        # 人数
        _count = random.randint(1, 5)

        # パーティー生成
        _memberList = []
        for _ in range(_count):
            _memberList.append(HumanGenerator.generate(level))

        return _memberList


class HumanGenerator(object):
    '''
    人間のキャラクターを自動作成するクラス
    '''

    @staticmethod
    def generate(_level: int) -> Human:
        '''
        生成する

        Levelを与えるとランダムにパラメタが設定されたHumanクラスのインスタンスを返却する
        '''
        human = Human()

        human.level = _level
        for _ in range(_level):
            human.levelup()

        human.exp = random.randint(1, 50)
        human.gold = random.randint(1, _level * 100)
        human.weapon = WeaponParams().weaponList[random.randint(0, 3)]
        if random.randint(0, 2) == 0:
            human.armor = None
        else:
            human.armor = ArmorParams().armorList[random.randint(0, 1)]
        human.name = HumanGenerator()._generateName()
        human.head = random.randint(0, 127)
        human.body = random.randint(0, 2)

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

        _idx1 = random.randint(0, len(_name1) - 1)
        _idx2 = random.randint(0, len(_name2) - 1)

        return _name1[random.randint(0, _idx1)] + _name2[random.randint(0, _idx2)]


class EnemyParty(Party):
    '''
    敵パーティー

    Partyクラスを継承
    HumanクラスまたはMonsterクラスを格納したListを管理する
    直接このクラスを使用せず、インスタンスを格納したenemyPartyをimportして使用すること
    '''

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.memberList = []

    def isEscape(self) -> bool:
        if isinstance(self.memberList[0], Monster):
            return self.memberList[0].escape
        else:
            True


enemyParty = EnemyParty()


class EnemyPartyGenerator(object):
    '''
    敵のパーティーを自動生成するクラス
    '''

    @staticmethod
    def generate(enemyClass):
        '''
        敵のパーティー生成

        enemyClassがHuman型の場合はPlayerPartyGeneratorの結果をそのまま返却する（使用するレベルはenemyClassが持っているレベル）
        以外の場合はenemyClassの持つ情報を元に新しくmemberListを生成して返却する
        '''
        _memberList = []
        if isinstance(enemyClass, Human):
            enemyClass.occr_min = 1
            enemyClass.occr_max = 5

        _count = random.randint(enemyClass.occr_min, enemyClass.occr_max)
        _x_step = 94 // _count if _count < 12 else 7
        for idx in range(_count):
            if isinstance(enemyClass, Human):
                _monster = HumanGenerator.generate(enemyClass.level)
                _monster.exp = enemyClass.level
            else:
                _monster = Monster()
                _monster.name = enemyClass.name + " " + chr(65 + idx)
                _monster.blt_x = enemyClass.blt_x
                _monster.blt_y = enemyClass.blt_y
                _monster.blt_w = enemyClass.blt_w
                _monster.blt_h = enemyClass.blt_h
                _monster.life = enemyClass.life + \
                    random.randint(0, enemyClass.life // 10 + 1)
                _monster.maxlife = _monster.life
                _monster.strength = enemyClass.strength + \
                    random.randint(0, enemyClass.strength // 10 + 1)
                _monster.defend = enemyClass.defend + \
                    random.randint(0, enemyClass.defend // 10 + 1)
                _monster.dexterity = enemyClass.dexterity + \
                    random.randint(0, enemyClass.dexterity // 10 + 1)
                _monster.exp = enemyClass.exp
                _monster.gold = enemyClass.gold
                _monster.escape = enemyClass.escape

            # 表示位置
            _monster.x = (idx * _x_step if idx < 12 else (idx - 12) * _x_step) + (
                188 - (_count * _x_step) / 2 if _count < 12 else 188 - (12 * _x_step) / 2)
            if isinstance(_monster, Monster) and _monster.blt_h == 32:
                _monster.y = 96
            else:
                _monster.y = random.randint(100, 112) if _count < 12 else (
                    random.randint(102, 106) if idx < 12 else random.randint(116, 120))

            _memberList.append(_monster)

        return _memberList
