# -*- coding: utf-8 -*-


class WeaponParam():
    '''
    武器の属性を持つクラス
    '''

    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int = 0, attack: int = 0, isDoubleHand: bool = False, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.attack = attack
        self.isDoubleHand = isDoubleHand
        self.price = price


class WeaponParams(object):
    '''
    武器のリストを持つクラス

    リストの要素はWeaponParamクラスのインスタンスとする
    他モジュールから利用する場合はweaponParamsをimportすること
    '''
    weaponList = None

    def __init__(self):
        '''
        クラス初期化
        '''
        # 武器の初期データを登録
        self.weaponList = (
            WeaponParam("KNIFE",  0, 48, 8, 16,  2, False,  10),
            WeaponParam("CLUB",  8, 48, 8, 16,  4, False,  20),
            WeaponParam("MACE", 16, 48, 8, 16,  8, False,  40),
            WeaponParam("SHORT SWORD", 24, 48, 8, 16, 16, False,  80),
            WeaponParam("AXE", 32, 48, 8, 16, 24, False,  160),
            WeaponParam("SPEAR", 48, 48, 8, 16, 32,  True,  320),
            WeaponParam("BROAD SWORD", 64, 48, 8, 16, 40, False,  640),
            WeaponParam("CLAYMORE", 56, 48, 8, 16, 48,  True, 1280),
            WeaponParam("BATTLE AXE", 80, 48, 8, 16, 60,  True, 2560),
        )


weaponParams = WeaponParams()


class ArmorParam():
    '''
    鎧の属性を持つクラス
    '''

    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int = 0, armor: int = 0, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.armor = armor
        self.price = price


class ArmorParams(object):
    '''
    鎧のリストを持つクラス

    リストの要素はArmorParamクラスのインスタンスとする
    他モジュールから利用する場合はarmorParamsをimportすること
    '''
    armorList = None

    def __init__(self):
        '''
        クラス初期化
        '''
        # 鎧の初期データを登録
        self.armorList = (
            ArmorParam("LEATHER", 24, 32, 8, 16,   4,    40),
            ArmorParam("HAUBERK", 32, 32, 8, 16,   8,   160),
            ArmorParam("HALF PLATE", 40, 32, 8, 16,  16,   640),
            ArmorParam("FULL PLATE", 48, 32, 8, 16,  32,  2560),
            ArmorParam("TABARD", 56, 32, 8, 16,  64, 10240),
            ArmorParam("MAGIC MANTLE", 72, 32, 8, 16, 128,    -1),
        )


armorParams = ArmorParams()


class ShieldParam():
    '''
    盾の属性を持つクラス
    '''

    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int = 0, armor: int = 0, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.armor = armor
        self.price = price


class ShieldParams(object):
    '''
    盾のリストを持つクラス

    リストの要素はShieldParamクラスのインスタンスとする
    他モジュールから利用する場合はshieldParamsをimportすること
    '''
    shieldList = None

    def __init__(self):
        '''
        クラス初期化
        '''
        # 盾の初期データを登録
        self.shieldList = (
            ArmorParam("S SHIELD", 128, 40, 8, 8,  2,   30),
            ArmorParam("M SHIELD", 136, 40, 8, 8,  8,  270),
            ArmorParam("L SHIELD", 144, 40, 8, 8, 24, 2430),
        )


shieldParams = ShieldParams()


class HelmetParam():
    '''
    兜の属性を持つクラス
    '''

    def __init__(self, name: str = "", blt_x: int = 0, blt_y: int = 0, blt_w: int = 0, blt_h: int = 0, armor: int = 0, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.armor = armor
        self.price = price


class HelmetParams(object):
    '''
    兜のリストを持つクラス

    リストの要素はHelmetParamクラスのインスタンスとする
    他モジュールから利用する場合はhelmetParamsをimportすること
    '''
    helmetList = None

    def __init__(self):
        '''
        クラス初期化
        '''
        #   兜の初期データを登録
        self.helmetList = (
            ArmorParam("CHAIN COIF", 128, 32, 8, 8,  4,   40),
            ArmorParam("WINGED HELM", 136, 32, 8, 8, 16,  320),
            ArmorParam("HORNED HELM", 144, 32, 8, 8, 32, 2560),
        )


helmetParams = HelmetParams()


class DrugParam():
    '''
    薬と容器の属性を持つクラス
    '''

    def __init__(self, name: tuple, price: int = 0):
        '''
        クラス初期化
        '''
        self.name = name
        self.price = price


class DrugParams(object):
    '''
    薬と容器のリストを持つクラス
    '''
    drugList = None

    def __init__(self):
        '''
        クラス初期化
        '''
        self.drugList = (
            DrugParam(["YO", "U", "KI"], 35),
            DrugParam(["KU", "SU", "RI"], 55),
        )


drugParams = DrugParams()
