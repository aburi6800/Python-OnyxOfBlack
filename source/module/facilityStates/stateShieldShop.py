# -*- coding: utf-8 -*-
import pyxel
import pyxel
from ..pyxelUtil import PyxelUtil
from ..facilityStates.baseShopState import BaseShopState
from ..character import playerParty
from ..character import Human
from ..item import shieldParams


class StateShieldShop(BaseShopState):
    '''
    盾屋のクラス

    BaseFacilityStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "ShieldShop"

        # この店で使うアイテムリスト
        self.itemList = shieldParams.shieldList

        # 店員の初期データ
        self.saleParson.name = "Hrolf"
        self.saleParson.head = 81
        self.saleParson.body = 1

    def _update_done(self):
        '''
        買った処理
        '''
        super()._update_done()
        playerParty.memberList[self.equipMember].shield = self.item

    def _update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.shield = self.item

    def _render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 152, ["O", "RE", "HA", " ", "KO", "NO", " ", "KU", "NI", "I", "TI", "HA", "D", "NN", "NO", "*Shield ", "me", "-", "ka", "-"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 160, ["*Hrolf Battershield ", "TA", "D", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 168, ["NA", "NI", "KA", " ", "KA", "LTU", "TE", "KE", "YO", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 176, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
