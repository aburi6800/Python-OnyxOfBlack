# -*- coding: utf-8 -*-
import pyxel
from ..baseState import BaseState

'''
 BaseFieldStateクラス
 - フィールド（街、ダンジョン）の基底クラス
 - 各フィールドで共通の処理を持つ
 - 3D迷路の描画処理に必要な情報を持つ（他のクラスでは必要としない）
 - 描画処理を行う
'''
class BaseFieldState(BaseState):

    # 方向
    # これはサブクラスでも必要・・・？
    DIRECTION_NORTH = 0
    DIRECTION_EAST = 1
    DIRECTION_SOUTH = 2
    DIRECTION_WEST = 3

    # 方向に対する増分
    # これはサブクラスでも必要・・・？
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

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super().__init__(stateStack)
        self.stateName = "(none)"
        
        # 壁の色1（正面）
        self.wallColor_front = pyxel.COLOR_LIGHTBLUE
        # 壁の色2（横）
        self.wallColor_side = pyxel.COLOR_DARKBLUE

    #
    # 各フレームの処理
    #
    def update(self):

#        print("BaseFieldState:update")

        pass

    #
    # 各フレームの画面描画処理
    #
    def render(self):

#        print("BaseFieldState:render")

        super().render()

        pyxel.rectb(151, 16, 82, 80, pyxel.COLOR_DARKBLUE)

        pyxel.line(190, 56, 151, 95, pyxel.COLOR_DARKBLUE)
        pyxel.line(193, 56, 232, 95, pyxel.COLOR_DARKBLUE)
        pyxel.line(152, 59, 232, 59, pyxel.COLOR_DARKBLUE)
        pyxel.line(152, 67, 232, 67, pyxel.COLOR_DARKBLUE)
        pyxel.line(152, 82, 232, 82, pyxel.COLOR_DARKBLUE)


    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print("BaseFieldState:onEnter")

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print("BaseFieldState:onExit")

    #
    # 3D迷路表示
    # - マップデータから抽出した14の要素を持つlistを引数とする
    # - listの値は以下 :
    #     0 : 通路
    #     1 : 壁
    #     2 : ドア（黄色）
    #     3 : ブラックタワーの壁（黒）
#    def drawMaze(self, dataList):
    def drawMaze(self, _x, _y, _direction, _map):

        _data = []
        for i in range(14):
            _get_x = _x + self.POS_X[_direction][i]
            _get_y = _y + self.POS_Y[_direction][i]
            if _get_x < 0 or _get_x > len(_map[_y]) or _get_y < 0 or _get_y > len(_map):
                _data.append(1)
            else:
                _data.append(_map[_get_y][_get_x])

        for _idx, _data in enumerate(_data):
            self._drawWall(_idx, _data)

    #
    # 3D迷路の壁表示
    # - idx : 何番目の壁を描くか
    # - data : マップの地形情報
    #
    def _drawWall(self, idx, data):

        _wallColor_front = pyxel.COLOR_BLACK
        _wallColor_side = pyxel.COLOR_BLACK

        # dataが0の場合は抜ける
        if data == 0:
            return

        # 描画色
        if data == 1:
            _wallColor_front = self.wallColor_front
            _wallColor_side = self.wallColor_side
        elif data == 2:
            _wallColor_front = pyxel.COLOR_YELLOW
            _wallColor_side = pyxel.COLOR_YELLOW
        elif data == 3:
            _wallColor_front = pyxel.COLOR_BLACK
            _wallColor_side = pyxel.COLOR_BLACK

        # idxの値により壁を描画する
        if idx == 0:
            pyxel.rect( 172, 52, 8, 8, _wallColor_front)
            pyxel.tri( 180, 53, 183, 56, 180, 58, _wallColor_side)
        elif idx == 1:
            pyxel.rect( 180, 52, 8, 8, _wallColor_front)
            pyxel.tri( 188, 53, 191, 56, 188, 58, _wallColor_side)
        elif idx == 2:
            pyxel.rect( 204, 52, 8, 8, _wallColor_front)
            pyxel.tri( 203, 53, 200, 56, 203, 58, _wallColor_side)
        elif idx == 3:
            pyxel.rect( 196, 52, 8, 8, _wallColor_front)
            pyxel.tri( 195, 53, 192, 56, 195, 58, _wallColor_side)
        elif idx == 4:
            pyxel.rect( 188, 52, 8, 8, _wallColor_front)

        elif idx == 5:
            pyxel.rect( 156, 44, 24, 24, _wallColor_front)
            pyxel.rect( 180, 52, 8, 8, _wallColor_side)
            pyxel.tri( 180, 45, 187, 52, 180, 52, _wallColor_side)
            pyxel.tri( 180, 59, 187, 59, 180, 66, _wallColor_side)
        elif idx == 6:
            pyxel.rect( 204, 44, 24, 24, _wallColor_front)
            pyxel.rect( 196, 52, 8, 8, _wallColor_side)
            pyxel.tri( 203, 45, 196, 52, 203, 52, _wallColor_side)
            pyxel.tri( 197, 60, 203, 60, 203, 66, _wallColor_side)
        elif idx == 7:
            pyxel.rect( 180, 44, 24, 24, _wallColor_front)

        elif idx == 8:
            pyxel.rect( 152, 28, 12, 56, _wallColor_front)
            pyxel.rect( 164, 44, 16, 24, _wallColor_side)
            pyxel.tri( 164, 29, 179, 44, 164, 44, _wallColor_side)
            pyxel.tri( 164, 67, 179, 67, 164, 82, _wallColor_side)
        elif idx == 9:
            pyxel.rect( 220, 28, 12, 56, _wallColor_front)
            pyxel.rect( 204, 44, 16, 24, _wallColor_side)
            pyxel.tri( 219, 29, 204, 44, 219, 44, _wallColor_side)
            pyxel.tri( 204, 67, 219, 67, 219, 82, _wallColor_side)
        elif idx == 10:
            pyxel.rect(  154+8,  28, 80, 80, 12)

        elif idx == 11:
            pyxel.rect( 152, 28, 12, 56, _wallColor_side)
            pyxel.tri( 152, 17, 163, 28, 152, 28, _wallColor_side)
            pyxel.tri( 152, 83, 163, 83, 152, 94, _wallColor_side)
        elif idx == 12:
            pyxel.rect( 220, 28, 12, 56, _wallColor_side)
            pyxel.tri( 231, 17, 220, 28, 231, 28, _wallColor_side)
            pyxel.tri( 220, 83, 231, 83, 231, 94, _wallColor_side)
#        elif idx == 13:
#            pyxel.rect( 154+0,  0, 96, 96, _wallColor_side)
