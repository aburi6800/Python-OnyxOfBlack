# -*- coding: utf-8 -*-
from module.character import Character

'''
 Human
 - 人間のクラス
'''
class Human(Character):

    #
    # クラス初期化
    #
    def __init__(self):
        self._name = ""
        self._life = 0
        self._str = 0
        self._dex = 0
        self._exp = 0
        self._gold = 0
        self._head = None
        self._helmet = None
        self._armor = None
        self._shield = None
        self._weapon = None
        self._potion = -1
