# -*- coding: utf-8 -*-
import random
import pyxel
from .pyxelUtil import PyxelUtil
from .stateStack import StateStack
from .character import HumanPartyGenerator
from .character import PlayerParty
from .character import Party
from .character import Human


class GameMaster(object):
    '''ゲームマスタークラス

    StateStackとゲーム全体の進行を管理する
    ゲームループのupdate/renderからStateを呼び出すアダプタとなる
    '''

    # StateStack
    stateStack = StateStack()

    # プレイヤーパーティー    
    playerParty = PlayerParty()

    def __init__(self):
        '''クラス初期化'''
        # 最初のStateを登録
        self.stateStack.push(self.stateStack.STATE_TITLE)

        # エンカウントした？
        self.isEncount = False

        # タイマー
        self.tick = 0

        # テストでランダムパーティー生成をプレイヤーパーティとする
        _party = HumanPartyGenerator.generate()
        for __member in _party.memberList:
            self.playerParty.addMember(__member)

    def update(self):
        '''各フレームの処理'''
        self.stateStack.update()

        # fieldのstateの場合はランダムエンカウントする
        if self.stateStack.isField():
            if pyxel.btn(pyxel.KEY_UP):
                if random.randint(0, 10) == 0:
                    self.isEncount = True

            if self.isEncount:
                self.tick += 1
                if self.tick > 10:
                    self.isEncount = False
                    self.stateStack.push(self.stateStack.STATE_BATTLE)

    def render(self):
        '''各フレームの描画処理'''
        self.stateStack.render()

        # エンカウント時のメッセージ
        if self.isEncount:
            PyxelUtil.text(8, 140, ["NA", "NI", "KA", "TI", "KA", "TU",
                                    "D", "I", "TE", "KI", "TA", "*!"], pyxel.COLOR_RED)
