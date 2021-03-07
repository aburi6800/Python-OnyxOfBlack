# -*- coding: utf-8 -*-
from module.eventHandler import eventhandler
from module.messageHandler import messagehandler


class DrawDecorator():
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function):
        def decorateFunc(*args, **kwargs):

            # 引数の関数を実行
            function(*args, **kwargs)

            # イベントハンドラでイベントが実行中の場合は、イベントハンドラのdrawメソッドを呼ぶ
            if eventhandler.isExecute:
                eventhandler.draw()

            # メッセージハンドラにキューが登録されてる場合は、メッセージハンドラのdrawメソッドを呼ぶ
            if messagehandler.isEnqueued():
                messagehandler.draw()

        # 定義した関数を返却する    
        return decorateFunc

