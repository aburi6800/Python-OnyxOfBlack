# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..systemStates.baseSystemState import BaseSystemState
# 以下テスト用に宣言
from ..character import HumanPartyGenerator
from ..character import PlayerParty
from ..character import Human

'''
 StateTitleクラス
 - タイトル画面のクラス(BaseSystemStateを継承)
 - タイトルの表示と各Stateへの遷移を行う
'''
class StateTitle(BaseSystemState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateTitle, self).__init__(stateStack)
        self.stateName = "Title"

        self.playerParty = PlayerParty()

        self.tick = 0
        self.selected = 0

    #
    # 各フレームの処理
    #
    def update(self):

#        print(self.stateName + ":update")

        if pyxel.btn(pyxel.KEY_G):
            self.selected = 1
            self.tick = 0

        if self.selected != 0:
            self.tick = self.tick + 1
            if self.tick > 11:
                if self.selected == 1:
                    # テストでランダムパーティー生成をプレイヤーパーティとする
                    self.party = HumanPartyGenerator.generate()
                    for __member in self.party.getMemberList():
                        self.playerParty.addMember(__member)
                    
                    self.stateStack.push(self.stateStack.STATE_CITY)

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print(self.stateName + ":render")

        PyxelUtil.text(64, 36, ["*Role Playing game"], 2)
        pyxel.blt(72, 48, 0, 0,  0, 26, 16, 0)
        pyxel.blt(52, 54, 0, 0, 16, 63, 24, 0)
        PyxelUtil.text(117, 68, ["*of"], 9)
        pyxel.blt(124, 54, 0, 64, 16, 80, 24, 0)

        color = [7, 7, 7, 7]
        if self.selected != 0:
            if self.tick % 2 == 0:
                color[self.selected - 1] = 0
            else:
                color[self.selected - 1] = 7

        PyxelUtil.text(88, 110, ["*[C]reate Character"], color[3])
        PyxelUtil.text(88, 118, ["*[G]o to Town"], color[0])
        PyxelUtil.text(88, 126, ["*[L]ook character State"], color[1])
        PyxelUtil.text(88, 134, ["*[K]ill Character"], color[2])

        PyxelUtil.text(68, 160, ["*COPYRIGHT BY ABURI6800 2020"], 2)
        PyxelUtil.text(68, 168, ["*ORIGINAL GAME BY B.P.S. 1984"], 2)

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

