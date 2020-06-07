# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class State(metaclass = ABCMeta):

    #
    # 各フレームの処理
    #
    @abstractmethod
    def update(self):

        pass

    #
    # 各フレームの画面描画処理
    #
    @abstractmethod
    def render(self):

        pass

    #
    # 状態開始時の処理
    #
    @abstractmethod
    def onEnter(self):

        pass

    #
    # 状態終了時の処理
    #
    @abstractmethod
    def onExit(self):

        pass


