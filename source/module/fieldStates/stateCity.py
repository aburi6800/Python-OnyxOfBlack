# -*- coding: utf-8 -*-
import pyxel
from module.pyxelUtil import PyxelUtil
from module.fieldStates.baseFieldState import BaseFieldState

'''
 StateCityクラス
 - ウツロの街のクラス(BaseFiledStateを継承)
 - マップデータを保持する
 - イベントの処理を持つ
 - 各Stateへの遷移を行う
'''
# 方向
DIRECTION_NORTH = 0
DIRECTION_EAST = 1
DIRECTION_SOUTH = 2
DIRECTION_WEST = 3

# 方向に対する増分
VX = [ 0, 1, 0,-1]
VY = [-1, 0, 1, 0]

class StateCity(BaseFieldState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateCity, self).__init__(stateStack)
        self.stateName = "City"

        # 変数定義
        self.tick = 0
        self.selected = 0

        # 自分の最初の座標と方向
        self.x = 1
        self.y = 1
        self.direction = DIRECTION_SOUTH

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

        # 画面描画用のリスト
        self.drawData = []

    #
    # 各フレームの処理
    #
    def update(self):

#        print(self.stateName + ":update")

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

        self.drawData = []
        for i in range(14):
            map_get_x = self.x + self.POS_X[self.direction][i]
            map_get_y = self.y + self.POS_Y[self.direction][i]
            if map_get_x < 0 or map_get_x > 5 or map_get_y < 0 or map_get_y > 5:
                self.drawData.append(1)
            else:
                self.drawData.append(self.map[map_get_y][map_get_x])

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print(self.stateName + ":render")

        super().render()
        pyxel.blt(152, 17, 0, 0, 40, 80, 32, 0)
        super().drawMaze(self.drawData)

        menuColor = [7, 7, 7, 7, 7]
        if self.selected != 0:
            if self.tick % 2 == 0:
                menuColor[self.selected - 1] = 0
            else:
                menuColor[self.selected - 1] = 7

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

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print(self.stateName + ":onExit")

