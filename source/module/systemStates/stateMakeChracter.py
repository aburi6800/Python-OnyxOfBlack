# -*- coding: utf-8 -*-
import random

import pyxel
from module.character import HumanGenerator, playerParty
from module.direction import Direction
from module.input import Input
from module.pyxelUtil import PyxelUtil
from module.state import State
from module.systemStates.baseSystemState import BaseSystemState
from overrides import overrides


class StateMakeCharacter(BaseSystemState):
    '''
    キャラクター作成画面クラス\n
    BaseSystemStateを継承。\n
    キャラクターの作成を行う。\n
    作成したキャラクターはCharacterStockクラスに格納される。\n
    '''
    # 状態の定数
    STATE_INIT = 0
    STATE_INPUT_NAME = 1
    STATE_SELECT_HAIR = 2
    STATE_SELECT_CROTHES = 3
    STATE_APPLY = 4
    STATE_MORE = 5
    STATE_DONE = 6

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    def makeInitialHuman(self):
        '''
        人間キャラクタを作成する。\n
        能力値以外は初期値とする。
        '''
        self.character = HumanGenerator().generate(1)
        self.character.name = ""
        self.character.exp = 0
        self.character.weapon = None
        self.character.armor = None
        self.character.shield = None
        self.character.helmet = None
        self.character.body = 0

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

        if self.state == self.STATE_INIT:
            self.update_init()
        if self.state == self.STATE_INPUT_NAME:
            self.update_input_name()
        elif self.state == self.STATE_SELECT_HAIR:
            self.update_select_hair()
        elif self.state == self.STATE_SELECT_CROTHES:
            self.update_select_crothes()
        elif self.state == self.STATE_APPLY:
            self.update_apply()
        elif self.state == self.STATE_MORE:
            self.update_more()
        elif self.state == self.STATE_DONE:
            self.update_done()

    def update_init(self):
        '''
        キャラクタ作成初期化処理
        '''
        # 名前用の文字入力クラス
        self.nameInput = Input(14, 32, 8)

        # 人間のキャラクタクラス
        self.character = None

        # 頭のリストを初期化
        self.hairList = []
        while len(self.hairList) < 8:
            n = random.randint(0, 127)
            if not n in self.hairList:
                self.hairList.append(n)

        # 名前入力へ
        self.state = self.STATE_INPUT_NAME

    def update_input_name(self):
        '''
        名前入力処理
        '''
        # 文字入力クラスのupdateメソッドを呼ぶ
        self.nameInput.update()

        # 文字入力が完了したか
        if self.nameInput.isEnter and self.nameInput.value != "":
            pyxel.play(3, 0, loop=False)

            # 人間キャラクタ作成
            self.makeInitialHuman()
            self.character.gold = self.character.gold + 100
            self.character.name = self.nameInput.value

            # 髪型選択の準備
            self.hair_num = 0

            # 状態を髪型選択へ
            self.state = self.STATE_SELECT_HAIR

    def update_select_hair(self):
        '''
        髪型選択処理
        '''
        if pyxel.btnp(pyxel.KEY_LEFT) and self.hair_num % 8 > 0:
            self.hair_num -= 1

        if pyxel.btnp(pyxel.KEY_RIGHT) and self.hair_num % 8 < 7:
            self.hair_num += 1

#        if pyxel.btnp(pyxel.KEY_UP) and self.hair_num // 8 > 0:
#            self.hair_num -= 8

