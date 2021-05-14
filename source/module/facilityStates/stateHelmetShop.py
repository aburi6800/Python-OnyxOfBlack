# -*- coding: utf-8 -*-
import os

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

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 店員の初期データ
        self.saleParson.name = "Niels"
        self.saleParson.head = 107
        self.saleParson.body = 8

        # 画像をロード
        pyxel.image(0).load(0, 205, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/png/helmetshop.png")))

    @overrides
    def update_equip(self):
        '''
        装備する人を選ぶ処理\n
        既に同じ兜を装備している場合はエラー処理に遷移する。
        '''
        self.update_common()

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                # 選択した人の装備の名称と購入する装備の名称を比較
                if playerParty.memberList[_value].helmet != None and playerParty.memberList[_value].helmet.name == self.item.name:
                    # 同じ場合はエラー
                    self.errorMessage = [
                        "MO", "U", " ", "MO", "LTU", "TE", "MA", "SU", "YO", "."]
                    self.retuenState = self.state
                    self.state = self.STATE_ERROR
                else:
                    self.equipMember = _value
                    self.state = self.STATE_DONE

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
        self.saleParson.helmet = item

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
