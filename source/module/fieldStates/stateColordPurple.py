# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.colord_all import colord_all
from module.params.monster import monsterParams
from overrides import overrides


class StateColordPurple(BaseFieldState):
    '''
    カラー迷路（紫）のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    stateName = "COLORD_PURPLE"

    # マップ
    _map = colord_all.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(5),
        HumanGenerator.generate(6),
        monsterParams["WIRKAT_LV2"],
        monsterParams["WIRKAT_LV2"],
        monsterParams["BEAST_LV1"],
        monsterParams["BEAST_LV1"],
        monsterParams["DEMON_LV2"],
        monsterParams["DEMON_LV2"],
        monsterParams["GHOST_LV1"],
        monsterParams["GHOST_LV1"],
        monsterParams["TROLL_LV1"],
        monsterParams["DEMON_LV2"],
        monsterParams["MIER_LV1"],
        monsterParams["MIER_LV2"],
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
        self.set_wall_color(pyxel.COLOR_PURPLE, pyxel.COLOR_PURPLE, pyxel.COLOR_BLACK)

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()
