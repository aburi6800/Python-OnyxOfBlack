# -*- coding: utf-8 -*-
import random
import pyxel
from .pyxelUtil import PyxelUtil
from .stateStack import StateStack
from .character import HumanPartyGenerator
from .character import PlayerParty
from .character import Party
from .character import Human

'''
 GameMasterクラス
 - StateStackとゲーム全体の進行を管理する
 - ゲームループのupdate/renderからStateを呼び出すアダプタとなる
'''
class GameMaster(object):
    
    # StateStack
    stateStack = StateStack()

    def __init__(self):

        # 最初のStateを登録
        self.stateStack.push(self.stateStack.STATE_TITLE)

        # エンカウントした？
        self.isEncount = False

        # タイマー
        self.tick = 0

    def update(self):
        self.stateStack.update()

        print(self.stateStack.isField())

        # fieldのstateの場合はランダムエンカウントする
        if self.stateStack.isField():
            if pyxel.btn(pyxel.KEY_UP):
                if random.randint(0, 10) == 0:
                    self.isEncount = True

            if self.isEncount:
                self.tick +=1
                if self.tick > 10:
                    self.stateStack.push(self.stateStack.STATE_BATTLE)


    def render(self):
        self.stateStack.render()

        if self.isEncount:
            PyxelUtil.text(8, 140, ["NA", "NI", "KA", "TI", "KA", "TU", "D", "I", "TE", "KI", "TA", "*!"], pyxel.COLOR_RED)

