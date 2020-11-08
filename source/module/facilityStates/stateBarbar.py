# -*- coding: utf-8 -*-
import random
import pyxel

from ..character import playerParty
from ..params.barbar import barbarParams
from ..pyxelUtil import PyxelUtil
from .baseShopState import BaseShopState


class StateBarbar(BaseShopState):
    '''
    床屋のクラス

    BaseFacilityStateクラスを継承
    選択したキャラクターの頭部変更を行う
    '''

    # この店で使うアイテムリスト
    itemList = barbarParams

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 店員の初期データ
        self.saleParson.name = "Sasaki"
        self.saleParson.head = 114
        self.saleParson.body = 8

    def update_equip(self):
        '''
        装備する人を選ぶ処理

        スーパークラスのメソッドをオーバーライドしている
        床屋では散髪中のメッセージを表示するだけの処理
        '''
        if self.tick > 129 and pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_DONE

    def update_done(self):
        '''
        買った処理
        '''
        super().update_done()

        # 頭の種類をランダムで決定する。ただし、色は変えない。
        head = random.randint(
            0, 31) * ((playerParty.memberList[self.buyMember].head // 32) * 32)
        playerParty.memberList[self.buyMember].head = head

    def render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["*BAR BAR ", "sa", "sa", "ki", "HE",
                                 "YO", "U", "KO", "SO", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["su", "te", "ki", "NA", " ",
                                 "he", "a", "-", "su", "ta", "i", "ru", " ", "NI", " ", "SI", "MA", "SE", "NN", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def render_buy(self):
        '''
        散髪する人を選ぶ表示

        スーパークラスのメソッドをオーバーライド
        '''
        PyxelUtil.text(16, 140, ["TA", "D", "RE", "NO", " ",
                                 "ka", "mi", "ka", "d", "ta", " ", "WO", " ", "KA", "E", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TA", "D", "I", "KI", "NN", " ", "HA", " ",
                                 "*" + str(self.itemList[0].price) + "G.P. ", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 172, ["*[L] ", "MI", "SE",
                                 "WO", "TE", "D", "RU"], pyxel.COLOR_YELLOW)

    def render_equip(self):
        '''
        装備する人を選ぶ表示

        スーパークラスのメソッドをオーバーライド
        '''
        PyxelUtil.text(16, 140, ["TE", "D", "HA", " ", "KO", "TI", "RA", "NI", " ", "O",
                                 "SU", "WA", "RI", " ", "KU", "TA", "D", "SA", "I", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["ti", "lyo", "ki",
                                 "ti", "lyo", "ki", "*..."], pyxel.COLOR_WHITE)
        if self.tick > 120:
            PyxelUtil.text(16, 164, [
                           "HA", "I", ",", "TE", "D", "KI", "MA", "SI", "TA", "."], pyxel.COLOR_WHITE)
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