#        if pyxel.btnp(pyxel.KEY_DOWN) and self.hair_num // 8 < 3:
#            self.hair_num += 8

        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.play(3, 0, loop=False)

            # 頭部設定
            self.character.head = self.hairList[self.hair_num]

            # 服装選択の準備
            self.crothes_num = 0

            # 状態を服装選択へ
            self.state = self.STATE_SELECT_CROTHES

    def update_select_crothes(self):
        '''
        服選択処理
        '''
        if pyxel.btnp(pyxel.KEY_LEFT) and self.crothes_num % 8 > 0:
            self.crothes_num -= 1

        if pyxel.btnp(pyxel.KEY_RIGHT) and self.crothes_num % 8 < 7:
            self.crothes_num += 1

        if pyxel.btnp(pyxel.KEY_ENTER):
            pyxel.play(3, 0, loop=False)

            # 体設定
            self.character.body = self.crothes_num + 1

            # 状態を確認へ
            self.state = self.STATE_APPLY

    def update_apply(self):
        '''
        確認処理
        '''
        if pyxel.btnp(pyxel.KEY_Y):
            pyxel.play(3, 0, loop=False)

            # 作ったキャラクタをプレイヤーパーティーに追加
            playerParty.addMember(self.character)

            # プレイヤーパーティーの人数は5人未満か
            if len(playerParty.memberList) < 5:
                # 状態を追加確認へ
                self.state = self.STATE_MORE
            else:
                # 状態をキャラクタ作成完了へ
                self.state = self.STATE_DONE
                self.tick = 0

        if pyxel.btnp(pyxel.KEY_N):
            pyxel.play(3, 0, loop=False)

            # 名前入力に戻る
            self.state = self.STATE_INIT

    def update_more(self):
        '''
        追加確認処理
        '''
        if pyxel.btnp(pyxel.KEY_Y):
            pyxel.play(3, 0, loop=False)

            # 名前入力時のメッセージ、先頭を削除
            del self.INPUT_NAME_MESSAGE[0]

            # 状態をキャラクタ作成初期化へ
            self.state = self.STATE_INIT

        if pyxel.btnp(pyxel.KEY_N):
            pyxel.play(3, 0, loop=False)

            # 状態をキャラクタ作成完了へ
            self.state = self.STATE_DONE
            self.tick = 0

    def update_done(self):
        '''
        キャラクタ作成完了処理
        '''
        if self.tick == 1:
            pyxel.playm(0)

        if self.tick > 120:
            # 自分自身のstateをpopする
            self.stateStack.pop()
            # 街のStateをpushする
            self.stateStack.push(State.CITY)

            # プレイヤーパーティーの最初の位置と方向を設定
            playerParty.x = 17
            playerParty.y = 4
            playerParty.direction = Direction.SOUTH

    @overrides	
    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        # 完了
        if self.state == self.STATE_DONE:
            PyxelUtil.text(94, 40, ("*PREPARE TO DIE !!"), pyxel.COLOR_WHITE)
            x = (120 if len(playerParty.memberList) % 2 != 0 else 130) - \
                (len(playerParty.memberList) // 2) * 32
            for member in playerParty.memberList:
                self.drawCharacter(member, x, 60)
                x += 32
            return

        # 名前入力
        if self.state >= self.STATE_INPUT_NAME:
            pyxel.rectb(10, 18, 160, 25, pyxel.COLOR_NAVY)
            PyxelUtil.text(14, 23, self.INPUT_NAME_MESSAGE[0] + ("ME", " ", "NO", " ", "NA", "MA", "E", "HA",
                                                                 "* ?"), pyxel.COLOR_YELLOW if self.state == self.STATE_INPUT_NAME else pyxel.COLOR_WHITE)
            self.nameInput.draw()

        # 髪型選択
        if self.state >= self.STATE_SELECT_HAIR:
            pyxel.rect(120, 40, 90, 38, pyxel.COLOR_BLACK)
            pyxel.rectb(120, 40, 90, 38, pyxel.COLOR_NAVY)
            PyxelUtil.text(124, 45, ("KA", "MI", "KA", "D", "TA", "WO"),
                           pyxel.COLOR_YELLOW if self.state == self.STATE_SELECT_HAIR else pyxel.COLOR_WHITE)
            PyxelUtil.text(124, 52, ("E", "RA", "NN", "TE", "D", "KU", "TA", "D", "SA", "I"),
                           pyxel.COLOR_YELLOW if self.state == self.STATE_SELECT_HAIR else pyxel.COLOR_WHITE)
            for _idx in range(0, 8):
                pyxel.blt(134 + _idx * 8, 64, 1,
                          (self.hairList[_idx] % 32) * 8, (self.hairList[_idx] // 32) * 8, 8, 8)

            # カーソルは髪型選択時のみ表示
            if self.state == self.STATE_SELECT_HAIR and pyxel.frame_count % 4 == 0:
                pyxel.rect(133 + (self.hair_num % 8) * 8, 65 +
                           (self.hair_num // 8) * 16, 8, 8, pyxel.COLOR_WHITE)

        if self.state >= self.STATE_SELECT_CROTHES:
            # キャラクター表示
            pyxel.rect(40, 70, 32, 32, pyxel.COLOR_BLACK)
            pyxel.rectb(40, 70, 32, 32, pyxel.COLOR_NAVY)
            self.drawCharacter(self.character, 45, 76)

            # 服装選択
            pyxel.rect(100, 70, 140, 46, pyxel.COLOR_BLACK)
            pyxel.rectb(100, 70, 140, 46, pyxel.COLOR_NAVY)
            PyxelUtil.text(104, 75, ("HU", "KU", "SO", "U", "WO"),
                           pyxel.COLOR_YELLOW if self.state == self.STATE_SELECT_CROTHES else pyxel.COLOR_WHITE)
            PyxelUtil.text(104, 82, ("E", "RA", "NN", "TE", "D", "KU", "TA", "D", "SA", "I"),
                           pyxel.COLOR_YELLOW if self.state == self.STATE_SELECT_CROTHES else pyxel.COLOR_WHITE)
            for _idx in range(0, 8):
                pyxel.blt(110 + _idx * 16, 98, 1, 168 + _idx *
                          8, 32, 8, 16, pyxel.COLOR_BLACK)

            # カーソルは髪型選択時のみ表示
            if self.state == self.STATE_SELECT_CROTHES and pyxel.frame_count % 4 == 0:
                pyxel.rect(110 + self.crothes_num * 16,
                           98, 8, 12, pyxel.COLOR_WHITE)

        if self.state >= self.STATE_APPLY:
            pyxel.rect(60, 160, 126, 16, pyxel.COLOR_BLACK)
            pyxel.rectb(60, 160, 126, 16, pyxel.COLOR_NAVY)
            PyxelUtil.text(64, 165, ("KO", "RE", "TE", "D", " ", "I", "I", "TE", "D", "SU", "KA", "* ? (Y/N)"),
                           pyxel.COLOR_YELLOW if self.state == self.STATE_APPLY else pyxel.COLOR_WHITE)

        if self.state >= self.STATE_MORE:
            pyxel.rect(70, 165, 134, 16, pyxel.COLOR_BLACK)
            pyxel.rectb(70, 165, 134, 16, pyxel.COLOR_NAVY)
            PyxelUtil.text(74, 170, ("MO", "U", "HI", "TO", "RI", " ", "I", "KI", "MA", "SU", "KA", "* ? (Y/N)"),
                           pyxel.COLOR_YELLOW if self.state == self.STATE_MORE else pyxel.COLOR_WHITE)

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 名前入力時のメッセージ
        self.INPUT_NAME_MESSAGE = [
            ("HI", "TO", "RI"),
            ("HU", "TA", "RI"),
            ("SA", "NN", "NI", "NN"),
            ("YO", "NI", "NN"),
            ("KO", "D", "NI", "NN"),
        ]

        # 名前用の文字入力クラス
        self.nameInput = None

        # 人間のキャラクタクラス
        self.character = None

        # 最初の状態
        self.state = self.STATE_INIT

        # 頭のリスト
        self.hairList = []

        # プレイヤーパーティーを初期化
        playerParty.initialize()

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
