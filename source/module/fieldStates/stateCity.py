# -*- coding: utf-8 -*-
import random

import pyxel
from module.character import (EnemyPartyGenerator, HumanGenerator, enemyParty,
                              playerParty)
from module.direction import Direction
from module.fieldStates.baseFieldState import BaseFieldState
from module.map.uturotown import uturotown
from module.params.monster import monsterParams
from module.pyxelUtil import PyxelUtil
from module.state import State
from overrides import overrides


class StateCity(BaseFieldState):
    '''
    街のクラス\n
    BaseFieldStateを継承。\n
    遭遇する敵リストと街のイベント処理を持つ
    '''

    # マップ
    _map = uturotown.map

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(1),
        HumanGenerator.generate(1),
        HumanGenerator.generate(1),
        HumanGenerator.generate(2),
        monsterParams["BAT_LV1"],
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
            "17040D": self.draw_gate,
            "18040D": self.draw_gate,
            "17030U": "playerParty.restoreCondition()",
            "18030U": "playerParty.restoreCondition()",
            "27073D": self.draw_shieldshop,
            "26073U": "self.stateStack.push(State.SHIELDSHOP)",
            "27061D": self.draw_armorshop,
            "28061U": "self.stateStack.push(State.ARMORSHOP)",
            "27081D": self.draw_weaponshop,
            "28081U": "self.stateStack.push(State.WEAPONSHOP)",
            "27101D": self.draw_helmetshop,
            "28101U": "self.stateStack.push(State.HELMETSHOP)",
            "27113D": self.draw_barbar,
            "26113U": "self.stateStack.push(State.BARBAR)",
            "16083D": self.draw_donotenter,
            "21052D": self.draw_inn,
            "23092D": self.draw_physicker,
            "23100D": self.draw_physicker_exit,
            "23103D": self.draw_drugs,
            "22103U": "self.stateStack.push(State.DRUGS)",
            "23101D": self.draw_surgery,
            "24101U": "self.stateStack.push(State.SURGERY)",
            "23111D": self.draw_examinations,
            "24111U": "self.stateStack.push(State.EXAMINATIONS)",
            "17141D": self.draw_thewall,
            "18143D": self.draw_thewall,
            "14050D": self.draw_jail,
            "02023U": "self.startEvent('city_002.json')",
            "18090D": self.draw_directionmarket,
            "18092D": self.draw_directionmarket,
            "21151D": self.draw_cemetery,
            "22151D": self.draw_cemetery,
            "25199U": "self.startEvent('city_003.json')",
            "26199U": "self.startEvent('city_004.json')",
            "25209U": "self.startEvent('city_005.json')",
            "26209U": "self.startEvent('city_006.json')",
            "17172D": self.draw_temple,
            "18172D": self.draw_temple,
            "19172D": self.draw_temple,
            "17182U": "playerParty.restoreCondition()",
            "18182U": "playerParty.restoreCondition()",
            "19182U": "playerParty.restoreCondition()",
            "15149U": "self.startEvent('city_001.json')",
            "11079U": "self.startEvent('city_007.json')",
        }

    @overrides
    def encount_enemy(self):
        '''
        敵とエンカウントした時の処理\n
        街の場合、南側に行くとモンスターも出現する。
        '''
        self.isEncount = True
        if playerParty.y < 12:
            enemyParty.memberList = EnemyPartyGenerator.generate(
                self.enemy_set[random.randint(0, 2)])
        else:
            enemyParty.memberList = EnemyPartyGenerator.generate(
                self.enemy_set[random.randint(0, len(self.enemy_set) - 1)])

    def update_to_cemetery(self):
        '''
        墓地の穴のイベント
        '''
        if pyxel.btn(pyxel.KEY_D):
            if playerParty.x == 25 and playerParty.y == 19:
                playerParty.x = 9
                playerParty.y = 6
            if playerParty.x == 26 and playerParty.y == 19:
                playerParty.x = 10
                playerParty.y = 6
            if playerParty.x == 25 and playerParty.y == 20:
                playerParty.x = 9
                playerParty.y = 7
            if playerParty.x == 26 and playerParty.y == 20:
                playerParty.x = 10
                playerParty.y = 7
            # カウントタイマーを初期化しておく
            self.tick = 0
            # 墓地の地下へ
            self.stateStack.push(State.CEMETERY)

    def update_to_dungeon(self):
        '''
        地下迷宮の入口のイベント
        '''
