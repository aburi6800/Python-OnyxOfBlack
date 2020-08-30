# -*- coding: utf-8 -*-
import pyxel

from ..baseState import BaseState
from ..character import playerParty
from ..pyxelUtil import PyxelUtil


class BaseFacilityState(BaseState):
    '''
    施設の基底クラス

    各施設で共通の処理を持つ
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

    def update(self):
        '''
        各フレームの処理
        '''
        pass

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        # メンバーの所持金を表示
        for idx, member in enumerate(playerParty.memberList):
            PyxelUtil.text(
                136, 16 + idx * 16, ["*{:1d} : {:5d} G.P.".format(idx + 1, member.gold)], pyxel.COLOR_WHITE)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        pass

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
