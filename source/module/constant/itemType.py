# -*- coding: utf-8 -*-
from enum import IntEnum, auto

class ItemType(IntEnum):
    '''
    アイテム種別のEnumクラス
    '''

    WEAPON = auto()
    ARMOR = auto()
    SHIELD = auto()
    HELMET = auto()
