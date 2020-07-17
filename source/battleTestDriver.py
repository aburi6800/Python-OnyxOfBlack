# -*- coding: utf-8 -*-
import pyxel
from module.gameMaster2 import gameMaster


class App:
    '''
    戦闘のテスト処理

    StateStackを持ち、先頭のStateのupdateとdrawを実行する
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        # Pyxel初期化～実行
        pyxel.init(256, 192)
        pyxel.load("../assets/onyxofblack.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        '''
        各フレームの処理
        '''
        gameMaster.update()

    def draw(self):
        '''
        各フレームの画面描画処理
        '''
        pyxel.cls(pyxel.COLOR_BLACK)
        gameMaster.render()


if __name__ == "__main__":
    '''
    アプリケーション実行
    '''
    App()
