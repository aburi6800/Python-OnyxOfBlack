# -*- coding: utf-8 -*-
 
import pyxel
from .module.pyxelUtil import PyxelUtil
from .module.stateStack import StateStack

"""
  The Onyx of Black
  Created By 
"""

# 方向
DIRECTION_NORTH = 0
DIRECTION_EAST = 1
DIRECTION_SOUTH = 2
DIRECTION_WEST = 3

# 方向に対する増分
VX = [ 0, 1, 0,-1]
VY = [-1, 0, 1, 0]

# 自分の位置と方向からマップのどこを参照するかを、参照順に定義
# 参照順のイメージは以下（上向きである前提、自分の位置はCとする）
# |0|1|2|3|4|
#   |5|6|7|
#   |8|9|A|
#   |B|C|D|
POS_X = [
    [-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0],
    [ 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
    [ 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0],
    [-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0]
]
POS_Y = [
    [-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0],
    [-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0],
    [ 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
    [ 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0]
]

class App:

    def __init__(self):

        # pyxel初期化
#        pyxel.init(192, 128)
        pyxel.init(256, 192, fps=5)

        # リソースをロード
        pyxel.load("../data/onyxofblack.pyxres", True, False, False, False)

        # StateStack初期化   
        self.sStack = StateStack()
        self.sStack.push(self.sStack.STATE_TITLE)

        # 変数定義
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
            [ 1, 0, 0, 0, 1, 1],
            [ 1, 0, 1, 0, 1, 1],
            [ 1, 0, 1, 0, 0, 1],
            [ 1, 0, 1, 1, 0, 1],
            [ 1, 0, 0, 0, 0, 1],
            [ 1, 1, 1, 1, 1, 1]
        ]

        # pyxel実行
        pyxel.run(self.update, self.draw)


    def update(self):
        self.__update_move()

    #
    # キー入力で方向・座標変更
    #
    def __update_move(self):
        # 上：前進する
        if pyxel.btn(pyxel.KEY_UP):
            # 前が壁であるかチェック
            if self.map[self.y + VY[self.direction]][self.x + VX[self.direction]] == 0:
                self.x = self.x + VX[self.direction]
                self.y = self.y + VY[self.direction]

        # 右：右回転する
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = self.direction + 1
            if self.direction > DIRECTION_WEST:
                self.direction = DIRECTION_NORTH
        
        # 左：左回転する
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = self.direction - 1
            if self.direction < DIRECTION_NORTH:
                self.direction = DIRECTION_WEST

        
    def draw(self):
        pyxel.cls(0)

        # グリッド
        pyxel.line(  154+0, 47, 154+95, 47, 1)
        pyxel.line(  154+0, 55, 154+95, 55, 1)
        pyxel.line(  154+0, 71, 154+95, 71, 1)
        pyxel.line( 154+48, 48,  154+0, 95, 1)
        pyxel.line( 154+48, 48, 154+95, 95, 1)
        pyxel.line(  154+0, 87, 154+95, 87, 1)

        # 街なら空を描く

        for i in range(14):
            map_x = self.x + POS_X[self.direction][i]
            map_y = self.y + POS_Y[self.direction][i]
            if map_x < 0 or map_x > 5 or map_y < 0 or map_y > 5:
                data = 1
            else:
                data = self.map[map_y][map_x]
#            print(str(map_x) + ":" + str(map_y) + "=" + str(data))

            if data == 1:
                self.__drawMaze(i)

        # test
        self.__drawPlayer(0,  1, 0, 0, 0, 0)
        self.__drawPlayer(1, 34, 0, 0, 0, 0)
        self.__drawPlayer(2, 88, 0, 0, 0, 0)
        self.__drawPlayer(3,100, 0, 0, 0, 0)

        PyxelUtil.text(8, 128, ["*ONYX", "WO", "ME", "SA", "D", "SI", "TE", ",", "KA", "D", "NN", "HA", "D", "RI", "MA", "SI", "LYO", "U", "*!"], 14)


    def __drawMaze(self, num):

        if num == 0:
            pyxel.rect(  154+8, 40, 16, 16, 12)
            pyxel.tri( 154+24, 40, 154+40, 48, 154+24, 55, 1)
        elif num == 1:
            pyxel.rect( 154+24, 40, 16, 16, 12)
            pyxel.tri( 154+40, 40, 154+48, 48, 154+40, 55, 1)
        elif num == 2:
            pyxel.rect( 154+72, 40, 16, 16, 12)
            pyxel.tri( 154+71, 40, 154+71, 55, 154+56, 48, 1)
        elif num == 3:
            pyxel.rect( 154+56, 40, 16, 16, 12)
            pyxel.tri( 154+55, 40, 154+55, 55, 154+48, 48, 1)
        elif num == 4:
            pyxel.rect( 154+40, 40, 16, 16, 12)

        elif num == 5:
            pyxel.rect(  154+0, 24, 24, 48, 12)
            pyxel.rect( 154+24, 40, 16, 16, 1)
            pyxel.tri( 154+24, 24, 154+39, 39, 154+24, 40, 1)
            pyxel.tri( 154+24, 56, 154+39, 56, 154+24, 71, 1)
        elif num == 6:
            pyxel.rect( 154+72, 24, 24, 48, 12)
            pyxel.rect( 154+56, 40, 16, 16, 1)
            pyxel.tri( 154+71, 24, 154+56, 39, 154+71, 39, 1)
            pyxel.tri( 154+71, 56, 154+56, 56, 154+71, 71, 1)
        elif num == 7:
            pyxel.rect( 154+24, 24, 48, 48, 12)

        elif num == 8:
            pyxel.rect(  154+0,  8,  8, 80, 12)
            pyxel.rect(  154+8, 24, 16, 48, 1)
            pyxel.tri(  154+8,  8, 154+23, 23,  154+8, 23, 1)
            pyxel.tri(  154+8, 87, 154+23, 72,  154+8, 72, 1)
        elif num == 9:
            pyxel.rect( 154+88,  8,  8, 80, 12)
            pyxel.rect( 154+72, 24, 16, 48, 1)
            pyxel.tri( 154+87,  8, 154+87, 23, 154+72, 23, 1)
            pyxel.tri( 154+87, 87, 154+87, 72, 154+72, 72, 1)
        elif num == 10:
            pyxel.rect(  154+8,  8, 80, 80, 12)

        elif num == 11:
            pyxel.rect(  154+0,  8,  8, 80, 1)
            pyxel.tri(  154+0,  0,  154+7,  7,  154+0,  7, 1)
            pyxel.tri(  154+0, 95,  154+7, 88,  154+0, 88, 1)
        elif num == 12:
            pyxel.rect( 154+88,  8,  8, 80, 1)
            pyxel.tri( 154+95,  0, 154+88,  7, 154+95,  7, 1)
            pyxel.tri( 154+95, 95, 154+88, 88, 154+95, 88, 1)
        elif num == 13:
            pyxel.rect( 154+0,  0, 96, 96, 12)


    def __drawPlayer(self, number, head, helm, body, weapon, shield):

        pyxel.blt( 12, (number * 20) +  2, 1,  (head % 32) * 8,  int(head / 32) * 8,  8,  8, 0) # 頭
        pyxel.blt( 12, (number * 20) + 10, 1,  32, 32,  8, 16, 0) # 体
        pyxel.blt(  4, (number * 20) +  2, 1,   0, 48,  8, 16, 0) # 武器
        PyxelUtil.text( 24,  (number * 20) + 4, ["*PLAYER"], number + 7) # 名前
        pyxel.rect( 24, (number * 20) + 12, 16, 3,  5)
        pyxel.rect( 24, (number * 20) + 15, 30, 1,  6)


if __name__ == "__main__":
    App()
