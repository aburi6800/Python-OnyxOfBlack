# -*- coding: utf-8 -*-
import os

import pyxel
from module.character import playerParty
from module.facilityStates.baseShopState import BaseShopState
from module.params.drug import drugParams
from module.pyxelUtil import PyxelUtil
from overrides import overrides


class StateDrugs(BaseShopState):
    '''
    薬屋のクラス\n
    BaseFacilityStateクラスを継承\n
    選択した商品の購入、キャラクターへの装備を行う。
    '''

    # この店で使うアイテムリスト
    itemList = drugParams

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 店員の初期データ
        self.saleParson.name = "Pandra"
        self.saleParson.head = 94
        self.saleParson.body = 9

        # 画像をロード
        pyxel.image(0).load(0, 205, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/png/drugs.png")))

    @overrides
    def update_done(self):
        '''
        買った処理\n
        スーパークラスの処理で金額が減るので、その前に所持数のチェックを行う
        '''
        # 容器を購入した時
        if self.itemNumber == 0:
            if playerParty.memberList[self.equipMember].potion == -1:
                # 容器をまだ持っていないときは、容器を購入済にする
                playerParty.memberList[self.equipMember].potion = 0
            else:
                # 容器を持っているときは、エラーとする
                self.errorMessage = ["*" + playerParty.memberList[self.equipMember].name, " ", "HA", " ", "SU", "TE", "D", "NI", " ", "YO", "U", "KI", "WO", " ", "MO", "LTU", "TE", "I", "MA", "SU", "."]
                self.state = self.STATE_ERROR
                return

        # 薬を購入した時
        if self.itemNumber == 1:
            if playerParty.memberList[self.equipMember].potion == -1:
                # 容器をまだ持っていないときは、エラーとする
                self.errorMessage = ["*" + playerParty.memberList[self.equipMember].name, " ", "HA", " ", "YO", "U", "KI", "WO", " ", "MO", "LTU", "TE", "I", "MA", "SE", "NN", "."]
                self.state = self.STATE_ERROR
                return
            elif playerParty.memberList[self.equipMember].potion == 4:
                # 既に最大数の薬を持っているときは、エラーとする
                self.errorMessage = ["*" + playerParty.memberList[self.equipMember].name, " ", "NO", " ", "YO", "U", "KI", "NI", "HA", " ", "MO", "U", "HA", "I", "RI", "MA", "SE", "NN", "."]
                self.state = self.STATE_ERROR
                return
            else:
                # 容器を持っていて最大数未満のときは、薬の数を追加する
                playerParty.memberList[self.equipMember].potion += 1

        super().update_done()

    @overrides
    def draw_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["I", "RA", "LTU", "SI", "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["WA", "TA", "SI", "HA", "* Pandra ",
                                 " ", "YA", "KU", "SA", "D", "I", "SI", "YO", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 156, ["KU", "SU", "RI", "TO", " ",
                                 "SO", "NO", "YO", "U", "KI", "WO", " ", "O", "I", "TE", "I", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
