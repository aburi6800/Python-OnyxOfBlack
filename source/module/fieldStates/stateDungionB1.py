# -*- coding: utf-8 -*-
import pyxel

from ..character import HumanGenerator, playerParty
from ..map.dungionB1 import dungionB1
from ..monster import monsterParams
from ..pyxelUtil import PyxelUtil
from .baseFieldState import BaseFieldState
from .stateDungionB2 import StateDungionB2


class StateDungionB1(BaseFieldState):
    '''
    地下迷宮B1のクラス

    BaseFieldStateを継承
    遭遇する敵リストとイベント処理を持つ
    '''

    # マップ
    _map = dungionB1.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(2),
        monsterParams.monsterList[monsterParams.BAT_LV1],
        monsterParams.monsterList[monsterParams.SKELTON_LV1],
        monsterParams.monsterList[monsterParams.WOLF],
        monsterParams.monsterList[monsterParams.COBOLD_LV1],
    )

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "03069U": self.update_to_up,
            "03069D": self.draw_to_up,
            "18219U": self.update_to_down,
            "18219D": self.draw_to_down,
        }

    def update_to_up(self):
        '''
        上に上がる階段のイベント
        '''
        if pyxel.btnp(pyxel.KEY_U):
            playerParty.x = 11
            playerParty.y = 7
            # 町へ戻る
            self.popState()

    def update_to_down(self):
        '''
        下に降りる階段のイベント
        '''
        if pyxel.btnp(pyxel.KEY_D):
            self.pushState(StateDungionB2)

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
