# -*- coding: utf-8 -*-
import random

import pyxel
from module.baseState import BaseState
from module.character import Human, enemyParty, playerParty
from module.messageHandler import message, messageCommand, messagehandler
from module.pyxelUtil import PyxelUtil
from overrides import overrides
from module.state import State


class StateBattle(BaseState):
    '''
    戦闘シーンのクラス/n
    BaseStateクラスを継承
    '''
    # 状態の定数
    STATE_ENCOUNT = 0
    STATE_CHOOSE_ACTION = 1
    STATE_ENEMY_ESCAPE_JUDGE = 2
    STATE_CHOOSE_TARGET = 3
    STATE_START_BATTLE = 4
    STATE_BATTLE = 5
    STATE_WIN_GETEXP = 6
    STATE_WIN_GETGOLD = 7
    STATE_LOSE = 8
    STATE_RUNAWAY_JUDGE = 10
    STATE_RUNAWAY_SUCCESS = 11
    STATE_RUNAWAY_FAILED = 12
    STATE_JUDGE_TALK = 28
    STATE_CHOOSE_TALK = 29
    STATE_TALK = 30

    # ハンドラ用定数
    HANDLER_UPDATE = 0
    HANDLER_RENDER = 1

    # キーとインデックスの辞書
    key_to_index = {
        pyxel.KEY_1: 0,
        pyxel.KEY_2: 1,
        pyxel.KEY_3: 2,
        pyxel.KEY_4: 3,
        pyxel.KEY_5: 4,
    }

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

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
            self.STATE_ENCOUNT: [self.update_encount, self.draw_encount],
            self.STATE_CHOOSE_ACTION: [self.update_choose_action, self.draw_choose_action],
            self.STATE_ENEMY_ESCAPE_JUDGE: [self.update_enemy_escape_judge, self.draw_enemy_escape_judge],
            self.STATE_CHOOSE_TARGET: [self.update_choose_target, self.draw_choose_target],
            self.STATE_START_BATTLE: [self.update_start_battle, self.draw_start_battle],
            self.STATE_BATTLE: [self.update_battle, self.draw_battle],
            self.STATE_WIN_GETEXP: [self.update_win_getexp, self.draw_win_getexp],
            self.STATE_WIN_GETGOLD: [self.update_win_getgold, self.draw_win_getgold],
            self.STATE_LOSE: [self.update_lose, self.draw_lose],
            self.STATE_RUNAWAY_JUDGE: [self.update_runaway_judge, self.draw_runaway_judge],
            self.STATE_RUNAWAY_FAILED: [self.update_runaway_failed, self.draw_runaway_failed],
            self.STATE_RUNAWAY_SUCCESS: [self.update_runaway_success, self.draw_runaway_success],
            self.STATE_JUDGE_TALK: [self.update_judge_talk, self.draw_judge_talk],
            self.STATE_CHOOSE_TALK: [self.update_choose_talk, self.draw_choose_talk],
            self.STATE_TALK: [self.update_talk, self.draw_talk],
        }

        # 状態
        self.state = 0

    def change_state(self, _state):
        '''
        状態変更処理
        '''
        self.state = _state
        self.tick = 0
        self.message = []

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_UPDATE]()

    def update_encount(self):
        '''
        遭遇時の処理
        '''
        if self.tick > 80:
            self.change_state(self.STATE_CHOOSE_ACTION)

    def update_choose_action(self):
        '''
        プレイヤーパーティーの行動決定処理
        '''
        # コマンド入力
        if pyxel.btnp(pyxel.KEY_A):
            self.change_state(self.STATE_ENEMY_ESCAPE_JUDGE)
        if pyxel.btnp(pyxel.KEY_T):
            self.change_state(self.STATE_JUDGE_TALK)
        if pyxel.btnp(pyxel.KEY_R):
            self.change_state(self.STATE_RUNAWAY_JUDGE)

    def update_enemy_escape_judge(self):
        '''
        敵逃走判定処理
        '''
        if self.tick > 30:
            if self.isEnemyEscpaed:
                # 敵が逃げる場合は勝利
                self.change_state(self.STATE_WIN_GETEXP)
            else:
                # 敵が逃げない場合はプレイヤーパーティーの攻撃対象選択処理へ
                self.change_state(self.STATE_CHOOSE_TARGET)

        if self.tick == 1:
            # 敵パーティーは逃げるか？
            if enemyParty.isEscape():
                _playerStrength = 0
                for _member in playerParty.memberList:
                    _playerStrength += _member.strength
                _enemyStrength = 0
                for _member in enemyParty.memberList:
                    _enemyStrength += _member.strength
                if (_playerStrength + random.randint(0, 12)) > (_enemyStrength + random.randint(0, 12)):
                    self.isEnemyEscpaed = True

    def update_choose_target(self):
        '''
        プレイヤーパーティーの攻撃対象選択処理
        '''
        # 敵が1人の時は選択不要
        if len(enemyParty.memberList) == 1:
            playerParty.memberList[self.member_index].target = enemyParty.memberList[0]
            self.member_index += 1
        else:
            _idx = 0

            if pyxel.btnp(pyxel.KEY_1):
                _idx = 1
            elif pyxel.btnp(pyxel.KEY_2) and len(enemyParty.memberList) > 1:
                _idx = 2
            elif pyxel.btnp(pyxel.KEY_3) and len(enemyParty.memberList) > 2:
                _idx = 3
            elif pyxel.btnp(pyxel.KEY_4) and len(enemyParty.memberList) > 3:
                _idx = 4
            elif pyxel.btnp(pyxel.KEY_5) and len(enemyParty.memberList) > 4:
                _idx = 5

            if _idx > 0:
                playerParty.memberList[self.member_index].target = enemyParty.memberList[_idx - 1]
                self.member_index += 1

        # メンバーインデックスがプレイヤーパーティーを超えたら戦闘開始処理へ
        if self.member_index > len(playerParty.memberList) - 1:
            # プレイヤーパーティーのインデックス初期化
            self.member_index = 0
            self.change_state(self.STATE_START_BATTLE)

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

        # イニシアチブ、攻撃値、防御値を設定
        for _member in self.turn_table:
