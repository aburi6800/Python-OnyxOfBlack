# -*- coding: utf-8 -*-
import os
import pickle

import pyxel
from module.character import playerParty
from module.pyxelUtil import PyxelUtil
from module.state import State
from module.systemStates.baseSystemState import BaseSystemState
from overrides import overrides


class StateTitle(BaseSystemState):
    '''
    タイトル画面クラス\n
    BaseSystemStateを継承。\n
    タイトル画面の表示と各Stateへの遷移を行う。
    '''
    # 状態の定数
    STATE_RESPECT = 1
    STATE_TITLE = 2

    # フェードイン／アウトの色
    TEXTCOLOR = [pyxel.COLOR_BLACK] * 5
    TEXTCOLOR += [pyxel.COLOR_DARKBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_LIGHTBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_WHITE] * 30
    TEXTCOLOR += [pyxel.COLOR_LIGHTBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_DARKBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_BLACK] * 10

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        if self.state == self.STATE_RESPECT:
            self.update_respect()
        elif self.state == self.STATE_TITLE:
            self.update_title()

    def update_respect(self):
        '''
        ヘンク・B・ロジャースへの敬意
        '''
        if self.tick - 1 == len(self.TEXTCOLOR):
            self.state = self.STATE_TITLE

    def update_title(self):
        '''
        タイトル
        '''
        if self.selected == 0:
            if pyxel.btnp(pyxel.KEY_N):
                pyxel.play(3, 0, loop=False)
                self.selected = 1
                self.tick = 0

            if pyxel.btnp(pyxel.KEY_C) and self.doContinue:
                pyxel.play(3, 0, loop=False)
                self.selected = 2
                self.tick = 0

        else:
            if self.tick > 21:
                if self.selected == 1:
                    self.selected = 0
                    self.pushState(State.MAKECHARACTER)
                if self.selected == 2:
                    # セーブデータをロード
                    with open("savedata.dat", mode="rb") as f:
                        SaveData = pickle.load(f)
                    # stateStackのstatesを復元する
                    self.setStates(SaveData.states)
                    # 先頭は必ずキャンプなので、popする
                    self.popState()
                    # プレイヤーパーティーの復元
                    playerParty.resotreSaveData(SaveData.playerParty)

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        if self.state == self.STATE_RESPECT:
            self.draw_respect()
        elif self.state == self.STATE_TITLE:
            self.draw_title()

    def draw_respect(self):
        '''
        ヘンク・B・ロジャースへの敬意
        '''
        PyxelUtil.text(
            48, 95, ["*With all due respect to Henk B. Rogers."], self.TEXTCOLOR[self.tick - 1])

    def draw_title(self):
        '''
        タイトル
        '''
        PyxelUtil.text(64, 36, ["*Role Playing game"], 2)
        pyxel.blt(72, 48, 0, 0,  0, 26, 16, 0)
        pyxel.blt(52, 54, 0, 0, 16, 63, 24, 0)
        PyxelUtil.text(117, 68, ["*of"], 9)
        pyxel.blt(124, 54, 0, 64, 16, 80, 24, 0)

        color = [7, 7, 7, 7]
        if self.selected != 0:
            if self.tick % 2 == 0:
                color[self.selected - 1] = 0
            else:
                color[self.selected - 1] = 7

        PyxelUtil.text(104, 110, ["*[N]EW GAME"], color[0])
        if self.doContinue:
            PyxelUtil.text(104, 125, ["*[C]ONTINUE"], color[1])

        PyxelUtil.text(68, 160, ["*COPYRIGHT BY ABURI6800 2020"], 2)
        PyxelUtil.text(68, 168, ["*ORIGINAL GAME BY B.P.S. 1984"], 2)

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # このクラスの状態
        self.state = self.STATE_RESPECT

        # 選択番号
        self.selected = 0

        # セーブデータ存在チェック
        if os.path.exists("savedata.dat"):
            self.doContinue = True
        else:
            self.doContinue = False

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
