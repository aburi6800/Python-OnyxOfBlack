# -*- coding: utf-8 -*-
import random
from typing import List

from module.constant.alignment import Alignment
from module.constant.direction import Direction
from module.constant.itemType import ItemType
from module.params.armor import armorParams
from module.params.weapon import weaponParams


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
        self.isEscape = False
        self.isPlayer = False
        self.blt_w = 0
        self.bly_h = 0
        self.x = 0
        self.y = 0
        self.hasItem = False

    def setDisplayPosition(self, _count: int, _idx: int) -> None:
        '''
        敵キャラクターの表示位置を算出して設定する。\n
        引数として、敵パーティーのメンバー総数と、対象キャラクターのインデックスを指定する。
        '''
        if _count < 12:
            _x_step = (104 - self.blt_w) / (_count + 1)
            self.x = 132 + ((_idx + 1) * _x_step)
        else:
            if _idx < 12:
                _x_step = (104 - self.blt_w) / 11
                self.x = 132 + ((_idx + 1) * _x_step)
            else:
                _x_step = (104 - self.blt_w) / ((_count - 12) + 1)
                self.x = 132 + (((_idx - 12) + 1) * _x_step)
        if isinstance(self, Monster) and self.blt_h == 32:
            self.y = 98
        else:
            self.y = random.randint(100, (128 - self.blt_h)) if _count < 12 else (
                random.randint(100, (128 - self.blt_h)) if _idx < 12 else random.randint(110, (132 - self.blt_h)))


