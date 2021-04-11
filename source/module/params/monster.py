# -*- coding: utf-8 -*-

class MonsterParam():
    '''
    モンスターの属性クラス
    '''
    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int=0, level: int = 0, life: int = 0, strength: int = 0, defend: int = 0, dexterity: int = 0, exp: int = 0, gold: int = 0, occr_min: int = 0, occr_max: int = 0, escape: bool = False):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.level = level
        self.life = life
        self.maxlife = life
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
    "WOLF_LV1":MonsterParam("WOLF", 96, 0, 16, 16, 1, 4, 7, 1, 4, 2, 0, 3, 6, True),
    "BAT_LV1":MonsterParam("BAT", 0, 0, 16, 8, 2, 2, 5, 1, 9, 2, 0, 3, 10, True),
    "BAT_LV2":MonsterParam("BAT", 0, 0, 16, 8, 2, 2, 5, 1, 9, 2, 0, 5, 20, True),
    "KOBOLD_LV1":MonsterParam("KOBOLD", 16, 0, 16, 16, 2, 6, 9, 4, 3, 3, 20, 5, 8, True),
    "KOBOLD_LV2":MonsterParam("KOBOLD", 16, 0, 16, 16, 2, 6, 9, 4, 3, 3, 20, 7, 15, True),
    "ZOMBIE_LV1":MonsterParam("ZOMBIE", 48, 0, 16, 16, 1, 8, 9, 2, 2, 2, 0, 2, 5, False),
    "ZOMBIE_LV2":MonsterParam("ZOMBIE", 48, 0, 16, 16, 1, 8, 9, 2, 2, 2, 0, 4, 12, False),
    "SKELETON_LV1":MonsterParam("SKELETON", 32, 0, 16, 16, 2, 4, 7, 3, 2, 2, 15, 3, 5, False),
    "SKELETON_LV2":MonsterParam("SKELETON", 32, 0, 16, 16, 2, 4, 7, 3, 2, 2, 15, 4, 12, False),
    "GOBLIN_LV1":MonsterParam("GOBLIN", 80, 0, 16, 16, 3, 8, 9, 6, 5, 5, 40, 5, 10, True),
    "GOBLIN_LV2":MonsterParam("GOBLIN", 80, 0, 16, 16, 3, 8, 9, 5, 5, 5, 40, 7, 15, True),
    "AZTEC_LV1":MonsterParam("AZTEC", 64, 0, 16, 16, 3, 7, 12, 4, 5, 4, 60, 2, 5, True),
    "AZTEC_LV2":MonsterParam("AZTEC", 64, 0, 16, 16, 3, 9, 12, 4, 5, 4, 60, 5, 8, True),
    "LION_LV1":MonsterParam("LION", 112, 0, 16, 16, 3, 12, 15, 4, 4, 3, 0, 1, 2, True),
    "LION_LV2":MonsterParam("LION", 112, 0, 16, 16, 3, 18, 15, 4, 4, 3, 0, 2, 5, True),
    "MUMMY_LV1":MonsterParam("MUMMY", 192, 0, 16, 16, 4, 12, 13, 10, 5, 6, 0, 2, 5, False),
    "MUMMY_LV2":MonsterParam("MUMMY", 192, 0, 16, 16, 4, 12, 13, 10, 5, 6, 0, 4, 10, False),
    "ORC_LV1":MonsterParam("ORC", 176, 0, 16, 16, 4, 16, 16, 12, 6, 7, 100, 3, 6, True),
    "ORC_LV2":MonsterParam("ORC", 176, 0, 16, 16, 4, 16, 16, 12, 6, 7, 100, 4, 10, True),
    "SLIME_LV1":MonsterParam("SLIME", 128, 0, 16, 16, 4, 24, 20, 13, 4, 8, 0, 2, 5, False),
    "SLIME_LV2":MonsterParam("SLIME", 128, 0, 16, 16, 5, 24, 20, 13, 4, 8, 0, 4, 6, False),
    "SPIDER_LV1":MonsterParam("SPIDER", 144, 0, 16, 16, 5, 20, 22, 16, 8, 7, 0, 1, 2, True),
    "SPIDER_LV2":MonsterParam("SPIDER", 144, 0, 16, 16, 5, 20, 22, 16, 8, 7, 0, 2, 4, True),
    "SPIDER_LV3":MonsterParam("SPIDER", 144, 0, 16, 16, 5, 20, 22, 16, 8, 7, 0, 4, 6, True),
    "GHOUL_LV1":MonsterParam("GHOUL", 160, 0, 16, 16, 5, 13, 20, 20, 7, 8, 180, 2, 5, False),
    "GHOUL_LV2":MonsterParam("GHOUL", 160, 0, 16, 16, 5, 13, 20, 20, 7, 8, 180, 4, 10, False),
    "COBRA_LV1":MonsterParam("COBRA", 96, 16, 16, 16, 5, 18, 26, 25, 6, 10, 0, 1, 2, True),
    "COBRA_LV2":MonsterParam("COBRA", 96, 16, 16, 16, 5, 18, 26, 25, 6, 10, 0, 1, 4, True),
    "BLAAB_LV1":MonsterParam("BLAAB", 224, 0, 16, 16, 6, 45, 45, 25, 8, 12, 0, 1, 3, True),
    "BLAAB_LV2":MonsterParam("BLAAB", 224, 0, 16, 16, 6, 45, 45, 25, 8, 12, 0, 2, 5, True),
    "VAMPIRE_LV1":MonsterParam("VAMPIRE", 32, 16, 16, 16, 5, 18, 23, 25, 12, 10, 0, 3, 7, True),
    "VAMPIRE_LV2":MonsterParam("VAMPIRE", 32, 16, 16, 16, 5, 18, 23, 25, 12, 10, 0, 5, 9, True),
    "VAMPIRE_LV3":MonsterParam("VAMPIRE", 32, 16, 16, 16, 5, 18, 23, 25, 12, 10, 0, 7, 12, True),
    "OGRE_LV1":MonsterParam("OGRE", 208, 0, 16, 16, 6, 32, 30, 32, 6, 15, 150, 1, 3, True),
    "OGRE_LV2":MonsterParam("OGRE", 208, 0, 16, 16, 6, 32, 30, 32, 6, 15, 150, 2, 5, True),
    "HOBGOBLIN_LV1":MonsterParam("HOBGOBLIN", 240, 0, 16, 16, 6, 37, 34, 35, 8, 17, 300, 2, 2, True),
    "WIRKAT_LV1":MonsterParam("WIRKAT", 48, 16, 16, 16, 6, 30, 35, 30, 9, 16, 400, 1, 3, True),
    "WIRKAT_LV2":MonsterParam("WIRKAT", 48, 16, 16, 16, 6, 30, 35, 30, 9, 16, 400, 2, 5, True),
    "KRAKEN_LV1":MonsterParam("KRAKEN", 0, 16, 32, 32, 5, 150, 55, 45, 28, 500, 2500, 1, 1, False),
    "TAURUS_LV1":MonsterParam("TAURUS", 192, 16, 24, 24, 8, 95, 300, 40, 15, 200, 500, 1, 3, True),
    "GIANT_LV1":MonsterParam("GIANT", 216, 16, 24, 24, 8, 100, 500, 60, 18, 400, 700, 1, 2, False),
    "BEAST_LV1":MonsterParam("BEAST", 112, 16, 16, 16, 6, 40, 150, 100, 13, 100, 0, 1, 3, True),
    "HIDER_LV1":MonsterParam("HIDER", 144, 16, 16, 16, 6, 30, 110, 100, 15, 100, 250, 1, 3, True),
    "DEMON_LV1":MonsterParam("DEMON", 80, 16, 16, 16, 6, 45, 100, 120, 13, 110, 0, 1, 1, False),
    "DEMON_LV2":MonsterParam("DEMON", 80, 16, 16, 16, 6, 45, 100, 120, 13, 110, 0, 1, 2, False),
    "GHOST_LV1":MonsterParam("GHOST", 64, 16, 16, 16, 6, 20, 90, 100, 9, 90, 0, 1, 2, True),
    "TROLL_LV1":MonsterParam("TROLL", 128, 16, 16, 16, 6, 65, 120, 110, 10, 120, 0, 2, 6, True),
    "MIER_LV1":MonsterParam("MIER", 160, 16, 16, 16, 6, 30, 200, 90, 12, 100, 0, 5, 5, True),
    "MIER_LV2":MonsterParam("MIER", 160, 16, 16, 16, 6, 30, 200, 90, 12, 100, 0, 4, 6, True),
    "WRAITH_LV1":MonsterParam("WRAITH", 176, 16, 16, 16, 7, 40, 250, 120, 9, 130, 0, 1, 5, True),
}
