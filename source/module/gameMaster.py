# -*- coding: utf-8 -*-
import random

import pyxel

from .character import HumanPartyGenerator, enemyParty, playerParty
from .pyxelUtil import PyxelUtil
from .stateStack import stateStack


class GameMaster(object):
    '''
    ゲームマスタークラス

    シーンを管理すろStateStackとプレイヤーパーティーの情報を持つ
    ゲーム全体の進行を管理する
    ゲームループのupdate/renderからStateを呼び出すアダプタとなる
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        # 最初のStateを登録
        stateStack.push(stateStack.STATE_TITLE)

        # テストでランダムパーティー生成をプレイヤーパーティとする
        level = 1
        playerParty.memberList = HumanPartyGenerator.generate(level)

        enemyParty.memberList = []

    def update(self):
        '''
        各フレームの処理
        '''
        stateStack.update()

    def render(self):
        '''
        各フレームの描画処理
        '''
        stateStack.render()


gameMaster = GameMaster()
