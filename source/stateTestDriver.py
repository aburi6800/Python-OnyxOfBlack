# -*- coding: utf-8 -*-
from module.stateStack import StateStack
import pyxel

class App:

    def __init__(self):

        # stateStackのテスト
        self.sStack = StateStack()
        self.sStack.push(self.sStack.STATE_TITLE)

        self.message_y = 0
        self.timeCount = 0

        pyxel.init(192, 192)
        pyxel.run(self.update, self.draw)

    def update(self):

#        print("update")
        self.sStack.update()

    def draw(self):

#        print("draw")
        self.sStack.render(self)
        self.timeCount = self.timeCount + 1

App()

