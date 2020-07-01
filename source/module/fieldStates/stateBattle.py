# -*- coding: utf-8 -*-
import pyxel
from module.pyxelUtil import PyxelUtil
from module.fieldStates.baseFieldState import BaseFieldState

'''
 StateBattleクラス
 - 戦闘シーンのクラス(BaseSystemStateを継承)
'''
class StateBattle(BaseFieldState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateBattle, self).__init__(stateStack)
        self.stateName = "Battle"

    #
    # 各フレームの処理
    #
    def update(self):

        pass

    #
    # 各フレームの画面描画処理
    #
    def render(self):

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
