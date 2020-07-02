# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..baseState import BaseState
from ..character import PlayerParty
from ..character import Party
from ..character import Human
from ..character import HumanPartyGenerator

'''
 StateBattleクラス
 - 戦闘シーンのクラス
'''
class StateBattle(BaseState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super().__init__(stateStack)
        self.stateName = "Battle"

        # プレイヤーパーティー
        self.playerParty = PlayerParty()

        # 敵パーティー
        self.enemyParty = Party()

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

        # 敵の描画
        for _idx in range(len(self.enemyParty.getMemberList())):
            _chr = self.enemyParty.getMember(_idx)
            super().drawCharacter(_chr, 136 + _idx * 16, 108 + (_idx % 2) * 4)

    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print(self.stateName + ":onEnter")

        # 敵パーティー生成
        self.enemyParty = HumanPartyGenerator.generate()

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print(self.stateName + ":onExit")
