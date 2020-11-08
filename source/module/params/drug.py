# -*- coding: utf-8 -*-

class DrugParam():
    '''
    薬と容器の属性クラス
    '''
    def __init__(self, name: tuple, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.price = price


'''
薬と容器の属性のTupleリスト

リストの要素はDrugParamクラスのインスタンス
'''
drugParams = (
    DrugParam(["YO", "U", "KI"], 35),
    DrugParam(["KU", "SU", "RI"], 55),
)
