# -*- coding: utf-8 -*-
import pyxel
from .pyxelUtil import PyxelUtil
from .abstractState import AbstractState
from .character import PlayerParty
from .item import WeaponParams
from .item import ArmorParams
from .item import ShieldParams
from .item import HelmParams

'''
 BaseStateクラス
 - 各Stateの規定クラス
 - AbstractStateを継承
 - renderメソッドでは画面の枠線とプレイヤーキャラクターの描画を行う
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
        _x = [16, 36, 60, 84, 104]
        _y = [108, 112, 108, 112, 108]

        for _idx in range(len(self.playerParty.getMemberList())):
            _member = self.playerParty.getMember(_idx)

            # 頭
            if _member.helmet == None:
                _head_x = (_member.head % 32) * 8
                _head_y = (_member.head // 32) * 8
            else:
                pass
            pyxel.blt(_x[_idx] + 8, _y[_idx], 1, _head_x, _head_y, 8, 8, 0)

            # 体
            if _member.armor == None:
                _armor_x = 0
                _armor_y = 32
                _armor_w = 8
                _armor_h = 16
            else:
                _armor_x = _member.armor.blt_x
                _armor_y = _member.armor.blt_y
                _armor_w = _member.armor.blt_w
                _armor_h = _member.armor.blt_h
            pyxel.blt(_x[_idx] + 8, _y[_idx] + 8, 1, _armor_x, _armor_y, _armor_w, _armor_h, 0)

            # 武器
            if _member.weapon != None:
                _weapon_x = _member.weapon.blt_x
                _weapon_y = _member.weapon.blt_y
                _weapon_w = _member.weapon.blt_w
                _weapon_h = _member.weapon.blt_h
                pyxel.blt(_x[_idx], _y[_idx], 1, _weapon_x, _weapon_y, _weapon_w, _weapon_h, 0)

            # 盾
            if _member.shield != None:
                pass

            # ステータス
            PyxelUtil.text( 16,  (_idx + 1) * 16, ["*" + _member.name], pyxel.COLOR_WHITE) # 名前
            pyxel.rect( 16, (_idx + 1) * 16 + 8, _member.life, 3,  5)
            pyxel.rect( 16, (_idx + 1) * 16 + 11, _member.exp, 1,  6)

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

