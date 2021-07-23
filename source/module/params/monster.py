# -*- coding: utf-8 -*-

class MonsterParam():
    '''
    モンスターの属性クラス
    '''
    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int=0, level: int = 0, life: int = 0, strength: int = 0, defend: int = 0, dexterity: int = 0, exp: int = 0, gold: int = 0, occr_min: int = 0, occr_max: int = 0, isEscape: bool = False, hasItem: bool = False):
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
        self.isEscape = isEscape
        self.hasItem = hasItem


'''
モンスターの属性のディクショナリ

リストの要素はMonsterParamクラスのインスタンス
'''
monsterParams = {
    "WOLF_LV1":MonsterParam("WOLF", 96, 0, 16, 16, 1, 4, 3, 1, 4, 3, 0, 3, 6, True,False),
    "BAT_LV1":MonsterParam("BAT", 0, 0, 16, 8, 2, 2, 1, 2, 5, 2, 0, 3, 10, True,False),
    "BAT_LV2":MonsterParam("BAT", 0, 0, 16, 8, 2, 2, 1, 2, 5, 2, 0, 5, 20, True,False),
    "KOBOLD_LV1":MonsterParam("KOBOLD", 16, 0, 16, 16, 2, 6, 4, 5, 2, 4, 15, 5, 8, True,False),
    "KOBOLD_LV2":MonsterParam("KOBOLD", 16, 0, 16, 16, 2, 6, 4, 5, 2, 4, 15, 7, 15, True,False),
    "ZOMBIE_LV1":MonsterParam("ZOMBIE", 48, 0, 16, 16, 1, 8, 3, 2, 1, 2, 0, 2, 5, False,False),
    "ZOMBIE_LV2":MonsterParam("ZOMBIE", 48, 0, 16, 16, 1, 8, 3, 2, 1, 2, 0, 4, 12, False,False),
    "SKELETON_LV1":MonsterParam("SKELETON", 32, 0, 16, 16, 2, 5, 3, 3, 3, 5, 10, 3, 5, False,False),
    "SKELETON_LV2":MonsterParam("SKELETON", 32, 0, 16, 16, 2, 5, 3, 3, 3, 5, 10, 4, 12, False,False),
    "GOBLIN_LV1":MonsterParam("GOBLIN", 80, 0, 16, 16, 3, 10, 6, 7, 3, 7, 25, 5, 10, True,True),
    "GOBLIN_LV2":MonsterParam("GOBLIN", 80, 0, 16, 16, 3, 10, 6, 7, 3, 7, 25, 7, 15, True,True),
    "AZTEC_LV1":MonsterParam("AZTEC", 64, 0, 16, 16, 3, 8, 5, 5, 3, 8, 40, 2, 5, True,True),
    "AZTEC_LV2":MonsterParam("AZTEC", 64, 0, 16, 16, 3, 8, 5, 5, 3, 8, 40, 5, 8, True,True),
    "LION_LV1":MonsterParam("LION", 112, 0, 16, 16, 3, 18, 10, 6, 4, 10, 0, 1, 2, True,False),
    "LION_LV2":MonsterParam("LION", 112, 0, 16, 16, 3, 18, 10, 6, 4, 10, 0, 2, 5, True,False),
    "MUMMY_LV1":MonsterParam("MUMMY", 192, 0, 16, 16, 4, 13, 8, 6, 4, 12, 200, 2, 5, False,False),
    "MUMMY_LV2":MonsterParam("MUMMY", 192, 0, 16, 16, 4, 13, 8, 6, 4, 12, 200, 4, 10, False,False),
    "ORC_LV1":MonsterParam("ORC", 176, 0, 16, 16, 4, 15, 10, 8, 6, 13, 300, 3, 6, True,True),
    "ORC_LV2":MonsterParam("ORC", 176, 0, 16, 16, 4, 15, 10, 8, 6, 13, 300, 4, 10, True,True),
    "SLIME_LV1":MonsterParam("SLIME", 128, 0, 16, 16, 4, 18, 12, 15, 7, 13, 0, 2, 5, False,False),
    "SLIME_LV2":MonsterParam("SLIME", 128, 0, 16, 16, 5, 18, 12, 15, 7, 13, 0, 4, 6, False,False),
    "SPIDER_LV1":MonsterParam("SPIDER", 144, 0, 16, 16, 5, 16, 18, 26, 10, 20, 0, 1, 2, True,False),
    "SPIDER_LV2":MonsterParam("SPIDER", 144, 0, 16, 16, 5, 16, 18, 26, 10, 20, 0, 2, 4, True,False),
    "SPIDER_LV3":MonsterParam("SPIDER", 144, 0, 16, 16, 5, 16, 18, 26, 10, 20, 0, 4, 6, True,False),
    "GHOUL_LV1":MonsterParam("GHOUL", 160, 0, 16, 16, 5, 18, 22, 22, 8, 13, 270, 2, 5, False,True),
    "GHOUL_LV2":MonsterParam("GHOUL", 160, 0, 16, 16, 5, 18, 22, 22, 8, 13, 270, 4, 10, False,True),
    "COBRA_LV1":MonsterParam("COBRA", 96, 16, 16, 16, 5, 14, 26, 26, 10, 20, 0, 1, 2, True,False),
    "COBRA_LV2":MonsterParam("COBRA", 96, 16, 16, 16, 5, 14, 26, 26, 10, 20, 0, 1, 4, True,False),
    "BLAAB_LV1":MonsterParam("BLAAB", 224, 0, 16, 16, 6, 45, 27, 28, 12, 40, 0, 1, 3, True,False),
    "BLAAB_LV2":MonsterParam("BLAAB", 224, 0, 16, 16, 6, 45, 27, 28, 12, 40, 0, 2, 5, True,False),
    "VAMPIRE_LV1":MonsterParam("VAMPIRE", 32, 16, 16, 16, 5, 10, 21, 16, 14, 15, 0, 3, 7, True,False),
    "VAMPIRE_LV2":MonsterParam("VAMPIRE", 32, 16, 16, 16, 5, 10, 21, 16, 14, 15, 0, 5, 9, True,False),
    "VAMPIRE_LV3":MonsterParam("VAMPIRE", 32, 16, 16, 16, 5, 10, 21, 16, 14, 15, 0, 7, 12, True,False),
    "OGRE_LV1":MonsterParam("OGRE", 208, 0, 16, 16, 6, 30, 25, 32, 14, 40, 1100, 1, 3, True,True),
    "OGRE_LV2":MonsterParam("OGRE", 208, 0, 16, 16, 6, 30, 25, 32, 14, 40, 150, 2, 5, True,True),
    "HOBGOBLIN_LV1":MonsterParam("HOBGOBLIN", 240, 0, 16, 16, 6, 26, 30, 30, 15, 30, 1300, 2, 2, True,True),
    "WIRKAT_LV1":MonsterParam("WIRKAT", 48, 16, 16, 16, 6, 30, 34, 36, 16, 30, 400, 1, 3, True,False),
    "WIRKAT_LV2":MonsterParam("WIRKAT", 48, 16, 16, 16, 6, 30, 34, 36, 16, 30, 400, 2, 5, True,False),
    "KRAKEN_LV1":MonsterParam("KRAKEN", 0, 16, 32, 32, 5, 120, 50, 47, 16, 500, 5000, 1, 1, False,False),
    "TAURUS_LV1":MonsterParam("TAURUS", 192, 16, 24, 24, 8, 80, 60, 45, 22, 200, 500, 1, 3, True,True),
    "GIANT_LV1":MonsterParam("GIANT", 216, 16, 24, 24, 8, 70, 65, 65, 20, 400, 700, 1, 2, False,True),
    "BEAST_LV1":MonsterParam("BEAST", 112, 16, 16, 16, 6, 36, 45, 40, 16, 120, 0, 1, 3, False,False),
    "HIDER_LV1":MonsterParam("HIDER", 144, 16, 16, 16, 6, 30, 40, 35, 15, 100, 250, 1, 3, True,True),
    "DEMON_LV1":MonsterParam("DEMON", 80, 16, 16, 16, 6, 25, 32, 45, 18, 110, 0, 1, 1, False,True),
    "DEMON_LV2":MonsterParam("DEMON", 80, 16, 16, 16, 6, 25, 32, 45, 18, 110, 0, 1, 2, False,True),
    "GHOST_LV1":MonsterParam("GHOST", 64, 16, 16, 16, 6, 26, 35, 38, 22, 90, 0, 1, 2, True,False),
    "TROLL_LV1":MonsterParam("TROLL", 128, 16, 16, 16, 6, 55, 42, 38, 18, 120, 0, 2, 6, True,True),
    "MIER_LV1":MonsterParam("MIER", 160, 16, 16, 16, 6, 36, 48, 36, 20, 100, 0, 5, 5, True,False),
    "MIER_LV2":MonsterParam("MIER", 160, 16, 16, 16, 6, 36, 48, 36, 20, 100, 0, 4, 6, True,False),
    "WRAITH_LV1":MonsterParam("WRAITH", 176, 16, 16, 16, 7, 40, 46, 50, 18, 130, 0, 1, 5, True,False),
}
