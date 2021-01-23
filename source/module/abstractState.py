# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbstractState(metaclass=ABCMeta):
    '''
    Stateクラスの抽象クラス\n
    BaseStateクラスの基底抽象クラス。\n
    各Stateクラスはこのクラスを継承すること。
    '''
    class StateParams():
        '''
        Stateクラス生成時のパラメタ定義クラス。\n
        継承先クラスで必要なパラメタがあれば、継承先クラスで個別に定義すること。
        '''
        pass

    def __init__(self, **kwargs) -> None:
        '''
        クラス初期化\n
        継承先クラスで特に引数を必要としない場合でも、無条件にこのメソッドを呼ぶこと。
        '''
        # パラメタ定義クラスのインスタンス生成
        stateParams = self.StateParams()

		# キーワード引数の値をパラメタ定義クラスのメンバに設定する。
        # 対象のメンバが存在しない場合は、TypeErrorを発生させる。
        for key in vars(stateParams.__class__):
            # ダンダーメソッド以外を対象とする
            if key[0:2] != "__":
                # キーワード引数から対象メンバをキーに値を取得する
                value = kwargs.get(key, None)
                # 取得失敗時
                if  value == None:
                    raise TypeError("missing kwargs : '" + str(key) + "' is not found.")
                    break
                # 取得成功時
                else:
                    exec("stateParams." + key + " = '" + value + "'")

    @abstractmethod
    def update(self) -> None:
        '''
        各フレームの処理
        '''
        pass

    @abstractmethod
    def draw(self) -> None:
        '''
        各フレームの描画処理
        '''
        pass

    @abstractmethod
    def onEnter(self) -> None:
        '''
        状態開始時の処理
        '''
        pass

    @abstractmethod
    def onExit(self) -> None:
        '''
        状態終了時の処理
        '''
        pass
