# -*- coding: utf-8 -*-

class HelmetParam():
    '''
    兜の属性クラス
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
兜の属性のTupleリスト

リストの要素はShieldParamクラスのインスタンス
'''
helmetParams = (
    HelmetParam("CHAIN COIF", 128, 40, 8, 8, 4, 1, 40),
    HelmetParam("WINGED HELM", 136, 40, 8, 8, 16, 8, 320),
    HelmetParam("HORNED HELM", 144, 40, 8, 8, 32, 16, 2560),
)
