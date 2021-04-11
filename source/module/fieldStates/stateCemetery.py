# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.cemetery import cemetery
from module.params.monster import monsterParams
from overrides import overrides


class StateCemetery(BaseFieldState):
    '''
    墓地の地下のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    STATENAME = "CEMETERY"

    # マップ
    _map = cemetery.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(1),
        HumanGenerator.generate(2),
        monsterParams["WOLF_LV1"],
        monsterParams["BAT_LV1"],
        monsterParams["ZOMBIE_LV1"],
        monsterParams["SKELETON_LV1"],
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
        self.set_wall_color(pyxel.COLOR_RED, pyxel.COLOR_PURPLE)

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()
