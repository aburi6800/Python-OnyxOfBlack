# -*- coding: utf-8 -*-

from module.character import playerParty

# Stateのリスト
states = []

class SaveData():
    '''
    セーブデータのクラス

    ゲームで保存する場合は、このクラスのメンバに値を設定し、saveメソッドをデータを定義する
    '''
    def __init__(self, states, playerParty):
        # Stateのリスト
        self.states = states

        # PlayerParty
        self.playerParty = playerParty

