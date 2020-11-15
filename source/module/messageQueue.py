# -*- coding: utf-8 -*-
from collections import deque

import pyxel

from module.pyxelUtil import PyxelUtil


class messageQueue():
    '''
    メッセージキュークラス

    登録された各コマンドクラスのupdate、drawメソッドを実行する
    コマンドキューへの登録は各コマンドクラスが自ら行う
    '''
    commands = deque([])

    def __init__(self):
        pass

    def isEnqueued(self):
        return True if len(self.commands) > 0 else False

    def enqueue(self, _command):
        self.commands.append(_command)

    def deque(self):
        self.commands.popleft()

    def update(self):
        if len(self.commands) > 0:
            command = self.commands[0]
            if command.isComplete:
                self.deque()
            else:
                self.commands[0].update()

    def draw(self):
        if len(self.commands) > 0:
            self.commands[0].draw()


messagequeue = messageQueue()


class message():
    '''
    メッセージクラス
    '''
    def __init__(self, message, color:int = 7):
        self.message = message
        self.color = color


class baseCommand():
    '''
    コマンド基底クラス
    '''
    def __init__(self):
        self.isComplete = False

    def isComplete(self):
        return self.isCOmplete

    def update(self):
        pass

    def draw(self):
        pass

    def complete(self):
        self.isCOmplete = True


class messageCommand(baseCommand):
    '''
    メッセージコマンドクラス
    '''
    def __init__(self):
        super().__init__()

        self.messageList = []
        self.idx = 0
        self.status = 0
        # ステータス
        # 0:メッセージ表示状態
        # 1:キー入力待ち状態

    def addMessage(self, message:message):
        self.messageList.append(message)

    def update(self):
        super().update()

        # キー入力待ち状態の時に[SPACE]キーを押されたらidxを判定。
        # messageListの要素数を超えていない場合は、メッセージ表示状態する。
        # messageListの要素数を超えたらcompleteする。
        # キー入力待ち状態以外の時は、何もしない
        if self.status == 0:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.idx += 5
                if self.idx < len(self.messageList):
                    self.status = 0
                else:
                    self.complete()

    def draw(self):
        super().draw()

        # メッセージ表示状態の場合は、以下を処理する。
        #   idx～idx+4までを画面に表示し、キー入力待ち状態にする
        # キー入力待ち状態の時は、キー入力待ちメッセージを表示する
        if self.status == 0:
            for _idx in range(self.idx, self.idx + 4):
                if _idx < len(self.messageList):
                    PyxelUtil.text(16, 140 + (_idx * 8), self.messageList[_idx].message, self.messageList[_idx].color)
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)


class chooseCommand():
    '''
    選択クラス
    '''
    