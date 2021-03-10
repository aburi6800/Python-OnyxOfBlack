# -*- coding: utf-8 -*-
import pyxel

class Input():
    '''
    文字入力クラス

    使用方法は以下。
    1.このクラスのインスタンスを生成する。
      インスタンス生成時に、座標と最大文字数を指定できる。（指定しない場合は、座標は(0,0)、最大文字数は無制限となる）
    2.アプリケーションのupdateメソッドで、このクラスのupdateメソッドを呼ぶ。
      同時に、このクラスのisEnterがTrueの場合は、所定の変数にこのクラスのvalueの値を格納する。
    3.drawメソッドの中でこのクラスのdrawメソッドを呼ぶ。
    なお、画面内に複数の入力箇所がある場合は、同時にインスタンスを生成すると全てに同じ文字が入力されるため、
    アプリケーションでインスタンスの生成、またはupdate/drawメソッドの呼び出しを制御する必要がある。
    '''
    # 入力文字列
    value = ""

    # 入力完了フラグ
    isEnter = False

    def __init__(self):
        '''
        クラス初期化
        '''
        self.__init__(0, 0)

    def __init__(self, x:int, y:int, maxLen:int = -1):
        '''
        クラス初期化

        通常はこちらを使用すること
        '''
        # 入力座標
        self.x = x
        self.y = y

        # 最大文字数
        self.maxLen = maxLen

        # キーの辞書
        self.keydict = {
            pyxel.KEY_A: {"func" : self.add, "args": {"keystr": "A"}},
            pyxel.KEY_B: {"func" : self.add, "args": {"keystr": "B"}},
            pyxel.KEY_C: {"func" : self.add, "args": {"keystr": "C"}},
            pyxel.KEY_D: {"func" : self.add, "args": {"keystr": "D"}},
            pyxel.KEY_E: {"func" : self.add, "args": {"keystr": "E"}},
            pyxel.KEY_F: {"func" : self.add, "args": {"keystr": "F"}},
            pyxel.KEY_G: {"func" : self.add, "args": {"keystr": "G"}},
            pyxel.KEY_H: {"func" : self.add, "args": {"keystr": "H"}},
            pyxel.KEY_I: {"func" : self.add, "args": {"keystr": "I"}},
            pyxel.KEY_J: {"func" : self.add, "args": {"keystr": "J"}},
            pyxel.KEY_K: {"func" : self.add, "args": {"keystr": "K"}},
            pyxel.KEY_L: {"func" : self.add, "args": {"keystr": "L"}},
            pyxel.KEY_M: {"func" : self.add, "args": {"keystr": "M"}},
            pyxel.KEY_N: {"func" : self.add, "args": {"keystr": "N"}},
            pyxel.KEY_O: {"func" : self.add, "args": {"keystr": "O"}},
            pyxel.KEY_P: {"func" : self.add, "args": {"keystr": "P"}},
            pyxel.KEY_Q: {"func" : self.add, "args": {"keystr": "Q"}},
            pyxel.KEY_R: {"func" : self.add, "args": {"keystr": "R"}},
            pyxel.KEY_S: {"func" : self.add, "args": {"keystr": "S"}},
            pyxel.KEY_T: {"func" : self.add, "args": {"keystr": "T"}},
            pyxel.KEY_U: {"func" : self.add, "args": {"keystr": "U"}},
            pyxel.KEY_V: {"func" : self.add, "args": {"keystr": "V"}},
            pyxel.KEY_W: {"func" : self.add, "args": {"keystr": "W"}},
            pyxel.KEY_X: {"func" : self.add, "args": {"keystr": "X"}},
            pyxel.KEY_Y: {"func" : self.add, "args": {"keystr": "Y"}},
            pyxel.KEY_Z: {"func" : self.add, "args": {"keystr": "Z"}},
            pyxel.KEY_ENTER: {"func" : self.enter, "args": None},
            pyxel.KEY_BACKSPACE: {"func" : self.backspace, "args": None},
            pyxel.KEY_DELETE: {"func" : self.backspace, "args": None},
        }

        # 入力文字列を初期化
        self.value = ""

        # 直前の入力文字列
        self.preValue = ""

    def add(self, keystr: str):
        '''
        入力文字列追加処理
        '''
        if self.maxLen == -1 or len(self.value) < self.maxLen:
            self.value = self.value + keystr

    def enter(self):
        '''
        入力完了処理
        '''
        if self.value != "":
            self.isEnter = True

    def backspace(self):
        '''
        入力文字列削除処理
        '''
        self.value = self.value[0: len(self.value) - 1]

    def update(self):
        '''
        各フレームの処理
        '''
        # 入力終了していたら処理せずにreturnする
        if self.isEnter:
            return

        # 毎フレーム、直前の入力文字列を退避
        self.preValue = self.value

        # キーの辞書を走査
        for _key, _cont in self.keydict.items():
            if pyxel.btnp(_key):
                if _cont["args"] == None:
                    _cont["func"]()
                else:
                    _cont["func"](**_cont["args"])

    def draw(self):
        '''
        各フレームの描画処理
        '''
        # 入力文字列が変わってるか
        if self.value != self.preValue:
            # 入力文字列を消す    
            pyxel.rect(self.x, self.y, len(self.value) * 4, 5, pyxel.COLOR_BLACK)

        # 入力文字列を表示する
        pyxel.text(self.x, self.y, self.value, pyxel.COLOR_WHITE)

        # 入力完了していなければ、カーソルを表示する
        if self.isEnter == False and pyxel.frame_count % 4 == 0:
            pyxel.rect(self.x + len(self.value) * 4, self.y, 3, 5, pyxel.COLOR_WHITE)
