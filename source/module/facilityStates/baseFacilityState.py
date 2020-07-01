# -*- coding: utf-8 -*-
import pyxel
from ..baseState import BaseState

'''
 BaseFacilityStateクラス
 - 施設の基底クラス
 - 各施設で共通の処理を持つ
'''
class BaseFacilityState(BaseState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(BaseFacilityState, self).__init__(stateStack)
        self.stateName = "(none)"

    #
    # 各フレームの処理
    #
    def update(self):

#        print(self.stateName + ":update")
        pass

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print(self.stateName + ":render")

        super().render()

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

