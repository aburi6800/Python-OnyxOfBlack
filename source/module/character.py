# -*- coding: utf-8 -*-

'''
 Characterクラス
 - キャラクタ1人の属性を持つクラス
'''
class Character:

    #
    # クラス初期化
    #
    def __init__(self):
        _name = ""
        _life = 0
        _str = 0
        _dex = 0
        _exp = 0
        _gold = 0

    #
    # キャラクタ生成
    #
    def create(self):
        self._name = "AAAAA"
        self._life = 10
        self._str = 10
        self._dex = 10
        self._exp = 0
        self._gold = 40
