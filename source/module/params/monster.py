# -*- coding: utf-8 -*-

class MonsterParam():
    '''
    モンスターの属性クラス
    '''
    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int=0, life: int = 0, strength: int = 0, defend: int = 0, dexterity: int = 0, exp: int = 0, gold: int = 0, occr_min: int = 0, occr_max: int = 0, escape: bool = False):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.life = life
        self.strength = strength
        self.defend = defend
        self.dexterity = dexterity
        self.exp = exp
        self.gold = gold
        self.occr_min = occr_min
        self.occr_max = occr_max
        self.escape = escape


'''
モンスターの属性のディクショナリ

リストの要素はMonsterParamクラスのインスタンス
'''
monsterParams = {
    "BAT_LV1":MonsterParam("BAT", 0, 0, 16, 8, 2, 2, 1, 7, 3, 0, 4, 10, True),
    "BAT_LV2":MonsterParam("BAT", 0, 0, 16, 8, 4, 4, 1, 8, 4, 0, 8, 20, True),
    "COBOLD_LV1":MonsterParam("COBOLD", 16, 0, 16, 16, 5, 5, 3, 4, 5, 2, 2, 5, True),
    "SKELTON_LV1":MonsterParam("SKELTON", 32, 0, 16, 16, 6, 4, 2, 3, 5, 1, 3, 5, True),
    "ZOMBIE_LV1":MonsterParam("ZOMBIE", 48, 0, 16, 16, 8, 5, 4, 1, 5, 0, 2, 5, False),
    "COBOLD_LV2":MonsterParam("COBOLD", 16, 0, 16, 16, 7, 7, 5, 5, 6, 2, 5, 10, True),
    "SKELTON_LV2":MonsterParam("SKELTON", 32, 0, 16, 16, 8, 6, 4, 4, 6, 1, 5, 10, True),
    "ZOMBIE_LV2":MonsterParam("ZOMBIE", 48, 0, 16, 16, 10, 7, 3, 2, 6, 0, 4, 8, False),
    "AZTEC_LV1":MonsterParam("AZTEC", 64, 0, 16, 16, 8, 12, 10, 6, 10, 20, 3, 5, True),
    "GOBLIN_LV1":MonsterParam("GOBLIN", 80, 0, 16, 16, 10, 10, 12, 5, 8, 10, 3, 5, True),
    "AZTEC_LV2":MonsterParam("AZTEC", 64, 0, 16, 16, 22, 20, 18, 5, 15, 20, 5, 8, True),
    "GOBLIN_LV2":MonsterParam("GOBLIN", 80, 0, 16, 16, 26, 22, 16, 5, 15, 10, 5, 10, True),
    "WOLF_LV1":MonsterParam("WOLF", 96, 0, 16, 16, 10, 10, 6, 10, 12, 0, 3, 5, True),
    "LION_LV1":MonsterParam("LION", 122, 0, 16, 16, 20, 14, 6, 8, 30, 0, 1, 1, True),
    "SLIME_LV1":MonsterParam("SLIME", 128, 0, 16, 16, 12, 12, 6, 10, 20, 0, 2, 5, False),
    "WOLF_LV2":MonsterParam("WOLF", 96, 0, 16, 16, 12, 12, 8, 12, 20, 0, 5, 10, True),
    "LION_LV2":MonsterParam("LION", 122, 0, 16, 16, 24, 16, 8, 10, 24, 0, 3, 5, True),
    "SLIME_LV2":MonsterParam("SLIME", 128, 0, 16, 16, 14, 14, 8, 12, 24, 0, 2, 8, False),
    "SPIDER_LV1":MonsterParam("SPIDER", 144, 0, 16, 16, 14, 12, 8, 10, 24, 0, 3, 5, True),
    "GHOUL_LV1":MonsterParam("GHOUL", 160, 0, 16, 16, 30, 24, 16, 8, 30, 20, 2, 5, False),
}
