# -*- coding: utf-8 -*-
import pyxel
from module.stateStack import StateStack

'''
 Appクラス
 - アプリケーション本体クラス
 - StateStackを持ち、先頭のStateのupdateとdrawを実行する
'''

class App:

    #
    # クラス初期化
    #
    def __init__(self):

        # StateStack
        self.sStack = StateStack()

        # 最初のStateを登録
        self.sStack.push(self.sStack.STATE_TITLE)
#        self.sStack.push(self.sStack.STATE_CITY)

        # Pyxel初期化
        pyxel.init(256, 192, fps=10)

        # リソースのロード
        pyxel.load("../data/onyxofblack.pyxres")

        # Pyxel実行
        pyxel.run(self.update, self.draw)

    #
    # 各フレームの処理
    #
    def update(self):

        pyxel.cls(pyxel.COLOR_BLACK)
        self.sStack.update()

    #
    # 各フレームの画面描画処理
    #
    def draw(self):

        render = self.sStack.getRender()
        render()


if __name__ == "__main__":
    App()

