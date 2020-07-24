# -*- coding: utf-8 -*-

#from .singleton import Singleton
from .systemStates.stateTitle import StateTitle
from .battleStates.stateBattle import StateBattle
from .fieldStates.baseFieldState import BaseFieldState
from .fieldStates.stateCity import StateCity
from .facilityStates.stateWeaponShop import StateWeaponShop
from .facilityStates.stateArmorShop import StateArmorShop
from .facilityStates.stateShieldShop import StateShieldShop
from .facilityStates.stateHelmetShop import StateHelmetShop
#import stateBarbar
#import stateBank
#import stateSurgery
#import stateDrug
#import stateExaminations


class StateStack(object):
    '''
    Stateをスタックで保持するクラス

    SIngletonとする
    Stateのpush,popは各Stateの中で行う
    '''

    STATE_TITLE = "Title"
    STATE_CITY = "City"
    STATE_BATTLE = "Battle"
    STATE_WEAPONSHOP = "WeaponShop"
    STATE_ARMORSHOP = "ArmorShop"
    STATE_SHIELDSHOP = "ShieldShop"
    STATE_HELMETSHOP = "HelmetShop"

    def __init__(self):
        '''
        クラス初期化
        '''
        self.states = []
        self.stateDic = {
            self.STATE_TITLE: StateTitle,
            self.STATE_CITY: StateCity,
            self.STATE_BATTLE: StateBattle,
            self.STATE_WEAPONSHOP: StateWeaponShop,
            self.STATE_ARMORSHOP: StateArmorShop,
            self.STATE_SHIELDSHOP: StateShieldShop,
            self.STATE_HELMETSHOP: StateHelmetShop
        }

    def update(self):
        '''
        現在先頭にあるStateのupdateメソッドを実行する
        '''
        if len(self.states) > 0:
            self.states[0].update()

    def render(self):
        '''
        現在先頭にあるStateのrenderメソッドを実行する
        '''
        if len(self.states) > 0:
            self.states[0].render()

    def push(self, stateName: str):
        '''
        StateNameで指定されたStateをスタックに追加する

        StateNameはこのクラスで定義した変数（STATE_～）を使用する
        追加されたStackはonEnterメソッドが実行される
        '''
        self.states.insert(0, self.stateDic[stateName](self))
        # State開始時の処理を呼び出す
        self.states[0].onEnter()

    def pop(self):
        '''
        スタックの先頭からStateを削除する

        削除前にStackのonExitメソッドが実行される
        '''
        # State終了時の処理を呼び出す
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

    def init(self, stateName: str):
        '''
        スタックを初期化してstateを登録する
        '''
        self.states = []
        self.push(stateName)


stateStack = StateStack()
