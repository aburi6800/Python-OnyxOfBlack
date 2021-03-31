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
    "WOLF_LV1":MonsterParam("WOLF", 96, 0, 16, 16, 8, 7, 1, 7, 6, 0, 1, 8, True),
    "BAT_LV1":MonsterParam("BAT", 0, 0, 16, 8, 1, 5, 1, 13, 4, 0, 3, 10, True),
    "BAT_LV2":MonsterParam("BAT", 0, 0, 16, 8, 1, 5, 1, 13, 4, 0, 5, 20, True),
    "KOBOLD_LV1":MonsterParam("KOBOLD", 16, 0, 16, 16, 6, 5, 1, 5, 6, 10, 2, 8, True),
    "KOBOLD_LV2":MonsterParam("KOBOLD", 16, 0, 16, 16, 6, 5, 1, 5, 6, 10, 5, 15, True),
    "ZOMBIE_LV1":MonsterParam("ZOMBIE", 48, 0, 16, 16, 5, 9, 1, 6, 8, 0, 2, 5, False),
    "ZOMBIE_LV2":MonsterParam("ZOMBIE", 48, 0, 16, 16, 5, 9, 1, 6, 8, 0, 4, 12, False),
    "SKELETON_LV1":MonsterParam("SKELETON", 32, 0, 16, 16, 4, 6, 1, 4, 7, 10, 3, 5, False),
    "SKELETON_LV2":MonsterParam("SKELETON", 32, 0, 16, 16, 4, 6, 1, 4, 7, 10, 4, 12, False),
    "GOBLIN_LV1":MonsterParam("GOBLIN", 80, 0, 16, 16, 15, 10, 1, 6, 10, 30, 3, 5, True),
    "GOBLIN_LV2":MonsterParam("GOBLIN", 80, 0, 16, 16, 15, 10, 1, 6, 10, 30, 4, 15, True),
    "AZTEC_LV1":MonsterParam("AZTEC", 64, 0, 16, 16, 8, 6, 1, 5, 8, 60, 3, 6, True),
    "AZTEC_LV2":MonsterParam("AZTEC", 64, 0, 16, 16, 8, 6, 1, 5, 8, 60, 5, 8, True),
    "LION_LV1":MonsterParam("LION", 112, 0, 16, 16, 12, 9, 1, 7, 9, 0, 1, 1, True),
    "LION_LV2":MonsterParam("LION", 112, 0, 16, 16, 12, 9, 1, 7, 9, 0, 2, 5, True),
    "MUMMY_LV1":MonsterParam("MUMMY", 192, 0, 16, 16, 8, 15, 1, 5, 12, 0, 2, 5, False),
    "MUMMY_LV2":MonsterParam("MUMMY", 192, 0, 16, 16, 8, 15, 1, 5, 12, 0, 4, 10, False),
    "ORC_LV1":MonsterParam("ORC", 176, 0, 16, 16, 18, 17, 1, 10, 12, 100, 3, 6, True),
    "ORC_LV2":MonsterParam("ORC", 176, 0, 16, 16, 18, 17, 1, 10, 12, 100, 4, 10, True),
    "SLIME_LV1":MonsterParam("SLIME", 128, 0, 16, 16, 15, 10, 1, 8, 10, 0, 2, 5, False),
    "SLIME_LV2":MonsterParam("SLIME", 128, 0, 16, 16, 15, 10, 1, 8, 10, 0, 4, 6, False),
    "SPIDER_LV1":MonsterParam("SPIDER", 144, 0, 16, 16, 14, 12, 1, 10, 24, 0, 3, 5, True),
    "GHOUL_LV1":MonsterParam("GHOUL", 160, 0, 16, 16, 30, 24, 1, 8, 30, 20, 2, 5, False),
}
