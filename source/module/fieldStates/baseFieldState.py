# -*- coding: utf-8 -*-
import random
import pyxel
from ..pyxelUtil import PyxelUtil
from ..baseState import BaseState
from ..character import playerParty
from ..character import enemyParty
from ..character import EnemyPartyGenerator


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
    # |0|1|4|3|2|
    #   |5|7|6|
    #   |8|A|9|
    #   |B|D|C|
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

    # 迷路描画の壁の色（正面）
    WALLCOLOR_FRONT = (
        None,
        pyxel.COLOR_LIGHTBLUE,
        pyxel.COLOR_YELLOW,
        pyxel.COLOR_BLACK,
    )

    # 迷路描画の壁の色（側面）
    WALLCOLOR_SIDE = (
        None,
        pyxel.COLOR_DARKBLUE,
        pyxel.COLOR_YELLOW,
        pyxel.COLOR_BLACK,
    )

    # 迷路描画の座標オフセット
    OFFSET_X = 150
    OFFSET_Y = 14

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "(none)"

        # エンカウントフラグ
        self.isEncount = False

    def update(self):
        '''
        各フレームの処理
        '''
        # エンカウントしたか？
        if self.isEncount:
            self.tick += 1
            if self.tick > 10:
                self.isEncount = False
                self.tick = 0
                enemyParty.memberList = EnemyPartyGenerator.generate(
                    self.enemy_set[random.randint(0, len(self.enemy_set) - 1)])
                self.stateStack.push(self.stateStack.STATE_BATTLE)
            else:
                return

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

        if pyxel.btnp(pyxel.KEY_UP) and self._can_move_forward():
            if random.randint(0, 20) == 0:
#                self.isEncount = True
                pass
            else:
                playerParty.saveCondition()
                playerParty.x = playerParty.x + self.VX[playerParty.direction]
                playerParty.y = playerParty.y + self.VY[playerParty.direction]

    def _can_move_forward(self) -> bool:
        '''
        前進できるかを判定する

        マップデータを方向によりシフトした結果の下位1ビットが立っている（＝目の前の壁情報が通行不可）場合は、前進不可と判定する
        '''
