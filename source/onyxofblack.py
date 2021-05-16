# -*- coding: utf-8 -*-
import pyxel
from module.stateStack import stateStack
from module.constant.state import State


class App:
    '''
    アプリケーションのクラス

    StateStackを持ち、先頭のStateのupdateとdrawを実行する
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        # タイトルのstateをpush
        stateStack.push(State.TITLE)

        # Pyxel初期化～実行
#        pyxel.init(256, 192)
        pyxel.init(256, 192, fullscreen=True, quit_key=pyxel.KEY_NONE)
        pyxel.load("assets/onyxofblack.pyxres")
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
        stateStack.draw()


if __name__ == "__main__":
    '''
    アプリケーション実行
    '''
    App()
