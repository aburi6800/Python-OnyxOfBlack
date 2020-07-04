# -*- coding: utf-8 -*-
import pyxel
from ..facilityStates.baseFacilityState import BaseFacilityState


class StateHelmetShop(BaseFacilityState):
    '''
    兜屋のクラス

    BaseFacilityStateクラスを継承
    選択した商品の購入、キャラクターへの装備を行う
    '''

    def __init__(self, stateStack):
        '''
        クラス初期化
        '''
        super().__init__(stateStack)
        self.stateName = "HelmetShop"

    def update(self):
        '''
        各フレームの処理
        '''
        pass

    def render(self):
        '''
        各フレームの描画処理
        '''
        super().render()

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        pass

    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
