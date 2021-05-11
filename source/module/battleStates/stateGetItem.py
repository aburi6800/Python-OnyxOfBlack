# -*- coding: utf-8 -*-
import random

import pyxel
from module.baseState import BaseState
from module.character import enemyParty, playerParty
from module.params.weapon import weaponParams
from module.params.armor import armorParams
from module.pyxelUtil import PyxelUtil
from overrides import overrides


class StateGetItem(BaseState):
    '''
    アイテム取得のクラス/n
    BaseStateクラスを継承
    '''
    # 状態の定数
    STATE_ITEMSELECT = 0
    STATE_CHOOSE_EQUIP = 1
    STATE_CHOOSE_ERROR = 2
    STATE_EQUIP = 3
    STATE_LEAVE = 4

    # ハンドラ用定数
    HANDLER_UPDATE = 0
    HANDLER_DRAW = 1

    # キーとインデックスの辞書
    key_to_index = {
        pyxel.KEY_1: 0,
        pyxel.KEY_2: 1,
        pyxel.KEY_3: 2,
        pyxel.KEY_4: 3,
        pyxel.KEY_5: 4,
    }

    # アイテムの種別
    ITEMTYPE_WEAPON = 1
    ITEMTYPE_ARMOR = 2
    ITEMTYPE_SHIELD = 3 # 未実装だが定数としては定義しておく
    ITEMTYPE_HELMET = 4 # 未実装だが定数としては定義しておく

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 時間カウント用
        self.tick = 0

        # アイテムの種別
        self.itemType = 0

        # アイテム
        self.item = None

        # メンバーのインデックス
        self.member_index = 0

        # メッセージリスト
        # 各リスト要素の1つ目はメッセージリスト、2つ目は表示色
        self.message = []

        # ハンドラ辞書
        self.handler = {
            self.STATE_ITEMSELECT: [self.update_itemSelect, self.draw_itemSelect],
            self.STATE_CHOOSE_EQUIP: [self.update_choose_equip, self.draw_choose_equip],
            self.STATE_CHOOSE_ERROR: [self.update_choose_error, self.draw_choose_error],
            self.STATE_EQUIP: [self.update_equip, self.draw_equip],
            self.STATE_LEAVE: [self.update_leave, self.draw_leave],
        }

        # 状態
        self.state = 0

    def change_state(self, _state):
        '''
        状態変更処理
        '''
        self.state = _state
        self.tick = 0
        self.message = []

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_UPDATE]()

    def update_itemSelect(self):
        '''
        アイテム選出時の処理
        '''
        _r = random.randint(0, 4)
        if _r == 0 or _r == 1:
            # 武器を選出
            self.item = weaponParams[random.randint(enemyParty.level - 1, enemyParty.level + 2)]
            self.item.attack = int(self.item.attack * 1.5)
            self.itemType = self.ITEMTYPE_WEAPON
        elif _r == 2 or _r == 3:
            # 鎧を選出
            self.item = armorParams[random.randint((enemyParty.level - 1) // 2, (enemyParty.level - 1) // 2 + 1)]
            self.item.armor = int(self.item.armor * 1.5)
            self.itemType = self.ITEMTYPE_ARMOR

        self.change_state(self.STATE_CHOOSE_EQUIP)

    def update_choose_equip(self):
        '''
        装備するメンバーの選択処理
        '''
        if pyxel.btnp(pyxel.KEY_L):
            self.change_state(self.STATE_LEAVE)
            return

        _idx = 0

        if pyxel.btnp(pyxel.KEY_1):
            _idx = 1
        elif pyxel.btnp(pyxel.KEY_2) and len(playerParty.memberList) > 1:
            _idx = 2
        elif pyxel.btnp(pyxel.KEY_3) and len(playerParty.memberList) > 2:
            _idx = 3
        elif pyxel.btnp(pyxel.KEY_4) and len(playerParty.memberList) > 3:
            _idx = 4
        elif pyxel.btnp(pyxel.KEY_5) and len(playerParty.memberList) > 4:
            _idx = 5

        if _idx > 0:
            self.member_index = _idx - 1
            # 種別が武器の時で両手持ちの時は、対象キャラクターが盾を持っている場合はエラーとする
            if self.itemType == self.ITEMTYPE_WEAPON and self.item.isDoubleHand and playerParty.memberList[self.member_index].shield != None:
                self.change_state(self.STATE_CHOOSE_ERROR)
            else:
                self.change_state(self.STATE_EQUIP)


    def update_choose_error(self):
        '''
        装備不可エラーの処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.change_state(self.STATE_CHOOSE_EQUIP)


    def update_equip(self):
        '''
        アイテム装備処理
        '''
        if self.itemType == self.ITEMTYPE_WEAPON:
            playerParty.memberList[self.member_index].weapon = self.item
        elif self.itemType == self.ITEMTYPE_ARMOR:
            playerParty.memberList[self.member_index].armor = self.item
        else:
            pass

        self.change_state(self.STATE_LEAVE)

    def update_leave(self):
        '''
        終了処理
        '''
        self.stateStack.pop()

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_DRAW]()

    def draw_itemSelect(self):
        '''
        アイテム選出時の表示処理
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_choose_equip(self):
        '''
        装備するメンバーの選択表示処理
        '''
        PyxelUtil.text(16, 140, ["SU", "HA", "D", "RA", "SI", "I",
                                "* " + self.item.name + " ", "WO", " ", "MI", "TU", "KE", "TA", "* !"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TA", "D", "RE", "KA", "D", " ", "TU", "KA", "I", "MA", "SU", "KA", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(56, 172, ["*[L] ", "TU", "KA",
                                 "WA", "NA", "I"], pyxel.COLOR_YELLOW)

    def draw_choose_error(self):
        '''
        装備不可エラーの表示処理
        '''
        PyxelUtil.text(16, 140, ["*" + playerParty.memberList[self.member_index].name + " ", "HA", 
                                "* " + self.item.name + " ", "WO", " ", "MO", "TE", "NA", "I", "* !"], pyxel.COLOR_RED)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_equip(self):
        '''
        アイテム装備表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_leave(self):
        '''
        終了表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 状態を最初に設定する
        self.state = self.STATE_ITEMSELECT

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass

    def clearMessage(self) -> None:
        '''
        メッセージクリア
        '''
        self.message = []

    def addMessage(self, argMessage, argColor=pyxel.COLOR_WHITE) -> None:
        '''
        メッセージ追加処理\n
        引数に追加するメッセージ（リスト）と表示色（省略時は白）を指定する。
        '''
        self.message.append([argMessage, argColor])