#        if pyxel.btn(pyxel.KEY_D):
#            playerParty.x = 3
#            playerParty.y = 6
#            # カウントタイマーを初期化しておく
#            self.tick = 0
#            # 地下迷宮へ
#            self.stateStack.push(State.DUNGEONB1)
        pass

    def draw_gate(self):
        '''
        ゲートの表示
        '''
        for _x in range(12, 66, 4):
            pyxel.rect(_x + self.DRAW_OFFSET_X, 12 + self.DRAW_OFFSET_Y,
                       2, 54, pyxel.COLOR_BLACK)
        pyxel.rect(32 + self.DRAW_OFFSET_X, 29 + self.DRAW_OFFSET_Y,
                   18, 9, pyxel.COLOR_YELLOW)
        PyxelUtil.text(33 + self.DRAW_OFFSET_X, 30 + self.DRAW_OFFSET_Y,
                       "*GATE", pyxel.COLOR_BLACK)

    def draw_shieldshop(self):
        '''
        盾屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*SHIELD", pyxel.COLOR_BLACK)

    def draw_armorshop(self):
        '''
        鎧屋の前に立った時の表示
        '''
        PyxelUtil.text(32 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*ARMOR", pyxel.COLOR_BLACK)

    def draw_weaponshop(self):
        '''
        武器屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*WEAPON", pyxel.COLOR_BLACK)

    def draw_helmetshop(self):
        '''
        兜屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*HELMET", pyxel.COLOR_BLACK)

    def draw_barbar(self):
        '''
        床屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*BARBAR", pyxel.COLOR_BLACK)

    def draw_donotenter(self):
        '''
        "DO NOT ENTER!"のメッセージ
        '''
        PyxelUtil.text(162, 112, "*DO NOT ENTER !", pyxel.COLOR_RED)
        pyxel.blt(136, 108, 2, 112, 16, 16, 16, 0)
        pyxel.blt(224, 108, 2, 112, 16, 16, 16, 0)

    def draw_inn(self):
        '''
        宿屋の前に立った時の表示
        '''
        PyxelUtil.text(22 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*UTSURO INN", pyxel.COLOR_BLACK)

    def draw_physicker(self):
        '''
        研究所の前に立った時の表示
        '''
        PyxelUtil.text(24 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*PHYSICKER", pyxel.COLOR_BLACK)

    def draw_physicker_exit(self):
        '''
        研究所の出口の前に立った時の表示
        '''
        PyxelUtil.text(34 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*EXIT", pyxel.COLOR_BLACK)

    def draw_drugs(self):
        '''
        薬屋の前に立った時の表示
        '''
        PyxelUtil.text(32 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*DRUGS", pyxel.COLOR_BLACK)

    def draw_surgery(self):
        '''
        緊急治療の前に立った時の表示
        '''
        PyxelUtil.text(28 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*SURGERY", pyxel.COLOR_BLACK)

    def draw_examinations(self):
        '''
        身体検査の前に立った時の表示
        '''
        PyxelUtil.text(18 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*EXAMINATIONS", pyxel.COLOR_BLACK)

    def draw_thewall(self):
        '''
        謎の壁の表示
        '''
        PyxelUtil.text(177, 112, "*THE WALL", pyxel.COLOR_WHITE)

    def draw_jail(self):
        '''
        牢屋の前に立った時の表示
        '''
        PyxelUtil.text(32 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*JAIL", pyxel.COLOR_BLACK)

    def draw_directionmarket(self):
        '''
        MARKETへの看板の表示
        '''
        if playerParty.direction == Direction.NORTH:
            PyxelUtil.text(166, 112, ["*   MARKET ->"], pyxel.COLOR_WHITE)
        else:
            PyxelUtil.text(166, 112, ["*<- MARKET"], pyxel.COLOR_WHITE)

    def draw_cemetery(self):
        '''
        墓地への看板の表示
        '''
        PyxelUtil.text(16 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*+ CEMETERY +", pyxel.COLOR_BLACK)

    def draw_temple(self):
        '''
        寺院への看板の表示
        '''
        PyxelUtil.text(30 + self.DRAW_OFFSET_X, 22 + self.DRAW_OFFSET_Y,
                       "*TEMPLE", pyxel.COLOR_BLACK)

    def draw_to_dungeon(self):
        '''
        地下迷宮の入口の表示
        '''
#        PyxelUtil.text(16, 140, ["SI", "TA", "NI", " ", "O", "RI", "RU", " ", "KA", "I",
#                                 "TA", "D", "NN", " ", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)
        pass

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()

    @overrides
    def isOuter(self) -> bool:
        '''
        屋外かどうかをboolで返却する

        このクラスは屋外なのでTrueを返却する
        '''
        return True
