# -*- coding: utf-8 -*-
import pyxel
from module.pyxelUtil import PyxelUtil
from module.character import Character
from module.party import Party
from module.fieldStates.baseFieldState import BaseFieldState

'''
 StateCityクラス
 - ウツロの街のクラス(BaseFiledStateを継承)
 - マップデータを保持する
 - イベントの処理を持つ
 - 各Stateへの遷移を行う
'''
class StateCity(BaseFieldState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateCity, self).__init__(stateStack)
        self.stateName = "City"

        self.tick = 0
        self.selected = 0
        self.party = Party()

    #
    # 各フレームの処理
    #
    def update(self):

#        print(self.stateName + ":update")

        if pyxel.btn(pyxel.KEY_W):
            self.selected = 1
            self.tick = 0

        if pyxel.btn(pyxel.KEY_A):
            self.selected = 2
            self.tick = 0

        if self.selected != 0:
            self.tick = self.tick + 1
            if self.tick > 11:
                if self.selected == 1:
                    self.selected = 0
                    self.stateStack.push(self.stateStack.STATE_WEAPONSHOP)
                if self.selected == 2:
                    self.selected = 0
                    self.stateStack.push(self.stateStack.STATE_ARMORSHOP)

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print(self.stateName + ":render")

        super().render()

        color = [7, 7, 7, 7, 7]
        if self.selected != 0:
            if self.tick % 2 == 0:
                color[self.selected - 1] = 0
            else:
                color[self.selected - 1] = 7

        PyxelUtil.text(16,  16, ["u", "tu", "ro", "NO", "MA", "TI"], 7)
        PyxelUtil.text(24,  30, ["*[W]:", "HU", "D", "KI", "YA"], color[0])
        PyxelUtil.text(24,  38, ["*[A]:", "YO", "RO", "I", "YA"], color[1])
        PyxelUtil.text(24,  46, ["*[S]:", "TA", "TE", "YA"], color[2])
        PyxelUtil.text(24,  54, ["*[H]:", "KA", "HU", "D", "TO", "YA"], color[3])
        PyxelUtil.text(24,  62, ["*[B]:", "TO", "KO", "YA"], color[4])

    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print(self.stateName + ":onEnter")

        self.tick = 0
        self.selected = 0

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print(self.stateName + ":onExit")

