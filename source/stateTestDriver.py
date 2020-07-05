# -*- coding: utf-8 -*-
import pyxel
from module.gameMaster import gameMaster


class App:
    '''
    アプリケーションのクラス

    StateStackを持ち、先頭のStateのupdateとdrawを実行する
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        # Pyxel初期化～実行
        pyxel.init(256, 192, fps=10)
        pyxel.load("../assets/onyxofblack.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        '''
        各フレームの処理
        '''
        pyxel.cls(pyxel.COLOR_BLACK)
        gameMaster.update()

    def draw(self):
        '''
        各フレームの画面描画処理
        '''
        gameMaster.render()


if __name__ == "__main__":
    '''
    アプリケーション実行
    '''
    App()