class Human(Character):
    '''
    人間のクラス\n
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
        self.alignment = Alignment.GOOD

    def levelup(self) -> None:
        '''
        レベルアップ処理
        '''
        # 増分値
        addPoint = 10
        # ライフの増分
        addLife = random.randint(2, addPoint - 5)
        addPoint = addPoint - addLife
        # 強さの増分
        addStrength = random.randint(1, addPoint - 3)
        addPoint = addPoint - addStrength
        # 防御力の増分
        addDefend = random.randint(1, addPoint - 2)
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

        self.alignment = Alignment.EVIL


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

    def addMember(self, chr: Character) -> None:
        '''
        パーティーメンバー追加
        '''
        self.memberList.append(chr)

    def removeMember(self, idx: int) -> None:
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
    eventFlg = [0] * 256

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 方向に対する増分
        self.VX = (0, 1, 0, -1)
        self.VY = (-1, 0, 1, 0)

        # プレイヤーパーティーの位置と方向
        self.x = 0
        self.y = 0
        self.direction = 0

        # プレイヤーパーティーの直前の位置と方向
        self.x_save = 0
        self.y_save = 0
        self.direction_save = 0

        # 状況のフラグ
        self.isEscaped = False

        # イベントフラグ
        self.eventFlg = [0] * 100

        if __debug__:
            print("PlayerParty : Initialized.")

    def resotreSaveData(self, playerParty) -> None:
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
        self.isEscaped = playerParty.isEscaped

        # イベントフラグ
        self.eventFlg = playerParty.eventFlg

        if __debug__:
            print("PlayerParty : Restored.")

    def initialize(self) -> None:
        '''
        初期化処理
        '''
        self.__init__()

    def addMember(self, chr: Human) -> None:
        '''
        パーティーメンバー追加
        '''
        if len(self.memberList) < 5:
            self.memberList.append(chr)
        else:
            raise Exception("can't add a member.")

    def getAvarageLevel(self) -> int:
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

    def saveCondition(self) -> None:
        '''
        状態を保存する
        '''
        self.x_save = self.x
        self.y_save = self.y
        self.direction_save = self.direction
        if __debug__:
            print("PlayerParty : Condition saved. x={:02d}".format(
                self.x_save) + ",y={:02d}".format(self.y_save) + ",direction={:01d}".format(self.direction_save))

    def restoreCondition(self) -> None:
        '''
        状態を復元する
        '''
        self.x = self.x_save
        self.y = self.y_save
        self.direction = self.direction_save
        if __debug__:
            print("PlayerParty : Condition restored. x={:02d}".format(
                self.x) + ",y={:02d}".format(self.y) + ",direction={:01d}".format(self.direction))

    def turnLeft(self) -> None:
        '''
        左を向く
        '''
        # 状態を保存
        self.saveCondition()
        # 方向を変える
        self.direction -= 1
        if self.direction < Direction.NORTH:
            self.direction = Direction.WEST

    def turnRight(self) -> None:
        '''
        右を向く
        '''
        # 状態を保存
        self.saveCondition()
        # 方向を変える
        self.direction += 1
        if self.direction > Direction.WEST:
            self.direction = Direction.NORTH

    def turnBack(self) -> None:
        '''
        後ろを向く
        '''
        # 状態を保存
        self.saveCondition()
        # 方向を変える
        self.direction = (self.direction + 2) % 4

    def moveForward(self) -> None:
        '''
        前に進む
        '''
        # 状態を保存
        self.saveCondition()
        # 座標を変更
        self.x = self.x + self.VX[self.direction]
        self.y = self.y + self.VY[self.direction]


playerParty = PlayerParty()


class HumanPartyGenerator(object):
    '''
    人間のパーティーを自動作成するクラス

    人数は1～4人でランダム
    レベルは1～プレイヤーパーティーの平均+2の範囲でランダム
    レベルを引数とし、Humanオブジェクトを格納したリストを返却する
    '''
    @staticmethod
    def generate(level: int = 1, alignment: int = Alignment.GOOD) -> List:
        '''
        人間のパーティー生成
        '''
        # 人数
        _count = random.randint(1, 5)

        # パーティー生成
        _memberList = []
        for _idx in range(_count):
            _human = HumanGenerator.generate(level, alignment)
            _human.setDisplayPosition(_count, _idx)
            _memberList.append(_human)

        return _memberList


class HumanGenerator(object):
    '''
    人間のキャラクターを自動作成するクラス
    '''

    @staticmethod
    def generate(_level: int, _alignment: int = Alignment.GOOD) -> Human:
        '''
        生成する

        Levelを与えるとランダムにパラメタが設定されたHumanクラスのインスタンスを返却する
        '''
        human = Human()

        for _ in range(_level):
            human.levelup()

        human.exp = random.randint(0, 10) + _level * 5
        human.gold = random.randint(1, _level * 100)
        human.weapon = weaponParams[random.randint(0, 3)]
        if random.randint(0, 2) == 0:
            human.armor = None
        else:
            human.armor = armorParams[random.randint(0, 1)]
        human.name = HumanGenerator()._generateName()
        human.head = random.randint(0, 159)
        human.body = random.randint(0, 2)
        human.alignment = _alignment
        human.isEscape = True if _alignment == Alignment.GOOD else False
        human.blt_w = 8
        human.blt_h = 19

        return human

    @staticmethod
    def _generateName() -> str:
        '''
        名前を生成する
        '''
        _name1 = [
            "ANNA", "ARES", "ALEY", "ADAL", "AR",
            "BEBY", "BORD", "BEAN", "BOYO", "BO",
            "CHRY", "CHAC", "CIEL", "CALM", "CAN",
            "DALD", "DORY", "DEOL", "DWAF", "DON",
            "ENNE", "ELAC", "EYAR", "ERAC", "EMY",
            "FARD", "FISH", "FEEN", "FOYA", "FORT",
            "GEAR", "GINN", "GORY", "GANG", "GON",
            "HEAR", "HACK", "HIYA", "HIRO", "HELL",
            "INO", "IYAN", "IELA", "IONC", "IN",
            "JOE", "JACK", "JOHN", "JEIB", "JAY",
            "KARL", "KIM", "KALK", "KORE", "KAN",
            "LARY", "LESY", "LOKA", "LYCK", "LA",
            "MICH", "MARY", "MOMO", "MEAR", "MEGA",
            "NU", "NOE", "NACK", "NICK", "NEL",
            "OTTO", "ORA", "OMNY", "OWAR", "OL",
            "PYCKY", "PACK", "PARY", "PONY", "PU",
            "QUER", "QUCK", "QUA", "QUNE", "QEL",
            "ROBY", "RABI", "RENY", "ROSA", "REI",
            "SHERY", "SACK", "SOYA", "SEAN", "SOL",
            "TERL", "TONY", "TORA", "TANY", "TOM",
            "UAE", "UNO", "UNIY", "UES", "US",
            "VARY", "VOCK", "VELY", "VYLO", "VON",
            "WICK", "WOOD", "WAGO", "WENN", "WARE",
            "XECK", "XALY", "XYAS", "XORA", "XAN",
            "YEAN", "YONA", "YOHA", "YACK", "YRE",
            "ZALY", "ZOE", "ZEE", "ZERA", "ZOL"]
        _name2 = ["", "SON", "A", "RY", "N", "NA", "NIA", "PU", "PO", "ON", "Y",
                  "K", "S", "EL", "ER", "CS", "FA", "PI", "C", "CK", "DA", "ON", "B"]

        _idx1 = random.randint(0, len(_name1) - 1)
        _idx2 = random.randint(0, len(_name2) - 1)

        return _name1[random.randint(0, _idx1)] + _name2[random.randint(0, _idx2)]


class EnemyParty(Party):
    '''
    敵パーティークラス\n
    Partyクラスを継承。\n
    HumanクラスまたはMonsterクラスを格納したListを管理する。\n
    利用するクラスでは、直接このクラスを使用せず、インスタンスを格納したenemyPartyをimportして使用すること。\n
    '''

    def __init__(self):
        super().__init__()

        # レベル
        self.level = 0

        # アイテム
        self.item = None

        # アイテム種別
        self.itemType = None

    def initialize(self) -> None:
        self.memberList = []

    def generate(self, enemyClass) -> None:
        '''
        敵パーティーを設定する\n
        パーティーの生成はEnemyPartyGeneratorメソッドで行い、生成したパーティーのレベルを保存する
        '''
        self.memberList = EnemyPartyGenerator.generate(enemyClass)
        self.level = self.memberList[0].level

        if self.memberList[0].hasItem and random.randint(0, 32) == 0:
            # アイテムを持っている場合、ランダムで選出
            if self.memberList[0].name[0:5] == "HIDER":
                self.item = armorParams[5]
                self.itemType = ItemType.ARMOR
            else:
                _r = random.randint(0, 4)
                if _r == 0 or _r == 1:
                    # 武器を選出
                    _rndMin = enemyParty.level - 1
                    _rndMax = enemyParty.level + 2
                    self.item = weaponParams[random.randint(
                        _rndMin, _rndMax if _rndMax < 9 else 8)]
                    self.item.attack = int(self.item.attack * 1.5)
                    self.itemType = ItemType.WEAPON
                elif _r == 2 or _r == 3:
                    # 鎧を選出
                    _rndMin = (enemyParty.level - 1) // 2
                    _rndMax = (enemyParty.level + 2) // 2 + 1
                    self.item = armorParams[random.randint(
                        _rndMin, _rndMax if _rndMax < 5 else 4)]
                    self.item.armor = int(self.item.armor * 1.5)
                    self.itemType = ItemType.ARMOR

    def isEscape(self) -> bool:
        if isinstance(self.memberList[0], Monster):
            return self.memberList[0].isEscape
        else:
            True


enemyParty = EnemyParty()


class EnemyPartyGenerator(object):
    '''
    敵のパーティーを自動生成するクラス
    '''

    @staticmethod
    def generate(enemyClass) -> List:
        '''
        敵のパーティー生成

        enemyClassがHuman型の場合はPlayerPartyGeneratorの結果をそのまま返却する（使用するレベルはenemyClassが持っているレベル）
        以外の場合はenemyClassの持つ情報を元に新しくmemberListを生成して返却する
        '''
        # パーティーのメンバーリスト初期化
        _memberList = []

        if isinstance(enemyClass, Human):
            _memberList = HumanPartyGenerator.generate(
                enemyClass.level, Alignment.GOOD if random.randint(1, 6) < 5 else Alignment.EVIL)
            if __debug__:
                print("enemy party generated.")
                for v in _memberList:
                    print(v)
            return _memberList

        _count = random.randint(enemyClass.occr_min, enemyClass.occr_max)

        for idx in range(_count):
            _monster = Monster()
            _monster.name = enemyClass.name + " " + chr(65 + idx)
            _monster.blt_x = enemyClass.blt_x
            _monster.blt_y = enemyClass.blt_y
            _monster.blt_w = enemyClass.blt_w
            _monster.blt_h = enemyClass.blt_h
            _monster.level = enemyClass.level
            _monster.life = enemyClass.life + \
                random.randint(0, enemyClass.life // 5 + 1)
            _monster.maxlife = _monster.life
            _monster.strength = enemyClass.strength + \
                random.randint(0, enemyClass.strength // 5 + 1)
            _monster.defend = enemyClass.defend + \
                random.randint(0, enemyClass.defend // 5 + 1)
            _monster.dexterity = enemyClass.dexterity + \
                random.randint(0, enemyClass.dexterity // 5 + 1)
            _monster.exp = enemyClass.exp
            _monster.gold = enemyClass.gold
            _monster.isEscape = enemyClass.isEscape
            _monster.hasItem = enemyClass.hasItem

            # 表示位置
            _monster.setDisplayPosition(_count, idx)

            _memberList.append(_monster)

        if __debug__:
            print("enemy party generated.")
            for v in _memberList:
                print(v)

        return _memberList
