# -*- coding: utf-8 -*-

import pyxel
from module.character import playerParty
from module.fieldStates.baseFieldState import BaseFieldState
#from module.fieldStates.city.stateCity import StateCity
from module.messageQueue import messageCommand2, messagequeue
from module.state import State
from overrides import overrides


class StateEventWell(BaseFieldState):
    '''
    井戸のイベント
    '''

    def __init__(self):
        super().__init__()

        # 画像読み込み
        pyxel.image(0).load(0, 205, "well.png")

        # メッセージ登録
        c = messageCommand2()
        c.addMessage(["KA", "RE", "TA", " ", "I", "TO", "D", "KA", "D", "A", "RU", "."])
        c.addMessage(["SI", "TA", "NI", " ", "O", "RI", "RA", "RE", "SO", "U", "TA", "D", "."])
        c.addMessage([""])
        c.addChoose(["*[D] ","O", "RI", "TE", "MI", "RU"], pyxel.KEY_D, self.choose_Down)
        c.addChoose(["*[L] ","KO", "NO", "HA", "D", "WO", " ", "TA", "TI", "SA", "RU"], pyxel.KEY_L, self.choose_Leave)
        messagequeue.enqueue(c)

    @overrides
    def update_execute(self):
        pass

    def choose_Down(self):
        '''
        [D]選択時の処理
        '''
        # stateStackから自分を削除する
        self.popState()

        # プレイヤーパーティーの座標設定
        playerParty.x = 10
        playerParty.y = 10

        # 井戸の中へ
        self.pushState(State.WELLB1)

    def choose_Leave(self):
        '''
        [L]選択時の処理
        '''
        c = messageCommand2()
        c.addMessage(["KI", "MI", "TA", "TI", "HA", " ", "KO", "KO", "KA", "RA", " ", "TA", "TI", "SA", "LTU", "TA", "."])

        # stateStackから自分を削除する
        self.popState()

    @overrides
    def draw(self):
        '''
        画面描画処理
        '''
        super().draw()

        # 画像表示
        pyxel.blt(self.DRAW_OFFSET_X + 15, self.DRAW_OFFSET_Y + 15, 0, 0, 205, 50, 50)

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()
