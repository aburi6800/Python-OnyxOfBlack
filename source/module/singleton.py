# -*- coding: utf-8 -*-

'''
 Singletonクラス
 - 常にインスタンスを１つだけ保持するクラスの基底クラス
'''
class Singleton(object):

    #
    # インスタンス生成
    #
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        
        return cls._instance
