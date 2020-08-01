# -*- coding: utf-8 -*-
import random

import pyxel

from ..baseState import BaseState
from ..character import Human, Monster, enemyParty, playerParty
from ..pyxelUtil import PyxelUtil


class StateBattle(BaseState):
    '''
    戦闘シーンのクラス

    BaseStateクラスを継承
    '''
    # 状態の定数
    STATE_ENCOUNT = 0
    STATE_CHOOSE_ACTION = 1
    STATE_ENEMY_ESCAPE_JUDGE = 2
    STATE_CHOOSE_TARGET = 3
    STATE_START_BATTLE = 4
    STATE_BATTLE = 5
    STATE_WIN = 6
    STATE_LOSE = 7
    STATE_RUNAWAY_JUDGE = 10
    STATE_RUNAWAY_SUCCESS = 11
    STATE_RUNAWAY_FAILED = 12
    STATE_CHOOSE_TALK = 29

    # ハンドラ用定数
    HANDLER_UPDATE = 0
    HANDLER_RENDER = 1

    # このクラスの状態
    state = STATE_ENCOUNT

    # キーとインデックスの辞書
    key_to_index = {
        pyxel.KEY_1: 0,
        pyxel.KEY_2: 1,
        pyxel.KEY_3: 2,
        pyxel.KEY_4: 3,
        pyxel.KEY_5: 4,
    }

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "Battle"

        # 行動順リスト
        self.turn_table = []

        # 行動順リストのインデックス
        self.turn_index = 0

        # 時間カウント用
        self.tick = 0

        # 逃走に成功したか？
        self.isRunaway = False

        # 敵は逃走したか？
        self.isEnemyEscpaed = False

        # メンバーのインデックス
        self.member_index = 0

        # メッセージリスト
        self.message = []
        self.memsage_color = pyxel.COLOR_WHITE

        # 報酬
        self.reward_exp = 0
        self.reward_gold = 0

        # ハンドラ辞書
        self.handler = {
            self.STATE_ENCOUNT: [self.update_encount, self.render_encount],
            self.STATE_CHOOSE_ACTION: [self.update_choose_action, self.render_choose_action],
            self.STATE_ENEMY_ESCAPE_JUDGE: [self.update_enemy_escape_judge, self.render_enemy_escape_judge],
            self.STATE_CHOOSE_TARGET: [self.update_choose_target, self.render_choose_target],
            self.STATE_START_BATTLE: [self.update_start_battle, self.render_start_battle],
            self.STATE_BATTLE: [self.update_battle, self.render_battle],
            self.STATE_WIN: [self.update_win, self.render_win],
            self.STATE_LOSE: [self.update_lose, self.render_lose],
            self.STATE_RUNAWAY_JUDGE: [self.update_runaway_judge, self.render_runaway_judge],
            self.STATE_RUNAWAY_FAILED: [self.update_runaway_failed, self.render_runaway_failed],
            self.STATE_RUNAWAY_SUCCESS: [self.update_runaway_success, self.render_runaway_success],
            self.STATE_CHOOSE_TALK: [self.update_choose_talk, self.render_choose_talk],
        }

    def update(self):
        '''
        各フレームの処理
        '''
        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_UPDATE]()

    def update_encount(self):
        '''
        遭遇時の処理
        '''
        if self.tick > 60:
            self.tick = 0
            self.state = self.STATE_CHOOSE_ACTION

        self.tick += 1

    def update_choose_action(self):
        '''
        プレイヤーパーティーの行動決定処理
        '''
        # コマンド入力
        if pyxel.btnp(pyxel.KEY_A):
            self.state = self.STATE_ENEMY_ESCAPE_JUDGE
        if pyxel.btnp(pyxel.KEY_T):
            self.state = self.STATE_CHOOSE_TALK
        if pyxel.btnp(pyxel.KEY_R):
            self.state = self.STATE_RUNAWAY_JUDGE

    def update_enemy_escape_judge(self):
        '''
        敵逃走判定処理
        '''
        if self.tick > 30:
            self.tick = 0
            if self.isEnemyEscpaed:
                # 敵が逃げる場合は勝利
                self.state = self.STATE_WIN
            else:
                # 敵が逃げない場合はプレイヤーパーティーの攻撃対象選択処理へ
                self.state = self.STATE_CHOOSE_TARGET

        if  self.tick == 0:
            # 敵パーティーは# 逃げるか？
            if enemyParty.isEscape():
                _playerStrength = 0
                for _member in playerParty.memberList:
                    _playerStrength = _playerStrength + _member.strength
                _enemyStrength = 0
                for _member in enemyParty.memberList:
                    _enemyStrength = _enemyStrength + _member.strength
                if (_playerStrength + random.randint(0, 10)) > (_enemyStrength + random.randint(0, 10)):
                    self.isEnemyEscpaed = True

        self.tick += 1

    def update_choose_target(self):
        '''
        プレイヤーパーティーの攻撃対象選択処理
        '''
        # 敵が1人の時は選択不要
        if len(enemyParty.memberList) == 1:
            playerParty.memberList[self.member_index].target = enemyParty.memberList[0]
            self.member_index += 1
        else:
            if pyxel.btnp(pyxel.KEY_1):
                playerParty.memberList[self.member_index].target = enemyParty.memberList[0]
                self.member_index += 1
            elif pyxel.btnp(pyxel.KEY_2):
                playerParty.memberList[self.member_index].target = enemyParty.memberList[1]
                self.member_index += 1
            elif pyxel.btnp(pyxel.KEY_3):
                playerParty.memberList[self.member_index].target = enemyParty.memberList[2]
                self.member_index += 1
            elif pyxel.btnp(pyxel.KEY_4):
                playerParty.memberList[self.member_index].target = enemyParty.memberList[3]
                self.member_index += 1
            elif pyxel.btnp(pyxel.KEY_5):
                playerParty.memberList[self.member_index].target = enemyParty.memberList[4]
                self.member_index += 1

        # メンバーインデックスがプレイヤーパーティーを超えたら戦闘開始処理へ
        if self.member_index > len(playerParty.memberList) - 1:
            self.message = None
            self.state = self.STATE_START_BATTLE

    def update_start_battle(self):
        '''
        戦闘開始処理
        '''
        # 敵の全てに対して、ランダムに攻撃対象を決定
        for _member in enemyParty.memberList:
            _member.target = playerParty.memberList[random.randint(
                0, len(playerParty.memberList) - 1)]

        # 行動順リスト
        self.turn_table = playerParty.memberList + enemyParty.memberList

        # イニシアチブを設定
        for _member in self.turn_table:
            _member.initiative = _member.dexterity + random.randint(0, 6)
            _member.attack = _member.strength + random.randint(0, 6)
            _member.accept = _member.defend + random.randint(0, 6)

        # イニシアチブ値で降順でソート
        self.turn_table = sorted(
            self.turn_table, key=lambda k: k.initiative, reverse=True)

        # 行動順リストのインデックス初期化
        self.turn_index = 0

        # プレイヤーパーティーのインデックス初期化
        self.member_index = 0

        # 戦闘処理へ
        self.state = self.STATE_BATTLE

    def update_battle(self):
        '''
        戦闘処理
        '''
        if self.tick > 30:
            self.tick = 0
            # 次の行動順リストへ
            self.turn_index += 1

            if self.turn_index > len(self.turn_table) - 1:
                # プレイヤーパーティーが全滅していたらプレイヤーパーティー全滅処理へ
                if len(playerParty.memberList) == 0:
                    self.state = self.STATE_LOSE
                    return

                # 敵パーティーが全滅していたらプレイヤーパーティー勝利処理へ
                if len(enemyParty.memberList) == 0:
                    self.state = self.STATE_WIN
                    return
                
                # どちらのパーティーも残っていたらプレイヤーパーティー行動決定処理へ
                self.state = self.STATE_CHOOSE_ACTION
                return

        if self.tick == 0:
            # 攻撃するキャラクター
            _attacker = self.turn_table[self.turn_index]

            # 攻撃の対象キャラクター
            _target = _attacker.target

            # 攻撃対象が生きていなければ抜ける
            if _target == None or _target.life < 1:
                self.tick = 31
                return

            # メッセージ初期化
            self.message = []

            # 攻撃ヒット判定
            if _attacker.attack < _target.dexterity:
                # 避けた
                self.message.append(["*" + _target.name + " ", "KA", "D"])
                self.message.append(
                    ["*" + _attacker.name + " ", "WO", " ", "YO", "KE", "TA", "."])
            else:
                # ダメージ算出
                _damage = _attacker.attack

                if isinstance(_attacker, Human):
                    _damage = _damage + _attacker.weapon.attack
                _damage = _damage - _target.accept

                if isinstance(_target, Human):
                    if _target.armor != None:
                        _damage = _damage - _target.armor.armor
                    if _target.shield != None:
                        _damage = _damage - _target.shiled.armor
                    if _target.helmet != None:
                        _damage = _damage - _target.shiled.helmet

                if _damage < 1:
                    # 受け止めた
                    self.message.append(["*" + _target.name + " ", "KA", "D"])
                    self.message.append(
                        ["*" + _attacker.name + " ", "WO", " ", "U", "KE", "TO", "ME", "TA", "."])
                else:

                    _target.life = _target.life - _damage
                    if _target.life < 1:
                        # しとめた
                        self.message.append(
                            ["*" + _attacker.name + " ", "KA", "D"])
                        self.message.append(
                            ["*" + _target.name + " ", "WO", " ", "SI", "TO", "ME", "TA", "* !"])

                        #  行動順リストから外す
                        for _idx, _value in enumerate(self.turn_table):
                            if _value is _target:
                                del self.turn_table[_idx]
                                break

                        # プレイヤーパーティーから外す
                        for _idx, _value in enumerate(playerParty.memberList):
                            if _value is _target:
                                del playerParty.memberList[_idx]
                                break

                        # 敵パーティーから外す
                        for _idx, _value in enumerate(enemyParty.memberList):
                            if _value is _target:
                                self.reward_exp = self.reward_exp + _target.exp
                                self.reward_gold = self.reward_gold + _target.gold
                                print("reward=" + str(self.reward_exp) +
                                      "exp. " + str(self.reward_gold) + "gold.")
                                del enemyParty.memberList[_idx]
                                break

                    else:
                        # ダメージをあたえた
                        self.message.append(
                            ["*" + _attacker.name + " ", "KA", "D", "* " + _target.name + " ", "NI"])
                        self.message.append(["*" + str(_damage) + " ", "NO", " ", "ta", "d",
                                             "me", "-", "si", "d", "WO", " ", "A", "TA", "E", "TA", "* !"])

        self.tick += 1

    def update_win(self):
        '''
        プレイヤーパーティー勝利処理
        '''
        if self.reward_gold > 0:
            if pyxel.btn(pyxel.KEY_SPACE):
                for _member in playerParty.memberList:
                    _member.exp = _member.exp + self.reward_exp
                    _member.gold = _member.gold + self.reward_gold
                self.stateStack.pop()            
        else:
            for _member in playerParty.memberList:
                _member.exp = _member.exp + self.reward_exp
            self.stateStack.pop()            

    def update_lose(self):
        '''
        プレイヤーパーティー全滅処理
        '''
        if pyxel.btn(pyxel.KEY_SPACE):
            self.stateStack.init(self.stateStack.STATE_TITLE)

    def update_runaway_judge(self):
        '''
        逃走判定処理
        '''
        _enemyDexterity = 0
        for _member in enemyParty.memberList:
            _enemyDexterity = _enemyDexterity + _member.dexterity
        _playerDexterity = 0
        for _member in playerParty.memberList:
            _playerDexterity = _playerDexterity + _member.dexterity
        if (random.randint(0, 100) + _playerDexterity) - (random.randint(0, 100) + _enemyDexterity) > 0:
            self.state = self.STATE_RUNAWAY_SUCCESS
        else:
            self.state = self.STATE_RUNAWAY_FAILED

    def update_runaway_success(self):
        '''
        逃走成功処理
        '''
        if self.tick > 30:
            self.tick = 0
            self.stateStack.pop()

        self.tick += 1

    def update_runaway_failed(self):
        '''
        逃走失敗処理
        '''
        if self.tick > 30:
            self.tick = 0
            self.state = self.STATE_START_BATTLE
            for _member in playerParty.memberList:
                _member.target = None 
        self.tick += 1

    def update_choose_talk(self):
        '''
        会話選択処理
        '''
        pass

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

        # 敵の描画
        if self.state != self.STATE_ENCOUNT:
            for _chr in enemyParty.memberList:
                super().drawCharacter(_chr, _chr.x, _chr.y)

            for _idx in range(5 if len(enemyParty.memberList) > 5 else len(enemyParty.memberList)):
                # ステータス
                PyxelUtil.text(136,  (_idx + 1) * 16 - 2,
                               ["*" + enemyParty.memberList[_idx].name], pyxel.COLOR_WHITE)  # 名前
                pyxel.rect(136, (_idx + 1) * 16 + 6,
                           enemyParty.memberList[_idx].life, 3,  5)

        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_RENDER]()

    def render_encount(self):
        '''
        遭遇時の表示処理
        '''
        PyxelUtil.text(56, 148, ["NA", "NI", "KA", " ", "TI", "KA",
                                 "TU", "D", "I", "TE", "KI", "TA", "* !"], pyxel.COLOR_RED)

    def render_choose_action(self):
        '''
        プレイヤーパーティーの行動決定表示処理
        '''
        PyxelUtil.text(16, 140, ["TO", "D", "U", "SI",
                                 "MA", "SU", "KA", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(32, 156, ["*[A] ", "TA", "TA",
                                 "KA", "U"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(32, 164, ["*[R] ", "NI", "KE",
                                 "D", "RU"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(32, 172, ["*[T] ", "HA", "NA",
                                 "SU"], pyxel.COLOR_YELLOW)

    def render_enemy_escape_judge(self):
        '''
        敵逃走判定表示処理
        '''
        if self.isEnemyEscpaed:
            PyxelUtil.text(16, 140, ["NI", "KE", "D", "TE", " ", "I", "LTU", "TA", "*..."], pyxel.COLOR_WHITE)
        else:
            PyxelUtil.text(90, 148, ["** * *  BATTLE  * * *"], pyxel.COLOR_RED)

    def render_choose_target(self):
        '''
        プレイヤーパーティーの攻撃対象選択表示処理
        '''
        if len(enemyParty.memberList) == 1:
            return

        PyxelUtil.text(16, 140, ["TO", "D", "RE", "WO", " ", "KO", "U", "KE", "D", "KI", " ", "SI", "MA",
                                 "SU", "KA", ",", "*" + playerParty.memberList[self.member_index].name, "* ?"], pyxel.COLOR_WHITE)
        for _idx in range(5 if len(enemyParty.memberList) > 5 else len(enemyParty.memberList)):
            PyxelUtil.text(24, 148 + _idx * 8,
                           "*[{:1}]".format(_idx + 1), pyxel.COLOR_YELLOW)
            PyxelUtil.text(40, 148 + _idx * 8, "*" +
                           enemyParty.memberList[_idx].name, pyxel.COLOR_LIGHTBLUE)

    def render_start_battle(self):
        '''
        戦闘開始表示処理
        ※実際はここで表示をするものはない
        '''

    def render_battle(self):
        '''
        戦闘表示処理
        '''
        if self.message != None and len(self.message) == 2:
            PyxelUtil.text(16, 148, self.message[0], pyxel.COLOR_WHITE)
            PyxelUtil.text(16, 164, self.message[1], pyxel.COLOR_WHITE)

    def render_win(self):
        '''
        プレイヤーパーティー勝利表示処理
        '''
        if self.reward_gold > 0:
            PyxelUtil.text(16, 148, ["*" + str(self.reward_gold) + " G.P. ", "TU", "D", "TU", "NO", " ", "*gold", "WO", " ", "MI", "TU", "KE", "TA", "* !"], pyxel.COLOR_WHITE)
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def render_lose(self):
        '''
        プレイヤーパーティー全滅表示処理
        '''
        PyxelUtil.text(70, 156, ["*+ + ", "SE", "D", "NN", "ME", "TU", " ", "SI", "MA", "SI", "TA", "* + +"], pyxel.COLOR_RED)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def render_runaway_judge(self):
        '''
        逃走成功表示処理
        ※実際はここで表示をするものはない
        '''

    def render_runaway_success(self):
        '''
        逃走成功表示処理
        '''
        PyxelUtil.text(46, 148, ["I", "TU", "MO", " ", "U", "MA", "KU", "I", "KU", "TO", "HA",
                                 " ", "KA", "KI", "D", "RI", "MA", "SE", "NN", "YO", "*..."], pyxel.COLOR_WHITE)

    def render_runaway_failed(self):
        '''
        逃走失敗表示処理
        '''
        PyxelUtil.text(56, 148, ["SI", "MA", "LTU", "TA", "* ! ", "NI",
                                 "KE", "D", "RA", "RE", "NA", "I", "* !"], pyxel.COLOR_RED)

    def render_choose_talk(self):
        '''
        会話選択表示処理
        '''
        PyxelUtil.text(32, 156, ["*[J] ", "NA", "KA",
                                 "MA", "NI", " ", "SA", "SO", "U"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(32, 164, ["*[G] ", "WA", "KA",
                                 "RE", "RU"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(32, 172, ["*[T] ", "ka", "ne",
                                 "WO", " ", "TA", "D", "SE"], pyxel.COLOR_YELLOW)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 状態を最初に設定する
        self.state = self.STATE_CHOOSE_ACTION

        # 報酬を初期化
        self.reward_exp = 0
        self.reward_gold = 0

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
