# -*- coding: utf-8 -*-
import pyxel
from module.systemStates.baseSystemState import BaseSystemState
from module.pyxelUtil import PyxelUtil

class StateTitle(BaseSystemState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateTitle, self).__init__(stateStack)
        self.stateName = "Title"

    #
    # 各フレームの処理
    #
    def update(self):

        print(self.stateName + ":update")
#        self.stateStack.push(self.stateStack.STATE_CITY)
        pass

    #
    # 各フレームの画面描画処理
    #
    def render(self):

        print(self.stateName + ":render")
        pyxel.text( 54, 49, "Role Playing game", 4)
        pyxel.blt( 70, 68, 0,  0,  0, 26, 16, 0)
        pyxel.blt( 50, 74, 0,  0, 16, 63, 24, 0)
        pyxel.text( 114, 88, "OF", 9)
        pyxel.blt(122, 74, 0, 64, 16, 80, 24, 0)


    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print(self.stateName + ":onEnter")

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print(self.stateName + ":onExit")

