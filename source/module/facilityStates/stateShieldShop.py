# -*- coding: utf-8 -*-
import pyxel
from module.character import playerParty
from module.facilityStates.baseShopState import BaseShopState
from module.params.shield import shieldParams
from module.pyxelUtil import PyxelUtil
from overrides import overrides


class StateShieldShop(BaseShopState):
    '''
    盾屋のクラス\n
    BaseFacilityStateクラスを継承。\n
    選択した商品の購入、キャラクターへの装備を行う。
    '''

    # この店で使うアイテムリスト
    itemList = shieldParams

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 店員の初期データ
        self.saleParson.name = "Hrolf"
        self.saleParson.head = 81
        self.saleParson.body = 1

    @overrides
    def update_done(self):
        '''
        買った処理
        '''
        super().update_done()
        playerParty.memberList[self.equipMember].shield = self.item

    @overrides
    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.shield = self.item

    @overrides
    def draw_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["O", "RE", "HA", " ", "KO", "NO", " ", "KU", "NI", "I",
                                 "TI", "HA", "D", "NN", "NO", "*Shield ", "me", "-", "ka", "-"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*Hrolf Battershield ",
                                 "TA", "D", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 156, ["NA", "NI", "KA", " ", "KA",
                                 "LTU", "TE", "KE", "YO", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
