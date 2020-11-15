# -*- coding: utf-8 -*-
import pyxel
from module.character import Human, playerParty
from module.facilityStates.baseFacilityState import BaseFacilityState
from module.pyxelUtil import PyxelUtil


class StateExaminations(BaseFacilityState):
    '''
    身体検査のクラス

    BaseFacilityStateクラスを継承
    キャラクターのステータス調査を行う
    '''
    # 状態の定数
    STATE_ENTER = 0
    STATE_CHOOSE = 1
    STATE_DONE = 2
    STATE_LEAVE = 3

    # ステータス表示対象のメンバー
    showMember = None

    # キーとメンバーの辞書
    keyMap = {
        pyxel.KEY_1: 0,
        pyxel.KEY_2: 1,
        pyxel.KEY_3: 2,
        pyxel.KEY_4: 3,
        pyxel.KEY_5: 4,
    }

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 医者の初期データ
        self.saleParson = Human()
        self.saleParson.name = "Slea"
        self.saleParson.head = 97
        self.saleParson.body = 9

    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

        if self.state == self.STATE_ENTER:
            self.update_enter()

        elif self.state == self.STATE_CHOOSE:
            self.update_choose()

        elif self.state == self.STATE_DONE:
            self.update_done()

        elif self.state == self.STATE_LEAVE:
            self.update_leave()

    def update_enter(self):
        '''
        店に入った時の処理
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            # メンバー選択へ
            self.state = self.STATE_CHOOSE

    def update_choose(self):
        '''
        メンバー選択処理
        '''
        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                self.showMember = playerParty.memberList[_value]
                self.state = self.STATE_DONE

        if pyxel.btnp(pyxel.KEY_L):
            self.state = self.STATE_LEAVE

    def update_done(self):
        '''
        ステータス表示処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_CHOOSE

    def update_leave(self):
        '''
        店を出る処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 状態を終了する
            self.popState()

    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        if self.state == self.STATE_ENTER:
            self.draw_enter()

        elif self.state == self.STATE_CHOOSE:
            self.draw_choose()

        elif self.state == self.STATE_DONE:
            self.draw_done()

        elif self.state == self.STATE_LEAVE:
            self.draw_leave()

        # 店員描画
        self.drawCharacter(self.saleParson, 178, 104)

    def draw_enter(self):
        '''
        施設に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["WA", "TA", "SI", "HA", "* Slea ", "TO", "I", "U",
                                 "i", "si", "lya", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_choose(self):
        '''
        メンバー選択描画処理
        '''
        PyxelUtil.text(16, 140, ["TA", "D", "RE", "WO", " ", "MI", "TE", " ", "A",
                                 "KE", "D", "MA", "SI", "LYO", "U", "KA", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 164, ["*[L] ", "TA", "TI",
                                 "SA", "RU"], pyxel.COLOR_YELLOW)

    def draw_done(self):
        '''
        ステータス描画処理
        '''
        PyxelUtil.text(16, 140, ["*LEVEL     " +
                                 str(self.showMember.level)], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*LIFE      " +
                                 str(self.showMember.maxlife)], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 156, ["*STRENGTH  " +
                                 str(self.showMember.strength)], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 164, ["*DEFEND    " +
                                 str(self.showMember.defend)], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 172, ["*DEXTERITY " +
                                 str(self.showMember.dexterity)], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_leave(self):
        '''
        店を出る描画処理
        '''
        PyxelUtil.text(16, 140, ["TO", "D", "U", "MO", " ", "A", "RI", "KA", "D", "TO",
                                 "U", " ", "KO", "D", "SA", "D", "I", "MA", "SI", "TA", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 回復対象メンバーの初期値
        self.showMember = None

        # 最初の状態
        self.state = self.STATE_ENTER

    def onExit(self):
        '''
        状態終了時の処理
        '''
        # パーティーの座標と方向を復帰
        playerParty.restoreCondition()
