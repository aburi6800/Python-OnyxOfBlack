# -*- coding: utf-8 -*-
import pyxel
from module.baseState import BaseState


class BaseSystemState(BaseState):
    '''
    システム周りのStateの基底クラス

    タイトル画面やキャラクター作成等、特殊な画面を想定している
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

    def draw(self):
        '''
        各フレームの描画処理
        '''
        # baseStateのdrawを呼ぶと画面の枠線やキャラクタが表示されるため、消去のみ行う
        pyxel.cls(pyxel.COLOR_BLACK)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
