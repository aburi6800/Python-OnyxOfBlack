# -*- coding: utf-8 -*-
from module.baseState import BaseState

'''
 BaseSystemStateクラス
 - システム画面（タイトル、キャラクター作成）の基底クラス
 - 各画面で共通の処理を持つ
'''
class BaseSystemState(BaseState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(BaseSystemState, self).__init__(stateStack)
        self.stateName = "(none)"

    #
    # 各フレームの処理
    #
    def update(self, app):

        print(self.stateName + ":update")

    #
    # 各フレームの画面描画処理
    #
    def render(self, app):

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

