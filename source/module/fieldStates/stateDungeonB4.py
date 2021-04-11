# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.dungeonB4 import dungeonB4
from module.params.monster import monsterParams
from overrides import overrides


class StateDungeonB4(BaseFieldState):
    '''
    地下迷宮B4のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    STATENAME = "DUNGEONB4"

    # マップ
    _map = dungeonB4.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(5),
        HumanGenerator.generate(6),
        monsterParams["SLIME_LV2"],
        monsterParams["SPIDER_LV2"],
        monsterParams["GHOUL_LV2"],
        monsterParams["COBRA_LV2"],
        monsterParams["BLAAB_LV1"],
        monsterParams["VAMPIRE_LV2"],
        monsterParams["OGRE_LV1"],
        monsterParams["HOBGOBLIN_LV1"],
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
