# -*- coding: utf-8 -*-
import os

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
    # 状態の定数
    STATE_NOEQUIP = 6

    # この店で使うアイテムリスト
    itemList = shieldParams

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 店員の初期データ
        self.saleParson.name = "Hrolf"
        self.saleParson.head = 115
        self.saleParson.body = 1

        # 画像をロード
        pyxel.image(0).load(0, 205, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/png/shieldshop.png")))

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

        if self.state == self.STATE_NOEQUIP:
            self.update_noequip()

    @overrides
    def update_equip(self):
        '''
        装備する人を選ぶ処理\n
        両手持ち武器を持っているときに盾を装備しようとすると、エラー処理に遷移する。\n
        盾屋独自の処理となる
        '''
        self.update_common()

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                self.equipMember = _value
                if playerParty.memberList[_value].weapon.isDoubleHand:
                    self.state = self.STATE_NOEQUIP
                else:
                    self.state = self.STATE_DONE

    def update_noequip(self):
        '''
        両手持ち武器を持っているときのエラー処理\n
        盾屋独自の処理となる
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            self.state = self.STATE_EQUIP

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
    def draw(self):
        '''
        各フレームの描画処理\n
        エラー処理を追加したもの。
        '''
        super().draw()

        if self.state == self.STATE_NOEQUIP:
            self.draw_noequip()

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

    def draw_noequip(self):
        '''
        両手持ち武器を持っているときのエラー表示処理\n
        盾屋独自の処理となる
        '''
        PyxelUtil.text(16, 140, ["SO", "NO", "HU", "D", "KI", "WO", " ", "MO", "LTU", "TE", "I", "TA", "RA"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TA", "TE", "HA", " ", "MO", "TE", "NA", "I", "SO", "D", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
