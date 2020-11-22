# -*- coding: utf-8 -*-
from module.baseState import BaseState
from module.battleStates.stateBattle import StateBattle
from module.facilityStates.stateArmorShop import StateArmorShop
from module.facilityStates.stateBarbar import StateBarbar
from module.facilityStates.stateDrugs import StateDrugs
from module.facilityStates.stateExaminations import StateExaminations
from module.facilityStates.stateHelmetShop import StateHelmetShop
from module.facilityStates.stateShieldShop import StateShieldShop
from module.facilityStates.stateSurgery import StateSurgery
from module.facilityStates.stateWeaponShop import StateWeaponShop
from module.fieldStates.baseFieldState import BaseFieldState
from module.fieldStates.stateCemetery import StateCemetery
from module.fieldStates.stateCity import StateCity
from module.fieldStates.stateDungeonB1 import StateDungeonB1
from module.fieldStates.stateDungeonB2 import StateDungeonB2
from module.fieldStates.stateDungeonB3 import StateDungeonB3
from module.fieldStates.stateDungeonB4 import StateDungeonB4
from module.fieldStates.stateDungeonB5 import StateDungeonB5
from module.fieldStates.stateWellB1 import StateWellB1
from module.fieldStates.stateWellB2 import StateWellB2
from module.fieldStates.stateWellB3 import StateWellB3
from module.fieldStates.stateWellB4 import StateWellB4
from module.state import State
from module.systemStates.stateCamp import StateCamp
from module.systemStates.stateMakeChracter import StateMakeCharacter
from module.systemStates.stateTitle import StateTitle


class StateStack(object):
    '''
    Stateをスタックで保持するクラス
    '''
    def __init__(self):
        '''
        クラス初期化
        '''

        # StateのEnumと対応するStateクラスの辞書
        self.__stateDict = {
            State.TITLE: StateTitle,
            State.MAKECHARACTER: StateMakeCharacter,
            State.CAMP: StateCamp,
            State.CEMETERY: StateCemetery,
            State.CITY: StateCity,
            State.WELLB1: StateWellB1,
            State.WELLB2: StateWellB2,
            State.WELLB3: StateWellB3,
            State.WELLB4: StateWellB4,
            State.DUNGEONB1 : StateDungeonB1,
            State.DUNGEONB2 : StateDungeonB2,
            State.DUNGEONB3 : StateDungeonB3,
            State.DUNGEONB4 : StateDungeonB4,
            State.DUNGEONB5 : StateDungeonB5,
            State.ARMORSHOP : StateArmorShop,
            State.BARBAR : StateBarbar,
            State.DRUGS : StateDrugs,
            State.EXAMINATIONS : StateExaminations,
            State.HELMETSHOP : StateHelmetShop,
            State.SHIELDSHOP : StateShieldShop,
            State.SURGERY : StateSurgery,
            State.WEAPONSHOP : StateWeaponShop,
            State.BATTLE : StateBattle,
        }

        self.clear("")

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
            self.states[0].draw()

    def push(self, stateName:str):
        '''
        指定されたStateをスタックに追加する

        追加されるStackはbuildStateメソッドによりスタック操作メソッドが追加され、onEnterメソッドが実行される
        '''
        state = self.__getInstance(stateName)

        if state != None:
            st = self.__buildState(state)
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

    def clear(self, stateName:str):
        '''
        スタックを初期化してstateを登録する
        '''
        self.states = []
        if __debug__:
            print("StateStack : cleared")

        state = self.__getInstance(stateName)

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

    def __buildState(self, _class):
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

    def __getInstance(self, stateName:str) -> BaseState:
        if stateName == "":
            return None

        state = self.__stateDict.get(stateName, None)

        return state


stateStack = StateStack()
