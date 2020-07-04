# -*- coding: utf-8 -*-
import pyxel
from ..baseState import BaseState


class BaseFacilityState(BaseState):
    '''
    施設の基底クラス

    各施設で共通の処理を持つ
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "(none)"

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
