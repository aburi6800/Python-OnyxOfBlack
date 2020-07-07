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
    # このクラスの状態
    state = 0

    # アイテム番号
    itemNumber = None

    # アイテム
    item = None

    # 買ったメンバー
    buyMember = None

    # 持つメンバー
    haveMember = None

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "ArmorShop"

        self.tick = 0
        self.selected = 0

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
        if self.state == 0:
            self._update_initial()

        if self.state == 1:
            self._update_select()

        if self.state == 4:
            self._update_leave()

        if self.state == 5:
            self._update_exit()

    def _update_initial(self):
        '''
        店に入った時の処理

        スペースキーの入力だけ待つ
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            self.itemNumber = 0
            self.item = armorParams.armorList[self.itemNumber]
            self.saleParson.armor = self.item
            self.state = 1

    def _update_select(self):
        '''
        選ぶ処理
        '''
        if pyxel.btn(pyxel.KEY_L):
            self.state = 4

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

    def _update_leave(self):
        '''
        店を出る処理
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            self.state = 5

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

        if self.state == 0:
            self._render_initial()

        if self.state == 1:
            self._render_select()

        if self.state == 4:
            self._render_leave()

        # 店員
        self.drawCharacter(self.saleParson, 178, 112)

    def _render_initial(self):
        '''
        店に入った時の表示
        '''
        PyxelUtil.text(16, 152, ["YO", "U", "KO", "SO", " ", "I", "RA",
                                 "LTU", "SI", "LYA", "I", "MA", "SE", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 160, ["WA", "TA", "SI", "HA", "* Blick Armstrong ",
                                 "TO", " ", "MO", "U", "SI", "MA", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 176, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def _render_select(self):
        '''
        選ぶ表示
        '''
        PyxelUtil.text(16, 152, ["*" + self.item.name + " (" + str(self.item.price) +
                                 " G.P.) ", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 160, ["TO", "D", "NA", "TA", "KA", "D", " ", "O", "KA",
                                 "I", "NI", "NA", "RI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 168, ["*[ANY KEY] ", "TU", "KI",
                                 "D", "NO", "a", "i", "te", "mu"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(56, 176, ["*[L]       ", "MI", "SE",
                                 "WO", "TE", "D", "RU"], pyxel.COLOR_YELLOW)

        # メンバーの所持金を表示
        for _idx in range(len(playerParty.memberList)):
            PyxelUtil.text(136, 16 + _idx * 16, ["*{:1d} : {:5d} G.P.".format(
                _idx + 1, playerParty.memberList[_idx].gold)], pyxel.COLOR_WHITE)

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
