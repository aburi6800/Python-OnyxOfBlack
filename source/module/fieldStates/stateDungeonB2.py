# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.dungeonB2 import dungeonB2
from module.params.monster import monsterParams
from overrides import overrides


class StateDungeonB2(BaseFieldState):
    '''
    地下迷宮B2のクラス\n
    BaseFieldStateを継承。\n
    遭遇する敵リストとイベント処理を持つ。
    '''

    # マップ
    _map = dungeonB2.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(4),
        monsterParams["COBOLD_LV2"],
        monsterParams["SKELTON_LV2"],
        monsterParams["ZOMBIE_LV2"],
        monsterParams["AZTEC_LV1"],
        monsterParams["GOBLIN_LV1"],
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
            "18219U": "self.startEvent('dungeonb2_001.json')",
            "16279U": "self.startEvent('dungeonb1_002.json')",
            "29199U": "self.startEvent('dungeonb1_002.json')",
            "26129U": "self.startEvent('dungeonb1_002.json')",
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
