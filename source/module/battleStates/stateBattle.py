# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..baseState import BaseState
from ..character import PlayerParty
from ..character import Party
from ..character import Human
from ..character import HumanPartyGenerator

class StateBattle(BaseState):
    '''戦闘シーンのクラス

    BaseStateクラスを継承
    '''

    def __init__(self, stateStack):
        '''クラス初期化'''
        super().__init__(stateStack)
        self.stateName = "Battle"

        # プレイヤーパーティー
        self.playerParty = PlayerParty()

        # 敵パーティー
        self.enemyParty = Party()

    def update(self):
        '''各フレームの処理'''
        pass
        # 流れ：
        # ・行動決定フェーズ
        # 　1.プレイヤーパーティーのメンバーそれぞれについてコマンドを選択し、行動キューに入れる（イニシアチブ値も決定する）
        # 　2.敵パーティーはそれぞれプレイヤーパーティーの誰を狙うかを決めて、行動キューに入れる（イニシアチブ値も決定する）
        # ・行動フェーズ
        #   1.行動キューをイニシアチブ値の降順でソートする
        #   2.行動キューの先頭から順に処理する
        # ・結果判定フェーズ
        #   1.プレイヤーパーティが全滅した場合は、ゲームオーバー
        #   2.敵パーティーが全滅した場合は、勝利の処理を行い、Stateを抜ける

    def render(self):
        '''各フレームの描画処理'''
        super().render()
        # 敵の描画
        for _idx in range(len(self.enemyParty.memberList)):
            _chr = self.enemyParty.getMember(_idx)
            super().drawCharacter(_chr, 136 + _idx * 18, 108 + (_idx % 2) * 4)

    def onEnter(self):
        '''状態開始時の処理'''
        # 敵パーティー生成
        self.enemyParty = HumanPartyGenerator.generate()

    def onExit(self):
        '''状態終了時の処理'''
