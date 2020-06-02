# -*- coding: utf-8 -*-
 
import pyxel
import pyxelKana

"""
  3D迷路
"""
class App:

    def __init__(self):

        # pyxel初期化
        pyxel.init(192, 128)

        # リソースをロード
        pyxel.load("data/onyxofblack.pyxres", True, False, False, False)

        # 方向
        self.DIRECTION_NORTH = 0
        self.DIRECTION_EAST = 1
        self.DIRECTION_SOUTH = 2
        self.DIRECTION_WEST = 3

        # 方向に対する増分
        self.VX = ( 0, 1, 0,-1)
        self.VY = (-1, 0, 1, 0)

        # 自分の位置と方向からマップのどこを参照するかを、参照順に定義
        # 参照順のイメージは以下（上向きである前提、自分の位置はCとする）
        # |0|1|2|3|4|
        #   |5|6|7|
        #   |8|9|A|
        #   |B|C|D|
        self.POS_X = (
            (-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0),
            ( 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
            ( 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0),
            (-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0)
        )
        self.POS_Y = (
            (-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0),
            (-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0),
            ( 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
            ( 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0)
        )

        # 変数定義
        # 自分の最初の座標と方向
        self.x = 1
        self.y = 1
        self.direction = self.DIRECTION_SOUTH

        # マップ
        # 0 = 通路
        # 1 = 壁
        # 外周は必ず壁とする
        self.map = [
            [ 1, 1, 1, 1, 1],
            [ 1, 0, 1, 0, 1],
            [ 1, 0, 1, 0, 1],
            [ 1, 0, 0, 1, 1],
            [ 1, 1, 1, 1, 1]
        ]

        # pyxel実行
        pyxel.run(self.update, self.draw)


    def update(self):
        pass


    def draw(self):
        pyxel.cls(0)
        pyxel.text(110, 16, "Python 3 + Pyxel", 15)
        self.writeKana(110, 24, ["u", "tu", "ro", "NO", "MA", "TI"])
        self.writeKana(110, 32, ["ta", "ti", "i", "ri", "ki", "nn", "si"])
        self.writeKana(110, 40, ["ha", "hd", "so", "ko", "nn"])
        pyxel.line(  0, 47, 95, 47, 1)
        pyxel.line(  0, 55, 95, 55, 1)
        pyxel.line(  0, 71, 95, 71, 1)
        pyxel.line( 48, 48,  0, 95, 1)
        pyxel.line( 48, 48, 95, 95, 1)

        for i in range(14):
            map_x = self.x + self.POS_X[self.direction][i]
            map_y = self.y + self.POS_Y[self.direction][i]
            if map_x < 0 or map_x > 5 or map_y < 0 or map_y > 5:
                data = 1
            else:
                data = self.map[map_y][map_x]
            print(str(map_x) + ":" + str(map_y) + "=" + str(data))

            if data == 1:
                self.drawWall(i)


    def drawWall(self, num):

        if num == 0:
            pyxel.rect(  8, 40, 16, 16, 12)
            pyxel.tri( 24, 40, 40, 48, 24, 55, 1)
        elif num == 1:
            pyxel.rect( 24, 40, 16, 16, 12)
            pyxel.tri( 40, 40, 48, 48, 40, 55, 1)
        elif num == 2:
            pyxel.rect( 72, 40, 16, 16, 12)
            pyxel.tri( 71, 40, 71, 55, 56, 48, 1)
        elif num == 3:
            pyxel.rect( 56, 40, 16, 16, 12)
            pyxel.tri( 55, 40, 55, 55, 48, 48, 1)
        elif num == 4:
            pyxel.rect( 40, 40, 16, 16, 12)

        elif num == 5:
            pyxel.rect(  0, 24, 24, 48, 12)
            pyxel.rect( 24, 40, 16, 16, 1)
            pyxel.tri( 24, 24, 39, 39, 24, 40, 1)
            pyxel.tri( 24, 56, 39, 56, 24, 71, 1)
        elif num == 6:
            pyxel.rect( 72, 24, 24, 48, 12)
            pyxel.rect( 56, 40, 16, 16, 1)
            pyxel.tri( 71, 24, 56, 39, 71, 39, 1)
            pyxel.tri( 71, 56, 56, 56, 71, 71, 1)
        elif num == 7:
            pyxel.rect( 24, 24, 48, 48, 12)

        elif num == 8:
            pyxel.rect(  0,  8,  8, 80, 12)
            pyxel.rect(  8, 24, 16, 48, 1)
            pyxel.tri(  8,  8, 23, 23,  8, 23, 1)
            pyxel.tri(  8, 87, 23, 72,  8, 72, 1)
        elif num == 9:
            pyxel.rect( 88,  8,  8, 80, 12)
            pyxel.rect( 72, 24, 16, 48, 1)
            pyxel.tri( 87,  8, 87, 23, 72, 23, 1)
            pyxel.tri( 87, 87, 87, 72, 72, 72, 1)
        elif num == 10:
            pyxel.rect(  8,  8, 80, 80, 12)

        elif num == 11:
            pyxel.rect(  0,  8,  8, 80, 1)
            pyxel.tri(  0,  0,  7,  7,  0,  7, 1)
            pyxel.tri(  0, 95,  7, 88,  0, 88, 1)
        elif num == 12:
            pyxel.rect( 88,  8,  8, 80, 1)
            pyxel.tri( 95,  0, 88,  7, 95,  7, 1)
            pyxel.tri( 95, 95, 88, 88, 95, 88, 1)
        elif num == 13:
            pyxel.rect( 0,  0, 96, 96, 12)


    def writeKana(self, x, y, txt):  

        for i in range(len(txt)):
            font_xy = pyxelKana.kana.KANA_DIC[txt[i]]
            fontx = font_xy[0]
            fonty = font_xy[1]
            pyxel.blt(x + 8 * i, y, 0, fontx, fonty, 7, 6, 14)

App()
