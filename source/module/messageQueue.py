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
        self.isComplete = True


class messageCommand(baseCommand):
    '''
    メッセージコマンドクラス
    '''
    def __init__(self):
        super().__init__()

        self.messageList = []
        self.idx = 0

        # ステータス
        # 0:メッセージ表示状態
        # 1:キー入力待ち状態
        self.status = 0

        # メッセージ表示行
        self.messageRow = 0

        # メッセージ表示桁
        self.messageCol = 0

    def addMessage(self, message:message):
        self.messageList.append(message)

    def update(self):
        super().update()

        # キー入力待ち状態の時に[SPACE]キーを押されたらidxを判定。
        # messageListの要素数を超えていない場合は、メッセージ表示状態する。
        # messageListの要素数を超えたらcompleteする。
        # キー入力待ち状態以外の時は、何もしない
        if self.status == 1:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.idx += 5
                if self.idx < len(self.messageList) - 1:
                    self.status = 0
                    self.messageRow = 0
                    self.messageCol = 0
                else:
                    self.complete()

    def draw(self):
        super().draw()

        # メッセージ表示状態の場合は、以下を処理する。
        #   idx～idx+4までを画面に表示し、キー入力待ち状態にする
        if self.status == 0:

            # 次のカラムへ
            self.messageCol += 1

            # カラム数がその行の文字数を超えたら、カラムを戻して次の行へ
            if self.messageCol > len(self.messageList[self.messageRow].message):
                self.messageCol = 1
                self.messageRow += 1

            # 現在行が0行目以外の時は、表示済の行を描画する
            if self.messageRow > 0:
                for _messageRow in range(0, self.messageRow):
                    _tempIdx = self.idx + _messageRow
                    PyxelUtil.text(16, 140 + (_messageRow * 8), self.messageList[_tempIdx].message, self.messageList[_tempIdx].color)

            _tempIdx = self.idx + self.messageRow
            if self.messageRow < 5 and _tempIdx < len(self.messageList):
                # 現在行は１文字ずつ送り表示する
                PyxelUtil.text(16, 140 + (self.messageRow * 8), self.messageList[_tempIdx].message[:self.messageCol], self.messageList[_tempIdx].color)

            else:
                # キー入力待ち状態にする
                self.status = 1

        # キー入力待ち状態の時は、キー入力待ちメッセージを表示する
        if self.status == 1:
            for _messageRow in range(0, 4):
                _tempIdx = self.idx + _messageRow
                if _tempIdx < len(self.messageList): 
                    PyxelUtil.text(16, 140 + (_messageRow * 8), self.messageList[_tempIdx].message, self.messageList[_tempIdx].color)
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)


class chooseCommand():
    '''
    選択クラス
    '''
    