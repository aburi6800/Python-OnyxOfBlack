# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator, playerParty
from module.fieldStates.baseFieldState import BaseFieldState
from module.fieldStates.stateDungeonB5 import StateDungeonB5
from module.map.wellB4 import wellB4
from module.params.monster import monsterParams
from module.pyxelUtil import PyxelUtil


class StateWellB4(BaseFieldState):
    '''
    井戸B2のクラス

    BaseFieldStateを継承
    遭遇する敵リストとイベント処理を持つ
    '''

    # マップ
    _map = wellB4.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(8),
        monsterParams["WOLF_LV2"],
        monsterParams["LION_LV2"],
        monsterParams["SLIME_LV2"],
        monsterParams["SPIDER_LV1"],
        monsterParams["GHOUL_LV1"],
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
            "10109U": self.update_to_upanddown,
            "10109D": self.draw_to_upanddown,
        }

    def update_to_upanddown(self):
        '''
        抜け穴のイベント
        '''
        if pyxel.btnp(pyxel.KEY_U):
            playerParty.x = 10
            playerParty.y = 10
            # 井戸B2へ戻る
            self.popState()

        if pyxel.btnp(pyxel.KEY_D):
            playerParty.x = 10
            playerParty.y = 10
            # 地下迷宮B5へ
            self.pushState(StateDungeonB5)

    def draw_to_upanddown(self):
        '''
        天井の抜け穴の表示
        '''
        PyxelUtil.text(16, 140, ["U", "E", "TO", "SI", "TA", "NI", " ", "NU",
                                 "KE", "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

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
