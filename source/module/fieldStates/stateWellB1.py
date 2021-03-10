# -*- coding: utf-8 -*-
import pyxel
from module.character import HumanGenerator, playerParty
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.wellB1 import wellB1
from module.messageHandler import messageCommand, messagehandler
from module.params.monster import monsterParams
from module.state import State
from overrides import overrides


class StateWellB1(BaseFieldState):
    '''
    井戸B1のクラス\n
    BaseFieldStateを継承。\n
    遭遇する敵リストとイベント処理を持つ。
    '''

    # マップ
    _map = wellB1.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(2),
        monsterParams["BAT_LV1"],
        monsterParams["BAT_LV2"],
        monsterParams["COBOLD_LV1"],
        monsterParams["SKELTON_LV1"],
        monsterParams["ZOMBIE_LV1"],
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
            "10109U": self.update_to_upanddown,
        }

    def update_to_upanddown(self):
        '''
        抜け穴のイベント
        '''
        def go_to_up(self):
            playerParty.x = 15
            playerParty.y = 14
            # 町へ戻る
            self.stateStack.pop()

        def go_to_down(self):
            playerParty.x = 10
            playerParty.y = 10
            # 井戸B2へ
            self.stateStack.push(State.WELLB2)

        if self.tick == 1:
            c = messageCommand()
            c.addMessage(["U", "E", "TO", "SI", "TA", "NI", " ", "NU", "KE", "A", "NA", "KA", "D", " ", "A", "RU", "."])
            c.addMessage([""])
            c.addChoose(["*[U] ","U", "E", " ", "NI", " ", "NO", "HO", "D", "RU"], pyxel.KEY_U, go_to_up)
            c.addChoose(["*[D] ","SI", "TA", " ", "NI", " ", "O", "RI", "RU"], pyxel.KEY_D, go_to_down)
            c.addChoose(["*[L] ","KO", "NO", "HA", "D", "WO", " ", "TA", "TI", "SA", "RU"], pyxel.KEY_L, None)
            messagehandler.enqueue(c)
            return

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
