# -*- coding: utf-8 -*-
from module.abstractState import AbstractState

class BaseState(AbstractState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        self.stateStack = stateStack
        self.stateName = "(none)"

    #
    # 各フレームの処理
    #
    def update(self):

        print("BaseState:update")

    #
    # 各フレームの画面描画処理
    #
    def render(self):

        print("BaseState:render")

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

