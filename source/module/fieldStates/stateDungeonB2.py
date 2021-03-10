# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.dungeonB2 import dungeonB2
from module.params.monster import monsterParams
from module.pyxelUtil import PyxelUtil
from module.state import State
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
            "18219U": self.update_to_up,
            "18219D": self.draw_to_up,
            "16279U": self.update_to_down,
            "16279D": self.draw_to_down,
            "29199U": self.update_to_down,
            "29199D": self.draw_to_down,
            "26129U": self.update_to_down,
            "26129D": self.draw_to_down,
        }

    def update_to_up(self):
        '''
        上に上がる階段のイベント
        '''
        if pyxel.btnp(pyxel.KEY_U):
            # B1へ戻る
            self.stateStack.pop()

    def update_to_down(self):
        '''
        下に降りる階段のイベント
        '''
        if pyxel.btnp(pyxel.KEY_D):
            self.stateStack.push(State.DUNGEONB3)

    def draw_to_up(self):
        '''
        上に上がる階段の表示
        '''
        PyxelUtil.text(16, 140, ["U", "E", "NI", " ", "A", "KA", "D", "RU", " ", "KA", "I",
                                 "TA", "D", "NN", " ", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

    def draw_to_down(self):
        '''
        下に降りる階段の表示
        '''
        PyxelUtil.text(16, 140, ["SI", "TA", "NI", " ", "O", "RI", "RU", " ", "KA", "I",
                                 "TA", "D", "NN", " ", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

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
