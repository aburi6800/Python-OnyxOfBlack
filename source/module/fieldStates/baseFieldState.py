# -*- coding: utf-8 -*-
import random

import pyxel

from ..baseState import BaseState
from ..battleStates.stateBattle import StateBattle
from ..character import EnemyPartyGenerator, enemyParty, playerParty
from ..pyxelUtil import PyxelUtil
from ..systemStates.stateCamp import StateCamp


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
    WALLCOLOR_FRONT = [
        None,
        pyxel.COLOR_LIGHTBLUE,
        pyxel.COLOR_YELLOW,
        pyxel.COLOR_BLACK,
        pyxel.COLOR_LIGHTBLUE,
    ]

    # 迷路描画の壁の色（側面）
    WALLCOLOR_SIDE = [
        None,
        pyxel.COLOR_DARKBLUE,
        pyxel.COLOR_YELLOW,
        pyxel.COLOR_BLACK,
        pyxel.COLOR_DARKBLUE,
    ]

    # 迷路描画の座標オフセット
    OFFSET_X = 150
    OFFSET_Y = 14

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

    def set_wall_color(self, _wallcolor_front=pyxel.COLOR_LIGHTBLUE, _wallcolor_side=pyxel.COLOR_DARKBLUE):
        '''
        壁の色を設定する処理

        途中で変更したい場合に使用する
        正面の壁の色、側面の壁の色の順に指定する
        扉の色、ブラックタワーの色は変更不可
        '''
        # 迷路描画の壁の色（正面）
        self.WALLCOLOR_FRONT[1] = _wallcolor_front
        self.WALLCOLOR_FRONT[4] = _wallcolor_front

        # 迷路描画の壁の色（側面）
        self.WALLCOLOR_SIDE[1] = _wallcolor_side
        self.WALLCOLOR_SIDE[4] = _wallcolor_side

    def update(self):
        '''
        各フレームの処理
        '''
        super().update()

        # パーティーは逃げてきたか？
        if playerParty.isEscape:
            # フラグを降ろす
            playerParty.isEscape = False
            # 方向のリストを作ってシャッフル
            _dirlist = [self.DIRECTION_NORTH, self.DIRECTION_EAST,
                        self.DIRECTION_SOUTH, self.DIRECTION_WEST]
            _dirlist = random.sample(_dirlist, len(_dirlist))
            # 各方向について移動可能か調べる
            for _direction in _dirlist:
                if self.can_move_forward(self._map, playerParty.x, playerParty.y, _direction):
                    # 移動可能の場合はその方向に移動
                    playerParty.x = playerParty.x + self.VX[_direction]
                    playerParty.y = playerParty.y + self.VX[_direction]
                    playerParty.direction = _direction
                    break
            return
            # どの方向にも移動できない（あり得ないが）場合はその場に留まるため、特に処理不要

        # エンカウントしているか？
        if self.isEncount:
            if self.tick > 30:
                self.isEncount = False
                self.tick = 0
                self.pushState(StateBattle)
                return
            else:
                return

        # イベントハンドラ
        if self._eventhandler("U") == False:
            # イベントが何もない場合、エンカウントするか？
            if self.tick == 1 and random.randint(0, 20) == 0:
                self.encount_enemy()
                return

        # キャンプ
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.pushState(StateCamp)

        # キー入力（右）
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.tick = 0
            playerParty.saveCondition()
            playerParty.direction += 1
            if playerParty.direction > self.DIRECTION_WEST:
                playerParty.direction = self.DIRECTION_NORTH
            return

        # キー入力（左）
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.tick = 0
            playerParty.saveCondition()
            playerParty.direction -= 1
            if playerParty.direction < self.DIRECTION_NORTH:
                playerParty.direction = self.DIRECTION_WEST
            return

        # キー入力（下）
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.tick = 0
            playerParty.saveCondition()
            playerParty.direction = (playerParty.direction + 2) % 4
            return

        # キー入力（上）
        if pyxel.btnp(pyxel.KEY_UP) and self.can_move_forward(self._map, playerParty.x, playerParty.y, playerParty.direction):
            self.tick = 0
