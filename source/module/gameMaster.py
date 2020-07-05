# -*- coding: utf-8 -*-
import random
import pyxel
from .pyxelUtil import PyxelUtil
from .stateStack import stateStack
from .character import HumanPartyGenerator
from .character import playerParty


class GameMaster(object):
    '''
    ゲームマスタークラス

    シーンを管理すろStateStackとプレイヤーパーティーの情報を持つ
    ゲーム全体の進行を管理する
    ゲームループのupdate/renderからStateを呼び出すアダプタとなる
    '''
    # エンカウントした？
    isEncount = False

    # タイマー
    tick = 0

    def __init__(self):
        '''
        クラス初期化
        '''
        # 最初のStateを登録
        stateStack.push(stateStack.STATE_TITLE)

        # テストでランダムパーティー生成をプレイヤーパーティとする
        _party = HumanPartyGenerator.generate()
        for _member in _party.memberList:
            playerParty.addMember(_member)

    def update(self):
        '''
        各フレームの処理
        '''
        stateStack.update()

        # fieldのstateの場合はランダムエンカウントする
        if stateStack.isField():
            #            if pyxel.btn(pyxel.KEY_UP):
            #                if random.randint(0, 20) == 0:
            #                    self.isEncount = True

            if self.isEncount:
                self.tick += 1
                if self.tick > 10:
                    self.isEncount = False
                    stateStack.push(StateStack().STATE_BATTLE)

    def render(self):
        '''
        各フレームの描画処理
        '''
        stateStack.render()

        # エンカウント時のメッセージ
        if self.isEncount:
            PyxelUtil.text(10, 146, ["NA", "NI", "KA", "TI", "KA", "TU",
                                     "D", "I", "TE", "KI", "TA", "*!"], pyxel.COLOR_RED)


gameMaster = GameMaster()
