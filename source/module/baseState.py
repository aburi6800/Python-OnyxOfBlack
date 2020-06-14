# -*- coding: utf-8 -*-
#import pyxel
from module.abstractState import AbstractState

class BaseState(AbstractState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        self.stateStack = stateStack
        self.stateName = "(none)"
#        # リソースをロード
#        pyxel.load("../../data/onyxofblack.pyxres", True, False, False, False)

    #
    # 各フレームの処理
    #
    def update(self):

        print(self.stateName + ":update")

    #
    # 各フレームの画面描画処理
    #
    def render(self):

        print(self.stateName + ":render")

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

