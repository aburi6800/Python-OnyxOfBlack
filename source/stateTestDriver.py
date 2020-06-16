# -*- coding: utf-8 -*-

import pyxel
from module.stateStack import StateStack

class App:

    def __init__(self):

        # stateStackのテスト
        self.sStack = StateStack()
        self.sStack.push(self.sStack.STATE_TITLE)

        # ゲーム全体で使う情報をここで初期化する
        # 各stateからはapp.xxxで参照できる
        self.message_y = 0
        self.timeCount = 0

        # Pyxel初期化
        pyxel.init(256, 192, fps=8)
        pyxel.load("../data/onyxofblack.pyxres")
        pyxel.run(self.update, self.draw)


    def update(self):

        pyxel.cls(pyxel.COLOR_BLACK)
        self.sStack.update()


    def draw(self):

        render = self.sStack.getRender()
        render()
        self.timeCount = self.timeCount + 1


if __name__ == "__main__":
    App()

