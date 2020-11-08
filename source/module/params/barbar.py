# -*- coding: utf-8 -*-

class BarbarParam():
    '''
    床屋の属性クラス
    '''
    def __init__(self, name: tuple, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.price = price


'''
床屋の属性のTupleリスト

リストの要素はBarbarParamクラスのインスタンス
'''
barbarParams = (
    BarbarParam(["SA", "NN", "HA", "HD", "TU"], 100),
)
