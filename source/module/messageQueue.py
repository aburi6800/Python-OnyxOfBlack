# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from collections import deque
from enum import IntEnum, auto

import pyxel

from module.pyxelUtil import PyxelUtil


class statusEnum(IntEnum):
    '''
    messageCommandの状態を表すEnum
    '''
    SHOW_MESSAGE = auto()
    WAIT_KEY = auto()
    WAIT_CHOOSE = auto()

class messageQueue():
    '''
    メッセージキュークラス\n
    登録された各コマンドクラスのupdate、drawメソッドを実行する。\n
    コマンドキューへの登録は各コマンドクラスが自ら行う。
    '''

    # メッセージキューに登録されるコマンドリスト
    commands = deque([])

    def __init__(self):
        '''
        クラス初期化
        '''
        pass

    def isEnqueued(self):
        '''
        メッセージキューにキューが登録されているかをboolean型で返却する。
        '''
        return True if len(self.commands) > 0 else False

    def enqueue(self, _command):
        '''
        メッセージキューにコマンドを登録する。
        '''
        self.commands.append(_command)

    def _dequeue(self):
        '''
        メッセージキューからコマンドを除去する。\n
        外部からは使用しないこと。
        '''
        self.commands.popleft()

    def update(self):
        '''
        updateメソッド\n
        isEnwueued=trueの場合に、baseStateのupdateメソッドから呼ばれる。\n
        メッセージキューに登録されたコマンドのupdateメソッドを実行する。\n
        コマンドが終了した場合は、メッセージキューからdequeueする。
        '''
        command = self.commands[0]
        if command.isComplete:
            self._dequeue()
        else:
            self.commands[0].update()

    def draw(self):
        '''
        drawメソッド\n
        isEnwueued=trueの場合に、baseStateのdrawメソッドから呼ばれる。\n
        '''
        if self.isEnqueued:
            if self.commands[0].isComplete == False:
                self.commands[0].draw()


messagequeue = messageQueue()


class message():
    '''
    メッセージクラス
    '''
    def __init__(self, message, color:int = pyxel.COLOR_WHITE):
        '''
        クラス初期化\n
        messageには表示するメッセージ(pyxelUtil.textメソッドに渡す値)を指定する。\n
        colorにはメッセージ表示文字色を指定する。（１行に１色）
        '''
        self.message = message
        self.color = color


class choose(message):
    '''
    選択肢クラス
    '''
    def __init__(self, message, color:int = pyxel.COLOR_YELLOW, key:int = pyxel.KEY_NONE, value:int = 0):
        super().__init__(message, color)
        self.key = key


class baseCommand(metaclass=ABCMeta):
    '''
    コマンド基底抽象クラス
    '''
    def __init__(self):
        '''
        クラス初期化
        '''
        # 完了フラグをFalseにする
        self.isComplete = False

    def isComplete(self):
        '''
        完了フラグを返却する
        '''
        return self.isCOmplete

    @abstractmethod
    def update(self):
        '''
        各フレームの処理
        '''
        pass

    @abstractmethod
    def draw(self):
        '''
        各フレームの描画処理
        '''
        pass

    def complete(self):
        '''
        完了フラグをTrueに設定する
        '''
        self.isComplete = True


