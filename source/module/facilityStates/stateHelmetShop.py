# -*- coding: utf-8 -*-
import pyxel
from module.character import playerParty
from module.facilityStates.baseShopState import BaseShopState
from module.params.helmet import helmetParams
from module.pyxelUtil import PyxelUtil
from overrides import overrides


class StateHelmetShop(BaseShopState):
    '''
    兜屋のクラス\n
    BaseShopStateクラスを継承。\n
    選択した商品の購入、キャラクターへの装備を行う。
    '''

    # この店で使うアイテムリスト
    itemList = helmetParams

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 店員の初期データ
        self.saleParson.name = "Niels"
        self.saleParson.head = 94
        self.saleParson.body = 8

        pyxel.image(0).load(0, 205, "helmetshop.png")

    @overrides
    def update_done(self):
        '''
        買った処理
        '''
        super().update_done()
        playerParty.memberList[self.equipMember].helmet = self.item

    @overrides
    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.helmet = self.item

    @overrides
    def draw_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["I", "RA", "LTU", "SI",
                                 "LYA", "I", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*Niels Hjelmerssion ", "TO", " ",
                                 "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
