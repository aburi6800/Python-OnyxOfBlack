# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..facilityStates.baseFacilityState import BaseFacilityState
from ..character import playerParty
from ..character import Human
from ..item import armorParams


class StateArmorShop(BaseFacilityState):
    '''
    鎧屋のクラス

    BaseFacilityStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
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

    # アイテム番号
    itemNumber = None

    # アイテム
    item = None

    # 買ったメンバー
    buyMember = None

    # 持つメンバー
    equipMember = None

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
        '''
        super().__init__(stateStack)
        self.stateName = "ArmorShop"

        self.tick = 0
        self.selected = 0
        self.state = self.STATE_ENTER

        # 店員の初期データ
        self.saleParson = Human()
        self.saleParson.name = "Blick Armstrong"
        self.saleParson.head = 13
        self.saleParson.body = 1
        self.saleParson.armor = None
        self.saleParson.weapon = None
        self.saleParson.shield = None
        self.saleParson.helm = None

    def update(self):
        '''
        各フレームの処理
        '''
        if self.state == self.STATE_ENTER:
            self._update_enter()

        elif self.state == self.STATE_BUY:
            self._update_buy()

        elif self.state == self.STATE_EQUIP:
            self._update_equip()

        elif self.state == self.STATE_DONE:
            self._update_done()

        elif self.state == self.STATE_LEAVE:
            self._update_leave()

        elif self.state == self.STATE_EXIT:
            self._update_exit()

    def _update_enter(self):
        '''
        店に入った時の処理
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            self.itemNumber = 0
            self.item = armorParams.armorList[self.itemNumber]
            self.saleParson.armor = self.item
            self.state = self.STATE_BUY

    def _update_buy(self):
        '''
        買う人を選ぶ処理
        '''
        if pyxel.btn(pyxel.KEY_L):
            self.state = self.STATE_LEAVE

        if pyxel.btn(pyxel.KEY_ENTER):
            _selected = False
            while _selected == False:
                self.itemNumber += 1
                if self.itemNumber > len(armorParams.armorList) - 1:
                    self.itemNumber = 0
                if armorParams.armorList[self.itemNumber].price > 0:
                    _selected = True
            self.item = armorParams.armorList[self.itemNumber]
            self.saleParson.armor = self.item

        for _key, _value in self.keyMap.items():
            if pyxel.btn(_key) and len(playerParty.memberList) > _value and playerParty.memberList[_value].gold > armorParams.armorList[self.itemNumber].price:
                self.buyMember = _value
                self.state = self.STATE_EQUIP

    def _update_equip(self):
        '''
        装備する人を選ぶ処理
        '''
        if pyxel.btn(pyxel.KEY_L):
            self.state = self.STATE_LEAVE

        if pyxel.btn(pyxel.KEY_ENTER):
            self.state = self.STATE_BUY
            _selected = False
            while _selected == False:
                self.itemNumber += 1
                if self.itemNumber > len(armorParams.armorList) - 1:
                    self.itemNumber = 0
                if armorParams.armorList[self.itemNumber].price > 0:
                    _selected = True
            self.item = armorParams.armorList[self.itemNumber]
            self.saleParson.armor = self.item

        for _key, _value in self.keyMap.items():
            if pyxel.btn(_key) and len(playerParty.memberList) > _value:
                self.equipMember = _value
                self.state = self.STATE_DONE

    def _update_done(self):
        '''
        買った処理
        '''
        playerParty.memberList[self.buyMember].gold -= armorParams.armorList[self.itemNumber].price
        playerParty.memberList[self.equipMember].armor = armorParams.armorList[self.itemNumber]
        self.state = self.STATE_BUY

    def _update_leave(self):
        '''
        店を出る処理
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            self.state = self.STATE_EXIT

    def _update_exit(self):
        '''
        店を出た処理
        '''
        self.stateStack.pop()

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        if self.state == self.STATE_ENTER:
            self._render_initial()

        elif self.state == self.STATE_BUY:
            self._render_buy()

        elif self.state == self.STATE_EQUIP:
            self._render_equip()

        elif self.state == self.STATE_LEAVE:
            self._render_leave()

        # 店員
        self.drawCharacter(self.saleParson, 178, 112)

        # メンバーの所持金を表示
        for _idx in range(len(playerParty.memberList)):
            PyxelUtil.text(136, 16 + _idx * 16, ["*{:1d} : {:5d} G.P.".format(
                _idx + 1, playerParty.memberList[_idx].gold)], pyxel.COLOR_WHITE)

    def _render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 152, ["YO", "U", "KO", "SO", " ", "I", "RA",
                                 "LTU", "SI", "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 160, ["WA", "TA", "SI", "HA", "* Blick Armstrong ",
                                 "TO", " ", "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 176, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def _render_buy(self):
        '''
        買う人を選ぶ表示
        '''
        PyxelUtil.text(16, 152, ["*" + self.item.name + " (" + str(self.item.price) +
                                 " G.P.) ", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 160, ["TO", "D", "NA", "TA", "KA", "D", " ", "O", "KA",
                                 "I", "NI", "NA", "RI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 168, ["*[ENTER] ", "TU", "KI",
                                 "D", "NO", "a", "i", "te", "mu"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(56, 176, ["*[L]     ", "MI", "SE",
                                 "WO", "TE", "D", "RU"], pyxel.COLOR_YELLOW)

    def _render_equip(self):
        '''
        装備する人を選ぶ表示
        '''
        PyxelUtil.text(16, 160, ["TO", "D", "NA", "TA", "KA", "D", " ", "O", "TU", "KA",
                                 "I", "NI", "NA", "RI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 168, ["*[ENTER] ", "TU", "KI",
                                 "D", "NO", "a", "i", "te", "mu"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(56, 176, ["*[L]     ", "MI", "SE",
                                 "WO", "TE", "D", "RU"], pyxel.COLOR_YELLOW)

    def _render_leave(self):
        '''
        店を出る表示
        '''
        PyxelUtil.text(16, 162, ["TO", "D", "U", "MO", " ", "A", "RI", "KA", "D", "TO", "U", " ",
                                 "KO", "D", "SA", "D", "I", "MA", "SI", "TA", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 176, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        self.tick = 0
        self.selected = 0

    def onExit(self):
        '''
        状態終了時の処理
        '''
        playerParty.restoreCondition()