#        _value = self._get_mapinfo(self.map, playerParty.y + self.VY[playerParty.direction], playerParty.x + self.VX[playerParty.direction], playerParty.direction)
        _value = self._get_mapinfo(self.map, playerParty.x, playerParty.y, playerParty.direction)
        print(bin(_value))
        if _value & 0b00000001 == 1:
            return False
        else:
            return True

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        # 迷路の枠線
        pyxel.rectb(self.OFFSET_X - 1, self.OFFSET_Y - 1, 80, 80, pyxel.COLOR_DARKBLUE)

        # 地面部のグリッド
        pyxel.line(0 + self.OFFSET_X, 40 + self.OFFSET_Y, 78 + self.OFFSET_X, 40 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.OFFSET_X, 43 + self.OFFSET_Y, 78 + self.OFFSET_X, 43 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.OFFSET_X, 50 + self.OFFSET_Y, 78 + self.OFFSET_X, 50 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.OFFSET_X, 69 + self.OFFSET_Y, 78 + self.OFFSET_X, 69 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)

        pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 0 + self.OFFSET_X, 78 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 78 + self.OFFSET_X, 78 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)

        if self.stateName != "City":
            # 天井部のグリッド
            pyxel.line(0 + self.OFFSET_X, 38 + self.OFFSET_Y, 78 + self.OFFSET_X, 38 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
            pyxel.line(0 + self.OFFSET_X, 35 + self.OFFSET_Y, 78 + self.OFFSET_X, 35 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
            pyxel.line(0 + self.OFFSET_X, 28 + self.OFFSET_Y, 78 + self.OFFSET_X, 28 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
            pyxel.line(0 + self.OFFSET_X,9 + self.OFFSET_Y, 78 + self.OFFSET_X, 9 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)

            pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 0 + self.OFFSET_X, 0 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
            pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 78 + self.OFFSET_X, 0 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        else:
            # 満天の星空
            pyxel.blt(self.OFFSET_X, self.OFFSET_Y, 0, 0, 40, 80, 32, 0)

        # 迷路
        self._draw_maze(playerParty.x, playerParty.y, playerParty.direction, self.map)

        try:
            # イベントが登録されている座標ならイベントの関数を呼び出す
            _key = "{:02d}".format(playerParty.x) + "{:02d}".format(playerParty.y) + "D"
            _event = self.event[_key]
            if _event != None:
                _event()
                return
        except KeyError:
            None

        # エンカウント時のメッセージ
        if self.isEncount:
            PyxelUtil.text(10, 146, ["NA", "NI", "KA", "TI", "KA", "TU",
                                     "D", "I", "TE", "KI", "TA", "*!"], pyxel.COLOR_RED)

        PyxelUtil.text(0, 0, "*X:" + str(playerParty.x) + " Y:" + str(playerParty.y) + " DIR:" +
                       str(playerParty.direction) + " MAP:" + bin(self.map[playerParty.y][playerParty.x]))

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

    def _draw_maze(self, _x, _y, _direction, _map):
        '''
        迷路を表示する

        利用元からは、X座標、Y座標、方向、マップデータを引数に与えること
        '''
        _data = 0
        for i in range(14):
            _get_x = _x + self.POS_X[_direction][i]
            _get_y = _y + self.POS_Y[_direction][i]

            if _get_x < 0 or _get_x > len(_map[_y]) - 1 or _get_y < 0 or _get_y > len(_map) - 1:
                _data = 0
            else:
                _data = self._get_mapinfo(_map, _get_x, _get_y, _direction)
            self._draw_wall(i, _data)

    def _right_2bit_rotate(self, n):
        '''
        2ビット右にローテートした値を返却する
        '''
        return ((n & 0b00000011) << 6) | ((n >> 2) & 0b11111111)

    def _left_2bit_rotate(self, n):
        '''
        2ビット左にローテートした値を返却する
        '''
        return ((n << 2) & 0b11111111) | (n >> 6)

    def _get_mapinfo(self, _map, _x, _y, _direction):
        '''
        指定した座標のマップ情報を取得する。

        取得対象のマップデータと方向は引数で指定する。
        返却される値は、方向によりデータをシフトした結果となる。
        '''
        _data = _map[_y][_x]
        if _direction > self.DIRECTION_NORTH:
            for _ in range(_direction):
                _data = self._right_2bit_rotate(_data)
        return _data

    def _draw_wall(self, _idx, _data):
        '''
        迷路を表示する

        drawMazeクラスからの利用を想定し、他のモジュールからの使用は想定していない
        描画番号とマップの地形情報に従って壁を描画する
        '''
        # dataが0の場合は壁を描画しないので抜ける
        if _data == 0:
            return

        # idxとの値により壁を描画する
        # |0|1|4|3|2|
        #   |5|7|6|
        #   |8|A|9|
        #   |B|D|C|
        if _idx == 1:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(35 + self.OFFSET_X, 38 + self.OFFSET_Y, 3,
                           3, self.WALLCOLOR_FRONT[_color])
        if _idx == 3:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(41 + self.OFFSET_X, 38 + self.OFFSET_Y, 3,
                           3, self.WALLCOLOR_FRONT[_color])
        if _idx == 4:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(38 + self.OFFSET_X, 38 + self.OFFSET_Y, 3,
                           3, self.WALLCOLOR_FRONT[_color])
            if _data & 0b00001100 != 0:
                _color = (_data >> 2) & 0b00000011
                pyxel.tri(43 + self.OFFSET_X, 36 + self.OFFSET_Y, 41 + self.OFFSET_X, 38 + self.OFFSET_Y,
                          43 + self.OFFSET_X, 38 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(41 + self.OFFSET_X, 40 + self.OFFSET_Y, 43 + self.OFFSET_X, 40 + self.OFFSET_Y,
                          43 + self.OFFSET_X, 42 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(41 + self.OFFSET_X, 39 + self.OFFSET_Y,
                           3, 1, self.WALLCOLOR_SIDE[_color])
            if _data & 0b11000000 != 0:
                _color = (_data >> 6) & 0b00000011
                pyxel.tri(35 + self.OFFSET_X, 36 + self.OFFSET_Y, 37 + self.OFFSET_X, 38 + self.OFFSET_Y,
                          35 + self.OFFSET_X, 38 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(35 + self.OFFSET_X, 40 + self.OFFSET_Y, 37 + self.OFFSET_X, 40 + self.OFFSET_Y,
                          35 + self.OFFSET_X, 42 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(35 + self.OFFSET_X, 39 + self.OFFSET_Y,
                           3, 1, self.WALLCOLOR_SIDE[_color])

        if _idx == 5:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(26 + self.OFFSET_X, 35 + self.OFFSET_Y, 9,
                           9, self.WALLCOLOR_FRONT[_color])
        if _idx == 6:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(44 + self.OFFSET_X, 35 + self.OFFSET_Y, 9,
                           9, self.WALLCOLOR_FRONT[_color])
        if _idx == 7:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(35 + self.OFFSET_X, 35 + self.OFFSET_Y, 9,
                           9, self.WALLCOLOR_FRONT[_color])
            if _data & 0b00001100 != 0:
                _color = (_data >> 2) & 0b00000011
                pyxel.tri(50 + self.OFFSET_X, 29 + self.OFFSET_Y, 44 + self.OFFSET_X, 35 + self.OFFSET_Y,
                          50 + self.OFFSET_X, 35 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(44 + self.OFFSET_X, 43 + self.OFFSET_Y, 50 + self.OFFSET_X, 43 + self.OFFSET_Y,
                          50 + self.OFFSET_X, 49 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(44 + self.OFFSET_X, 36 + self.OFFSET_Y,
                           7, 7, self.WALLCOLOR_SIDE[_color])
            if _data & 0b11000000 != 0:
                _color = (_data >> 6) & 0b00000011
                pyxel.tri(28 + self.OFFSET_X, 29 + self.OFFSET_Y, 34 + self.OFFSET_X, 35 + self.OFFSET_Y,
                          28 + self.OFFSET_X, 35 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(28 + self.OFFSET_X, 43 + self.OFFSET_Y, 34 + self.OFFSET_X, 43 + self.OFFSET_Y,
                          28 + self.OFFSET_X, 49 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(28 + self.OFFSET_X, 36 + self.OFFSET_Y,
                           7, 7, self.WALLCOLOR_SIDE[_color])

        if _idx == 8:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(5 + self.OFFSET_X, 28 + self.OFFSET_Y, 23,
                           23, self.WALLCOLOR_FRONT[_color])
        if _idx == 9:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(51 + self.OFFSET_X, 28 + self.OFFSET_Y, 23,
                           23, self.WALLCOLOR_FRONT[_color])
        if _idx == 10:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(28 + self.OFFSET_X, 28 + self.OFFSET_Y, 23,
                           23, self.WALLCOLOR_FRONT[_color])
            if _data & 0b00001100 != 0:
                _color = (_data >> 2) & 0b00000011
                pyxel.tri(69 + self.OFFSET_X, 10 + self.OFFSET_Y, 51 + self.OFFSET_X, 28 + self.OFFSET_Y,
                          69 + self.OFFSET_X, 28 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(51 + self.OFFSET_X, 50 + self.OFFSET_Y, 69 + self.OFFSET_X, 50 + self.OFFSET_Y,
                          69 + self.OFFSET_X, 68 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(51 + self.OFFSET_X, 29 + self.OFFSET_Y, 19,
                           21, self.WALLCOLOR_SIDE[_color])
            if _data & 0b11000000 != 0:
                _color = (_data >> 6) & 0b00000011
                pyxel.tri(9 + self.OFFSET_X, 10 + self.OFFSET_Y, 27 + self.OFFSET_X, 28 + self.OFFSET_Y,
                          9 + self.OFFSET_X, 28 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(9 + self.OFFSET_X, 50 + self.OFFSET_Y, 27 + self.OFFSET_X, 50 + self.OFFSET_Y,
                          9 + self.OFFSET_X, 68 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(9 + self.OFFSET_X, 29 + self.OFFSET_Y, 19,
                           21, self.WALLCOLOR_SIDE[_color])

        if _idx == 11:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(0 + self.OFFSET_X, 9 + self.OFFSET_Y, 10,
                           61, self.WALLCOLOR_FRONT[_color])
        if _idx == 12:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(69 + self.OFFSET_X, 9 + self.OFFSET_Y, 10,
                           61, self.WALLCOLOR_FRONT[_color])
        if _idx == 13:
            if _data & 0b00000011 != 0:
                _color = _data & 0b00000011
                pyxel.rect(10 + self.OFFSET_X, 9 + self.OFFSET_Y, 59,
                           61, self.WALLCOLOR_FRONT[_color])
            if _data & 0b00001100 != 0:
                _color = (_data >> 2) & 0b00000011
                pyxel.tri(78 + self.OFFSET_X, 0 + self.OFFSET_Y, 69 + self.OFFSET_X, 9 + self.OFFSET_Y,
                          78 + self.OFFSET_X, 9 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(69 + self.OFFSET_X, 69 + self.OFFSET_Y, 78 + self.OFFSET_X, 69 + self.OFFSET_Y,
                          78 + self.OFFSET_X, 78 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(69 + self.OFFSET_X, 10 + self.OFFSET_Y, 10,
                           59, self.WALLCOLOR_SIDE[_color])
            if _data & 0b11000000 != 0:
                _color = (_data >> 6) & 0b00000011
                pyxel.tri(0 + self.OFFSET_X, 0 + self.OFFSET_Y, 9 + self.OFFSET_X, 9 + self.OFFSET_Y,
                          0 + self.OFFSET_X, 9 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.tri(0 + self.OFFSET_X, 69 + self.OFFSET_Y, 9 + self.OFFSET_X, 69 + self.OFFSET_Y,
                          0 + self.OFFSET_X, 78 + self.OFFSET_Y, self.WALLCOLOR_SIDE[_color])
                pyxel.rect(0 + self.OFFSET_X, 10 + self.OFFSET_Y, 10,
                           59, self.WALLCOLOR_SIDE[_color])
