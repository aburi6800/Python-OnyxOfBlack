# -*- coding: utf-8 -*-
import random

import pyxel

from ..character import (EnemyPartyGenerator, HumanGenerator, enemyParty,
                         playerParty)
from ..fieldStates.baseFieldState import BaseFieldState
from ..map.uturotown import uturotown
from ..monster import monsterParams
from ..pyxelUtil import PyxelUtil


class StateCity(BaseFieldState):
    '''
    街のクラス

    BaseFieldStateを継承
    遭遇する敵リストと街のイベント処理を持つ
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "City"

        # 変数定義
        self.tick = 0
        self.isEncount = False

        # マップ
        # 0 = 通路
        # 1 = 壁
        # 2 = ドア
        # 3 = ブラックタワー
        # 外周は必ず壁とする
        self.map = uturotown.map

        # イベント
        # マップ上の座標に対応するイベントの関数の辞書
        # 座標は"01013U"のようにX座標とY座標を2桁にした値と方向の値を結合し、"U"(update用)か"D"(draw用)を付与したものとする
        self.event = {
            "17040D": self.draw_gate,
            "18040D": self.draw_gate,
            "17030U": self.update_gate,
            "18030U": self.update_gate,
            "27073D": self.draw_shieldshop,
            "26073U": self.update_shieldshop,
            "27061D": self.draw_armorshop,
            "28061U": self.update_armorshop,
            "27081D": self.draw_weaponshop,
            "28081U": self.update_weaponshop,
            "27101D": self.draw_helmetshop,
            "28101U": self.update_helmetshop,
            "27113D": self.draw_barbar,
            "26113U": self.update_barbar,
            "16083D": self.draw_donotenter,
            "21052D": self.draw_inn,
            "23092D": self.draw_physicker,
            "23100D": self.draw_physicker_exit,
            "23103D": self.draw_drugs,
            "23101D": self.draw_surgery,
            "23111D": self.draw_examinations,
            "17141D": self.draw_thewall,
            "18143D": self.draw_thewall,
            "14050D": self.draw_jail,
            "02023D": self.draw_secretmessage,
            "02023U": self.update_secretmessage,
            "18090D": self.draw_directionmarket,
            "18092D": self.draw_directionmarket,
            "21151D": self.draw_cemetery,
            "22151D": self.draw_cemetery,
            "25199D": self.draw_to_cemetery,
            "26199D": self.draw_to_cemetery,
            "25209D": self.draw_to_cemetery,
            "26209D": self.draw_to_cemetery,
            "25199U": self.update_to_cemetery,
            "26199U": self.update_to_cemetery,
            "25209U": self.update_to_cemetery,
            "26209U": self.update_to_cemetery,
            "17172D": self.draw_temple,
            "18172D": self.draw_temple,
            "19172D": self.draw_temple,
            "17182U": self.update_temple,
            "18182U": self.update_temple,
            "19182U": self.update_temple,
        }

        # 出現するモンスターリスト
        self.enemy_set = (
            HumanGenerator.generate(1),
            HumanGenerator.generate(1),
            HumanGenerator.generate(2),
            monsterParams.monsterList[monsterParams.BAT_LV1],
            monsterParams.monsterList[monsterParams.SKELTON_LV1],
            monsterParams.monsterList[monsterParams.WOLF],
            monsterParams.monsterList[monsterParams.ZOMBIE_LV1],
        )

    def encount_enemy(self):
        '''
        敵とエンカウントした時の処理

        街の場合、南側に行くとモンスターも出現する
        '''
        self.isEncount = True
        if playerParty.y < 12:
            enemyParty.memberList = EnemyPartyGenerator.generate(
                self.enemy_set[random.randint(0, 2)])
        else:
            enemyParty.memberList = EnemyPartyGenerator.generate(
                self.enemy_set[random.randint(0, len(self.enemy_set) - 1)])

    def update(self):
        '''
        各フレームの処理
        '''
        super().update()

    def update_gate(self):
        '''
        ゲートのイベント
        '''
        playerParty.restoreCondition()

    def update_shieldshop(self):
        '''
        盾屋に入るイベント
        '''
        self.stateStack.push(self.stateStack.STATE_SHIELDSHOP)

    def update_armorshop(self):
        '''
        鎧屋に入るイベント
        '''
        self.stateStack.push(self.stateStack.STATE_ARMORSHOP)

    def update_helmetshop(self):
        '''
        兜屋に入るイベント
        '''
        self.stateStack.push(self.stateStack.STATE_HELMETSHOP)

    def update_weaponshop(self):
        '''
        武器屋に入るイベント
        '''
        self.stateStack.push(self.stateStack.STATE_WEAPONSHOP)

    def update_barbar(self):
        '''
        床屋に入るイベント
        '''
        # self.stateStack.push(self.stateStack.STATE_BARBAR)
        pass

    def update_secretmessage(self):
        '''
        隠しメッセージ
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            playerParty.x = 11
            playerParty.y = 8
            playerParty.direction = self.DIRECTION_NORTH

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
            # 墓地の地下へ
            self.stateStack.push(self.stateStack.STATE_CEMETERY)

    def update_temple(self):
        '''
        寺院に入るイベント
        '''
        playerParty.restoreCondition()

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

    def draw_gate(self):
        '''
        ゲートの表示
        '''
        for _x in range(12, 66, 4):
            pyxel.rect(_x + self.OFFSET_X, 12 + self.OFFSET_Y,
                       2, 54, pyxel.COLOR_BLACK)
        pyxel.rect(32 + self.OFFSET_X, 29 + self.OFFSET_Y,
                   18, 9, pyxel.COLOR_YELLOW)
        PyxelUtil.text(33 + self.OFFSET_X, 30 + self.OFFSET_Y,
                       "*GATE", pyxel.COLOR_BLACK)

    def draw_shieldshop(self):
        '''
        盾屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*SHIELD", pyxel.COLOR_BLACK)

    def draw_armorshop(self):
        '''
        鎧屋の前に立った時の表示
        '''
        PyxelUtil.text(32 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*ARMOR", pyxel.COLOR_BLACK)

    def draw_weaponshop(self):
        '''
        武器屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*WEAPON", pyxel.COLOR_BLACK)

    def draw_helmetshop(self):
        '''
        兜屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*HELMET", pyxel.COLOR_BLACK)

    def draw_barbar(self):
        '''
        床屋の前に立った時の表示
        '''
        PyxelUtil.text(30 + self.OFFSET_X, 22 + self.OFFSET_Y,
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
        PyxelUtil.text(22 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*UTSURO INN", pyxel.COLOR_BLACK)

    def draw_physicker(self):
        '''
        研究所の前に立った時の表示
        '''
        PyxelUtil.text(24 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*PHYSICKER", pyxel.COLOR_BLACK)

    def draw_physicker_exit(self):
        '''
        研究所の出口の前に立った時の表示
        '''
        PyxelUtil.text(34 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*EXIT", pyxel.COLOR_BLACK)

    def draw_drugs(self):
        '''
        薬屋の前に立った時の表示
        '''
        PyxelUtil.text(32 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*DRUGS", pyxel.COLOR_BLACK)

    def draw_surgery(self):
        '''
        身体検査の前に立った時の表示
        '''
        PyxelUtil.text(28 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*SURGERY", pyxel.COLOR_BLACK)

    def draw_examinations(self):
        '''
        緊急治療の前に立った時の表示
        '''
        PyxelUtil.text(18 + self.OFFSET_X, 22 + self.OFFSET_Y,
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
        PyxelUtil.text(32 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*JAIL", pyxel.COLOR_BLACK)

    def draw_secretmessage(self):
        '''
        隠しメッセージ
        '''
        PyxelUtil.text(16, 140, ["I", "RO", " ", "I", "LTU", "KA",
                                 "I", " ", "TU", "D", "TU", "*..."], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_directionmarket(self):
        '''
        MARKETへの看板の表示
        '''
        if playerParty.direction == self.DIRECTION_NORTH:
            PyxelUtil.text(166, 112, ["*   MARKET ->"], pyxel.COLOR_WHITE)
        else:
            PyxelUtil.text(166, 112, ["*<- MARKET"], pyxel.COLOR_WHITE)

    def draw_cemetery(self):
        '''
        墓地への看板の表示
        '''
        PyxelUtil.text(16 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*+ CEMETERY +", pyxel.COLOR_BLACK)

    def draw_to_cemetery(self):
        '''
        墓地の穴の表示
        '''
        PyxelUtil.text(16, 140, ["SI", "D", "ME", "NN", "NI", " ", "NU", "KE",
                                 "A", "NA", "KA", "D", " ", "A", "RU", "* !!"], pyxel.COLOR_WHITE)

    def draw_temple(self):
        '''
        寺院への看板の表示
        '''
        PyxelUtil.text(30 + self.OFFSET_X, 22 + self.OFFSET_Y,
                       "*TEMPLE", pyxel.COLOR_BLACK)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        super().onEnter()

        self.tick = 0
        self.isEncount = False

        # プレイヤーパーティーの最初の位置と方向
        playerParty.x = 17
        playerParty.y = 4
        playerParty.direction = self.DIRECTION_SOUTH

    def onExit(self):
        '''
        状態終了時の処理
        '''
        super().onExit()

        pass
