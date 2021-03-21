# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.wellB3 import wellB3
from module.params.monster import monsterParams
from overrides import overrides


class StateWellB3(BaseFieldState):
    '''
    井戸B2のクラス\n
    BaseFieldStateを継承。\n
    遭遇する敵リストとイベント処理を持つ。
    '''

    # マップ
    _map = wellB3.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(6),
        monsterParams["AZTEC_LV2"],
        monsterParams["GOBLIN_LV2"],
        monsterParams["WOLF_LV1"],
        monsterParams["LION_LV1"],
        monsterParams["SLIME_LV1"],
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "10109U": "self.startEvent('wellb3_001.json')",
        }

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 壁の色を初期化する
        self.set_wall_color(pyxel.COLOR_LIGHTBLUE, pyxel.COLOR_DARKBLUE)

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()
