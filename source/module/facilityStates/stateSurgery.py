# -*- coding: utf-8 -*-
import pyxel

from ..character import Human, playerParty
from ..pyxelUtil import PyxelUtil
from .baseFacilityState import BaseFacilityState


class StateSurgery(BaseFacilityState):
    '''
    緊急治療のクラス

    BaseFacilityStateクラスを継承
    キャラクターのLIFEの回復を行う
    '''
    # 状態の定数
    STATE_ENTER = 0
    STATE_CHOOSE = 1
    STATE_ISSURGERY = 2
    STATE_NOMONEY = 3
    STATE_DONE = 4
    STATE_LEAVE = 5
    STATE_NOSURGERY = 6

    # 回復対象のメンバー
    member = None

    # 回復対象のメンバーのインデックス
    memberIndex = 0

    # 回復費用
    price = 0

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "Surgery"

        # 医者の初期データ
        self.saleParson = Human()
        self.saleParson.name = "Slea"
        self.saleParson.head = 96
        self.saleParson.body = 9

        # 初期設定
        self.onEnter()

    def update(self):
        '''
        各フレームの処理
        '''
        if self.state == self.STATE_ENTER:
            self.update_enter()

        elif self.state == self.STATE_ISSURGERY:
            self.update_issurgery()

        elif self.state == self.STATE_DONE:
            self.update_done()

        elif self.state == self.STATE_LEAVE:
            self.update_leave()

        elif self.state == self.STATE_NOSURGERY:
            self.update_nosurgery()

    def update_enter(self):
        '''
        店に入った時の処理
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            # 次の対象メンバーを探す。いない場合は終了する。
            if self.searchSurgeryMember():
                # 治療確認へ
                self.state = self.STATE_ISSURGERY
            else:
                # 治療不可へ
                self.state = self.STATE_NOSURGERY

    def update_issurgery(self):
        '''
        治療確認処理
        '''
        if pyxel.btnp(pyxel.KEY_Y):
            # メンバーの所持金が治療費以上か
            if self.member.gold >= self.price:
                # メンバーの所持金から治療費を減算
                self.member.gold = self.member.gold - self.price
                # メンバーのライフを回復
                self.member.life = self.member.maxlife
                # 治療終了へ
                self.state = self.STATE_DONE
            else:
                # 治療不可へ
                self.state = self.STATE_NOMONEY

        if pyxel.btnp(pyxel.KEY_N):
            # 次の対象メンバーを探す。いない場合は終了する。
            if self.searchSurgeryMember():
                return
            else:
                # 治療不可へ
                self.state = self.STATE_NOSURGERY

    def update_done(self):
        '''
        治療処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 次の対象メンバーを探す。いない場合は終了する。
            if self.searchSurgeryMember():
                # 診察料算出
                self.price = round(
                    (self.member.maxlife - self.member.life) * (1 + self.member.level / 2))
                # 治療確認へ
                self.state = self.STATE_ISSERGERY
            else:
                # 治療終了へ
                self.state = self.STATE_LEAVE

    def update_leave(self):
        '''
        店を出る処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 状態を終了する
            self.stateStack.pop()

    def update_nomoney(self):
        '''
        治療不可処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 次の対象メンバーを探す。いない場合は終了する。
            if self.searchSurgeryMember():
                # 治療確認へ
                self.state = self.STATE_ISSURGERY
            else:
                # 店を出る
                self.state = self.STATE_LEAVE

    def update_nosurgery(self):
        '''
        治療不要処理
        '''
        self.update_leave()

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        if self.state == self.STATE_ENTER:
            self.render_enter()

        elif self.state == self.STATE_ISSURGERY:
            self.render_issurgery()

        elif self.state == self.STATE_DONE:
            self.render_done()

        elif self.state == self.STATE_LEAVE:
            self.render_leave()

        elif self.state == self.STATE_NOSURGERY:
            self.render_nosurgery()

        # 店員描画
        self.drawCharacter(self.saleParson, 178, 104)

    def render_enter(self):
        '''
        施設に入った時の表示
        '''
        PyxelUtil.text(16, 140, ["WA", "TA", "SI", "HA", "* Slea ",
                                 "i", "si", "lya", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TO", "D", "RE", "TO", "D", "RE", " ", "SI", "NN", "SA", "TU",
                                 " ", "SI", "TE", " ", "A", "KE", "D", "MA", "SI", "LYO", "U", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def render_iseurgery(self):
        '''
        治療確認描画処理
        '''
        PyxelUtil.text(16, 140, ["*" + self.member.name + " ", "NO", " ", "TI", "RI", "LYO", "U", "HI",
                                 " ", "HA", " ", "*" + str(self.price) + "gold", " ", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["TI", "RI", "LYO", "U", " ",
                                 "SI", "MA", "SU", "KA", "*? [Y/N]"], pyxel.COLOR_WHITE)

    def render_done(self):
        '''
        治療完了描画処理
        '''
        PyxelUtil.text(16, 140, ["*" + self.member.name + " ", "HA", " ", "SU", "LTU", "KA", "RI", " ",
                                 "YO", "KU", "NA", "RI", "MA", "SI", "TA", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def render_leave(self):
        '''
        店を出る描画処理
        '''
        PyxelUtil.text(16, 140, ["O", "TA", "D", "I",
                                 "SI", "D", "NI", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def render_nosurgery(self):
        '''
        治療不要描画処理
        '''
        PyxelUtil.text(16, 140, ["MI", "NA", "SA", "NN", " ", "KE",
                                 "NN", "KO", "U", "TE", "D", "SU", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 回復対象メンバーの初期値
        self.member = None

        # 回復対象メンバーのインデックス初期値
        self.memberIndex = -1

        # 最初の状態
        self.state = self.STATE_ENTER

    def onExit(self):
        '''
        状態終了時の処理
        '''
        # パーティーの座標と方向を復帰
        playerParty.restoreCondition()

    def searchSurgeryMember(self) -> bool:
        '''
        治療対象の次のメンバーを探す
        対象のメンバーがいる場合はself.memberとself.memberIndex設定してTrueを返却する
        対象がいない場合はself.memberにNone、self.memberIndexに-1を設定してFalseを返却する
        '''
        self.member = None
        for idx, member in enumerate(playerParty.memberList):
            if member.life < member.maxlife and idx != self.memberIndex:
                # 回復対象メンバー
                self.member = member
                # 回復対象メンバーのインデックス
                self.memberIndex = idx
                # 診察料算出
                self.price = round(
                    (self.member.maxlife - self.member.life) * (1 + self.member.level / 2))
                return True

        # 最後まで対象のメンバーが見つからなかった場合はmemberIndexに-1を設定する
        self.memberIndex = -1
        return False
