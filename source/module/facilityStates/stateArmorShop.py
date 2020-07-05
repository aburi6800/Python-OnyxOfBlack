# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..facilityStates.baseFacilityState import BaseFacilityState
from ..character import playerParty
from ..character import Human
from ..item import ArmorParams


class StateArmorShop(BaseFacilityState):
    '''
    鎧屋のクラス

    BaseFacilityStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "ArmorShop"

        self.tick = 0
        self.selected = 0

        # 店員の初期データ
        self.saleParson = Human()
        self.saleParson.name = "Blick Armstrong"
        self.saleParson.head = 13
        self.saleParson.body = 1
        self.saleParson.armor = None
        self.saleParson.weapon = None
        self.saleParson.shield = None
        self.saleParson.helm = None

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

        PyxelUtil.text(16, 152, ["YO", "U", "KO", "SO", " ", "I", "RA", "LTU", "SI", "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 160, ["WA", "TA", "SI" ,"HA", "* Blick Armstrong ", "TO", " ", "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 176, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
        self.drawCharacter(self.saleParson, 178, 112)

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
        playerParty.restoreCondition
