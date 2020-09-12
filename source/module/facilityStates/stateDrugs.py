# -*- coding: utf-8 -*-
import pyxel

from ..character import playerParty
from ..pyxelUtil import PyxelUtil
from ..item import drugParams
from .baseShopState import BaseShopState


class StateDrugs(BaseShopState):
    '''
    薬屋のクラス

    BaseFacilityStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    # この店で使うアイテムリスト
    itemList = drugParams.drugList

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 店員の初期データ
        self.saleParson.name = "Pandra"
        self.saleParson.head = 94
        self.saleParson.body = 9

    def update_done(self):
        '''
        買った処理

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

    def render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["I", "RA", "LTU", "SI", "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["WA", "TA", "SI", "HA", "* Pandra ",
                                 " ", "YA", "KU", "SA", "D", "I", "SI", "YO", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 156, ["KU", "SU", "RI", "TO", " ",
                                 "SO", "NO", "YO", "U", "KI", "WO", " ", "O", "I", "TE", "I", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)
