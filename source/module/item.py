# -*- coding: utf-8 -*-
from .singleton import Singleton

'''
 WeaponParamクラス
 - 武器のパラメータを持つ
'''
class WeaponParam():

    def __init__(self, name = "", blt_x = 0, blt_y = 0, blt_w = 0, blt_h = 0, attack = 0, isDoubleHand = False, price = 0):
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.attack = attack
        self.isDoubleHand = isDoubleHand
        self.price = price


'''
 WeaponParamsクラス
 - 武器のパラメータのリストを持つ
'''
class WeaponParams(Singleton):

    weaponList = []

    def __init__(self):

        # 武器の初期データを登録
        self.weaponList.append(WeaponParam("KNIFE"      ,  0, 48, 8, 16,  2, False,  10))
        self.weaponList.append(WeaponParam("CLUB"       ,  8, 48, 8, 16,  4, False,  20))
        self.weaponList.append(WeaponParam("MACE"       , 16, 48, 8, 16,  8, False,  40))
        self.weaponList.append(WeaponParam("SHORT SWORD", 24, 48, 8, 16, 16, False,  80))
        self.weaponList.append(WeaponParam("AXE"        , 32, 48, 8, 16, 24, False,  160))
        self.weaponList.append(WeaponParam("SPEAR"      , 48, 48, 8, 16, 32,  True,  320))
        self.weaponList.append(WeaponParam("BROAD SWORD", 64, 48, 8, 16, 40, False,  640))
        self.weaponList.append(WeaponParam("CLAYMORE"   , 56, 48, 8, 16, 48,  True, 1280))
        self.weaponList.append(WeaponParam("BATTLE AXE" , 80, 48, 8, 16, 60,  True, 2560))


'''
 ArmorParamクラス
 - 鎧のパラメータを持つ
'''
class ArmorParam():

    def __init__(self, name = "", blt_x = 0, blt_y = 0, blt_w = 0, blt_h = 0, attack = 0, price = 0):
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.attack = attack
        self.price = price


'''
 ArmorParamsクラス
 - 鎧のパラメータのリストを持つ
'''
class ArmorParams(Singleton):

    armorList = []

    def __init__(self):

        # 鎧の初期データを登録
        self.armorList.append(ArmorParam("LEATHER"      , 24, 32, 8, 16,   4,    40))
        self.armorList.append(ArmorParam("HAUBERK"      , 32, 32, 8, 16,   8,   160))
        self.armorList.append(ArmorParam("HALF PLATE"   , 40, 32, 8, 16,  16,   640))
        self.armorList.append(ArmorParam("FULL PLATE"   , 48, 32, 8, 16,  32,  2560))
        self.armorList.append(ArmorParam("TABARD"       , 56, 32, 8, 16,  64, 10240))
        self.armorList.append(ArmorParam("MAGIC MANTLE" , 72, 32, 8, 16, 128,     0))


'''
 ShieldParamクラス
 - 盾のパラメータを持つ
'''
class ShieldParam():

    def __init__(self, name = "", blt_x = 0, blt_y = 0, blt_w = 0, blt_h = 0, defence = 0, price = 0):
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.defence = defence
        self.price = price


'''
 ShieldParamsクラス
 - 盾のパラメータのリストを持つ
'''
class ShieldParams(Singleton):

    shieldList = []

    def __init__(self):

        # 盾の初期データを登録
        self.shieldList.append(ArmorParam("S SHIELD" , 128, 40, 8, 8,   2,    30))
        self.shieldList.append(ArmorParam("M SHIELD" , 136, 40, 8, 8,   8,   270))
        self.shieldList.append(ArmorParam("L SHIELD" , 144, 40, 8, 8,  24,  2430))


'''
 HelmParamクラス
 - 兜のパラメータを持つ
'''
class HelmParam():

    def __init__(self, name = "", blt_x = 0, blt_y = 0, blt_w = 0, blt_h = 0, defence = 0, price = 0):
        self.name = name
        self.blt_x = blt_x
        self.blt_y = blt_y
        self.blt_w = blt_w
        self.blt_h = blt_h
        self.defence = defence
        self.price = price


'''
 HelmParamsクラス
 - 兜のパラメータのリストを持つ
'''
class HelmParams(Singleton):

    helmList = []

    def __init__(self):

        #   兜の初期データを登録
        self.helmList.append(ArmorParam("CHAIN COIF"   , 128, 32, 8, 8,   4,    40))
        self.helmList.append(ArmorParam("WINGED HELM"  , 136, 32, 8, 8,  16,   320))
        self.helmList.append(ArmorParam("HORNED HELM"  , 144, 32, 8, 8,  32,  2560))
