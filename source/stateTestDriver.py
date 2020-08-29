# -*- coding: utf-8 -*-
import pyxel
#from module.gameMaster import gameMaster
from module.stateStack import stateStack

class App:
    '''
    アプリケーションのクラス

    StateStackを持ち、先頭のStateのupdateとdrawを実行する
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        # 最初のStateを登録
        stateStack.init(stateStack.STATE_TITLE)

        # Pyxel初期化～実行
        pyxel.init(256, 192)
        pyxel.load("../assets/onyxofblack.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        '''
        各フレームの処理
        '''
        stateStack.update()

    def draw(self):
        '''
        各フレームの画面描画処理
        '''
        pyxel.cls(pyxel.COLOR_BLACK)
        stateStack.render()


if __name__ == "__main__":
    '''
    アプリケーション実行
    '''
    App()
