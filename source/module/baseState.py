# -*- coding: utf-8 -*-
import pyxel
from module.abstractState import AbstractState

class BaseState(AbstractState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        self.stateStack = stateStack
        self.stateName = "(none)"
        print("BaseState:")
        print(self.stateStack)

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

        pyxel.rectb(8, 8, 240, 96, pyxel.COLOR_DARKBLUE)
        pyxel.rectb(152, 16, 79, 79, pyxel.COLOR_DARKBLUE)
        pyxel.rectb(8, 103, 120, 32, pyxel.COLOR_DARKBLUE)
        pyxel.rectb(127, 103, 121, 32, pyxel.COLOR_DARKBLUE)

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

