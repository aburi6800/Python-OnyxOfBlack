# -*- coding: utf-8 -*-


class Singleton(object):
    '''
    常にインスタンスを1つだけ保持するクラスの基底クラス

    Singletonなクラスにする場合は、このクラスを継承する
    '''

    def __new__(cls, *args, **kargs):
        '''
        インスタンス生成
        '''
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)

        return cls._instance
