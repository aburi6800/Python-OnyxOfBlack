# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.dungeonB1 import dungeonB1
from module.params.monster import monsterParams
from overrides import overrides


class StateDungeonB1(BaseFieldState):
    '''
    地下迷宮B1のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    STATENAME = "DUNGEONB1"

    # マップ
    _map = dungeonB1.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(2),
        HumanGenerator.generate(3),
        monsterParams["BAT_LV1"],
        monsterParams["BAT_LV1"],
        monsterParams["WOLF_LV1"],
        monsterParams["WOLF_LV1"],
        monsterParams["KOBOLD_LV1"],
        monsterParams["KOBOLD_LV1"],
        monsterParams["ZOMBIE_LV1"],
        monsterParams["ZOMBIE_LV1"],
        monsterParams["SKELETON_LV1"],
        monsterParams["SKELETON_LV1"],
        monsterParams["GOBLIN_LV1"],
        monsterParams["AZTEC_LV1"],
        monsterParams["LION_LV1"],
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

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
