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
    def update_equip(self):
        '''
        装備する人を選ぶ処理\n
        両手持ち武器を持っているときに盾を装備しようとすると、エラー処理に遷移する。\n
        また、既に同じ盾を装備している場合もエラー処理に遷移する。
        '''
        self.update_common()

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                # 選択した人が両手持ち武器を持っているか判定する
                if playerParty.memberList[_value].weapon != None and playerParty.memberList[_value].weapon.isDoubleHand:
                    # 両手持ち武器を持っている場合はエラー
                    self.errorMessage = [
                        "SO", "NO", "HU", "D", "KI", "TE", "D", "HA", " ", "MO", "TE", "MA", "SE", "NN", "."]
                    self.retuenState = self.state
                    self.state = self.STATE_ERROR
                    return
                # 選択した人の装備の名称と購入する装備の名称を比較
                elif playerParty.memberList[_value].shield != None and playerParty.memberList[_value].shield.name == self.item.name:
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
        playerParty.memberList[self.equipMember].shield = self.item

    @overrides
    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.shield = item

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
