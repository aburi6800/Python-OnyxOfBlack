# -*- coding: utf-8 -*-
import pyxel
from module.pyxelUtil import PyxelUtil
from module.abstractState import AbstractState
from module.character import PlayerParty
from module.item import WeaponParams
from module.item import ArmorParams
from module.item import ShieldParams
from module.item import HelmParams

'''
 BaseStateクラス
 - 各Stateの規定クラス
 - AbstractStateを継承
 - 
'''
class BaseState(AbstractState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        self.stateStack = stateStack
        self.stateName = "(none)"
        self.playerParty = PlayerParty()

    #
    # 各フレームの処理
    #
    def update(self):

#        print("BaseState:update")

        pass

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print("BaseState:render")

        pyxel.rectb(8, 8, 240, 128, pyxel.COLOR_DARKBLUE)
        pyxel.line(128, 8 ,128, 135, pyxel.COLOR_DARKBLUE)
        pyxel.line(8, 104 ,248, 104, pyxel.COLOR_DARKBLUE)

        # プレイヤーキャラクタ
        __x = [16, 36, 60, 84, 104]
        __y = [108, 112, 108, 112, 108]
        print("MEMBER COUNT:" + str(len(self.playerParty.getMemberList())))

        for __idx in range(len(self.playerParty.getMemberList())):
            __member = self.playerParty.getMember(__idx)

            # 頭
            __head_x = (__member.head % 32) * 8
            __head_y = (__member.head // 32) * 8
            pyxel.blt(__x[__idx] + 8, __y[__idx], 1, __head_x, __head_y, 8, 8, 0)
            # 体
            if __member.armor == None:
                __armor_x = 0
                __armor_y = 32
                __armor_w = 8
                __armor_h = 16
            else:
                __armor_x = __member.armor.blt_x
                __armor_y = __member.armor.blt_y
                __armor_w = __member.armor.blt_w
                __armor_h = __member.armor.blt_h
            pyxel.blt(__x[__idx] + 8, __y[__idx] + 8, 1, __armor_x, __armor_y, __armor_w, __armor_h, 0)
            # 武器
            if __member.weapon != None:
                __weapon_x = __member.weapon.blt_x
                __weapon_y = __member.weapon.blt_y
                __weapon_w = __member.weapon.blt_w
                __weapon_h = __member.weapon.blt_h
                pyxel.blt(__x[__idx], __y[__idx], 1, __weapon_x, __weapon_y, __weapon_w, __weapon_h, 0)

            # ステータス
            PyxelUtil.text( 16,  (__idx + 1) * 16, ["*" + __member.name], pyxel.COLOR_WHITE) # 名前
            pyxel.rect( 16, (__idx + 1) * 16 + 8, __member.life, 3,  5)
            pyxel.rect( 16, (__idx + 1) * 16 + 11, __member.exp, 1,  6)


    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print("BaseState:onEnter")

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print("BaseState:onExit")