#            if isinstance(_member, Human):
            _member.initiative = _member.dexterity + random.randint(1, 12)
            _member.attack = _member.strength + random.randint(1, 12)
            _member.accept = _member.defend + random.randint(1, 12)

        # イニシアチブ値で降順でソート
        self.turn_table = sorted(
            self.turn_table, key=lambda k: k.initiative, reverse=True)

        # 行動順リストのインデックス初期化
        self.turn_index = 0

        # メッセージ初期化
        self.message = []

        # 戦闘処理へ
        self.change_state(self.STATE_BATTLE)

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
                    self.change_state(self.STATE_LOSE)
                    return

                # 敵パーティーが全滅していたらプレイヤーパーティー勝利処理へ
                if len(enemyParty.memberList) == 0:
                    self.change_state(self.STATE_WIN_GETEXP)
                    return

                # どちらのパーティーも残っていたらプレイヤーパーティー行動決定処理へ
                self.state = self.STATE_CHOOSE_ACTION
                return

        if self.tick == 1:
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
#                m = messageCommand()
#                m.addMessage(message(["*" + _target.name + " ", "KA", "D"]))
#                m.addMessage(message(["*" + _attacker.name + " ", "WO", " ", "YO", "KE", "TA", "."]))
#                messagehandler.enqueue(m)
                self.message.append(["*" + _target.name + " ", "KA", "D"])
                self.message.append(
                    ["*" + _attacker.name + " ", "WO", " ", "YO", "KE", "TA", "."])
            else:
                # ダメージ算出
                _damage = _attacker.attack

                # 人間のキャラクタで武器を持っている場合は補正
                if isinstance(_attacker, Human) and _attacker.weapon != None:
                    _damage = _damage + _attacker.weapon.attack

                # 武器が刃物の場合、ダメージから防御値を減算
                _damage = _damage - _target.accept

                # 人間の場合は装備品の防御値をダメージから減算
                if isinstance(_target, Human):
                    # 鎧
                    if _target.armor != None:
                        _damage = _damage - _target.armor.armor
                    # 盾
                    if _target.shield != None:
                        _damage = _damage - _target.shield.armor
                    # 兜
                    if _target.helmet != None:
                        _damage = _damage - _target.helmet.armor

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

    def update_win_getexp(self):
        '''
        経験値獲得処理
        '''
        _member = playerParty.memberList[self.member_index]
        if self.tick == 1:
            # 経験値加算
            _member.exp = _member.exp + self.reward_exp
            if _member.exp > 100:
                _member.exp = 100

            # 経験値は100か？
            if _member.exp == 100:
                # メッセージをセット
                self.message = []
                self.message.append(["**** CONGRATULATIONS ***"])
                self.message.append(["*" + playerParty.memberList[self.member_index].name + " ", "HA", " ", "re", "he", "d", "ru", "* " + str(
                    playerParty.memberList[self.member_index].level + 1) + " ", "NI", " ", "NA", "RI", "MA", "SI", "TA", "."])

        if _member.exp == 100:
            if pyxel.btnp(pyxel.KEY_SPACE):
                # レベルアップ
                _member.levelup()

                self.tick = 0
                self.member_index += 1

        else:
            self.tick = 0
            self.member_index += 1

        if self.member_index > len(playerParty.memberList) - 1:
            if self.reward_gold == 0:
                self.stateStack.pop()
            else:
                self.change_state(self.STATE_WIN_GETGOLD)

    def update_win_getgold(self):
        '''
        ゴールド獲得処理
        '''
        if self.tick == 1:
            # ゴールドを分配
            self.reward_gold = self.reward_gold // len(playerParty.memberList)
            # 分配した結果、0ゴールドなら戦闘終了
            if self.reward_gold == 0:
                self.stateStack.pop()

        if pyxel.btnp(pyxel.KEY_SPACE):
            # プレイヤーパーティーの各メンバーのゴールドを加算
            for _member in playerParty.memberList:
                _member.gold = _member.gold + self.reward_gold
            # 戦闘終了
            self.stateStack.pop()

    def update_lose(self):
        '''
        プレイヤーパーティー全滅処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.stateStack.clear()
            self.stateStack.push(State.TITLE)

    def update_runaway_judge(self):
        '''
        逃走判定処理
        '''
        _enemyDexterity = 0
        for _member in enemyParty.memberList:
            _enemyDexterity += _member.dexterity
        _enemyDexterity = (_enemyDexterity //
                           len(enemyParty.memberList)) + random.randint(0, 12)
        _playerDexterity = 0
        for _member in playerParty.memberList:
            _playerDexterity += _member.dexterity
        _playerDexterity = (
            _playerDexterity // len(playerParty.memberList)) + random.randint(0, 12)
        if _playerDexterity > _enemyDexterity:
            self.change_state(self.STATE_RUNAWAY_SUCCESS)
        else:
            self.change_state(self.STATE_RUNAWAY_FAILED)

    def update_runaway_success(self):
        '''
        逃走成功処理
        '''
        if self.tick > 30:
            playerParty.isEscape = True
            self.tick = 0
            self.stateStack.pop()
        else:
            self.tick += 1

    def update_runaway_failed(self):
        '''
        逃走失敗処理
        '''
        if self.tick > 30:
            self.change_state(self.STATE_START_BATTLE)
            for _member in playerParty.memberList:
                _member.target = None
        else:
            self.tick += 1

    def update_judge_talk(self):
        '''
        会話判定処理
        '''
        # 敵のパーティーは人間か？
        if isinstance(enemyParty.memberList[0], Human):
            # プレイヤーパーティーの人数 + 敵パーティーの人数 は 5以内か？
            if len(playerParty.memberList) + len(enemyParty.memberList) <= 5:
                # 会話選択へ
                self.change_state(self.STATE_CHOOSE_TALK)
            else:
                # 会話表示へ
                self.change_state(self.STATE_TALK)

        else:
            # 戦闘へ
            self.change_state(self.STATE_START_BATTLE)
            for _member in playerParty.memberList:
                _member.target = None

    def update_choose_talk(self):
        '''
        会話選択処理
        '''
        if pyxel.btnp(pyxel.KEY_J):
            # 敵パーティーをプレイヤーパーティーに加える
            for _member in enemyParty.memberList:
                playerParty.memberList.append(_member)
            # 戦闘終了
            self.stateStack.pop()

        if pyxel.btnp(pyxel.KEY_G):
            # 戦闘終了
            self.stateStack.pop()

        if pyxel.btnp(pyxel.KEY_Y):
            # 戦闘へ
            self.change_state(self.STATE_ENEMY_ESCAPE_JUDGE)

    def update_talk(self):
        '''
        会話表示処理
        '''
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 戦闘終了
            self.stateStack.pop()

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        # 敵の描画
        if self.state != self.STATE_ENCOUNT:
            for _chr in enemyParty.memberList:
                super().drawCharacter(_chr, _chr.x, _chr.y)

            for _idx in range(5 if len(enemyParty.memberList) > 5 else len(enemyParty.memberList)):
                # ステータス
                PyxelUtil.text(136,  (_idx + 1) * 16 - 2,
                               ["*" + enemyParty.memberList[_idx].name], pyxel.COLOR_WHITE)  # 名前
                pyxel.rect(136, (_idx + 1) * 16 + 6,
                           enemyParty.memberList[_idx].maxlife, 3,  pyxel.COLOR_RED)
                pyxel.rect(136, (_idx + 1) * 16 + 6,
                           enemyParty.memberList[_idx].life, 3,  pyxel.COLOR_DARKBLUE)

        _handler = self.handler.get(self.state, None)
        if _handler != None:
            _handler[self.HANDLER_RENDER]()

    def draw_encount(self):
        '''
        遭遇時の表示処理
        '''
        PyxelUtil.text(56, 148, ["NA", "NI", "KA", " ", "TI", "KA",
                                 "TU", "D", "I", "TE", "KI", "TA", "* !"], pyxel.COLOR_RED)

    def draw_choose_action(self):
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

    def draw_enemy_escape_judge(self):
        '''
        敵逃走判定表示処理
        '''
        if self.isEnemyEscpaed:
            PyxelUtil.text(16, 140, [
                           "NI", "KE", "D", "TE", " ", "I", "LTU", "TA", "*..."], pyxel.COLOR_WHITE)
        else:
            PyxelUtil.text(90, 148, ["** * *  BATTLE  * * *"], pyxel.COLOR_RED)

    def draw_choose_target(self):
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

    def draw_start_battle(self):
        '''
        戦闘開始表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_battle(self):
        '''
        戦闘表示処理
        '''
        if self.message != None and len(self.message) == 2:
            PyxelUtil.text(16, 148, self.message[0], pyxel.COLOR_WHITE)
            PyxelUtil.text(16, 164, self.message[1], pyxel.COLOR_WHITE)

    def draw_win_getexp(self):
        '''
        経験値獲得表示処理
        '''
        if self.message != None and len(self.message) == 2:
            PyxelUtil.text(16, 148, self.message[0], pyxel.COLOR_WHITE)
            PyxelUtil.text(16, 164, self.message[1], pyxel.COLOR_WHITE)
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_win_getgold(self):
        '''
        ゴールド獲得表示処理
        '''
        if self.reward_gold > 0:
            PyxelUtil.text(16, 148, ["*" + str(self.reward_gold) + " G.P. ", "TU", "D", "TU",
                                     "NO", " ", "*gold", "WO", " ", "MI", "TU", "KE", "TA", "* !"], pyxel.COLOR_WHITE)
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_lose(self):
        '''
        プレイヤーパーティー全滅表示処理
        '''
        PyxelUtil.text(70, 156, ["*+ + ", "SE", "D", "NN", "ME", "TU",
                                 " ", "SI", "MA", "SI", "TA", "* + +"], pyxel.COLOR_RED)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def draw_runaway_judge(self):
        '''
        逃走成功表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_runaway_success(self):
        '''
        逃走成功表示処理
        '''
        PyxelUtil.text(46, 148, ["I", "TU", "MO", " ", "U", "MA", "KU", "I", "KU", "TO", "HA",
                                 " ", "KA", "KI", "D", "RI", "MA", "SE", "NN", "YO", "*..."], pyxel.COLOR_WHITE)

    def draw_runaway_failed(self):
        '''
        逃走失敗表示処理
        '''
        PyxelUtil.text(56, 148, ["SI", "MA", "LTU", "TA", "* ! ", "NI",
                                 "KE", "D", "RA", "RE", "NA", "I", "* !"], pyxel.COLOR_RED)

    def draw_judge_talk(self):
        '''
        会話判定表示処理\n
        ※実際はここで表示をするものはない
        '''
        pass

    def draw_choose_talk(self):
        '''
        会話選択表示処理
        '''
        PyxelUtil.text(16, 140, ["NA", "NI", "WO", " ", "HA", "NA",
                                 "SI", "KA", "KE", "MA", "SU", "KA", "* ?"], pyxel.COLOR_WHITE)
        PyxelUtil.text(32, 156, ["*[J] JOIN US."], pyxel.COLOR_YELLOW)
        PyxelUtil.text(
            32, 164, ["*[G] GOOD LUCK & GOOD BY."], pyxel.COLOR_YELLOW)
        PyxelUtil.text(
            32, 172, ["*[Y] YOUR MONEY OR YOUR LIFE."], pyxel.COLOR_YELLOW)

    def draw_talk(self):
        '''
        会話表示処理
        '''
        PyxelUtil.text(16, 148, ["*ONYX", "WO", " ", "ME", "SA", "D", "SI", "TE", " ", "KA",
                                 "D", "NN", "HA", "D", "RI", "MA", "SI", "LYO", "U", "* !"], pyxel.COLOR_WHITE)
        PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # 状態を最初に設定する
        self.state = self.STATE_CHOOSE_ACTION

        # 報酬を初期化
        self.reward_exp = 0
        self.reward_gold = 0

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
