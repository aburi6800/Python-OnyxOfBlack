# -*- coding: utf-8 -*-

class MonsterParam():
    '''
    モンスターの属性を持つクラス
    '''

    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h.int=0, life: int = 0, strength: int = 0, defend: int = 0, dexterity: int = 0, exp: int = 0, gold: int = 0, occr_min: int = 0, occr_max: int = 0, escape: bool = False)
    '''
        クラス初期化
        '''
    self.name = name
    self.life = life
    self.strength = strength
    self.defend = defend
    self.dexterity = dexterity
    self.exp = exp
    self.gold = gold
    self.escape = escape
    self.blt_x = blt_x
    self.blt_y = blt_y
    self.blt_w = blt_w
    self.blt_h = blt_h


class MonsterParams(object):
    '''
    モンスターのリストを持つクラス

    リストの要素はMonsterParamクラスのインスタンスとする
    他モジュールから利用する場合はmonsterParamsをimportすること
    '''
    monsterList = None

    def __init__(self):
        '''
        クラス初期化
        '''
        # モンスターの初期データを登録
        # NAME, BLT_X, BLT_Y, BLT_W, BLT_H, LIFE, STRENGTH, DEFEND, DEXTERITY, EXP, GOLD, OCCR_MIN, OCCR_MAX, ESCAPE
        self.monsterList = (
            MonsterParam("BAT"    ,   0,  0, 16,  8,   1,  2,  2, 12,  1,  0,  8, 20,  True),
            MonsterParam("COBOLD" ,  16,  0, 16, 16,   3,  4,  3,  4,  2,  5,  5, 10,  True),
            MonsterParam("SKELTON",  32,  0, 16, 16,   4,  5,  3,  3,  2,  3,  5, 10, False),
            MonsterParam("ZOMBIE" ,  48,  0, 16, 16,  10, 12, 10,  8,  2,  0,  3,  8, False),
            MonsterParam("AZTEC"  ,  64,  0, 16, 16,   8, 10, 12, 10,  3, 10,  3,  5,  True),
            MonsterParam("GOBLIN" ,  80,  0, 16, 16,  10, 10, 10, 10,  3,  8,  5, 10,  True),
            MonsterParam("WOLF"   ,  96,  0, 16, 16,  20, 18, 16, 20,  3,  0,  7, 14,  True),
            MonsterParam("LION"   , 112,  0, 16, 16,  24, 20, 20, 18,  4,  0,  1,  1,  True),
            MonsterParam("SLIME"  , 128,  0, 16, 16,  28, 22, 12, 12,  4,  0,  5, 10, False),
            MonsterParam("SPIDER" , 144,  0, 16, 16,  22, 20, 18, 20,  4,  0,  5,  7,  True),
            MonsterParam("KRAKEN" ,   0, 16, 32, 32, 100, 30, 30, 30, 10,  0,  1,  1, False),
            MonsterParam("GHOUL"  , 160,  0, 16, 16,  20, 24, 22, 20,  5,  5,  1,  5,  True),
            MonsterParam("ORC"    , 176,  0, 16, 16,  28, 22, 28, 18,  5, 10,  6,  7,  True),
            MonsterParam("MUMMY"  , 192,  0, 16, 16,  22, 24, 20, 18,  5,  0,  5, 10, False),
        )


monsterParams = MonsterParams()
