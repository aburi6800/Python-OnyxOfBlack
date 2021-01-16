# -*- coding: utf-8 -*-
from collections import deque

import pyxel

from module.pyxelUtil import PyxelUtil


class messageQueue():
    '''
    メッセージキュークラス\n
    登録された各コマンドクラスのupdate、drawメソッドを実行する。\n
    コマンドキューへの登録は各コマンドクラスが自ら行う。
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
    def __init__(self, message, color:int = pyxel.COLOR_WHITE):
        self.message = message
        self.color = color


class choose(message):
    '''
    選択肢クラス
    '''
    def __init__(self, message, color:int = pyxel.COLOR_YELLOW, key:int = pyxel.KEY_NONE, value:int = 0):
        super().__init__(message, color)
        self.key = key


class chooseValue():
    '''
    選択結果保存クラス
    '''
    value = None


choosevalue = chooseValue()


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

    def addMessage(self, _message, color:int = pyxel.COLOR_WHITE):
        _messageList = []

        # 引数の型を調べて変換する
        if type(_message) == str:
            _messageList.append(_message)
        else:
            _messageList = list(_message)

        m = message(_messageList, color)
        self.messageList.append(m)

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
                # 状態を変更する
                self.changeStatus()

        # キー入力待ち状態の時は、キー入力待ちメッセージを表示する
        if self.status == 1 or self.status == 2:
            for _messageRow in range(0, self.messageRow):
                _tempIdx = self.idx + _messageRow
                PyxelUtil.text(16, 140 + (_messageRow * 8), self.messageList[_tempIdx].message, self.messageList[_tempIdx].color)

            if self.status == 1:
                PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def changeStatus(self):
        # キー入力待ち状態にする
        self.status = 1


class chooseCommand(messageCommand):
    '''
    選択肢コマンドクラス
    '''
    def __init__(self):
        super().__init__()

        # 選択肢の辞書
        self.chooseDict = {}

    def addChoose(self, _message, key:int = pyxel.KEY_NONE, value = 0):
        _messageList = []

        # 引数の型を調べて変換する
        if type(_message) == str:
            _messageList.append(_message)
        else:
            _messageList = list(_message)

        c = choose(_messageList, pyxel.COLOR_YELLOW)
        # 親クラスが持つメッセージリストにメッセージとして登録
        self.messageList.append(c)

        # キーと値を選択肢の辞書に追加
        self.chooseDict[key] = value

    def update(self):
        super().update()

        # 選択肢入力待ち状態の時に定義されたいずれかのキーを押されたらchoosevalueを設定し、終了する。
        if self.status == 2:
            for _key, _value in self.chooseDict.items():
                if pyxel.btnp(_key):
                    choosevalue.value = _value
                    self.complete()

    def changeStatus(self):
        # 次ページのメッセージがあるか
        if self.idx + 5 < len(self.messageList) - 1:
            # 次ページのメッセージがある場合は、SPACEキーの入力待ちとする
            self.status = 1
        else:
            # 次ページのメッセージがない場合は、選択肢の入力待ちとする
            choosevalue.value = None
            self.status = 2
    

class messageCommand2(baseCommand):
    '''
    メッセージコマンドクラス２
    '''
    def __init__(self):
        super().__init__()

        self.messageList = []
        self.idx = 0

        # ステータス
        # 0:メッセージ表示状態
        # 1:キー入力待ち状態
        # 2:選択待ち状態
        self.status = 0

        # メッセージ表示行
        self.messageRow = 0

        # メッセージ表示桁
        self.messageCol = 0

        # 選択肢の辞書
        self.chooseDict = {}

    def addMessage(self, _message, color:int = pyxel.COLOR_WHITE):
        '''
        メッセージを登録する。\n
        messageCommandのインスタンス生成後に、表示したいメッセージと色を引数に呼び出す。\n
        enqueueする前に呼ぶこと。
        '''
        _messageList = []

        # 引数の型を調べて変換する
        if type(_message) == str:
            _messageList.append(_message)
        else:
            _messageList = list(_message)

        m = message(_messageList, color)
        self.messageList.append(m)

    def addChoose(self, _message, key:int = pyxel.KEY_NONE, callback = None):
        '''
        選択肢を登録する。\n
        messageCommandのインスタンス生成後に、表示したい選択肢を設定するために呼び出す。\n
        引数にはメッセージの他、対応するキーとコールバック先のメソッドを指定する。\n
        enqueueする前に呼ぶこと。
        '''
        _messageList = []

        # 引数の型を調べて変換する
        if type(_message) == str:
            _messageList.append(_message)
        else:
            _messageList = list(_message)

        c = choose(_messageList, pyxel.COLOR_YELLOW)
        # 親クラスが持つメッセージリストにメッセージとして登録
        self.messageList.append(c)

        # キーと値を選択肢の辞書に追加
        self.chooseDict[key] = callback

    def update(self):
        '''
        各フレームの処理。\n
        enqueueした後、completeするまでの間、各Stateのupdateメソッドは実行されず、このメソッドが呼ばれる。
        '''
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
            return

        # 選択肢入力待ち状態の時に定義されたいずれかのキーを押されたら登録されている関数を呼び出し、終了する。
        if self.status == 2:
            for _key, _value in self.chooseDict.items():
                if pyxel.btnp(_key):
                    _value()
                    self.complete()

    def draw(self):
        super().draw()

        # 現在行が0行目以外の時は、表示済の行を描画する
        if self.messageRow > 0:
            for _messageRow in range(0, self.messageRow):
                _tempIdx = self.idx + _messageRow
                PyxelUtil.text(16, 140 + (_messageRow * 8), self.messageList[_tempIdx].message, self.messageList[_tempIdx].color)

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
#            if self.messageRow > 0:
#                for _messageRow in range(0, self.messageRow):
#                    _tempIdx = self.idx + _messageRow
#                    PyxelUtil.text(16, 140 + (_messageRow * 8), self.messageList[_tempIdx].message, self.messageList[_tempIdx].color)

            _tempIdx = self.idx + self.messageRow
            if self.messageRow < 5 and _tempIdx < len(self.messageList):
                # 現在行は１文字ずつ送り表示する
                PyxelUtil.text(16, 140 + (self.messageRow * 8), self.messageList[_tempIdx].message[:self.messageCol], self.messageList[_tempIdx].color)

            else:
                # 状態を変更する
                self.changeStatus()

        # キー入力待ち状態の時は、キー入力待ちメッセージを表示する
#        if self.status == 1 or self.status == 2:
#            for _messageRow in range(0, self.messageRow):
#                _tempIdx = self.idx + _messageRow
#                PyxelUtil.text(16, 140 + (_messageRow * 8), self.messageList[_tempIdx].message, self.messageList[_tempIdx].color)

            if self.status == 1:
                PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def changeStatus(self):
        # キー入力待ち状態にする
        self.status = 1

    def changeStatus(self):
        # 次ページのメッセージがあるか
        if self.idx + 5 < len(self.messageList) - 1:
            # 次ページのメッセージがある場合は、SPACEキーの入力待ちとする
            self.status = 1
        else:
            # 次ページのメッセージがない場合は、まずはSPACEキーの入力待ちとする
            self.status = 1
            # 現在の表示内容に選択肢が含まれているか判定し、含まれている場合は選択肢の入力待ちとする
            for _messageRow in range(0, self.messageRow):
                if isinstance(self.messageList[self.idx + _messageRow], choose):
                    self.status = 2
                    break

    
