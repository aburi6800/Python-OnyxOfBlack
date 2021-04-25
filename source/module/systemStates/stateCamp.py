# -*- coding: utf-8 -*-
import os
import pickle

import pyxel
from module.character import playerParty
from module.facilityStates.baseFacilityState import BaseFacilityState
from module.pyxelUtil import PyxelUtil
from module.savedata import SaveData
from module.state import State
from overrides import overrides

class StateCamp(BaseFacilityState):
    '''
    キャンプメニューのクラス\n
    薬の使用／セーブ／ゲーム終了を行う。
    '''
    # 状態の定数
    STATE_MENU = 0
    STATE_POTION_SELECTHAVE = 1
    STATE_POTION_SELECTHAVEERROR = 2
    STATE_POTION_SELECTUSE = 3
    STATE_POTION_SELECTUSEERROR = 4
    STATE_POTION_DONE = 5
    STATE_SAVE_DOSAVE = 6
    STATE_SAVE_DONE = 7
    STATE_QUIT_DOQUIT = 8

    # キーとメンバーの辞書
    keyMap = {
        pyxel.KEY_1: 0,
        pyxel.KEY_2: 1,
        pyxel.KEY_3: 2,
        pyxel.KEY_4: 3,
        pyxel.KEY_5: 4,
    }

    # 状態
    state = STATE_MENU

    # 薬を使うメンバー
    haveMember = None

    # 薬を飲むメンバー
    useMember = None

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # 画像をロード
        pyxel.image(0).load(0, 205, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/png/camp.png")))

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

        if self.state == self.STATE_MENU:
            self.update_menu()
        elif self.state == self.STATE_POTION_SELECTHAVE:
            self.update_potion_selecthave()
        elif self.state == self.STATE_POTION_SELECTHAVEERROR:
            self.update_potion_selecthaveerror()
        elif self.state == self.STATE_POTION_SELECTUSE:
            self.update_potion_selectuse()
        elif self.state == self.STATE_POTION_SELECTUSEERROR:
            self.update_potion_selectuseerror()
        elif self.state == self.STATE_POTION_DONE:
            self.update_potion_done()
        elif self.state == self.STATE_SAVE_DOSAVE:
            self.update_save_dosave()
        elif self.state == self.STATE_SAVE_DONE:
            self.update_save_done()
        elif self.state == self.STATE_QUIT_DOQUIT:
            self.update_quit_doquit()
        
    def update_menu(self):
        '''
        メニューの処理\n
        選択されたキーにより状態を変更する
        '''
        # 薬を飲む
        if pyxel.btnp(pyxel.KEY_D):
            self.state = self.STATE_POTION_SELECTHAVE

        # セーブ
        if pyxel.btnp(pyxel.KEY_S):
            self.state = self.STATE_SAVE_DOSAVE

        # ゲームを中断
        if pyxel.btnp(pyxel.KEY_Q):
            self.state = self.STATE_QUIT_DOQUIT

        # キャンプを終わる
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.stateStack.pop()

    def update_potion_selecthave(self):
        '''
        薬の所持者選択\n
        1～5で持っている場合のみ選択し、状態を薬の使用者選択に変更。\n
        [SPACE]でメニューに戻る。
        '''
        self.haveMember = -1

        if pyxel.btnp(pyxel.KEY_SPACE):
            # 状態をメニューへ
            self.state = self.STATE_MENU
            return

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                self.haveMember = _value

        if self.haveMember != -1:
            if playerParty.memberList[self.haveMember].potion < 1:
                self.state = self.STATE_POTION_SELECTHAVEERROR
            else:
                self.state = self.STATE_POTION_SELECTUSE

    def update_potion_selecthaveerror(self):
        '''
        薬の所持者選択のエラー\n
        [SPACE]で薬の所持者選択に戻る。
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_POTION_SELECTHAVE

    def update_potion_selectuse(self):
        '''
        薬の使用者選択\n
        1～5で対象者を選択し薬を使用後、状態を薬の使用完了に変更。\n
        ただし、体力が減少している者にしか使えない。\n
        [SPACE]でメニューに戻る。
        '''
        self.useMember = -1

        if pyxel.btnp(pyxel.KEY_SPACE):
            # 状態をメニューへ
            self.state = self.STATE_MENU
            return

        for _key, _value in self.keyMap.items():
            if pyxel.btnp(_key) and len(playerParty.memberList) > _value:
                self.useMember = _value

        if self.useMember != -1:
            if playerParty.memberList[self.useMember].life == playerParty.memberList[self.useMember].maxlife:
                self.state = self.STATE_POTION_SELECTUSEERROR
            else:
                playerParty.memberList[self.haveMember].potion -= 1
                playerParty.memberList[self.useMember].life += 30
                if playerParty.memberList[self.useMember].life > playerParty.memberList[self.useMember].maxlife:
                    playerParty.memberList[self.useMember].life = playerParty.memberList[self.useMember].maxlife
                self.state = self.STATE_POTION_DONE

    def update_potion_selectuseerror(self):
        '''
        薬の使用者選択のエラー\n
        [SPACE]で薬の使用者選択に戻る。
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_POTION_SELECTUSE

    def update_potion_done(self):
        '''
        薬の使用完了\n
        [SPACE]でメニューに戻る。
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 状態をメニューへ
            self.state = self.STATE_MENU

    def update_save_dosave(self):
        '''
        セーブの確認\n
        [y]ならセーブを実行して状態をセーブ完了へ、[n]ならメニューに戻る。
        '''
        if pyxel.btnp(pyxel.KEY_Y):
            # セーブを実行
            s = SaveData(self.stateStack.states, playerParty)
            with open('savedata.dat', 'wb') as f:
                pickle.dump(s, f, protocol=3)

            # 状態をセーブ完了へ
            self.state = self.STATE_SAVE_DONE

        if pyxel.btnp(pyxel.KEY_N):
            # 状態をメニューへ
            self.state = self.STATE_MENU

    def update_save_done(self):
        '''
        セーブ完了\n
        [SPACE]でメニューに戻る。
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 状態をメニューへ
            self.state = self.STATE_MENU

    def update_quit_doquit(self):
        '''
        終了の確認\n
        [y]ならタイトルへ戻り、[n]ならメニューに戻る。
        '''
        if pyxel.btnp(pyxel.KEY_Y):
            # stateのスタックをクリア
            self.stateStack.clear()
            # タイトルのstateをpush
            self.stateStack.push(State.TITLE)

        if pyxel.btnp(pyxel.KEY_N):
            # 状態をメニューへ
            self.state = self.STATE_MENU

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        if self.state == self.STATE_MENU:
            self.draw_menu()
        elif self.state == self.STATE_POTION_SELECTHAVE:
            self.draw_potion_selecthave()
        elif self.state == self.STATE_POTION_SELECTHAVEERROR:
            self.draw_potion_selecthaveerror()
        elif self.state == self.STATE_POTION_SELECTUSE:
            self.draw_potion_selectuse()
        elif self.state == self.STATE_POTION_SELECTUSEERROR:
            self.draw_potion_selectuseerror()
        elif self.state == self.STATE_POTION_DONE:
            self.draw_potion_done()
        elif self.state == self.STATE_SAVE_DOSAVE:
            self.draw_save_dosave()
        elif self.state == self.STATE_SAVE_DONE:
            self.draw_save_done()
        elif self.state == self.STATE_QUIT_DOQUIT:
            self.draw_quit_doquit()

    def draw_menu(self):
        '''
        メニューの描画処理
        '''
        PyxelUtil.text(97, 140, ["*** CAMP MENU **"], pyxel.COLOR_LIGHTBLUE)
        PyxelUtil.text(16, 148, ["*[D] ", "KU", "SU", "RI",
                                 "WO", " ", "NO", "MU"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 156, ["*[S] ", "se", "-",
                                 "hu", "d"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 164, ["*[Q] ", "ke", "d", "-", "mu", "WO",
                                 " ", "TI", "LYU", "U", "TA", "D", "NN"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 172, ["*[SPACE] ", "ki", "lya", "nn", "hu",
                                 "hd", "WO", " ", "O", "WA", "RU"], pyxel.COLOR_YELLOW)

    def draw_potion_selecthave(self):
        '''
        薬の所持者選択の描画処理
        '''
        PyxelUtil.text(16, 140, ["TA", "D", "RE", "NO", " ", "KU", "SU", "RI", "WO", " ", "TU", "KA", "I", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*[SPACE] ", "me", "ni", "lyu", "-", "HE", " ", "MO", "TO", "D", "RU"], pyxel.COLOR_YELLOW)

    def draw_potion_selecthaveerror(self):
        '''
        薬の所持者選択のエラー描画処理
        '''
        PyxelUtil.text(16, 140, ["*" + playerParty.memberList[self.haveMember].name, "HA", " ", "KU", "SU", "RI", "WO", " ", "MO", "LTU", "TE", "I", "NA", "I", "*!"], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_potion_selectuse(self):
        '''
        薬の使用者選択の描画処理
        '''
        PyxelUtil.text(16, 140, ["TA", "D", "RE", "KA", "D", " ", "NO", "MI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*[SPACE] ", "me", "ni", "lyu", "-", "HE", " ", "MO", "TO", "D", "RU"], pyxel.COLOR_YELLOW)

    def draw_potion_selectuseerror(self):
        '''
        薬の使用者選択選択のエラー描画処理
        '''
        PyxelUtil.text(16, 140, ["*" + playerParty.memberList[self.useMember].name, "HA", " ", "KI", "SU", "D", "WO", " ", "O", "LTU", "TE", "I", "NA", "I", "*!"], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_potion_done(self):
        '''
        薬の使用完了の描画処理
        '''
        PyxelUtil.text(16, 140, ["*" + playerParty.memberList[self.useMember].name, "NO", " ", "*LIFE", "KA", "D", " ", "KA", "I", "HU", "KU", "SI", "TA", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_save_dosave(self):
        '''
        セーブの確認の描画処理
        '''
        PyxelUtil.text(16, 140, ["se", "-", "hu", "d", " ", "SI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*[Y] / [N]"], pyxel.COLOR_YELLOW)

    def draw_save_done(self):
        '''
        セーブ完了の描画処理
        '''
        PyxelUtil.text(16, 140, ["se", "-", "hu", "d", " ", "SI", "MA", "SI", "TA", "."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_quit_doquit(self):
        '''
        終了の確認の描画処理
        '''
        PyxelUtil.text(16, 140, ["ke", "d", "-", "mu", "WO", " ", "SI", "LYU", "U", "RI", "LYO", "U", " ", "SI", "MA", "SU", "KA", "*?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(16, 148, ["*[Y] / [N]"], pyxel.COLOR_YELLOW)

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        pass

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
