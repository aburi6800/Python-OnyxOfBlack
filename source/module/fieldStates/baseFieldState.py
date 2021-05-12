# -*- coding: utf-8 -*-
import random

import pyxel
from module.baseState import BaseState
from module.character import enemyParty, playerParty
from module.direction import Direction
from module.eventData import eventdata
from module.eventHandler import eventhandler
from module.messageHandler import messagehandler
from module.params.monster import monsterParams
from module.pyxelUtil import PyxelUtil
from module.state import State
from overrides import EnforceOverrides, overrides


class BaseFieldState(BaseState, EnforceOverrides):
    '''
    フィールドのStateクラスの基底クラス\n
    各フィールドで共通の処理を持つ。\n
    迷路の描画処理に必要な情報を持つ。（他のクラスでは必要としない）\n
    迷路の描画処理を行う。
    '''

    # 自分の位置と方向からマップのどこを参照するかを、参照順に定義
    # 参照順のイメージは以下（上向きである前提、自分の位置はDとする）
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

    # 移動後判定フラグ
    isAfterMoved = False

    # エンカウントフラグ
    isEncount = False

    # 固定エンカウントフラグ
    isFixedEncount = False

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    def set_wall_color(self, wallcolor_front=pyxel.COLOR_LIGHTBLUE, wallcolor_side=pyxel.COLOR_DARKBLUE, doorcolor=pyxel.COLOR_YELLOW):
        '''
        壁の色を設定する。\n
        途中で変更したい場合に使用する。\n
        wallcolor_frontは正面の壁の色、wallcolor_sideは側面の壁の色を指定する。\n
        扉の色、ブラックタワーの色は変更不可。
        '''
        # 迷路描画の壁の色（正面）
        self.WALLCOLOR_FRONT[1] = wallcolor_front
        self.WALLCOLOR_FRONT[4] = wallcolor_front

        # 迷路描画の壁の色（側面）
        self.WALLCOLOR_SIDE[1] = wallcolor_side
        self.WALLCOLOR_SIDE[4] = wallcolor_side

        # ドアの色
        self.WALLCOLOR_FRONT[2] = doorcolor
        self.WALLCOLOR_SIDE[2] = doorcolor

    @overrides
    def update_execute(self):
        '''
        各フレームの処理
        '''
        super().update_execute()

        # パーティーは逃げてきたか？
        if playerParty.isEscaped:
            # フラグを降ろす
            playerParty.isEscaped = False
            # 以前の場所に戻す
            playerParty.restoreCondition()
            # イベントを強制的に終了
            eventhandler.isExecute = False

        # エンカウントしているか？
        if self.isEncount:
            if self.tick > 30:
                self.isEncount = False
                self.tick = 0
                self.stateStack.push(State.BATTLE)
                return
            else:
                return

        # イベントハンドラでイベントが実行中の場合は、イベントハンドラのupdateメソッドを呼んで終了する
        if eventhandler.isExecute:
            eventhandler.update()
            return

        # 固定エンカウントしていた場合は、イベント辞書からデータを削除する
        # 戦闘から逃げて終了した場合は、ここに到達する前に座標が変更されているのでイベントは削除されない
        if self.isFixedEncount:
            print("delete fixed-encount data.")
            try:
                # イベント辞書から削除
                del(eventdata.events[self.getEventKey(9, "U")])
            except KeyError as ke:
                # KeyErrorが発生しても無視する
                pass
            self.isFixedEncount = False

        # イベントチェック
        if self.checkEvent("U") == False:
            # イベントが何もない場合、エンカウントするか？
            if self.isAfterMoved and random.randint(0, 24) == 0:
                self.encount_enemy()
                return

        # キャンプ
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.stateStack.push(State.CAMP)

        # キー入力（右）
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.tick = 0
            playerParty.turnRight()
            return

        # キー入力（左）
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.tick = 0
            playerParty.turnLeft()
            return

        # キー入力（下）
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.tick = 0
            playerParty.turnBack()
            return

        # キー入力（上）
        if pyxel.btnp(pyxel.KEY_UP) and self.can_move_forward(self._map, playerParty.x, playerParty.y, playerParty.direction):
            self.tick = 0
            playerParty.moveForward()

            # 移動後判定フラグをFalseに設定する
            self.isAfterMoved = True
            return

        # 移動後判定フラグをFalseに設定する
        self.isAfterMoved = False

    def encount_enemy(self, monsterName: str = ""):
        '''
        敵とエンカウントした時の処理\n
        引数で指定されたモンスター（省略時はそのStateのenemy_setからランダムで指定）のenemyPartyを生成し、isEncountをTrueに変更する。\n
        マップにより特殊な条件でenemyPartyを生成する場合は、サブクラスでオーバーライドする。
        '''
        self.isEncount = True
        self.tick = 0

        if monsterName == "":
            enemyParty.generate(self.enemy_set[random.randint(0, len(self.enemy_set) - 1)])
        else:
            enemyParty.generate(monsterParams[monsterName])
            
    def update_fixed_encount_enemy(self):
        '''
        敵と固定エンカウントした時の処理\n
        固定エンカウントをしたい座標に、このメソッドをイベント辞書に登録する。\n
        isFixedEncountがFalseの時は、ランダムエンカウント時のメソッドを呼び出す。\n
        isFixedEncountがTrueの時は、イベント辞書から削除する。
        '''
        # 固定エンカウントしていない状態か？
        if self.isFixedEncount == False:
            self.isFixedEncount = True
            self.encount_enemy()
            return

    def can_move_forward(self, _map, _x: int, _y: int, _direction: int) -> bool:
        '''
        前進できるかを判定する。\n
        マップデータを方向によりシフトした結果の下位1ビットが立っている（＝目の前の壁情報が通行不可）場合は、前進不可と判定する。
        '''
        _value = self.get_mapinfo(_map, _x, _y, _direction)

        if _value & 0b000000000001 == 0b000000000001:
            return False
        else:
            return True

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        # 開発用
        PyxelUtil.text(0, 0, "*X:" + str(playerParty.x) + " Y:" + str(playerParty.y) + " DIR:" +
                       str(playerParty.direction) + "-" + bin(self._map[playerParty.y][playerParty.x]))

        # 迷路の枠線
        pyxel.rectb(self.DRAW_OFFSET_X - 1, self.DRAW_OFFSET_Y -
                    1, 81, 81, pyxel.COLOR_DARKBLUE)

        # 地面部のグリッド
        pyxel.line(0 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y, 78 +
                   self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y, 78 +
                   self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y, 78 +
                   self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(0 + self.DRAW_OFFSET_X, 69 + self.DRAW_OFFSET_Y, 78 +
                   self.DRAW_OFFSET_X, 69 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)

        pyxel.line(39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y, 0 +
                   self.DRAW_OFFSET_X, 78 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
        pyxel.line(39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y, 78 +
                   self.DRAW_OFFSET_X, 78 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)

        if self.tick > 0:
            if self.isOuter():
                # 満天の星空
                pyxel.blt(self.DRAW_OFFSET_X, self.DRAW_OFFSET_Y, 0, playerParty.direction * 32, 40, 80, 32, 0)
            else:
                # 天井部のグリッド
                pyxel.line(0 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y, 78 +
                           self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(0 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y, 78 +
                           self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(0 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y, 78 +
                           self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(0 + self.DRAW_OFFSET_X, 9 + self.DRAW_OFFSET_Y, 78 +
                           self.DRAW_OFFSET_X, 9 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)

                pyxel.line(39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y, 0 +
                           self.DRAW_OFFSET_X, 0 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)
                pyxel.line(39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y, 78 +
                           self.DRAW_OFFSET_X, 0 + self.DRAW_OFFSET_Y, pyxel.COLOR_DARKBLUE)

            # 迷路
            self.draw_maze(playerParty.x, playerParty.y,
                            playerParty.direction, self._map)

        # エンカウント時のメッセージ
        if self.isEncount:
            PyxelUtil.text(10, 146, ["NA", "NI", "KA", "TI", "KA", "TU",
                                     "D", "I", "TE", "KI", "TA", "*!"], pyxel.COLOR_RED)
            return

        # イベントハンドラでイベントが実行中の場合は、イベントハンドラのdrawメソッドを呼ぶ
        if eventhandler.isExecute:
            eventhandler.draw()

        # メッセージハンドラにキューが登録されてる場合は、メッセージハンドラのdrawメソッドを呼ぶ
        if messagehandler.isEnqueued():
            messagehandler.draw()

        # イベントハンドラ
        self.checkEvent("D")

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 壁の色を初期化する
        self.set_wall_color()

        # 移動後判定フラグ初期化
        self.isAfterMoved = False

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()

        # 壁の色を初期化する
        self.set_wall_color()

        # タイマーカウンタ初期化
        self.tick = 0

    def isOuter(self) -> bool:
        '''
        屋外かどうかをboolで返却する。\n
        Falseが初期値。Trueとしたければ子クラスでこのメソッドをオーバーライドする。\n
        '''
        return False

    def checkEvent(self, _mode) -> bool:
        '''
        プレイヤーパーティーの現在の座標に登録されているイベントがあれば、そのイベントの関数を呼び出す。\n
        引数の_modeには"U"(UPDATE)、または"D"(DRAW)のいづれかを指定する。（以外の場合は常にNoneを返却する）\n
        初めに位置＋方向で検索し、無ければ位置で検索する。\n
        戻り値として、イベントが発生した場合はTrue、発生していない場合はFalseを返却する。\n
        '''
        # 引数のmodeの指定が誤っている場合は、何もせす終了する
        if _mode != "U" and _mode != "D":
            return False

        # 現在の座標＋方向でイベントの関数を取得する
        _event = eventdata.events.get(self.getEventKey(playerParty.direction, _mode), None)

        if _event == None:
            # 取得できなかったときは、現在の座標でイベントの関数を取得する
            _event = eventdata.events.get(self.getEventKey(9, _mode), None)

        # イベントの関数が取得できた場合は呼び出しを行う
        if _event != None:
            if type(_event) is str:
                eval(_event)
            else:
                _event()
            return True

        # ここに到達している場合はイベントが発生していないため、Falseを返却する
        return False

    def getEventKey(self, direction, mode) -> str:
        '''
        イベントデータのキーを生成して返却する\n
        現在のStateの名称、プレイヤーパーティーの座標、引数の方向・モード（"U"(update)、"D"(draw))から
        EventDataを検索するためのキー文字列を生成し、返却する。\n
        '''
        return self.stateName + "{:02d}".format(playerParty.x) + \
            "{:02d}".format(playerParty.y) +  "{:01d}".format(direction) + mode

    def startEvent(self, eventFileName:str) -> None:
        '''
        イベントを開始する\n
        ただし、移動直後のみ開始する。
        '''
        if self.isAfterMoved:
            eventhandler.startEvent(eventFileName, self)

    def draw_maze(self, _x, _y, _direction, _map):
        '''
        迷路を表示する。\n
        利用元からは、X座標、Y座標、方向、マップデータを引数に与えること。\n
        '''
        _data = 0
        for i in range(14):
            _get_x = _x + self.POS_X[_direction][i]
            _get_y = _y + self.POS_Y[_direction][i]

            if _get_x < 0 or _get_x > len(_map[_y]) - 1 or _get_y < 0 or _get_y > len(_map) - 1:
                _data = 0
            else:
                _data = self.get_mapinfo(_map, _get_x, _get_y, _direction)
            self.draw_wall(i, _data)

    def __right_3bit_rotate(self, n) -> int:
        '''
        3ビット右にローテートした値を返却する。
        '''
        return ((n & 0b000000000111) << 9) | ((n >> 3) & 0b111111111111)

    def __left_3bit_rotate(self, n) -> int:
        '''
        3ビット左にローテートした値を返却する。
        '''
        return ((n << 3) & 0b111111111111) | (n >> 9)

    def get_mapinfo(self, _map, _x, _y, _direction) -> int:
        '''
        指定した座標のマップ情報を取得する。\n
        取得対象のマップデータと方向は引数で指定する。\n
        返却される値は、方向によりデータをシフトした結果となる。
        '''
        _data = _map[_y][_x]
        if _direction > Direction.NORTH:
            for _ in range(_direction):
                _data = self.__right_3bit_rotate(_data)
        return _data

    def draw_wall(self, _idx, _data):
        '''
        迷路を表示する。\n
        drawMazeクラスからの利用を想定し、他のモジュールからの使用は想定していない。\n
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
                _y = 0 if (self.isOuter() and _color == 3) else 39
                _h = 38 if (self.isOuter() and _color == 3) else 1
                pyxel.rect(35 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 3:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 39
                _h = 38 if (self.isOuter() and _color == 3) else 1
                pyxel.rect(41 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 4:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 39
                _h = 38 if (self.isOuter() and _color == 3) else 1
                pyxel.rect(38 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLCOLOR_FRONT[_color])
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 39
                _h = 38 if (self.isOuter() and _color == 3) else 1
                pyxel.tri(43 + self.DRAW_OFFSET_X, 36 + self.DRAW_OFFSET_Y,
                          41 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          43 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(41 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          43 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          43 + self.DRAW_OFFSET_X, 42 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(41 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 39
                _h = 38 if (self.isOuter() and _color == 3) else 1
                pyxel.tri(35 + self.DRAW_OFFSET_X, 36 + self.DRAW_OFFSET_Y,
                          37 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          35 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(35 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          37 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          35 + self.DRAW_OFFSET_X, 42 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(35 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLCOLOR_SIDE[_color])

        if _idx == 5:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 36
                _h = 43 if (self.isOuter() and _color == 3) else 7
                pyxel.rect(26 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           9, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 6:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 36
                _h = 43 if (self.isOuter() and _color == 3) else 7
                pyxel.rect(44 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           9, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 7:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 36
                _h = 43 if (self.isOuter() and _color == 3) else 7
                pyxel.rect(35 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           9, _h,
                           self.WALLCOLOR_FRONT[_color])
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 36
                _h = 43 if (self.isOuter() and _color == 3) else 7
                pyxel.tri(50 + self.DRAW_OFFSET_X, 29 + self.DRAW_OFFSET_Y,
                          44 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          50 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(44 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          50 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          50 + self.DRAW_OFFSET_X, 49 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(44 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           7, _h,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 36
                _h = 43 if (self.isOuter() and _color == 3) else 7
                pyxel.tri(28 + self.DRAW_OFFSET_X, 29 + self.DRAW_OFFSET_Y,
                          34 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          28 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(28 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          34 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          28 + self.DRAW_OFFSET_X, 49 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(28 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           7, _h,
                           self.WALLCOLOR_SIDE[_color])

        if _idx == 8:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 29
                _h = 50 if (self.isOuter() and _color == 3) else 21
                pyxel.rect(5 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           23, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 9:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 29
                _h = 50 if (self.isOuter() and _color == 3) else 21
                pyxel.rect(51 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           23, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 10:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 29
                _h = 50 if (self.isOuter() and _color == 3) else 21
                pyxel.rect(28 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           23, _h,
                           self.WALLCOLOR_FRONT[_color])
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 29
                _h = 50 if (self.isOuter() and _color == 3) else 21
                pyxel.tri(69 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          51 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(51 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(51 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           19, _h,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 29
                _h = 50 if (self.isOuter() and _color == 3) else 21
                pyxel.tri(9 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          27 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(9 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          27 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(9 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           19, _h,
                           self.WALLCOLOR_SIDE[_color])

        if _idx == 11:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 10
                _h = 69 if (self.isOuter() and _color == 3) else 59
                pyxel.rect(0 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 12:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 10
                _h = 69 if (self.isOuter() and _color == 3) else 59
                pyxel.rect(69 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLCOLOR_FRONT[_color])
        if _idx == 13:
            if _data & 0b000000000111 != 0:
                _color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 10
                _h = 69 if (self.isOuter() and _color == 3) else 59
                pyxel.rect(10 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           59, _h,
                           self.WALLCOLOR_FRONT[_color])
                if _data & 0b00000011 == 0b00000010:
                    pyxel.circ(17 + self.DRAW_OFFSET_X, 40 +
                               self.DRAW_OFFSET_Y, 2, pyxel.COLOR_BLACK)
            if _data & 0b000000111000 != 0:
                _color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 10
                _h = 69 if (self.isOuter() and _color == 3) else 59
                pyxel.tri(78 + self.DRAW_OFFSET_X, 1 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          78 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(69 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          78 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          78 + self.DRAW_OFFSET_X, 77 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(69 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLCOLOR_SIDE[_color])
            if _data & 0b111000000000 != 0:
                _color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _color == 3) else 10
                _h = 69 if (self.isOuter() and _color == 3) else 59
                pyxel.tri(0 + self.DRAW_OFFSET_X, 1 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          0 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.tri(0 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          0 + self.DRAW_OFFSET_X, 77 + self.DRAW_OFFSET_Y,
                          self.WALLCOLOR_SIDE[_color])
                pyxel.rect(0 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLCOLOR_SIDE[_color])
