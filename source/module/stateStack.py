# -*- coding: utf-8 -*-

from module.baseState import BaseState
from module.fieldStates.baseFieldState import BaseFieldState


class StateStack(object):
    '''
    Stateをスタックで保持するクラス

    Singletonとする
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        self.clear()
        if __debug__:
            print("StateStack : Initialized.")

    def update(self):
        '''
        現在先頭にあるStateのupdateメソッドを実行する
        '''
        if len(self.states) > 0 and self.states[0] != None:
            self.states[0].update()

    def draw(self):
        '''
        現在先頭にあるStateのrenderメソッドを実行する
        '''
        if len(self.states) > 0 and self.states[0] != None:
            self.states[0].render()

    def push(self, state):
        '''
        StateStackにStateをpushするtateNameで指定されたStateをスタックに追加する

        追加されるStackはonEnterメソッドが実行される
        '''
        if state != None:
            st = self.buildState(state)
            self.states.insert(0, st)
            if __debug__:
                print("StateStack : push " + str(st))
            # State開始時の処理を呼び出す
            self.states[0].onEnter()
        else:
            self.states.insert(0, None)
            if __debug__:
                print("StateStack : push(None)")

    def pop(self):
        '''
        スタックの先頭からStateを削除する

        削除前にStackのonExitメソッドが実行される
        '''
        # State終了時の処理を呼び出す
        if __debug__:
            print("StateStack : pop " + str(self.states[0]))
        
        if self.states[0] != None:
            self.states[0].onExit()
        self.states.pop(0)

    def isField(self) -> bool:
        '''
        現在のStateがBaseFieldの派生クラスかを判定する
        '''
        if len(self.states) > 0 and isinstance(self.states[0], BaseFieldState):
            return True
        else:
            return False

    def clear(self, state=None):
        '''
        スタックを初期化してstateを登録する
        '''
        self.states = []
        if __debug__:
            print("StateStack : cleared")
        self.push(state)

    def setStates(self, states):
        '''
        スタックのstatesを設定する

        データロード時のみ使用すること。
        '''
        self.states = states

    def getStates(self):
        '''
        stateのリストを取得する
        '''
        return self.states

    def buildState(self, _class):
        '''
        stateクラスのインスタンス生成処理

        インスタンス生成時に、コールバックメソッドを登録する
        '''
        _class = _class()
        _class.pushState = self.push
        _class.popState = self.pop
        _class.clearState = self.clear
        _class.isField = self.isField
        _class.setStates = self.setStates
        _class.getStates = self.getStates
        return _class


stateStack = StateStack()
