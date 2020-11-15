# -*- coding: utf-8 -*-
import pickle

import pyxel
from module.character import playerParty
from module.facilityStates.baseFacilityState import BaseFacilityState
from module.pyxelUtil import PyxelUtil
from module.savedata import SaveData


class StateCamp(BaseFacilityState):
    '''
    キャンプメニューのクラス

    薬の使用／セーブ／ゲーム終了を行う
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

        # 薬を飲む
        if pyxel.btnp(pyxel.KEY_D):
            pass

        # セーブ
        if pyxel.btnp(pyxel.KEY_S):
            s = SaveData(self.getStates(), playerParty)
            with open('savedata.dat', 'wb') as f:
                pickle.dump(s, f)

        # ゲームを中断
        if pyxel.btnp(pyxel.KEY_Q):
            # タイトルに戻る
            self.clearState()

        # キャンプを終わる
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.popState()

    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        PyxelUtil.text(97, 140, ["*** CAMP MENU **"], pyxel.COLOR_LIGHTBLUE)
        PyxelUtil.text(16, 148, ["*[D] ", "KU", "SU", "RI",
                                 "WO", " ", "NO", "MU"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 156, ["*[S] ", "se", "-",
                                 "hu", "d"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 164, ["*[Q] ", "ke", "d", "-", "mu", "WO",
                                 " ", "TI", "LYU", "U", "TA", "D", "NN"], pyxel.COLOR_YELLOW)
        PyxelUtil.text(16, 172, ["*[SPACE] ", "ki", "lya", "nn", "hu",
                                 "hd", "WO", " ", "O", "WA", "RU"], pyxel.COLOR_YELLOW)

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
