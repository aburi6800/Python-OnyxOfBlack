# -*- coding: utf-8 -*-
from module.character import Character

'''
 Playerクラス
 - プレイヤーキャラクタの属性を持つクラス
'''
class Player(Character):

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
        _head = ""
        _helmet = ""
        _armor = ""
        _shield = ""
        _weapon = ""
