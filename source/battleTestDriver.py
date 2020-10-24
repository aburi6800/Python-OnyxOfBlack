# -*- coding: utf-8 -*-
import pyxel
from module.pyxelUtil import PyxelUtil
from module.stateStack import stateStack
from module.character import HumanPartyGenerator
from module.character import EnemyPartyGenerator
from module.character import playerParty
from module.character import enemyParty
from module.monster import monsterParams
from module.battleStates.stateBattle import StateBattle


class App:
    '''
    戦闘のテストドライバー
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        # StateStackの初期化
        stateStack.clear()

        # Pyxel初期化
        pyxel.init(256, 192)
        pyxel.load("../assets/onyxofblack.pyxres")

        # テストでランダムパーティー生成をプレイヤーパーティとする
        level = 5
        playerParty.memberList = HumanPartyGenerator.generate(level)
        for member in playerParty.memberList:
            print(member)

        # 敵パーティー生成
        enemyParty.memberList = EnemyPartyGenerator.generate(monsterParams.monsterList[monsterParams.AZTEC])
        for value in enemyParty.memberList:
            print(value)

        # BattleStateをstateStackに登録
        stateStack.push(StateBattle)

        pyxel.run(self.update, self.draw)

    def update(self):
        '''
        各フレームの処理
        '''
        stateStack.update()

    def draw(self):
        '''
        各フレームの画面描画処理
        '''
        pyxel.cls(pyxel.COLOR_BLACK)
        stateStack.draw()


if __name__ == "__main__":
    '''
    アプリケーション実行
    '''
    App()
