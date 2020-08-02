# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..systemStates.baseSystemState import BaseSystemState


class StateTitle(BaseSystemState):
    '''
    タイトル画面クラス

    BaseSystemStateを継承
    タイトル画面の表示と各Stateへの遷移を行う
    '''
    # 状態の定数
    STATE_RESPECT = 1
    STATE_TITLE = 2

    # フェードイン／アウトの色
    TEXTCOLOR = [pyxel.COLOR_BLACK] * 10
    TEXTCOLOR += [pyxel.COLOR_DARKBLUE] * 10
    TEXTCOLOR += [pyxel.COLOR_LIGHTBLUE] * 10
    TEXTCOLOR += [pyxel.COLOR_WHITE] * 50
    TEXTCOLOR += [pyxel.COLOR_LIGHTBLUE] * 10
    TEXTCOLOR += [pyxel.COLOR_DARKBLUE] * 10
    TEXTCOLOR += [pyxel.COLOR_BLACK] * 30

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "Title"

        self.tick = 0
        self.state = self.STATE_RESPECT
        self.selected = 0

    def update(self):
        '''
        各フレームの処理
        '''
        self.tick += 1

        if self.state == self.STATE_RESPECT:
            self._update_respect()
        elif self.state == self.STATE_TITLE:
            self._update_title()

    def _update_respect(self):
        '''
        ヘンク・B・ロジャースへの敬意
        '''
        if self.tick == len(self.TEXTCOLOR):
            self.state = self.STATE_TITLE

    def _update_title(self):
        '''
        タイトル
        '''
        if pyxel.btnp(pyxel.KEY_G):
            self.selected = 1
            self.tick = 0

        if self.selected != 0:
            self.tick = self.tick + 1
            if self.tick > 21:
                if self.selected == 1:
                    self.stateStack.push(self.stateStack.STATE_CITY)

    def render(self):
        '''
        各フレームの描画処理
        '''
        if self.state == self.STATE_RESPECT:
            self._render_respect()
        elif self.state == self.STATE_TITLE:
            self._render_title()

    def _render_respect(self):
        '''
        ヘンク・B・ロジャースへの敬意
        '''
        PyxelUtil.text(48, 100, ["*With all due respect to Henk B. Rogers."], self.TEXTCOLOR[self.tick])

    def _render_title(self):
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

        PyxelUtil.text(88, 110, ["*[C]reate Character"], color[3])
        PyxelUtil.text(88, 118, ["*[G]o to Town"], color[0])
        PyxelUtil.text(88, 126, ["*[L]ook character State"], color[1])
        PyxelUtil.text(88, 134, ["*[K]ill Character"], color[2])

        PyxelUtil.text(68, 160, ["*COPYRIGHT BY ABURI6800 2020"], 2)
        PyxelUtil.text(68, 168, ["*ORIGINAL GAME BY B.P.S. 1984"], 2)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        pass

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
