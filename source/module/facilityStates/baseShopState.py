# -*- coding: utf-8 -*-
import pyxel

from ..character import Human, playerParty
from ..pyxelUtil import PyxelUtil
from .baseFacilityState import BaseFacilityState


class BaseShopState(BaseFacilityState):
    '''
    店の基底クラス

    BaseFacilityStateクラスを継承
    各店の共通の処理を持つ
    '''
    # 状態の定数
    STATE_ENTER = 0
    STATE_BUY = 1
    STATE_EQUIP = 2
    STATE_DONE = 3
    STATE_LEAVE = 4
    STATE_EXIT = 5

    # このクラスの状態
    state = STATE_ENTER

    # アイテムリスト
    itemList = None

    # アイテム番号
    itemNumber = None

    # アイテム
    item = None

    # 買ったメンバー
    buyMember = None

    # 持つメンバー
    equipMember = None

    # 店員
    saleParson = Human()

    # キーとメンバーの辞書
    keyMap = {
        pyxel.KEY_1: 0,
        pyxel.KEY_2: 1,
        pyxel.KEY_3: 2,
        pyxel.KEY_4: 3,
        pyxel.KEY_5: 4,
    }

    def __init__(self, stateStack):
        '''
        クラス初期化

        継承先のクラスでは、saleParsonとitemListの設定を行うこと。
        '''
        super().__init__(stateStack)

        # 店員
        self.saleParson = Human()

        self.onEnter()

    def update(self):
        '''
        各フレームの処理
        '''
        if self.state == self.STATE_ENTER:
            self.update_enter()

        elif self.state == self.STATE_BUY:
            self.update_buy()

        elif self.state == self.STATE_EQUIP:
            self.update_equip()

        elif self.state == self.STATE_DONE:
            self.update_done()

        elif self.state == self.STATE_LEAVE:
            self.update_leave()

        elif self.state == self.STATE_EXIT:
            self.update_exit()

    def update_enter(self):
        '''
        店に入った時の処理
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            self.itemNumber = 0
            self.item = self.itemList[self.itemNumber]
            self.update_equip_saleParson(self.item)
            self.state = self.STATE_BUY

    def update_buy(self):
        '''
        買う人を選ぶ処理
        '''
        self.update_common()

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value and playerParty.memberList[_value].gold >= self.item.price:
                self.buyMember = _value
                self.state = self.STATE_EQUIP

    def update_equip(self):
        '''
        装備する人を選ぶ処理
        '''
        self.update_common()

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                self.equipMember = _value
                self.state = self.STATE_DONE

    def update_done(self):
        '''
        買った処理

        継承先のクラスでは、memberに買ったitemを持たせること
        '''
        playerParty.memberList[self.buyMember].gold -= self.item.price
        self.state = self.STATE_BUY

    def update_leave(self):
        '''
        店を出る処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_EXIT

    def update_exit(self):
        '''
        店を出た処理
        '''
        self.stateStack.pop()

    def update_common(self):
        '''
        Lキー、ENTERキーを押したときの共通処理
        '''
        # Lキー
        if pyxel.btnp(pyxel.KEY_L):
            self.state = self.STATE_LEAVE

        # SPACEキー
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_BUY
            _selected = False
            while _selected == False:
                self.itemNumber += 1
                if self.itemNumber > len(self.itemList) - 1:
                    self.itemNumber = 0
                if self.itemList[self.itemNumber].price > 0:
                    _selected = True
            self.item = self.itemList[self.itemNumber]
            self.update_equip_saleParson(self.item)

    def update_equip_saleParson(self, item):
        '''
        店員の装備を変更する処理

        継承先のクラスでオーバーライドし、選択中のitemを持たせること
        '''
        None

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        if self.state == self.STATE_ENTER:
            self.render_initial()

        elif self.state == self.STATE_BUY:
            self.render_buy()

        elif self.state == self.STATE_EQUIP:
            self.render_equip()

        elif self.state == self.STATE_LEAVE:
            self.render_leave()

        # 店員
        self.drawCharacter(self.saleParson, 178, 104)

        # メンバーの所持金を表示
#        for idx, member in enumerate(playerParty.memberList):
#            PyxelUtil.text(
#                136, 16 + idx * 16, ["*{:1d} : {:5d} G.P.".format(idx + 1, member.gold)], pyxel.COLOR_WHITE)

    def render_initial(self):
        '''
        店に入った時の表示

        継承先のクラスでそれぞれ実装すること
        '''
        None

    def render_buy(self):
        '''
        買う人を選ぶ表示
        '''
        PyxelUtil.text(16, 140, ["*" + self.item.name + " (" + str(self.item.price) +
                                 " G.P.) ", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TO", "D", "NA", "TA", "KA", "D", " ", "O", "KA",
                                 "I", "NI", "NA", "RI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 156, ["*[SPACE] ", "TU", "KI",
                                 "D", "NO", "a", "i", "te", "mu"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(56, 164, ["*[L]     ", "MI", "SE",
                                 "WO", "TE", "D", "RU"], pyxel.COLOR_YELLOW)

    def render_equip(self):
        '''
        装備する人を選ぶ表示
        '''
        PyxelUtil.text(16, 140, ["TO", "D", "NA", "TA", "KA", "D", " ", "O", "TU", "KA",
                                 "I", "NI", "NA", "RI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 148, ["*[SPACE] ", "TU", "KI",
                                 "D", "NO", "a", "i", "te", "mu"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(56, 156, ["*[L]     ", "MI", "SE",
                                 "WO", "TE", "D", "RU"], pyxel.COLOR_YELLOW)

    def render_leave(self):
        '''
        店を出る表示
        '''
        PyxelUtil.text(16, 148, ["TO", "D", "U", "MO", " ", "A", "RI", "KA", "D", "TO", "U", " ",
                                 "KO", "D", "SA", "D", "I", "MA", "SI", "TA", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 最初の状態
        self.state = self.STATE_ENTER

    def onExit(self):
        '''
        状態終了時の処理
        '''
        # パーティーの座標と方向を復帰
        playerParty.restoreCondition()
