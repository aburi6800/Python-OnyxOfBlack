# -*- coding: utf-8 -*-
import pyxel
from module.abstractState import AbstractState
from module.party import Party

'''
 BaseStateクラス
 - 各Stateの規定クラス
 - AbstractStateを継承
 - 
'''
class BaseState(AbstractState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        self.stateStack = stateStack
        self.stateName = "(none)"
        self.playerParty = Party()

    #
    # 各フレームの処理
    #
    def update(self):

#        print("BaseState:update")

        pass

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print("BaseState:render")

        pyxel.rectb(8, 8, 240, 128, pyxel.COLOR_DARKBLUE)
        pyxel.line(128, 8 ,128, 135, pyxel.COLOR_DARKBLUE)
        pyxel.line(8, 104 ,248, 104, pyxel.COLOR_DARKBLUE)

    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print("BaseState:onEnter")

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print("BaseState:onExit")

