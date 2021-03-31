# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator, playerParty
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.cemetery import cemetery
from module.params.monster import monsterParams
from module.pyxelUtil import PyxelUtil
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
        monsterParams["BAT_LV1"],
        monsterParams["SKELETON_LV1"],
        monsterParams["ZOMBIE_LV1"],
        monsterParams["KOBOLD_LV1"],
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    def update_to_city(self):
        '''
        天井の抜け穴のイベント
        '''
        if pyxel.btn(pyxel.KEY_U):
            if playerParty.x == 9 and playerParty.y == 6:
                playerParty.x = 25
                playerParty.y = 19
            if playerParty.x == 10 and playerParty.y == 6:
                playerParty.x = 26
                playerParty.y = 19
            if playerParty.x == 9 and playerParty.y == 7:
                playerParty.x = 25
                playerParty.y = 20
            if playerParty.x == 10 and playerParty.y == 7:
                playerParty.x = 26
                playerParty.y = 20
            # 町へ戻る
            self.stateStack.pop()

    def draw_to_city(self):
        '''
        天井の抜け穴の表示
        '''
        PyxelUtil.text(16, 140, ["TE", "NN", "SI", "D", "LYO", "U", "NI", " ", "NU",
                                 "KE", "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

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
