# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..facilityStates.baseFacilityState import BaseFacilityState

'''
 StateArmorShopクラス
 - 鎧屋のクラス
 - 選択した商品の購入、キャラクターへの装備を行う
'''
class StateArmorShop(BaseFacilityState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateArmorShop, self).__init__(stateStack)
        self.stateName = "ArmorShop"

        self.tick = 0
        self.selected = 0

    #
    # 各フレームの処理
    #
    def update(self):

#        print(self.stateName + ":update")

        if pyxel.btn(pyxel.KEY_E):
            self.selected = 3
            self.tick = 0

        if self.selected != 0:
            self.tick = self.tick + 1
            if self.tick > 11:
                if self.selected == 3:
                    self.stateStack.pop()

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print(self.stateName + ":render")

        super().render()

        color = [7, 7, 7]
        if self.selected != 0:
            if self.tick % 2 == 0:
                color[self.selected - 1] = 0
            else:
                color[self.selected - 1] = 7

        PyxelUtil.text(16,  16, ["YO", "RO", "I", "YA"], 7)
        PyxelUtil.text(24,  30, ["*[B]:", "KA", "U"], color[0])
        PyxelUtil.text(24,  38, ["*[N]:", "TU", "KI", "D", "NO", "SI", "LYO", "U", "HI", "NN"], color[1])
        PyxelUtil.text(24,  46, ["*[E]:", "TE", "D", "RU"], color[2])

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

