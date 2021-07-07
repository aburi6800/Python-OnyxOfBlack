# -*- coding: utf-8 -*-
import os

import pyxel
from module.character import playerParty
from module.facilityStates.baseShopState import BaseShopState
from module.params.weapon import weaponParams
from module.pyxelUtil import PyxelUtil
from overrides import overrides


class StateWeaponShop(BaseShopState):
    '''
    武器屋のクラス\n
    BaseShopStateクラスを継承。\n
    選択した商品の購入、キャラクターへの装備を行う。
    '''
    # 状態の定数
    STATE_CONFIRM = 6

    # この店で使うアイテムリスト
    itemList = weaponParams

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 店員の初期データ
        self.saleParson.name = "Darnoc"
        self.saleParson.head = 114
        self.saleParson.body = 1

        # 画像をロード
        pyxel.image(0).load(0, 205, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/png/weaponshop.png")))

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

        if self.state == self.STATE_CONFIRM:
            self.update_confirm()

    @overrides
    def update_equip(self):
        '''
        装備する人を選ぶ処理\n
        盾を持っているときに両手持ち武器を装備しようとすると、確認処理に遷移する。\n
        また、既に同じ武器を装備している場合はエラー処理に遷移する。
        '''
        self.update_common()

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                # 選択した人の装備の名称と購入する装備の名称を比較
                if playerParty.memberList[_value].weapon != None and playerParty.memberList[_value].weapon.name == self.item.name:
                    # 同じ場合はエラー
                    self.errorMessage = [
                        "MO", "U", " ", "MO", "LTU", "TE", "MA", "SU", "YO", "."]
                    self.retuenState = self.state
                    self.state = self.STATE_ERROR
                # 盾を持っており両手持ち武器を装備しようとしているか判定する
                elif playerParty.memberList[_value].shield != None and self.item.isDoubleHand:
                    self.equipMember = _value
                    self.state = self.STATE_CONFIRM
                else:
                    self.equipMember = _value
                    self.state = self.STATE_DONE

    def update_confirm(self):
        '''
        両手持ち武器を買うときの確認処理\n
        武器屋独自の処理となる
        '''
        if pyxel.btn(pyxel.KEY_Y):
            # 盾を外す
            playerParty.memberList[self.equipMember].shield = None
            self.state = self.STATE_DONE

        if pyxel.btn(pyxel.KEY_N):
            self.state = self.STATE_EQUIP

    @overrides
    def update_done(self):
        '''
        買った処理
        '''
        super().update_done()
        playerParty.memberList[self.equipMember].weapon = self.item

    @overrides
    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理
        '''
        self.saleParson.weapon = item

    @overrides
    def draw(self):
        '''
        各フレームの描画処理\n
        確認処理を追加したもの。
        '''
        super().draw()

        if self.state == self.STATE_CONFIRM:
            self.draw_confirm()

    @overrides
    def draw_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["I", "RA", "LTU", "SI",
                                 "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*Darnoc ", "HU", "D", "KI", " ", "SE", "NN", "MO", "NN",
                                 "TE", "D", " ", "KO", "D", "SA", "D", "I", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_confirm(self):
        '''
        両手持ち武器を買うときの確認表示処理\n
        武器屋独自の処理となる
        '''
        PyxelUtil.text(16, 140, ["KO", "NO", "HU", "D", "KI", "HA", " ", "RI", "LYO", "U", "TE", "MO", "TI", "TA", "D", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TA", "TE", "WO", " ", "MO", "TE", "NA", "KU", "NA", "RU", "KA", "D", " ", "I", "I", "KA", "NE", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 164, ["* [Y] ", "HA", "I"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(56, 172, ["* [N] ", "I", "I", "E"], pyxel.COLOR_YELLOW)
