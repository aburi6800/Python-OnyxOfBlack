# -*- coding: utf-8 -*-
import pyxel

from ..character import HumanGenerator, playerParty, EnemyPartyGenerator, enemyParty
from ..fieldStates.baseFieldState import BaseFieldState
from ..map.dungionB2 import dungionB2
from ..monster import monsterParams
from ..pyxelUtil import PyxelUtil

class StateDungionB2(BaseFieldState):
    '''
    地下迷宮B2のクラス

    BaseFieldStateを継承
    遭遇する敵リストとイベント処理を持つ
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "dungionB2"

        # 変数定義
        self.tick = 0
        self.isEncount = False

        # マップ
        self.map = dungionB2.map

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "18219U": self.update_to_up,
            "18219D": self.draw_to_up,
            "16279U": self.update_to_down,
            "16279D": self.draw_to_down,
            "29199U": self.update_to_down,
            "29199D": self.draw_to_down,
            "26129U": self.update_to_down,
            "26129D": self.draw_to_down,
        }

        # 出現するモンスターリスト
        self.enemy_set = (
            HumanGenerator.generate(2),
            monsterParams.monsterList[monsterParams.BAT_LV1],
            monsterParams.monsterList[monsterParams.SKELTON_LV1],
            monsterParams.monsterList[monsterParams.WOLF],
            monsterParams.monsterList[monsterParams.COBOLD_LV1],
        )

    def update_to_up(self):
        '''
        抜け穴のイベント
        '''
        if pyxel.btnp(pyxel.KEY_U):
            # B1へ戻る
            self.stateStack.pop()

    def update_to_down(self):
        '''
        抜け穴のイベント
        '''
        if pyxel.btnp(pyxel.KEY_D):
            self.stateStack.push(self.stateStack.STATE_DUNGIONB3)

    def draw_to_up(self):
        '''
        抜け穴の表示
        '''
        PyxelUtil.text(16, 140, ["U", "E", "NI", " ", "NU", "KE", "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

    def draw_to_down(self):
        '''
        抜け穴の表示
        '''
        PyxelUtil.text(16, 140, ["SI", "TA", "NI", " ", "NU", "KE", "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

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

        pass
