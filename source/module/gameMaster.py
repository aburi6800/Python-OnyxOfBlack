# -*- coding: utf-8 -*-
from .character import playerParty
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

        # プレイヤーパーティーの最初の位置と方向
        playerParty.x = 17
        playerParty.y = 4
        playerParty.direction = self.DIRECTION_SOUTH

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