class messageCommand(baseCommand):
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
        self.status = statusEnum.SHOW_MESSAGE

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

    def addChoose(self, _message, key:int = pyxel.KEY_NONE, callback = None) -> None:
        '''
        選択肢を登録する。\n
        messageCommandのインスタンス生成後に、表示したい選択肢を設定するために呼び出す。\n
        引数にはメッセージの他、対応するキーとコールバック先のメソッドを指定する。\n
        enqueueする前に呼ぶこと。
        '''
        # メッセージリストの初期化
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

    def update(self) -> None:
        '''
        各フレームの処理。\n
        enqueueした後、completeするまでの間、各Stateのupdateメソッドは実行されず、このメソッドが呼ばれる。
        '''
        super().update()

        # メッセージ表示中の場合
        if self.status == statusEnum.SHOW_MESSAGE:

            # すべてのメッセージ、または現画面の最大行まで表示していなければ何もしない
            if self.messageRow < 5 and self.idx + self.messageRow < len(self.messageList):
                pass
            # すべてのメッセージを表示するか、現画面の最大行の表示を行った場合は、ステータスを変更する
            else:
                self.changeStatus()

            return

        # SPACEキー入力待ち状態の場合
        if self.status == statusEnum.WAIT_KEY:

            # SPACEキーを押されたか
            if pyxel.btnp(pyxel.KEY_SPACE):

                # メッセージリストのインデックスに5加算し、次ページの表示の準備を行う
                self.idx += 5

                # メッセージリストのインデックスがメッセージリストの要素数を超えているか判定する
                if self.idx < len(self.messageList) - 1:
                    # 超えていない場合は、メッセージ表示を行う
                    self.status = statusEnum.SHOW_MESSAGE
                    self.messageRow = 0
                    self.messageCol = 0
                else:
                    # 超えている場合は、完了処理を行う
                    self.complete()

            return

        # 選択肢入力待ち状態の場合
        if self.status == statusEnum.WAIT_CHOOSE:

            # 選択肢辞書の要素を走査
            for _key, _value in self.chooseDict.items():

                # 定義されたいずれかのキーを押されたら登録されているコールバック関数を呼び出し、完了処理を行う。
                if pyxel.btnp(_key):
                    # コールバック関数実行
                    if _value != None:
                        _value()
                    self.complete()

    def draw(self):
        '''
        各フレームの描画処理。
        '''
        super().draw()

        # メッセージ表示状態の場合は、以下を処理する。
        # ・idx～idx+4までを画面に表示し、キー入力待ち状態にする
        if self.status == statusEnum.SHOW_MESSAGE:

            # 次のカラムへ
            self.messageCol += 1

            # カラム数がその行の文字数を超えたら、カラムを戻して次の行へ
            if self.messageCol > len(self.messageList[self.messageRow].message):
                self.messageCol = 1
                self.messageRow += 1

            # 現在表示中のメッセージリストのインデックスを取得
            _tempIdx = self.idx + self.messageRow

            # メッセージをすべて表示したか、または現画面で最大行まで表示したかを判定する
            if self.messageRow < 5 and _tempIdx < len(self.messageList):
                # すべて表示していない、かつ現画面の最大行まで表示していない場合は、現在行を１文字ずつ送り表示する
                PyxelUtil.text(16, 140 + (self.messageRow * 8), self.messageList[_tempIdx].message[:self.messageCol], self.messageList[_tempIdx].color)

        # 以下は無条件に処理する。
        # 現在行が0行目以外の時は、表示済の行を描画する
        if self.messageRow > 0:
            for _messageRow in range(0, self.messageRow):
                _tempIdx = self.idx + _messageRow
                PyxelUtil.text(16, 140 + (_messageRow * 8), self.messageList[_tempIdx].message, self.messageList[_tempIdx].color)

        # キー入力待ち状態の時は、SPACEキー入力待ちメッセージを表示する
        if self.status == statusEnum.WAIT_KEY:
            PyxelUtil.text(180, 180, "*[HIT SPACE KEY]", pyxel.COLOR_YELLOW)

    def changeStatus(self):
        '''
        状態を変更する\n
        次ページのメッセージがある場合はSPACEキー入力待ちの状態に変更する。\n
        次ページのメッセージがなく、選択肢がメッセージ中に含まれていない場合も、SPACEキー入力待ちの状態に変更する。\n
        上記以外の場合は、選択肢入力街の状態に変更する。
        '''
        # 次ページのメッセージがあるか
        if self.idx + 5 < len(self.messageList) - 1:
            # 次ページのメッセージがある場合は、SPACEキーの入力待ちとする
            self.status = statusEnum.WAIT_KEY
        else:
            # 次ページのメッセージがない場合は、まずはSPACEキーの入力待ちを初期値とする
            self.status = statusEnum.WAIT_KEY
            # 現在の表示内容に選択肢が含まれているか判定する
            for _messageRow in range(0, self.messageRow):
                if isinstance(self.messageList[self.idx + _messageRow], choose):
                    # 選択肢が含まれている場合は選択肢の入力待ちとする
                    self.status = statusEnum.WAIT_CHOOSE
                    break

    
