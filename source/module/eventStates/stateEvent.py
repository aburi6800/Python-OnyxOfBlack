import json
import os

from module.baseState import BaseState
from module.messageQueue import messageCommand2, messagequeue


class event(BaseState):
    '''
    イベントクラス\n
    常にインスタンスは１つのみとする。\n
    イベントを発生させたい場合は、startメソッドをイベント定義のjsonファイルを指定して実行する。
    '''

    # イベント発生の状態
    occuring = False

    # イベントデータ
    eventData = {}

    # エントリーデータ
    entryData = {}

    # フラグリスト
    # 本来は別クラス（playerParty？）に持っているもの
    flg = [0] * 256

    def __init__(self, **kwargs) -> None:
        '''
        イベントクラスのコンストラクタ\n
        引数にイベントのjsonファイルを指定すること。
        '''
        super().__init__(**kwargs)

        # イベント発生中フラグをFalseにする
        self.occuring = False


    def start(self, eventFileName:str) -> None:
        '''
        イベント開始メソッド\n
        引数に指定されたイベントのjsonファイルを読み込み、イベント発生中フラグをTrueにする。
        '''
        # イベントのjsonファイルオープン
        f = open(os.path.dirname(__file__) + '/testevent.json', 'r')

        # イベントのjsonファイルロード
        self.eventData = json.load(f)

        # イベントの最初（キーが"init"）のエントリデータを取得
        self.entryData = self.getEntryData("init")

        # イベント発生中フラグをTrueにする
        self.occuring = True


    def getEntryData(self, key) -> dict:
        '''
        指定されたキーのエントリーデータをイベントデータから検索して返却する\n
        イベントデータに存在しないキーを指定された場合は、イベント終了コマンドのエントリーデータを返却する。\n
        呼び出し元では、エラーを回避するため、以下の手順で呼び出すこと。\n
            self.getEntryData(self.entryData.get("keyvalue"))
        '''
        if key == None:
            return {"command":"end", "args":{}}
        else:
            return self.eventData.get(key, {"command":"end", "args":{}})


    def update(self) -> None:
        '''
        １ループごとの処理を行う\n
        occuringがFalseの時は、何もせずに終了する。\n
        occuringがTrueの時は、entryDataのコマンドを実行する。\n
        '''
        if self.occuring == False:
            return

        # エントリーデータのコマンドと引数からメソッドを呼び出す\n
        eval("self.update_" + self.entryData["command"])(self.entryData["args"])
        

    def update_end(self, *args) -> None:
        '''
        イベント終了コマンド\n
        イベント発生中フラグをFalseにする
        '''
        self.occuring = False


    def update_judgeFlg(self, args) -> None:
        '''
        フラグ判定コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"flgNo" : フラグNo\n
        ・"on" : フラグがONのときに実行するエントリー名\n
        ・"off" : フラグがOFFのときに実行するエントリー名
        '''
        print(f"called:update_judgeFlg({args})")

        # プラグ判定
        if self.flg[int(args["flgNo"])] == 1:
            # 次のエントリーデータをセット
            self.entryData = self.getEntryData(args.get("on"))
        else:
            # 次のエントリーデータをセット
            self.entryData = self.getEntryData(args.get("off"))


    def update_loadPicture(self, args) -> None:
        '''
        画像ロードコマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"fileName" : ロードするファイル名
        ・"next"：次のイベント識別子
        '''
        print(f"called:update_loadPicture({args})")

        # 画像ロード
        # ここではロードするファイル名を表示するのみとする
        print(f"loaded:{args}")

        # 次のエントリーデータをセット
        self.entryData = self.getEntryData(args.get("next"))


    def update_printMessage(self, args) -> None:
        '''
        メッセージ表示コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"message"：メッセージのリスト
        ・"next"：次のイベントの識別子
        '''
        print(f"called:update_printMessage({args})")

        # メッセージを表示
        # ここではすべてのメッセージを表示する
        for v in args["message"]:
            print(f"message:{v}")

        # 次のエントリーデータをセット
        # 実装時はメッセージクラスの終了状態を判定し、次のエントリーデータをセットする
        self.entryData = self.getEntryData(args.get("next"))


    def update_chooseMessage(self, args) -> None:
        '''
        選択メッセージ表示コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"message"：選択肢のリスト
        ・"next"：次のイベントの識別子
        '''
        print(f"called:update_chooseMessage({args})")

        # メッセージを表示
        # ここではすべてのメッセージを表示する
        for v in args["choose"]:
            print(f"message:[{v['key']}]{v['message']}")

        # 次のエントリーデータをセット
        # 実装時はメッセージクラスの終了状態を判定し、次のエントリーデータをセットする
        self.entryData = self.getEntryData(args.get("choose")[0].get("next"))


    def update_setFlg(self, args) -> None:
        '''
        フラグ設定コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"flgNo"：設定対象のフラグNo
        ・"value"：フラグ設定値
        ・"next"：次のイベントの識別子
        '''
        print(f"called:update_setFlg({args})")

        # フラグセット
        print(f"FlgNo:{args['flgNo']} value:{args['value']}")

        # 次のエントリーデータをセット
        self.entryData = self.getEntryData(args.get("next"))


ev = event()
ev.start("testevent.json")

# ゲームループを想定したループ
while ev.occuring != False:
    ev.update()