#            if random.randint(0, 20) == 0:
#                self.encount_enemy()
#                pass
#            else:
            playerParty.saveCondition()
            playerParty.x = playerParty.x + self.VX[playerParty.direction]
            playerParty.y = playerParty.y + self.VY[playerParty.direction]
            return

    def encount_enemy(self):
        '''
        敵とエンカウントした時の処理

        enemyPartyを生成し、isEncountをTrueに変更する
        マップにより特殊な条件でenemyPartyを生成する場合は、サブクラスでオーバーライドする
        '''
        self.isEncount = True
        enemyParty.memberList = EnemyPartyGenerator.generate(
            self.enemy_set[random.randint(0, len(self.enemy_set) - 1)])

    def update_fixedencount_enemy(self):
        '''
        敵と固定エンカウントした時の処理

        固定エンカウントをしたい座標に、このメソッドをイベント辞書に登録する
        isFixedEncountがFalseの時は、ランダムエンカウント時のメソッドを呼び出す
        isFixedEncountがTrueの時は、イベント辞書から削除する
        '''
        # 固定エンカウントしていない状態か？
        if self.isFixedEncount == False:
            self.isFixedEncount = True
            self.isEncount = True
            self.encount_enemy()
            return

        # 上記の条件に合致しない場合は、固定エンカウントしている状態となる
        # 戦闘から逃げて終了した場合は、ここに到達する前に座標が変更されているのでイベントは削除されない
        # イベントのキー
        _key = "{:02d}".format(playerParty.x) + \
            "{:02d}".format(playerParty.y) + "9U"
        try:
            # イベント辞書から削除
            del(self.event[_key])
        except KeyError as ke:
            # KeyErrorが発生しても無視する
            pass
        self.isFixedEncount = False

    def can_move_forward(self, _map, _x: int, _y: int, _direction: int) -> bool:
        '''
        前進できるかを判定する

        マップデータを方向によりシフトした結果の下位1ビットが立っている（＝目の前の壁情報が通行不可）場合は、前進不可と判定する
        '''
        _value = self._get_mapinfo(_map, _x, _y, _direction)

        if _value & 0b000000000001 == 0b000000000001:
            return False
        else:
            return True

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        # 開発用
        PyxelUtil.text(0, 0, "*X:" + str(playerParty.x) + " Y:" + str(playerParty.y) + " DIR:" +
                       str(playerParty.direction) + " MAP:" + self.stateName + "-" + bin(self._map[playerParty.y][playerParty.x]))

        # 迷路の枠線
        pyxel.rectb(self.OFFSET_X - 1, self.OFFSET_Y -
                    1, 81, 81, pyxel.COLOR_DARKBLUE)

        # 地面部のグリッド
        pyxel.line(0 + self.OFFSET_X, 40 + self.OFFSET_Y, 78 +
                   self.OFFSET_X, 40 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.OFFSET_X, 43 + self.OFFSET_Y, 78 +
                   self.OFFSET_X, 43 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.OFFSET_X, 50 + self.OFFSET_Y, 78 +
                   self.OFFSET_X, 50 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.OFFSET_X, 69 + self.OFFSET_Y, 78 +
                   self.OFFSET_X, 69 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)

        pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 0 +
                   self.OFFSET_X, 78 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 78 +
                   self.OFFSET_X, 78 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)

        if self.tick > 0:
            if self.isOuter() == False:
                # 満天の星空
                pyxel.blt(self.OFFSET_X, self.OFFSET_Y, 0, 0, 40, 80, 32, 0)
            else:
                # 天井部のグリッド
                pyxel.line(0 + self.OFFSET_X, 38 + self.OFFSET_Y, 78 +
                           self.OFFSET_X, 38 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(0 + self.OFFSET_X, 35 + self.OFFSET_Y, 78 +
                           self.OFFSET_X, 35 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(0 + self.OFFSET_X, 28 + self.OFFSET_Y, 78 +
                           self.OFFSET_X, 28 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(0 + self.OFFSET_X, 9 + self.OFFSET_Y, 78 +
                           self.OFFSET_X, 9 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)

                pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 0 +
                           self.OFFSET_X, 0 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(39 + self.OFFSET_X, 39 + self.OFFSET_Y, 78 +
                           self.OFFSET_X, 0 + self.OFFSET_Y, pyxel.COLOR_DARKBLUE)

            # 迷路
            self._draw_maze(playerParty.x, playerParty.y,
                            playerParty.direction, self._map)

        # エンカウント時のメッセージ
        if self.isEncount:
            PyxelUtil.text(10, 146, ["NA", "NI", "KA", "TI", "KA", "TU",
                                     "D", "I", "TE", "KI", "TA", "*!"], pyxel.COLOR_RED)
            return

        # イベントハンドラ
        self._eventhandler("D")

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 壁の色を初期化する
        self.set_wall_color()

        # タイマーカウンタ初期化
        self.tick = 0

        # エンカウントフラグ初期化
        self.isEncount = False

        # 固定エンカウントフラグ初期化
        self.isFixedEncount = False

    def onExit(self):
        '''
        状態終了時の処理
        '''
        # 壁の色を初期化する
        self.set_wall_color()

        # タイマーカウンタ初期化
        self.tick = 0

    def isOuter(self) -> bool:
        '''
        屋外かどうかをboolで返却する

        Falseが初期値。Trueとしたければ子クラスでこのメソッドをオーバーライドする
        '''
        return False

    def _eventhandler(self, _mode):
        '''
        プレイヤーパーティーの現在の座標に登録されているイベントがあれば、そのイベントの関数を呼び出す

        引数の_modeには"U"(UPDATE)、または"D"(DRAW)のいづれかを指定する（以外の場合は常にNoneを返却する）
        初めに位置＋方向で検索し、無ければ位置で検索する。
        戻り値として、イベントが発生した場合はTrue、発生していない場合はFalseを返却する。
        '''
        # 引数のmodeの指定が誤っている場合は、何もせす終了する
        if _mode != "U" and _mode != "D":
            return False

        # 現在の座標＋方向でイベントが登録されている場合は、イベントの関数を呼び出す
        _key = "{:02d}".format(playerParty.x) + "{:02d}".format(playerParty.y) + \
            "{:01d}".format(playerParty.direction) + _mode
        _event = self.event.get(_key, None)
        if _event != None:
            _event()
            return True

        # 現在の座標でイベントが登録されている場合は、イベントの関数を呼び出す
        _key = "{:02d}".format(playerParty.x) + \
            "{:02d}".format(playerParty.y) + "9" + _mode
        _event = self.event.get(_key, None)
        if _event != None:
            _event()
            return True

        # ここに到達している場合はイベントが発生していないため、Falseを返却する
        return False

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

    def _right_3bit_rotate(self, n):
        '''
        3ビット右にローテートした値を返却する
        '''
        return ((n & 0b000000000111) << 9) | ((n >> 3) & 0b111111111111)

    def _left_3bit_rotate(self, n):
        '''
        3ビット左にローテートした値を返却する
        '''
        return ((n << 3) & 0b111111111111) | (n >> 9)

    def _get_mapinfo(self, _map, _x, _y, _direction):
        '''
        指定した座標のマップ情報を取得する。

        取得対象のマップデータと方向は引数で指定する。
        返却される値は、方向によりデータをシフトした結果となる。
        '''
        _data = _map[_y][_x]
        if _direction > self.DIRECTION_NORTH:
            for _ in range(_direction):
                _data = self._right_3bit_rotate(_data)
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
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(35 + self.OFFSET_X, 39 + self.OFFSET_Y,
                           3, 1,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 3:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(41 + self.OFFSET_X, 39 + self.OFFSET_Y,
                           3, 1,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 4:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(38 + self.OFFSET_X, 39 + self.OFFSET_Y,
                           3, 1,
                           self.WALLCOLOR_FRONT[_color])
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                pyxel.tri(43 + self.OFFSET_X, 36 + self.OFFSET_Y,
                          41 + self.OFFSET_X, 38 + self.OFFSET_Y,
                          43 + self.OFFSET_X, 38 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(41 + self.OFFSET_X, 40 + self.OFFSET_Y,
                          43 + self.OFFSET_X, 40 + self.OFFSET_Y,
                          43 + self.OFFSET_X, 42 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(41 + self.OFFSET_X, 39 + self.OFFSET_Y,
                           3, 1,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                pyxel.tri(35 + self.OFFSET_X, 36 + self.OFFSET_Y,
                          37 + self.OFFSET_X, 38 + self.OFFSET_Y,
                          35 + self.OFFSET_X, 38 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(35 + self.OFFSET_X, 40 + self.OFFSET_Y,
                          37 + self.OFFSET_X, 40 + self.OFFSET_Y,
                          35 + self.OFFSET_X, 42 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(35 + self.OFFSET_X, 39 + self.OFFSET_Y,
                           3, 1,
                           self.WALLCOLOR_SIDE[_color])

        if _idx == 5:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(26 + self.OFFSET_X, 36 + self.OFFSET_Y,
                           9, 7,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 6:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(44 + self.OFFSET_X, 36 + self.OFFSET_Y,
                           9, 7,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 7:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(35 + self.OFFSET_X, 36 + self.OFFSET_Y,
                           9, 7,
                           self.WALLCOLOR_FRONT[_color])
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                pyxel.tri(50 + self.OFFSET_X, 29 + self.OFFSET_Y,
                          44 + self.OFFSET_X, 35 + self.OFFSET_Y,
                          50 + self.OFFSET_X, 35 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(44 + self.OFFSET_X, 43 + self.OFFSET_Y,
                          50 + self.OFFSET_X, 43 + self.OFFSET_Y,
                          50 + self.OFFSET_X, 49 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(44 + self.OFFSET_X, 36 + self.OFFSET_Y,
                           7, 7,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                pyxel.tri(28 + self.OFFSET_X, 29 + self.OFFSET_Y,
                          34 + self.OFFSET_X, 35 + self.OFFSET_Y,
                          28 + self.OFFSET_X, 35 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(28 + self.OFFSET_X, 43 + self.OFFSET_Y,
                          34 + self.OFFSET_X, 43 + self.OFFSET_Y,
                          28 + self.OFFSET_X, 49 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(28 + self.OFFSET_X, 36 + self.OFFSET_Y,
                           7, 7,
                           self.WALLCOLOR_SIDE[_color])

        if _idx == 8:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(5 + self.OFFSET_X, 29 + self.OFFSET_Y,
                           23, 21,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 9:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(51 + self.OFFSET_X, 29 + self.OFFSET_Y,
                           23, 21,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 10:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(28 + self.OFFSET_X, 29 + self.OFFSET_Y,
                           23, 21,
                           self.WALLCOLOR_FRONT[_color])
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                pyxel.tri(69 + self.OFFSET_X, 10 + self.OFFSET_Y,
                          51 + self.OFFSET_X, 28 + self.OFFSET_Y,
                          69 + self.OFFSET_X, 28 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(51 + self.OFFSET_X, 50 + self.OFFSET_Y,
                          69 + self.OFFSET_X, 50 + self.OFFSET_Y,
                          69 + self.OFFSET_X, 68 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(51 + self.OFFSET_X, 29 + self.OFFSET_Y,
                           19, 21,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                pyxel.tri(9 + self.OFFSET_X, 10 + self.OFFSET_Y,
                          27 + self.OFFSET_X, 28 + self.OFFSET_Y,
                          9 + self.OFFSET_X, 28 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(9 + self.OFFSET_X, 50 + self.OFFSET_Y,
                          27 + self.OFFSET_X, 50 + self.OFFSET_Y,
                          9 + self.OFFSET_X, 68 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(9 + self.OFFSET_X, 29 + self.OFFSET_Y,
                           19, 21,
                           self.WALLCOLOR_SIDE[_color])

        if _idx == 11:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(0 + self.OFFSET_X, 10 + self.OFFSET_Y,
                           10, 59, self.WALLCOLOR_FRONT[_color])
        if _idx == 12:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(69 + self.OFFSET_X, 10 + self.OFFSET_Y,
                           10, 59, self.WALLCOLOR_FRONT[_color])
        if _idx == 13:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                pyxel.rect(10 + self.OFFSET_X, 10 + self.OFFSET_Y,
                           59, 59,
                           self.WALLCOLOR_FRONT[_color])
                if _data & 0b00000011 == 0b00000010:
                    pyxel.circ(17 + self.OFFSET_X, 40 +
                               self.OFFSET_Y, 2, pyxel.COLOR_BLACK)
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                pyxel.tri(78 + self.OFFSET_X, 1 + self.OFFSET_Y,
                          69 + self.OFFSET_X, 10 + self.OFFSET_Y,
                          78 + self.OFFSET_X, 10 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(69 + self.OFFSET_X, 68 + self.OFFSET_Y,
                          78 + self.OFFSET_X, 68 + self.OFFSET_Y,
                          78 + self.OFFSET_X, 77 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(69 + self.OFFSET_X, 10 + self.OFFSET_Y,
                           10, 59,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                pyxel.tri(0 + self.OFFSET_X, 1 + self.OFFSET_Y,
                          9 + self.OFFSET_X, 10 + self.OFFSET_Y,
                          0 + self.OFFSET_X, 10 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(0 + self.OFFSET_X, 68 + self.OFFSET_Y,
                          9 + self.OFFSET_X, 68 + self.OFFSET_Y,
                          0 + self.OFFSET_X, 77 + self.OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(0 + self.OFFSET_X, 10 + self.OFFSET_Y,
                           10, 59,
                           self.WALLCOLOR_SIDE[_color])
