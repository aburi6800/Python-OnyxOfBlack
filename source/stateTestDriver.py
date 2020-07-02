# -*- coding: utf-8 -*-
import pyxel
from module.gameMaster import GameMaster

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

        # GameMaster誕生
        self.gameMaster = GameMaster()

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
        self.gameMaster.update()

    #
    # 各フレームの画面描画処理
    #
    def draw(self):

        self.gameMaster.render()


if __name__ == "__main__":
    App()

