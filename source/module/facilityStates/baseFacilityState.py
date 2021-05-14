# -*- coding: utf-8 -*-
import pyxel
from module.baseState import BaseState
from module.character import playerParty
from module.pyxelUtil import PyxelUtil
from overrides import EnforceOverrides, overrides


class BaseFacilityState(BaseState, EnforceOverrides):
    '''
    施設の基底クラス\n
    各施設で共通の処理を持つ
    '''

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        super().__init__(**kwargs)

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        super().update_execute()

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        super().draw()

        for idx, member in enumerate(playerParty.memberList):
            _y = 14 + idx * 16
            # メンバーの薬の所持数を表示
            if member.potion != -1:
                pyxel.blt(63, _y + 1, 1, (0 if member.potion == 0 else 8), 40, 4, 5)
                PyxelUtil.text(68, _y, ["*x{:1d}".format(member.potion)], pyxel.COLOR_YELLOW)

            # メンバーの所持金を表示
            PyxelUtil.text(
                83, _y, ["*{:5d} G.P.".format(member.gold)], pyxel.COLOR_YELLOW)

        pyxel.blt(self.DRAW_OFFSET_X + 15, self.DRAW_OFFSET_Y + 15, 0, 0, 205, 50, 50)

    @overrides
    def onEnter(self):
        '''
        状態開始時の処理
        '''
        pass

    @overrides
    def onExit(self):
        '''
        状態終了時の処理
        '''
        pass
