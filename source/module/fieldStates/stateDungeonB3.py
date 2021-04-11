# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.dungeonB3 import dungeonB3
from module.params.monster import monsterParams
from module.pyxelUtil import PyxelUtil
from module.state import State
from overrides import overrides


class StateDungeonB3(BaseFieldState):
    '''
    地下迷宮B3のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    STATENAME = "DUNGEONB3"

    # マップ
    _map = dungeonB3.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(4),
        HumanGenerator.generate(5),
        monsterParams["MUMMY_LV2"],
        monsterParams["ORC_LV2"],
        monsterParams["SLIME_LV1"],
        monsterParams["SPIDER_LV1"],
        monsterParams["GHOUL_LV1"],
        monsterParams["COBRA_LV1"],
        monsterParams["VAMPIRE_LV1"],
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
