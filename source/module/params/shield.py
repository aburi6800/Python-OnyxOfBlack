# -*- coding: utf-8 -*-

class ShieldParam():
    '''
    盾の属性クラス
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
盾の属性のTupleリスト

リストの要素はShieldParamクラスのインスタンス
'''
shieldParams = (
    ShieldParam("S SHIELD", 128, 40, 8, 8, 2, 2, 30),
    ShieldParam("M SHIELD", 136, 40, 8, 8, 8, 8, 270),
    ShieldParam("L SHIELD", 144, 40, 8, 8, 24, 24, 2430),
)
