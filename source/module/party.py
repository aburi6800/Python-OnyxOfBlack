# -*- coding: utf-8 -*-
from module.singleton import Singleton
from module.character import Character

'''
 Partyクラス
 - パーティーを管理するクラス
 - Singletonとする
'''
class Party(Singleton):

    #
    # クラス初期化
    #
    def __init__(self):
        self.member = []

    #
    # メンバー追加
    #
    def addMember(self, chr: Character):
        if len(self.member) < 5:
            self.member.append(chr)
        else:
            raise Exception("can't add a member.")

    #
    # メンバー削除
    #
    def removeMember(self, idx):
        try:
            del self.member[idx]
        except:
            raise Exception("specified a member who doesn't exist.：" + str(idx))

    #
    # メンバー取得
    #
    def getMember(self, idx):
        try:
            return self.member[idx]
        except:
            raise Exception("specified a member who doesn't exist.：" + str(idx))
