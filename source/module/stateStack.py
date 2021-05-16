# -*- coding: utf-8 -*-
from typing import List

from module.baseState import BaseState
from module.battleStates.stateBattle import StateBattle
from module.constant.state import State
from module.facilityStates.stateArmorShop import StateArmorShop
from module.facilityStates.stateBarbar import StateBarbar
from module.facilityStates.stateDrugs import StateDrugs
from module.facilityStates.stateExaminations import StateExaminations
from module.facilityStates.stateHelmetShop import StateHelmetShop
from module.facilityStates.stateShieldShop import StateShieldShop
from module.facilityStates.stateSurgery import StateSurgery
from module.facilityStates.stateWeaponShop import StateWeaponShop
from module.fieldStates.baseFieldState import BaseFieldState
from module.fieldStates.stateBlacktower import StateBlackTower
from module.fieldStates.stateCemetery import StateCemetery
from module.fieldStates.stateCity import StateCity
from module.fieldStates.stateColordBlack import StateColordBlack
from module.fieldStates.stateColordBlue import StateColordBlue
from module.fieldStates.stateColordGreen import StateColordGreen
from module.fieldStates.stateColordPurple import StateColordPurple
from module.fieldStates.stateColordRed import StateColordRed
from module.fieldStates.stateColordWhite import StateColordWhite
from module.fieldStates.stateColordYellow import StateColordYellow
from module.fieldStates.stateDungeonB1 import StateDungeonB1
from module.fieldStates.stateDungeonB2 import StateDungeonB2
from module.fieldStates.stateDungeonB3 import StateDungeonB3
from module.fieldStates.stateDungeonB4 import StateDungeonB4
from module.fieldStates.stateDungeonB5 import StateDungeonB5
from module.fieldStates.stateWellB1 import StateWellB1
from module.fieldStates.stateWellB2 import StateWellB2
from module.fieldStates.stateWellB3 import StateWellB3
from module.fieldStates.stateWellB4 import StateWellB4
from module.systemStates.stateCamp import StateCamp
from module.systemStates.stateEnding import StateEnding
from module.systemStates.stateMakeChracter import StateMakeCharacter
from module.systemStates.stateTitle import StateTitle


class StateStack(object):
    '''
    Stateをスタックで保持するクラス
    '''
    def __init__(self) -> None:
        '''
        クラス初期化
        '''
        # StateのEnumと対応するStateクラスの辞書
        self.__stateDict = {
            State.TITLE: StateTitle,
            State.MAKECHARACTER: StateMakeCharacter,
            State.CAMP: StateCamp,
            State.ENDING: StateEnding,
            State.CEMETERY: StateCemetery,
            State.CITY: StateCity,
            State.WELLB1: StateWellB1,
            State.WELLB2: StateWellB2,
            State.WELLB3: StateWellB3,
            State.WELLB4: StateWellB4,
            State.DUNGEONB1: StateDungeonB1,
            State.DUNGEONB2: StateDungeonB2,
            State.DUNGEONB3: StateDungeonB3,
            State.DUNGEONB4: StateDungeonB4,
            State.DUNGEONB5: StateDungeonB5,
            State.COLORD_YELLOW: StateColordYellow,
            State.COLORD_RED: StateColordRed,
            State.COLORD_PURPLE: StateColordPurple,
            State.COLORD_GREEN: StateColordGreen,
            State.COLORD_BLUE: StateColordBlue,
            State.COLORD_WHITE: StateColordWhite,
            State.COLORD_BLACK: StateColordBlack,
            State.BLACKTOWER: StateBlackTower,
            State.ARMORSHOP: StateArmorShop,
            State.BARBAR: StateBarbar,
            State.DRUGS: StateDrugs,
            State.EXAMINATIONS: StateExaminations,
            State.HELMETSHOP: StateHelmetShop,
            State.SHIELDSHOP: StateShieldShop,
            State.SURGERY: StateSurgery,
            State.WEAPONSHOP: StateWeaponShop,
            State.BATTLE: StateBattle,
        }

        # スタックを初期化する
        self.clear()

        if __debug__:
            print("StateStack : Initialized.")

    def update(self) -> None:
        '''
        現在先頭にあるStateのupdateメソッドを実行する
        '''
        if len(self.states) > 0 and self.states[0] != None:
            self.states[0].update()

    def draw(self) -> None:
        '''
        現在先頭にあるStateのrenderメソッドを実行する
        '''
        if len(self.states) > 0 and self.states[0] != None:
            self.states[0].draw()

    def push(self, stateEnum: int, **kwargs) -> None:
        '''
        stateEnumで指定されたStateクラスのインスタンスを生成し、スタックの先頭に追加する。\n
        追加されるStateクラスはbuildStateメソッドによりスタック操作メソッドが追加された後、onEnterメソッドが実行される。
        '''
        if __debug__:
            print(f"StateStack : push({stateEnum}).")

        # stateEnumで指定されたStateクラスのインスタンスを生成する
        state = self.getInstance(stateEnum, **kwargs)

        # スタックの先頭に追加する
        self.states.insert(0, state)

        # インスタンスの生成に成功した場合
        if state != None:
            # State開始時の処理を呼び出す
            self.states[0].onEnter()

        if __debug__:
            print("StateStack : pushed -> " + str(state))

    def pop(self) -> None:
        '''
        スタックの先頭からStateを削除する。\n
        削除前にStackのonExitメソッドが実行される。
        '''
        if __debug__:
            print("StateStack : pop " + str(self.states[0]))

        # State終了時の処理を呼び出す
        if self.states[0] != None:
            self.states[0].onExit()

        # スタックの先頭からStateを削除する。
        self.states.pop(0)

        # スタックの戦闘になったStateのonEnterメソッドを実行する
        if self.states[0] != None:
            self.states[0].onEnter()

    def isField(self) -> bool:
        '''
        現在のStateがBaseFieldの派生クラスかを判定する
        '''
        if len(self.states) > 0 and isinstance(self.states[0], BaseFieldState):
            return True
        else:
            return False

    def clear(self) -> None:
        '''
        スタックを初期化し、stateNameに指定されたstateをスタックに登録する
        '''
        if __debug__:
            print("StateStack : clear")

        # スタック初期化
        self.states = []

    def setStates(self, states) -> None:
        '''
        List型で指定されたスタックをすべて設定する。\n
        データロード時のみ使用すること。
        '''
        self.states = states

    def getStates(self) -> List:
        '''
        stateのリストを取得する
        '''
        return self.states

    def getInstance(self, stateEnum: int, **kwargs) -> BaseState:
        '''
        StateのEnum値に該当するstateクラスを取得する
        '''
        # 戻り値の初期化
        state = None

        # 引数がNoneの時はNoneを返す
        if stateEnum == None:
            return None

        # stateの辞書からstateEnumに該当するstateクラスを取得する
        c = self.__stateDict.get(stateEnum, None)

        # stateクラスの取得に成功した場合、コールバックメソッドを登録し、インスタンスを生成する
        if c != None:
            kwargs["stateStack"] = self
            state = c(**kwargs)

        return state


stateStack = StateStack()
