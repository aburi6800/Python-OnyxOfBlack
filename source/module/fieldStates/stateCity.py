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
from overrides import overrides


class StateCity(BaseFieldState):
    '''
    街のクラス\n
    BaseFieldStateを継承。
    '''
    # State名
    stateName = "CITY"

    # マップ
    _map = uturotown.map

    # 屋内にいると判定するための座標リスト
    # このStateクラスのisOuterメソッドで使用する特別な情報
    inner_list = (
        "0306", "0307", "0308", "0309",
        "0408", "0409",
        "0506", "0507", "0508", "0509",
        "0606", "0609",
        "0706", "0709",
        "0806",
        "0911", "0912", "0913",
        "1006", "1007", "1008", "1011", "1012", "1013",
        "1106", "1107", "1108", "1111", "1112", "1113",
        "1306", "1307", "1308",
        "1406", "1407", "1408",
        "1506", "1507", "1508",
        "1606", "1607", "1608",
        "1906", "1907", "1908",
        "2006", "2007", "2008",
        "2106", "2107", "2108",
        "2206", "2207", "2208",
        "2310", "2311",
    )

    # 出現するモンスターリスト
    enemy_set = (
        HumanGenerator.generate(1),
        HumanGenerator.generate(1),
        HumanGenerator.generate(1),
        HumanGenerator.generate(2),
        monsterParams["WOLF_LV1"],
        monsterParams["WOLF_LV1"],
        monsterParams["ZOMBIE_LV1"],
    )

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    @overrides
    def encount_enemy(self):
        '''
        敵とエンカウントした時の処理\n
        街の場合、南側に行くとモンスターも出現する。
        '''
        self.isEncount = True
        if playerParty.y < 16:
            enemyParty.memberList = EnemyPartyGenerator.generate(
                self.enemy_set[random.randint(0, 3)])
        else:
            enemyParty.memberList = EnemyPartyGenerator.generate(
                self.enemy_set[random.randint(0, len(self.enemy_set) - 1)])

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

        プレイヤーパーティーの座標から、屋内にいると判定するための座標リストを検索し、
        ヒットした場合はFalse、ヒットしなかった場合はTrueを返却する。
        '''
        s = f'{playerParty.x:02}{playerParty.y:02}'
        for v in self.inner_list:
            if s == v:
                return False
        return True
