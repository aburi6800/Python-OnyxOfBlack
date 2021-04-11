# -*- coding: utf-8 -*-

class WeaponParam():
    '''
    武器の属性クラス
    '''
    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int = 0, attack: int = 0, weight: int = 0, isDoubleHand: bool = False, isBlade: bool = False, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.attack = attack
        self.weight = weight
        self.isDoubleHand = isDoubleHand
        self.isBlade = isBlade
        self.price = price


'''
武器の属性のTupleリスト

リストの要素はWeaponParamクラスのインスタンス
'''
weaponParams = (
    WeaponParam("KNIFE", 0, 64, 8, 16, 2, 1, False, True, 10),
    WeaponParam("CLUB", 8, 64, 8, 16, 4, 3, False, False, 20),
    WeaponParam("MACE", 16, 64, 8, 16, 8, 5, False, False, 40),
    WeaponParam("SHORT SWORD", 24, 64, 8, 16, 16, 2, False, True, 80),
    WeaponParam("AXE", 32, 64, 8, 16, 24, 5, False, True, 160),
    WeaponParam("SPEAR", 48, 64, 8, 16, 32, 4, True, True, 320),
    WeaponParam("BROAD SWORD", 64, 64, 8, 16, 40, 7, False, True, 640),
    WeaponParam("CLAYMORE", 56, 64, 8, 16, 48, 6, True, True, 1280),
    WeaponParam("BATTLE AXE", 80, 64, 8, 16, 60, 10, True, True, 2560),
)
