# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbstractState(metaclass=ABCMeta):
    '''Stateクラスの抽象クラス

    BaseStateクラスの基底クラス。もしかしていらないかも？
    '''

    @abstractmethod
    def update(self):
        '''各フレームの処理

        実装はなし
        '''
        pass

    @abstractmethod
    def render(self):
        '''各フレームの描画処理

        実装はなし
        '''
        pass

    @abstractmethod
    def onEnter(self):
        '''状態開始時の処理

        実装はなし
        '''
        pass

    @abstractmethod
    def onExit(self):
        '''状態終了時の処理

        実装はなし
        '''
        pass
