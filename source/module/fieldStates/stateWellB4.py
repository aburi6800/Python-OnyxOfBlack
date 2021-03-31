# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.wellB4 import wellB4
from module.params.monster import monsterParams
from overrides import overrides


class StateWellB4(BaseFieldState):
    '''
    井戸B4のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    STATENAME = "WELLB4"

    # マップ
    _map = wellB4.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(8),
        monsterParams["LION_LV2"],
        monsterParams["SLIME_LV2"],
        monsterParams["SPIDER_LV1"],
        monsterParams["GHOUL_LV1"],
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
