# -*- coding: utf-8 -*-
import sys

import pyxel

from module.character import (EnemyPartyGenerator, HumanGenerator, enemyParty,
                              playerParty)
from module.params.armor import armorParams
from module.params.helmet import helmetParams
from module.params.monster import monsterParams
from module.params.shield import shieldParams
from module.params.weapon import weaponParams
from module.state import State
from module.stateStack import stateStack


class App:
    '''
    戦闘のテストドライバー
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        # コマンドライン引数取得
        args = sys.argv
        print(len(args))
        print(args)
        if len(args) != 7:
            args = ["", "BAT_LV1", "1", "", "", "", ""]

        # StateStackの初期化
        stateStack.clear()

        # Pyxel初期化
        pyxel.init(256, 192)
        pyxel.load("../source/assets/onyxofblack.pyxres")

        # プレイヤーパーティ生成
        playerParty.initialize()

        level = int(args[2])

        for idx in range(5):
            member = HumanGenerator.generate(level)
            # 装備の指定
            member.weapon = weaponParams[int(args[3])] if args[3] != "" else None
            member.armor = armorParams[int(args[4])] if args[4] != "" else None
            member.shield = shieldParams[int(args[5])] if args[5] != "" else None
            member.helmet = helmetParams[int(args[6])] if args[6] != "" else None

            _log = member.name
            _log += " level=" + str(member.level)
            _log += " life=" + str(member.life)
            _log += " str=" + str(member.strength)
            _log += "+" + str(member.weapon.attack if member.weapon != None else 0)
            _log += " def=" + str(member.defend)
            _log += "+" + str(member.armor.armor if member.armor != None else 0)
            _log += "+" + str(member.shield.armor if member.shield != None else 0)
            _log += "+" + str(member.helmet.armor if member.helmet != None else 0)
            _log += " dex=" + str(member.dexterity)
            _log += " weapon=" 
            _log += member.weapon.name if member.weapon != None else "None"
            _log += " armor=" 
            _log += member.armor.name if member.armor != None else "None"
            _log += " shield=" 
            _log += member.shield.name if member.shield != None else "None"
            _log += " helm=" 
            _log += member.helmet.name if member.helmet != None else "None"
            print(_log)
            playerParty.addMember(member)

        # 敵パーティー生成
        enemyParty.memberList = EnemyPartyGenerator.generate(monsterParams[args[1]])
        for value in enemyParty.memberList:
            print(value)

        # BattleStateをstateStackに登録
        stateStack.push(State.BATTLE)

        pyxel.run(self.update, self.draw)

    def update(self):
        '''
        各フレームの処理
        '''
        stateStack.update()

    def draw(self):
        '''
        各フレームの画面描画処理
        '''
        pyxel.cls(pyxel.COLOR_BLACK)
        stateStack.draw()


if __name__ == "__main__":
    '''
    アプリケーション実行
    '''
    App()
