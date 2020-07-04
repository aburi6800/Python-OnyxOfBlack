# -*- coding: utf-8 -*-
from ..baseState import BaseState

class BaseSystemState(BaseState):
    '''
    システム周りのStateの基底クラス
    
    タイトル画面やキャラクター作成等、特殊な画面を想定している
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
        pass

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

