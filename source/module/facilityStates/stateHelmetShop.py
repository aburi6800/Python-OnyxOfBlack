# -*- coding: utf-8 -*-
import pyxel

from ..character import playerParty
from ..item import helmetParams
from ..pyxelUtil import PyxelUtil
from .baseShopState import BaseShopState


class StateHelmetShop(BaseShopState):
    '''
    兜屋のクラス

    BaseShopStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    # この店で使うアイテムリスト
    itemList = helmetParams.helmetList

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 店員の初期データ
        self.saleParson.name = "Niels"
        self.saleParson.head = 33
        self.saleParson.body = 2

    def update_done(self):
        '''
        買った処理
        '''
        super().update_done()
        playerParty.memberList[self.equipMember].helmet = self.item

    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.helmet = self.item

    def render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["I", "RA", "LTU", "SI",
                                 "LYA", "I", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*Niels Hjelmerssion ", "TO", " ",
                                 "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
