# -*- coding: utf-8 -*-
import random
import pyxel
from ..pyxelUtil import PyxelUtil
from ..fieldStates.baseFieldState import BaseFieldState

'''
 StateCityクラス
 - ウツロの街のクラス(BaseFiledStateを継承)
 - マップデータを保持する
 - イベントの処理を持つ
 - 各Stateへの遷移を行う
'''
class StateCity(BaseFieldState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateCity, self).__init__(stateStack)
        self.stateName = "City"

        # 変数定義
        self.isEncount = False
        self.tick = 0
        self.selected = 0

        # 自分の最初の座標と方向
        self.x = 1
        self.y = 1
        self.direction = BaseFieldState.DIRECTION_SOUTH

        # マップ
        # 0 = 通路
        # 1 = 壁
        # 外周は必ず壁とする
        self.map = [
            [ 1, 1, 1, 1, 1, 1],
            [ 1, 0, 1, 0, 1, 1],
            [ 2, 0, 0, 0, 1, 1],
            [ 1, 0, 0, 0, 0, 1],
            [ 1, 0, 1, 2, 0, 1],
            [ 1, 0, 0, 0, 0, 1],
            [ 1, 1, 1, 1, 1, 1]
        ]

    #
    # 各フレームの処理
    #
    def update(self):

#        print(self.stateName + ":update")

        if pyxel.btn(pyxel.KEY_UP):
            if random.randint(0, 10) == 0:
                self.isEncount = True

        if self.isEncount:
            self.tick +=1
            if self.tick > 10:
                self.stateStack.push(self.stateStack.STATE_BATTLE)

        '''
        if pyxel.btn(pyxel.KEY_W):
            self.selected = 1
            self.tick = 0

        if pyxel.btn(pyxel.KEY_A):
            self.selected = 2
            self.tick = 0

        if self.selected != 0:
            self.tick = self.tick + 1
            if self.tick > 11:
                if self.selected == 1:
                    self.selected = 0
                    self.stateStack.push(self.stateStack.STATE_WEAPONSHOP)
                if self.selected == 2:
                    self.selected = 0
                    self.stateStack.push(self.stateStack.STATE_ARMORSHOP)
        '''

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print(self.stateName + ":render")

        super().render()
        pyxel.blt(152, 17, 0, 0, 40, 80, 32, 0)
        
#        _drawData = []
#        for i in range(14):
#            map_get_x = self.x + self.POS_X[self.direction][i]
#            map_get_y = self.y + self.POS_Y[self.direction][i]
#            if map_get_x < 0 or map_get_x > 5 or map_get_y < 0 or map_get_y > 5:
#                _drawData.append(1)
#            else:
#                _drawData.append(self.map[map_get_y][map_get_x])
#        super().drawMaze(_drawData)
        super().drawMaze(self.x, self.y, self.direction, self.map)

        if self.isEncount:
            PyxelUtil.text(8, 140, ["NA", "NI", "KA", "TI", "KA", "TU", "D", "I", "TE", "KI", "TA", "*!"], pyxel.COLOR_RED)

#        menuColor = [7, 7, 7, 7, 7]
#        if self.selected != 0:
#            if self.tick % 2 == 0:
#                menuColor[self.selected - 1] = 0
#            else:
#                menuColor[self.selected - 1] = 7
#        PyxelUtil.text(16,  140, ["u", "tu", "ro", "NO", "MA", "TI"], 7)
#        PyxelUtil.text(24,  148, ["*[W]:", "HU", "D", "KI", "YA"], menuColor[0])
#        PyxelUtil.text(24,  156, ["*[A]:", "YO", "RO", "I", "YA"], menuColor[1])
#        PyxelUtil.text(24,  164, ["*[S]:", "TA", "TE", "YA"], menuColor[2])
#        PyxelUtil.text(24,  172, ["*[H]:", "KA", "HU", "D", "TO", "YA"], menuColor[3])
#        PyxelUtil.text(24,  180, ["*[B]:", "TO", "KO", "YA"], menuColor[4])

    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print(self.stateName + ":onEnter")

        self.tick = 0
        self.selected = 0
        self.isEncount = False

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print(self.stateName + ":onExit")

