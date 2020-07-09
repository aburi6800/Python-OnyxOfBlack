# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..facilityStates.baseShopState import BaseShopState
from ..character import playerParty
from ..character import Human
from ..item import helmetParams


class StateHelmetShop(BaseShopState):
    '''
    兜屋のクラス

    BaseShopStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "HelmetShop"

        # この店で使うアイテムリスト
        self.itemList = helmetParams.helmetList

        # 店員の初期データ
        self.saleParson.name = "Niels"
        self.saleParson.head = 33
        self.saleParson.body = 2

    def _update_done(self):
        '''
        買った処理
        '''
        super()._update_done()
        playerParty.memberList[self.equipMember].helmet = self.item

    def _update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.helmet = self.item

    def _render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 152, ["I", "RA", "LTU", "SI",
                                 "LYA", "I", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 160, ["*Niels Hjelmerssion ", "TO", " ",
                                 "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 176, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
