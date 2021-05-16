# -*- coding: utf-8 -*-
import random

import pyxel
from module.character import playerParty
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.blacktower import blacktower
from module.params.monster import monsterParams
from overrides import overrides


class StateBlackTower(BaseFieldState):
    '''
    カラー迷路（黒）のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    stateName = "BLACKTOWER"

    # マップ
    _map = blacktower.map

    # 出現するモンスターリスト
    enemy_set = (
        monsterParams["TAURUS_LV1"],
        monsterParams["TAURUS_LV1"],
        monsterParams["TAURUS_LV1"],
        monsterParams["TAURUS_LV1"],
        monsterParams["GIANT_LV1"],
        monsterParams["GIANT_LV1"],
        monsterParams["GIANT_LV1"],
        monsterParams["HIDER_LV1"],
        monsterParams["WRAITH_LV1"],
        monsterParams["WRAITH_LV1"],
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    @overrides
    def doEncounted(self) -> bool:
        '''
        エンカウントしたかを返却する\n
        '''
        if random.randint(0, 16) == 0:
            return True
        else:
            return False

    @overrides
    def update_execute(self):
        '''
        各フレームの処理\n
        ブラックタワーの上下左右ループを追加実装
        '''
        super().update_execute()

        # ループ判定
        if playerParty.x < 9:
            playerParty.x = 23
        elif playerParty.x > 23:
            playerParty.x = 9
        elif playerParty.y < 11:
            playerParty.y = 25
        elif playerParty.y > 25:
            playerParty.y = 11

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        # 壁の色を初期化する
        self.set_wall_color(pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK)

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()

    @overrides
    def isOuter(self) -> bool:
        '''
        屋外かどうかをboolで返却する。\n
        オーバーライドし、固定でTrueを返却する。
        '''
        return True
    
    @overrides
    def isSky(self) -> bool:
        '''
        ブラックタワー内かどうかをboolで返却する。\n
        オーバーライドし、固定でTrueを返却する。
        '''
        return True
