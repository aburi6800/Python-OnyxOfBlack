# -*- coding: utf-8 -*-
import os
import pickle
import random

import pyxel
from module.character import playerParty
from module.constant.state import State
from module.eventHandler import eventhandler
from module.messageHandler import messagehandler
from module.params.eventData import eventdata
from module.pyxelUtil import PyxelUtil
from module.systemStates.baseSystemState import BaseSystemState
from module.musicPlayer import musicPlayer
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
    STATE_TITLE_FADEIN = 5
    STATE_TITLE = 6

    # テキストのフェードイン／アウトの色
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
        ("HI", "HO", "U", " ", "hu", "d", "ra",
         "ltu", "ku", "o", "ni", "ki", "su", "."),
        ("SO", "RE", "WO", " ", "TE", "NI", "SU", "RE", "HA", "D"),
        ("MU", "KE", "D", "NN", "NO", "TI", "KA", "RA", "TO", " ", "TO", "MI",
         "WO", " ", "SA", "SU", "D", "KA", "RU", "TO", " ", "I", "U", "."),
        ("SO", "RE", "HA", " ", "u", "tu", "ro", "NO", "MA", "TI", "NO",
         " ", "hu", "d", "ra", "ltu", "ku", "ta", "wa", "-", "NO"),
        ("TO", "D", "KO", "KA", "NI", " ", "A", "RU", "TO", " ",
         "TU", "TA", "E", "RA", "RE", "TE", "I", "TA", "."),
        (""),
        ("KO", "NO", " ", "HA", "NA", "SI", "WO", " ", "MI",
         "MI", "NI", "SI", "TA", " ", "A", "NA", "TA", "HA"),
        ("KO", "NO", " ", "SI", "NN", "HI", "HD", "NO", " ", "TA", "KA",
         "RA", "WO", " ", "MO", "TO", "ME", "RU", "KO", "TO", "WO"),
        ("KE", "TU", "I", "SU", "RU", "."),
        ("SO", "SI", "TE", " ", "hu", "d", "ra", "ltu", "ku", "ta", "wa", "-",
         "NI", " ", "TU", "U", "SI", "D", "RU", "TO", " ", "I", "WA", "RE", "RU"),
        ("MA", "TI", "NO", " ", "HA", "I", "KI", "LYO",
         "HE", " ", "MU", "KA", "LTU", "TA", "*...")
    )

    # 星の数
    STAR_MAX = 100

    # 星の色
    STAR_COLOR = (
        pyxel.COLOR_LIGHTBLUE,
        pyxel.COLOR_YELLOW,
        pyxel.COLOR_DARKBLUE,
    )

    # 星の座標リスト
    star_flg = [0] * STAR_MAX
    star_x = [0] * STAR_MAX
    star_y = [0] * STAR_MAX
    star_speed = [0] * STAR_MAX
    star_col = [0] * STAR_MAX

    # タイトルロゴの色パターン
    # 各要素は赤系、緑系、青系の順で定義している
    TITLE_COLOR = (
        (pyxel.COLOR_NAVY, pyxel.COLOR_DARKBLUE, pyxel.COLOR_ORANGE, pyxel.COLOR_YELLOW, pyxel.COLOR_YELLOW),
        (pyxel.COLOR_NAVY, pyxel.COLOR_DARKBLUE, pyxel.COLOR_GREEN, pyxel.COLOR_LIME, pyxel.COLOR_WHITE),
        (pyxel.COLOR_NAVY, pyxel.COLOR_DARKBLUE, pyxel.COLOR_CYAN, pyxel.COLOR_LIGHTBLUE, pyxel.COLOR_WHITE),
    )

    # タイトルロゴのフェードイン処理用
    # タイトルロゴの座標、大きさ
    TITLE_X = 0
    TITLE_Y = 0
    TITLE_W = 152
    TITLE_H = 40

    # バッファの書き出し座標
    TITLE_BUFF_OFFSET_X = 0
    TITLE_BUFF_OFFSET_Y = 208

    # 処理中のタイトルロゴのパターン番号
    title_color_idx = 0

    # 元画像の取得元ピクセル座標
    title_get_x = 0
    title_get_y = 0

    # タイリング表示用のループカウント、0～3で1ループ
    title_get_loop_cnt = 0


    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # ストーリー表示用インデックス
        self.story_index = 0

        # ストーリー表示用カウンタ
        self.story_count = 0

        # イメージバンク0のタイトルフェードイン用のバッファ領域を初期化
        for _x in range(0, self.TITLE_W):
            for _y in range(0, self.TITLE_H):
                pyxel.image(0).set(self.TITLE_BUFF_OFFSET_X + _x, self.TITLE_BUFF_OFFSET_Y + _y, ["0"])


        # 音楽ロード
        musicPlayer.load("title.ogg")  # 音楽ファイルロード

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        # 音楽を再生
        if self.state != self.STATE_RESPECT:
            musicPlayer.play(loop=False)

        if self.state == self.STATE_RESPECT:
            self.update_respect()
        elif self.state == self.STATE_STORY:
            self.update_stoty()
            self.update_generatestar()
            self.update_movestar()
        elif self.state == self.STATE_STORY_WAIT:
            self.update_story_wait()
            self.update_generatestar()
            self.update_movestar()
        elif self.state == self.STATE_STORY_FADEOUT:
            self.update_story_fadeout()
            self.update_generatestar()
            self.update_movestar()
        elif self.state == self.STATE_TITLE_FADEIN:
            self.update_title_fadein()
            self.update_movestar()
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
            self.state = self.STATE_TITLE_FADEIN

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_TITLE

    def update_title_fadein(self):
        '''
        タイトルロゴフェードイン
        '''
        if pyxel.frame_count % 2 == 0:
            # タイトルロゴのピクセルを走査し、バッファに描き込む
            for _y in range(self.TITLE_Y + self.title_get_y, self.TITLE_H + 1, 2):
                for _x in range(self.TITLE_X + self.title_get_x, self.TITLE_W + 7, 8):
                    # イメージバンク0の指定した座標のピクセルの色を取得する
                    _pick_color = pyxel.image(0).get(_x, _y)
                    # 取得した色が現在のからーグループ以降に含まれているかを調べる
                    # 青系
                    if self.TITLE_COLOR[2][self.title_color_idx:].count(_pick_color):
                        pyxel.image(0).set(self.TITLE_BUFF_OFFSET_X + _x, self.TITLE_BUFF_OFFSET_Y + _y, self.TITLE_COLOR[2][self.title_color_idx])
                    # 緑系
                    elif self.TITLE_COLOR[1][self.title_color_idx:].count(_pick_color):
                        pyxel.image(0).set(self.TITLE_BUFF_OFFSET_X + _x, self.TITLE_BUFF_OFFSET_Y + _y, self.TITLE_COLOR[1][self.title_color_idx])
                    # 赤系
                    elif self.TITLE_COLOR[0][self.title_color_idx:].count(_pick_color):
                        pyxel.image(0).set(self.TITLE_BUFF_OFFSET_X + _x, self.TITLE_BUFF_OFFSET_Y + _y, self.TITLE_COLOR[0][self.title_color_idx])
                    
            # 横1ドット移動
            self.title_get_x += 2

            # 8ドット分処理したか
            if self.title_get_x > 8:
                # 8ドット分処理したら、次の処理に向けて準備する
                self.title_get_loop_cnt += 1
                # ループカウント1の場合：x+1ドット、y+1ドット目から処理する
                if self.title_get_loop_cnt == 1:
                    self.title_get_x = 1
                    self.title_get_y = 1
                # ループカウント2の場合：x+1ドット、y+0ドット目から処理する
                if self.title_get_loop_cnt == 2:
                    self.title_get_x = 1
                    self.title_get_y = 0
                # ループカウント3の場合：x+0ドット、y+1ドット目から処理する
                if self.title_get_loop_cnt == 3:
                    self.title_get_x = 0
                    self.title_get_y = 1
                # ループカウント4の場合：ループカウントをリセット、次のカラーグループでx+0ドット、y+0ドット目から処理する
                if self.title_get_loop_cnt == 4:
                    self.title_get_loop_cnt = 0
                    self.title_get_x = 0
                    self.title_get_y = 0
                    self.title_color_idx += 1
                    if self.title_color_idx >= len(self.TITLE_COLOR[0]):
                        self.state = self.STATE_TITLE

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = self.STATE_TITLE


    def update_generatestar(self):
        '''
        星の発生を行う
        '''
        # 3フレームごとに発生させる
        if pyxel.frame_count % 3 == 0:
            # 発生させる星を検索する
            for idx, value in enumerate(self.star_flg):
                if value == 0:
                    # 星を発生
                    self.star_flg[idx] = 1
                    self.star_x[idx] = random.randrange(-256, 256)
                    self.star_y[idx] = -1
                    self.star_speed[idx] = random.randrange(1, 4)
                    self.star_col[idx] = self.STAR_COLOR[random.randrange(0, 3)]
                    break

    def update_movestar(self):
        '''
        星の移動を行う
        '''
        # 生成された星を移動する
        for idx, value in enumerate(self.star_flg):
            if value == 1:
                self.star_x[idx] += self.star_speed[idx]
                self.star_y[idx] += self.star_speed[idx] * 1.5
                if self.star_x[idx] > 256 or self.star_y[idx] > 192:
                    self.star_flg[idx] = 0


    def update_title(self):
        '''
        タイトル
        '''
        if self.selected == 0:
            if pyxel.btnp(pyxel.KEY_N):
                musicPlayer.stop()
                pyxel.play(3, 0, loop=False)
                self.selected = 1
                self.tick = 0

            if pyxel.btnp(pyxel.KEY_C) and self.doContinue:
                musicPlayer.stop()
                pyxel.play(3, 0, loop=False)
                self.selected = 2
                self.tick = 0

            if pyxel.btnp(pyxel.KEY_Q):
                musicPlayer.stop()
                pyxel.play(3, 0, loop=False)
                self.selected = 3
                self.tick = 0

        else:
            if self.tick > 21:
                if self.selected == 1:
                    self.selected = 0
                    self.stateStack.push(State.MAKECHARACTER)
                elif self.selected == 2:
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
                elif self.selected == 3:
                    pyxel.quit()

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        if self.state == self.STATE_RESPECT:
            self.draw_respect()
        if self.state == self.STATE_STORY:
            self.draw_star()
            self.draw_story()
        if self.state == self.STATE_STORY_WAIT:
            self.draw_star()
            self.draw_story_wait()
        if self.state == self.STATE_STORY_FADEOUT:
            self.draw_star()
            self.draw_story_fadeout()
        if self.state == self.STATE_TITLE_FADEIN:
            self.draw_star()
            self.draw_title_fadein()
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
        if self.story_index > 0:
            for i in range(self.story_index):
                PyxelUtil.text(20, i * 14 + 20, self.STORY[i])

        PyxelUtil.text(20, self.story_index * 14 + 20,
                       self.STORY[self.story_index], self.TEXTCOLOR[self.story_count - 1])

    def draw_story_wait(self):
        '''
        ストーリー全文表示
        '''
        for i in range(len(self.STORY)):
            PyxelUtil.text(20, i * 14 + 20, self.STORY[i])

    def draw_story_fadeout(self):
        '''
        ストーリーフェードアウト
        '''
        for i in range(len(self.STORY)):
            PyxelUtil.text(20, i * 14 + 20,
                           self.STORY[i], self.TEXTCOLOR[self.story_count - 1])

    def draw_title_fadein(self):
        '''
        タイトルフェードイン
        '''
        pyxel.blt(52, 32, 0, self.TITLE_BUFF_OFFSET_X, self.TITLE_BUFF_OFFSET_Y, self.TITLE_W, self.TITLE_H, 0)

    def draw_star(self):
        '''
        星を描画
        '''
        # 生成された星を移動する
        for idx, value in enumerate(self.star_flg):
            if value == 1:
                pyxel.pset(self.star_x[idx], self.star_y[idx], self.star_col[idx])

    def draw_title(self):
        '''
        タイトル
        '''
        # ロゴ
        pyxel.blt(52, 32, 0, self.TITLE_X, self.TITLE_Y, self.TITLE_W, self.TITLE_H, 0)

        color = [7, 7, 7, 7]
        if self.selected != 0:
            if self.tick % 2 == 0:
                color[self.selected - 1] = 0
            else:
                color[self.selected - 1] = 7

        PyxelUtil.text(108, 110, ["*[N]EW GAME"], color[0])
        if self.doContinue:
            PyxelUtil.text(108, 120, ["*[C]ONTINUE"], color[1])
        PyxelUtil.text(108, 130, ["*[Q]UIT GAME"], color[2])

        PyxelUtil.text(64, 160, ["*COPYRIGHT BY ABURI6800 2020, 2021"], 2)
        PyxelUtil.text(74, 168, ["*ORIGINAL GAME BY B.P.S. 1984"], 2)

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

        # イベントデータ初期化
        eventdata.reset()

        # イベントハンドラ初期化
        eventhandler.isExecute = False

        # メッセージハンドラ初期化
        messagehandler.clear()

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
