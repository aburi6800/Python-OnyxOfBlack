# -*- coding: utf-8 -*-
import pyxel
from ..baseState import BaseState
from ..character import playerParty


class BaseFieldState(BaseState):
    '''
    フィールドのStateクラスの基底クラス

    各フィールドで共通の処理を持つ
    迷路の描画処理に必要な情報を持つ（他のクラスでは必要としない）
    迷路の描画処理を行う
    '''

    # 方向
    DIRECTION_NORTH = 0
    DIRECTION_EAST = 1
    DIRECTION_SOUTH = 2
    DIRECTION_WEST = 3

    # 方向に対する増分
    VX = (0, 1, 0, -1)
    VY = (-1, 0, 1, 0)

    # 自分の位置と方向からマップのどこを参照するかを、参照順に定義
    # 参照順のイメージは以下（上向きである前提、自分の位置はCとする）
    # |0|1|2|3|4|
    #   |5|6|7|
    #   |8|9|A|
    #   |B|C|D|
    POS_X = (
        (-2, -1, 2, 1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0),
        (3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
        (2, 1, -2, -1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0),
        (-3, -3, -3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0)
    )
    POS_Y = (
        (-3, -3, -3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0),
        (-2, -1, 2, 1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0),
        (3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
        (2, 1, -2, -1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0)
    )

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "(none)"

        # デフォルトの壁の色（正面）
        self.wallColor_front = pyxel.COLOR_LIGHTBLUE
        # デフォルトの壁の色（横）
        self.wallColor_side = pyxel.COLOR_DARKBLUE

    def update(self):
        '''
        各フレームの処理
        '''
        if pyxel.btnp(pyxel.KEY_RIGHT):
            playerParty.saveCondition()
            playerParty.direction += 1
            if playerParty.direction > self.DIRECTION_WEST:
                playerParty.direction = self.DIRECTION_NORTH

        if pyxel.btnp(pyxel.KEY_LEFT):
            playerParty.saveCondition()
            playerParty.direction -= 1
            if playerParty.direction < self.DIRECTION_NORTH:
                playerParty.direction = self.DIRECTION_WEST

        if pyxel.btnp(pyxel.KEY_UP) and self.can_move_forward():
            playerParty.saveCondition()
            playerParty.x = playerParty.x + self.VX[playerParty.direction]
            playerParty.y = playerParty.y + self.VY[playerParty.direction]

    def can_move_forward(self) -> bool:
        '''
        前進できるかを判定する

        マップデータの下位1ビットが立っていると前進不可と判定する
        '''
        if self.map[playerParty.y + self.VY[playerParty.direction]][playerParty.x + self.VX[playerParty.direction]] & 1 == 0:
            return True
        else:
            return False

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()
        # 迷路の枠線
        pyxel.rectb(151, 12, 82, 80, pyxel.COLOR_DARKBLUE)
        # 迷路のグリッド線
        pyxel.line(190, 52, 151, 91, pyxel.COLOR_DARKBLUE)
        pyxel.line(193, 52, 232, 91, pyxel.COLOR_DARKBLUE)
        pyxel.line(152, 55, 232, 55, pyxel.COLOR_DARKBLUE)
        pyxel.line(152, 63, 232, 63, pyxel.COLOR_DARKBLUE)
        pyxel.line(152, 79, 232, 79, pyxel.COLOR_DARKBLUE)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        pass

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass

    def draw_maze(self, _x, _y, _direction, _map):
        '''
        迷路を表示する

        利用元からは、X座標、Y座標、方向、マップデータを引数に与えること
        '''
        _data = []
        for i in range(14):
            _get_x = _x + self.POS_X[_direction][i]
            _get_y = _y + self.POS_Y[_direction][i]
            if _get_x < 0 or _get_x > len(_map[_y]) - 1 or _get_y < 0 or _get_y > len(_map) - 1:
                _data.append(0)
            else:
                _data.append(_map[_get_y][_get_x])

        for _idx, _value in enumerate(_data):
            self._draw_wall(_idx, _value)

    def _draw_wall(self, idx, data):
        '''
        迷路を表示する

        drawMazeクラスからの利用を想定し、他のモジュールからの使用は想定していない
        描画番号とマップの地形情報に従って壁を描画する
        '''
        _wallColor_front = pyxel.COLOR_BLACK
        _wallColor_side = pyxel.COLOR_BLACK

        # dataが0の場合は壁を描画しないので抜ける
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
            pyxel.rect(172, 48, 8, 8, _wallColor_front)
            pyxel.tri(180, 49, 183, 52, 180, 54, _wallColor_side)
        elif idx == 1:
            pyxel.rect(180, 48, 8, 8, _wallColor_front)
            pyxel.tri(188, 49, 191, 52, 188, 54, _wallColor_side)
        elif idx == 2:
            pyxel.rect(204, 48, 8, 8, _wallColor_front)
            pyxel.tri(203, 49, 200, 52, 203, 54, _wallColor_side)
        elif idx == 3:
            pyxel.rect(196, 48, 8, 8, _wallColor_front)
            pyxel.tri(195, 49, 192, 52, 195, 54, _wallColor_side)
        elif idx == 4:
            pyxel.rect(188, 48, 8, 8, _wallColor_front)

        elif idx == 5:
            pyxel.rect(156, 40, 24, 24, _wallColor_front)
            pyxel.rect(180, 48, 8, 8, _wallColor_side)
            pyxel.tri(180, 41, 187, 48, 180, 48, _wallColor_side)
            pyxel.tri(180, 55, 187, 55, 180, 62, _wallColor_side)
        elif idx == 6:
            pyxel.rect(204, 40, 24, 24, _wallColor_front)
            pyxel.rect(196, 48, 8, 8, _wallColor_side)
            pyxel.tri(203, 41, 196, 48, 203, 48, _wallColor_side)
            pyxel.tri(197, 56, 203, 56, 203, 62, _wallColor_side)
        elif idx == 7:
            pyxel.rect(180, 40, 24, 24, _wallColor_front)

        elif idx == 8:
            pyxel.rect(152, 24, 12, 56, _wallColor_front)
            pyxel.rect(164, 40, 16, 24, _wallColor_side)
            pyxel.tri(164, 25, 179, 40, 164, 40, _wallColor_side)
            pyxel.tri(164, 63, 179, 63, 164, 78, _wallColor_side)
        elif idx == 9:
            pyxel.rect(220, 24, 12, 56, _wallColor_front)
            pyxel.rect(204, 40, 16, 24, _wallColor_side)
            pyxel.tri(219, 25, 204, 40, 219, 40, _wallColor_side)
            pyxel.tri(204, 63, 219, 63, 219, 78, _wallColor_side)
        elif idx == 10:
            pyxel.rect(164, 24, 56, 56, _wallColor_front)

        elif idx == 11:
            pyxel.rect(152, 24, 12, 56, _wallColor_side)
            pyxel.tri(152, 13, 163, 24, 152, 24, _wallColor_side)
            pyxel.tri(152, 79, 163, 79, 152, 90, _wallColor_side)
        elif idx == 12:
            pyxel.rect(220, 24, 12, 56, _wallColor_side)
            pyxel.tri(231, 13, 220, 24, 231, 24, _wallColor_side)
            pyxel.tri(220, 79, 231, 79, 231, 90, _wallColor_side)
#        elif idx == 13:
#            pyxel.rect( 154+0,  0, 96, 96, _wallColor_side)
