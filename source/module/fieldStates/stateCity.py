# -*- coding: utf-8 -*-
import pyxel
from ..pyxelUtil import PyxelUtil
from ..character import playerParty
from ..fieldStates.baseFieldState import BaseFieldState


class StateCity(BaseFieldState):
    '''
    街のクラス

    BaseFieldStateを継承
    街のマップデータとイベントデータ、イベントの処理を持つ
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "City"

        # 変数定義
        self.tick = 0

        # マップ
        # 0 = 通路
        # 1 = 壁
        # 2 = ドア
        # 3 = ブラックタワー
        # 外周は必ず壁とする
        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 2, 1, 2, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 1, 2, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"0101U"のようにX座標とY座標を2桁にした値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            #            "0104U" : self.update_enter_shieldshop(),
            "0304U": self.update_enter_armorshop,
            #            "0106U" : self.update_enter_helmetshop(),
            "0306U": self.update_enter_weaponshop,
        }

    def update(self):
        '''
        各フレームの処理
        '''
        super().update()

        try:
            # イベントが登録されている座標ならイベントの関数を呼び出す
            _key = "{:02d}".format(playerParty.x) + "{:02d}".format(playerParty.y) + "U"
            _event = self.event[_key]
            if _event != None:
                print(_event)
                _event()
        except KeyError:
            None

    def update_enter_shieldshop(self):
        '''
        盾屋に入るイベント
        '''
#        self.stateStack.push(self.stateStack.STATE_SHIELDSHOP)
        pass

    def update_enter_armorshop(self):
        '''
        鎧屋に入るイベント
        '''
        self.stateStack.push(self.stateStack.STATE_ARMORSHOP)

    def update_enter_helmetshop(self):
        '''
        兜屋に入るイベント
        '''
#        self.stateStack.push(self.stateStack.STATE_HELMETSHOP)
        pass

    def update_enter_weaponshop(self):
        '''
        武器屋に入るイベント
        '''
        self.stateStack.push(self.stateStack.STATE_WEAPONSHOP)

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()
        # 満天の星空
        pyxel.blt(152, 17, 0, 0, 40, 80, 32, 0)
        # 迷路
        super().draw_maze(playerParty.x, playerParty.y, playerParty.direction, self.map)

#        # テスト：タコさんが表示できるのか？
#        pyxel.blt(176, 105, 2, 0, 16, 32, 32, 0)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        self.tick = 0
        self.selected = 0
        self.isEncount = False

        # プレイヤーパーティーの最初の位置と方向
        playerParty.x = 6
        playerParty.y = 1
        playerParty.direction = self.DIRECTION_SOUTH

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
