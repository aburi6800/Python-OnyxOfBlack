# -*- coding: utf-8 -*-

class ArmorParam():
    '''
    鎧の属性クラス
    '''
    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int = 0, armor: int = 0, weight: int = 0, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.armor = armor
        self.weight = weight
        self.price = price


'''
鎧の属性のTupleリスト

リストの要素はArmorParamクラスのインスタンス
'''
armorParams = (
    ArmorParam("LEATHER", 24, 40, 8, 16, 4, 1, 40),
    ArmorParam("HAUBERK", 32, 40, 8, 16, 8, 4, 160),
    ArmorParam("HALF PLATE", 40, 40, 8, 16, 16, 8, 640),
    ArmorParam("FULL PLATE", 48, 40, 8, 16, 32, 16, 2560),
    ArmorParam("TABARD", 56, 40, 8, 16, 64, 32, 10240),
    ArmorParam("MAGIC MANTLE", 72, 40, 8, 16, 128, 0, -1),
)
