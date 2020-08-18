# -*- coding: utf-8 -*-

class SaveData():
    '''
    セーブデータのクラス

    ゲームで保存する場合は、このクラスのメンバに値を設定し、saveメソッドをデータを定義する
    '''
    def __init__(self, stateStack, playerParty):
        # StateStack
        self.stateStack = stateStack

        # PlayerParty
        self.playerParty = playerParty

