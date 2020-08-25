# -*- coding: utf-8 -*-
import pyxel

from ..character import HumanGenerator
from ..map.dungionB3 import dungionB3
from ..monster import monsterParams
from ..pyxelUtil import PyxelUtil
from .baseFieldState import BaseFieldState


class StateDungionB3(BaseFieldState):
    '''
    地下迷宮B3のクラス

    BaseFieldStateを継承
    遭遇する敵リストとイベント処理を持つ
    '''

    # マップ
    _map = dungionB3.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(2),
        monsterParams.monsterList[monsterParams.BAT_LV1],
        monsterParams.monsterList[monsterParams.SKELTON_LV1],
        monsterParams.monsterList[monsterParams.WOLF],
        monsterParams.monsterList[monsterParams.COBOLD_LV1],
    )

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "dungionB3"

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "16289U": self.update_to_up,
            "16289D": self.draw_to_up,
            "28199U": self.update_to_up,
            "28199D": self.draw_to_up,
            "26129U": self.update_to_up,
            "26129D": self.draw_to_up,
            "06069U": self.update_to_down,
            "06069D": self.draw_to_down,
        }

        self.onEnter()

    def update_to_up(self):
        '''
        上に上がる階段のイベント
        '''
        if pyxel.btnp(pyxel.KEY_U):
            # B2へ戻る
            self.stateStack.pop()

    def update_to_down(self):
        '''
        下に降りる階段のイベント
        '''
        if pyxel.btnp(pyxel.KEY_D):
            self.stateStack.push(self.stateStack.STATE_DUNGIONB3)

    def draw_to_up(self):
        '''
        上に上がる階段の表示
        '''
        PyxelUtil.text(16, 140, ["U", "E", "NI", " ", "A", "KA", "D", "RU", " ", "KA", "I",
                                 "TA", "D", "NN", " ", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

    def draw_to_down(self):
        '''
        下に降りる階段の表示
        '''
        PyxelUtil.text(16, 140, ["SI", "TA", "NI", " ", "O", "RI", "RU", " ", "KA", "I",
                                 "TA", "D", "NN", " ", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 壁の色を初期化する
        self.set_wall_color(pyxel.COLOR_LIGHTBLUE, pyxel.COLOR_DARKBLUE)

    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()
