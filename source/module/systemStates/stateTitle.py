# -*- coding: utf-8 -*-
import os
import pickle

import pyxel
from module.character import playerParty
from module.events.eventData import eventdata
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
    STATE_STORY = 2
    STATE_STORY_WAIT = 3
    STATE_STORY_FADEOUT = 4
    STATE_TITLE = 5

    # フェードイン／アウトの色
    TEXTCOLOR = [pyxel.COLOR_BLACK] * 5
    TEXTCOLOR += [pyxel.COLOR_DARKBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_LIGHTBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_WHITE] * 30
    TEXTCOLOR += [pyxel.COLOR_LIGHTBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_DARKBLUE] * 5
    TEXTCOLOR += [pyxel.COLOR_BLACK] * 10

    # ストーリー
    # 秘宝「ブラックオニキス」。
    # それを手にすれば、無限の力と富を授かるという。
    # それはウツロの街のブラックタワーのどこかにあると伝えられていた。
    # この話を耳にしたあなたは、この神秘の宝を求める事を決意する。
    # そして、ブラックタワーに通じると言われている街の廃墟へと向かった。

    # The Black Onyx is a hidden treasure.
    # They say that if you get it, it will give you unlimited power and wealth.
    # It was said to be somewhere in the Black Tower in the city of Utsuro.
    # Upon hearing this story, you decide to seek out this mysterious treasure.
    # You head for the ruins of the city, which are said to lead to the Black Tower.
    STORY = (
        ("HI", "HO", "U", " ", "hu", "d", "ra", "ltu", "ku", "o", "ni", "ki", "su", "."),
        ("SO", "RE", "WO", " ", "TE", "NI", "SU", "RE", "HA", "D"),
        ("MU", "KE", "D", "NN", "NO", "TI", "KA", "RA", "TO", " ", "TO", "MI", "WO", " ", "SA", "SU", "D", "KA", "RU", "TO", " ", "I", "U", "."),
        ("SO", "RE", "HA", " ", "u", "tu", "ro", "NO", "MA", "TI", "NO", " ", "hu", "d", "ra", "ltu", "ku", "ta", "wa", "-", "NO"),
        ("TO", "D", "KO", "KA", "NI", " ", "A", "RU", "TO", " ", "TU", "TA", "E", "RA", "RE", "TE", "I", "TA", "."),
        (""),
        ("KO", "NO", " ", "HA", "NA", "SI", "WO", " ", "MI", "MI", "NI", "SI", "TA", " ", "A", "NA", "TA", "HA"),
        ("KO", "NO", " ", "SI", "NN", "HI", "HD", "NO", " ", "TA", "KA", "RA", "WO", " ", "MO", "TO", "ME", "RU", "KO", "TO", "WO"),
        ("KE", "TU", "I", "SU", "RU", "."),
        ("SO", "SI", "TE", " ", "hu", "d", "ra", "ltu", "ku", "ta", "wa", "-", "NI", " ", "TU", "U", "SI", "D", "RU", "TO", " ", "I", "WA", "RE", "RU"),
        ("MA", "TI", "NO", " ", "HA", "I", "KI", "LYO", "HE", " ", "MU", "KA", "LTU", "TA", "*...")
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # ストーリー表示用インデックス
        self.story_index = 0

        # ストーリー表示用カウンタ
        self.story_count = 0

        # イベントデータ初期化
        eventdata.reset()

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        if self.state == self.STATE_RESPECT:
            self.update_respect()
        elif self.state == self.STATE_STORY:
            self.update_stoty()
        elif self.state == self.STATE_STORY_WAIT:
            self.update_story_wait()
        elif self.state == self.STATE_STORY_FADEOUT:
            self.update_story_fadeout()
        elif self.state == self.STATE_TITLE:
            self.update_title()

    def update_respect(self):
        '''
        ヘンク・B・ロジャースへの敬意
        '''
        if self.tick - 1 == len(self.TEXTCOLOR):
            self.state = self.STATE_STORY

    def update_stoty(self):
        '''
        ストーリー表示
        '''
        if self.story_count >= 45:
            # 初期化
            self.story_index += 1
            self.story_count = 0

            if self.story_index >= len(self.STORY):
                self.state = self.STATE_STORY_WAIT
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_TITLE

        self.story_count += 1

    def update_story_wait(self):
        '''
        ストーリー全文表示
        '''
        self.story_count += 1
        if self.story_count >= 30:
            self.state = self.STATE_STORY_FADEOUT
            self.story_count = 45
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_TITLE

    def update_story_fadeout(self):
        '''
        ストーリー表示後フェードアウト
        '''
        self.story_count -= 1
        if self.story_count == 0:
            self.state = self.STATE_TITLE
        
        if pyxel.btnp(pyxel.KEY_SPACE):
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
                    self.stateStack.push(State.MAKECHARACTER)
                if self.selected == 2:
                    # セーブデータをロード
                    with open("savedata.dat", mode="rb") as f:
                        SaveData = pickle.load(f)
                    # stateStackを復元する
                    self.stateStack.states = SaveData.states
                    # 先頭は必ずキャンプなので、popする
                    self.stateStack.pop()
                    # StateStackへの参照を設定し直す
                    for state in self.stateStack.states:
                        state.stateStack = self.stateStack
                    # プレイヤーパーティーの復元
                    playerParty.resotreSaveData(SaveData.playerParty)

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        if self.state == self.STATE_RESPECT:
            self.draw_respect()
        if self.state == self.STATE_STORY:
            self.draw_story()
        if self.state == self.STATE_STORY_WAIT:
            self.draw_story_wait()
        if self.state == self.STATE_STORY_FADEOUT:
            self.draw_story_fadeout()
        elif self.state == self.STATE_TITLE:
            self.draw_title()

    def draw_respect(self):
        '''
        ヘンク・B・ロジャースへの敬意
        '''
        PyxelUtil.text(
            48, 95, ["*With all due respect to Henk B. Rogers."], self.TEXTCOLOR[self.tick - 1])

    def draw_story(self):
        '''
        ストーリー表示
        '''
        if pyxel.frame_count % 2 == 0:
            pyxel.blt(119, 72, 0, 0, 16, 16, 24)

        if self.story_index > 0:
            for i in range(self.story_index):
                PyxelUtil.text(20, i * 14 + 20, self.STORY[i])
        
        PyxelUtil.text(20, self.story_index * 14 + 20, self.STORY[self.story_index], self.TEXTCOLOR[self.story_count - 1])

    def draw_story_wait(self):
        '''
        ストーリー全文表示
        '''
        if pyxel.frame_count % 2 == 0:
            pyxel.blt(119, 72, 0, 0, 16, 16, 24)

        for i in range(len(self.STORY)):
            PyxelUtil.text(20, i * 14 + 20, self.STORY[i])

    def draw_story_fadeout(self):
        '''
        ストーリーフェードアウト
        '''
        if pyxel.frame_count % 2 == 0:
            pyxel.blt(119, 72, 0, 0, 16, 16, 24)

        for i in range(len(self.STORY)):
            PyxelUtil.text(20, i * 14 + 20, self.STORY[i], self.TEXTCOLOR[self.story_count - 1])

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

        PyxelUtil.text(58, 160, ["*COPYRIGHT BY ABURI6800 2020, 2021"], 2)
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
