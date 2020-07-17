# -*- coding: utf-8 -*-
import random
import pyxel
from ..pyxelUtil import PyxelUtil
from ..baseState import BaseState
from ..character import playerParty
from ..character import enemyParty
from ..character import Human
from ..character import Monster


class StateBattle(BaseState):
    '''
    戦闘シーンのクラス

    BaseStateクラスを継承
    '''
    # 状態の定数
    STATE_ENCOUNT = 0
    STATE_CHOOSE_ACTION = 1
    STATE_START_BATTLE = 2
    STATE_CHOOSE_TARGET = 3
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

        # メンバーのインデックス
        self.member_index = 0

        # メッセージリスト
        self.message = []

        # ハンドラ辞書
        self.handler = {
            self.STATE_ENCOUNT: [self.update_encount, self.render_encount],
            self.STATE_CHOOSE_ACTION: [self.update_choose_action, self.render_choose_action],
            self.STATE_START_BATTLE: [self.update_start_battle, self.render_start_battle],
            self.STATE_CHOOSE_TARGET: [self.update_choose_target, self.render_choose_target],
            self.STATE_BATTLE: [self.update_battle, self.render_battle],
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
        self.tick += 1
        if self.tick > 60:
            self.tick = 0
            self.state = self.STATE_CHOOSE_ACTION

    def update_choose_action(self):
        '''
        プレイヤーパーティーの行動決定処理
        '''
        if pyxel.btnp(pyxel.KEY_A):
            self.state = self.STATE_START_BATTLE
        if pyxel.btnp(pyxel.KEY_T):
            self.state = self.STATE_CHOOSE_TALK
        if pyxel.btnp(pyxel.KEY_R):
            self.state = self.STATE_RUNAWAY_JUDGE

    def update_start_battle(self):
        '''
        戦闘開始処理
        '''
        self.tick += 1
        if self.tick > 30:
            self.tick = 0

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

            # 行動順リストのインデックス
            self.turn_index = 0

            # プレイヤーパーティーのインデックス
            self.member_index = 0

            # プレイヤーパーティーの攻撃対象選択へ
            self.state = self.STATE_CHOOSE_TARGET

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

        # メンバーインデックスがプレイヤーパーティーを超えたら敵の行動選択処理へ
        if self.member_index > len(playerParty.memberList) - 1:
            self.message = None
            self.state = self.STATE_BATTLE

    def update_battle(self):
        '''
        戦闘処理
        '''
        if self.tick > 30:
            self.turn_index += 1
            self.tick = 0
            if self.turn_index > len(self.turn_table) - 1:
                self.state = self.STATE_CHOOSE_ACTION
                return

        if self.tick > 0:
            None

        if self.tick == 0:
            # 攻撃するキャラクター
            _attacker = self.turn_table[self.turn_index]

            # 攻撃の対象キャラクター
            _target = _attacker.target

            # 攻撃対象が生きていなければ抜ける
            if _target.life < 1:
                self.tick = 30
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

                        # メンバーリストから外す
                        for _idx, _value in enumerate(self.turn_table):
                            if _value is _target:
                                del self.turn_table[_idx]
                                break

                        for _idx, _value in enumerate(playerParty.memberList):
                            if _value is _target:
                                del playerParty.memberList[_idx]
                                break

                        for _idx, _value in enumerate(enemyParty.memberList):
                            if _value is _target:
                                del enemyParty.memberList[_idx]
                                break

                    else:
                        # ダメージをあたえた
                        self.message.append(
                            ["*" + _attacker.name + " ", "KA", "D", "* " + _target.name + " ", "NI"])
                        self.message.append(["*" + str(_damage) + " ", "NO", " ", "ta", "d",
                                             "me", "-", "si", "d", "WO", " ", "A", "TA", "E", "TA", "* !"])

        self.tick += 1

    def update_runaway_judge(self):
        '''
        逃走判定処理
        '''
        pass

    def update_runaway_success(self):
        '''
        逃走成功処理
        '''
        pass

    def update_runaway_failed(self):
        '''
        逃走失敗処理
        '''
        pass

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

    def render_start_battle(self):
        '''
        戦闘開始表示処理
        '''
        PyxelUtil.text(56, 148, ["**** BATTLE ***"], pyxel.COLOR_RED)

    def render_choose_target(self):
        '''
        プレイヤーパーティーの攻撃対象選択表示処理
        '''
        PyxelUtil.text(16, 140, ["TO", "D", "RE", "WO", " ", "KO", "U", "KE", "D", "KI", " ", "SI", "MA",
                                 "SU", "KA", ",", "*" + playerParty.memberList[self.member_index].name, "* ?"], pyxel.COLOR_WHITE)
        for _idx in range(5 if len(enemyParty.memberList) > 5 else len(enemyParty.memberList)):
            PyxelUtil.text(24, 148 + _idx * 8,
                           "*[{:1}]".format(_idx + 1), pyxel.COLOR_YELLOW)
            PyxelUtil.text(40, 148 + _idx * 8, "*" +
                           enemyParty.memberList[_idx].name, pyxel.COLOR_LIGHTBLUE)

    def render_battle(self):
        '''
        戦闘表示処理
        '''
        if self.message != None:
            PyxelUtil.text(16, 148, self.message[0], pyxel.COLOR_WHITE)
            PyxelUtil.text(16, 164, self.message[1], pyxel.COLOR_WHITE)

    def render_runaway_judge(self):
        '''
        逃走成功表示処理
        ※実際はここで表示をするものはない
        '''
        pass

    def render_runaway_success(self):
        '''
        逃走成功表示処理
        '''
        PyxelUtil.text(56, 148, ["I", "TU", "MO", " ", "U", "MA", "KU", "I", "KU", "TO", "HA",
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
        pass

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 状態を最初に設定する
        self.state = self.STATE_ENCOUNT

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
