# -*- coding: utf-8 -*-
import pyxel
from module.facility.baseFacilityState import BaseFacilityState

'''
 StateArmorShopクラス
 - 鎧屋のクラス
 - 選択した商品の購入、キャラクターへの装備を行う
'''
class StateArmorShop(BaseFacilityState):

    #
    # クラス初期化
    #
    def __init__(self, stateStack):

        super(StateArmorShop, self).__init__(stateStack)
        self.stateName = "ArmorShop"

    #
    # 各フレームの処理
    #
    def update(self):

        print(self.stateName + ":update")
        self.stateStack.pop()

    #
    # 各フレームの画面描画処理
    #
    def render(self, app):

        pyxel.text(0, app.message_y, self.stateName , 7)
        app.message_y = app.message_y + 6
        print(self.stateName + ":render")

    #
    # 状態開始時の処理
    #
    def onEnter(self):

        print(self.stateName + ":onEnter")

    #
    # 状態終了時の処理
    #
    def onExit(self):

        print(self.stateName + ":onExit")

