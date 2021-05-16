# -*- coding: utf-8 -*-
from enum import IntEnum, auto

class State(IntEnum):
    '''
    StateのENUMクラス
    '''
    TITLE = auto()
    MAKECHARACTER = auto()
    CAMP = auto()
    ENDING = auto()
    CEMETERY = auto()
    CITY = auto()
    WELLB1 = auto()
    WELLB2 = auto()
    WELLB3 = auto()
    WELLB4 = auto()
    DUNGEONB1 = auto()
    DUNGEONB2 = auto()
    DUNGEONB3 = auto()
    DUNGEONB4 = auto()
    DUNGEONB5 = auto()
    COLORD_YELLOW = auto()
    COLORD_RED = auto()
    COLORD_PURPLE = auto()
    COLORD_GREEN = auto()
    COLORD_BLUE = auto()
    COLORD_WHITE = auto()
    COLORD_BLACK = auto()
    BLACKTOWER = auto()
    ARMORSHOP = auto()
    BARBAR = auto()
    DRUGS = auto()
    EXAMINATIONS = auto()
    HELMETSHOP = auto()
    SHIELDSHOP = auto()
    SURGERY = auto()
    WEAPONSHOP = auto()
    BATTLE = auto()
