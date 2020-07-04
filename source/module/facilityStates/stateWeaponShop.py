# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..facilityStates.baseFacilityState import BaseFacilityState


class StateWeaponShop(BaseFacilityState):
    '''
    武器屋のクラス

    BaseFacilityStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "WeaponShop"

        self.tick = 0
        self.selected = 0

    def update(self):
        '''
        各フレームの処理
        '''
        if pyxel.btn(pyxel.KEY_E):
            self.selected = 3
            self.tick = 0

        if self.selected != 0:
            self.tick = self.tick + 1
            if self.tick > 11:
                if self.selected == 3:
                    self.stateStack.pop()

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        color = [7, 7, 7]
        if self.selected != 0:
            if self.tick % 2 == 0:
                color[self.selected - 1] = 0
            else:
                color[self.selected - 1] = 7

        PyxelUtil.text(16,  16, ["HU", "D", "KI", "YA"], 7)
        PyxelUtil.text(24,  30, ["*[B]:", "KA", "U"], color[0])
        PyxelUtil.text(24,  38, ["*[N]:", "TU", "KI", "D",
                                 "NO", "SI", "LYO", "U", "HI", "NN"], color[1])
        PyxelUtil.text(24,  46, ["*[E]:", "TE", "D", "RU"], color[2])

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        self.tick = 0
        self.selected = 0

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
