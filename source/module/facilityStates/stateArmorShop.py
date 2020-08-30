# -*- coding: utf-8 -*-
import pyxel

from ..character import playerParty
from ..item import armorParams
from ..pyxelUtil import PyxelUtil
from .baseShopState import BaseShopState


class StateArmorShop(BaseShopState):
    '''
    鎧屋のクラス

    BaseFacilityStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    # この店で使うアイテムリスト
    itemList = armorParams.armorList

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 店員の初期データ
        self.saleParson.name = "Blick"
        self.saleParson.head = 13
        self.saleParson.body = 4

    def update_done(self):
        '''
        買った処理
        '''
        super().update_done()
        playerParty.memberList[self.equipMember].armor = self.item

    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.armor = self.item

    def render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["YO", "U", "KO", "SO", " ", "I", "RA",
                                 "LTU", "SI", "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["WA", "TA", "SI", "HA", "* Blick Armstrong ",
                                 "TO", " ", "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
