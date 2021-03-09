import json
import os

import pyxel

from module.character import playerParty
from module.messageHandler import messageCommand, messagehandler
from module.state import State

class eventHandler():
    '''
    イベントハンドラー\n
    イベントを発生させるときは、eventhandler.startEventメソッドを呼ぶ。\n
    この際に、イベント定義のjsonファイル名を指定する。\n
    '''
    # 描画の座標オフセット
    DRAW_OFFSET_X = 150
    DRAW_OFFSET_Y = 14

    # イベントデータ
    eventData = {}

    # イベントセクションデータ
    eventSection = {}

    # イベント実行中フラグ
    isExecute = False

    # イベントが発生したStateへの参照
    calledState = None

    def __init__(self) -> None:
        '''
        コンストラクタ\n
        '''
        pass

    def startEvent(self, eventFileName, calledState) -> None:
        '''
        イベントを開始する。\n
        引数にイベントのjsonファイル名と、呼び出し元のState自身を指定する。
        '''

        # ファイル名にパスを追加する
        filePath = os.path.dirname(os.path.abspath(
            __file__)) + "/events/" + eventFileName
        print(f"load json file:{filePath}")

        # イベントのjsonファイルオープン
        f = open(filePath, 'r')

        # イベントのjsonファイルロード
        self.eventData = json.load(f)

        # イベントの最初（キーが"init"）のデータをエントリセクションデータに設定
        self.setNextSection("init")

        # イベント発生中フラグをTrueにする
        self.isExecute = True

        # 呼び出し元のStateへの参照
        self.calledState = calledState

    def getEventSection(self, key: str) -> dict:
        '''
        指定されたセクション名のデータをイベントセクションデータとして返却する。\n
        存在しないセクション名を指定された場合は、イベント終了のイベントセクションデータを返却する。
        '''
        if key == None:
            return {"command": "end", "args": {}}
        else:
            return self.eventData.get(key, {"command": "end", "args": {}})

    def setNextSection(self, sectionName: str) -> None:
        '''
        イベント定義jsonファイルの指定したセクション名に制御を移す。\n
        メッセージに選択肢がある場合、messagcommandからこのメソッドが呼ばれる。
        '''
        self.eventSection = self.getEventSection(sectionName)

    def update(self) -> None:
        '''
        １ループごとの処理を行う\n
        '''
        # イベントセクションデータのコマンドと引数から、各updateメソッドを呼び出す
        eval("self.update_" +
             self.eventSection["command"])(self.eventSection["args"])

    def update_end(self, *args) -> None:
        '''
        イベント終了コマンド\n
        '''
        print("called:update_end()")

        # イベント発生中フラグをFalseにする
        self.isExecute = False

    def update_judgeFlg(self, args) -> None:
        '''
        フラグ判定コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"flgNo" : フラグNo\n
        ・"on" : フラグがONのときに実行するセクション名\n
        ・"off" : フラグがOFFのときに実行するセクション名
        '''
        print(f"called:update_judgeFlg({args})")

        # プラグ判定
        if self.flg[int(args["flgNo"])] == 1:
            # 次のセクションデータをセット
            self.eventSection = self.setNextSection(args.get("on"))
        else:
            # 次のセクションデータをセット
            self.eventSection = self.setNextSection(args.get("off"))

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
        fileName = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/" + args.get("fileName")))
        print(f"loadPicture:{fileName}")
        pyxel.image(0).load(0, 205, fileName)

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_printMessage(self, args) -> None:
        '''
        メッセージ表示コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"message"：リスト形式で、１要素目にメッセージ種別、２要素目に選択キー、メッセージ、選択肢を指定する。複数指定可能。\n
        　　　　　　　　　　　　　　　　種別"M"の場合：メッセージ（文字列 or リスト）を指定する。\n
        　　　　　　　　　　　　　　　　種別"C"の場合：メッセージ（文字列 or リスト）と選択キー、イベント定義jsonファイルの遷移先セクション名を指定する。\n
        ・"next"：イベント定義jsonファイルの次のセクション名。選択肢があるメッセージの場合は設定不要。
        '''
        print(f"called:update_printMessage({args})")

        # メッセージ表示コマンドクラスのインスタンス生成
        cmd = messageCommand()

        # "message"の内容すべてに対してループ処理する
        for m in args["message"]:
            # 種別
            _type = m[0]
            # メッセージ内容
            _message = m[1]

            # 通常のメッセージ
            if _type == "M":
                cmd.addMessage(_message)

            # 選択メッセージ
            if _type == "C":
                # 選択キー
                _chooseKey = m[2]
                # 遷移先のセクション名からコールバックを生成する
                _next = (self.setNextSection, m[3])

                cmd.addChoose(_message, eval(_chooseKey), _next)

        # メッセージキューに登録
        # このあと、messagequeueに制御が移る
        messagehandler.enqueue(cmd)

        # 次のエントリーデータをセットする。
        # messagequeueの処理が終了した後、ここで設定されたentryDataの処理から再開される。
        self.eventSection = self.getEventSection(args.get("next", None))

    def update_setFlg(self, args) -> None:
        '''
        フラグ設定コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"flgNo"：設定対象のフラグNo\n
        ・"value"：フラグ設定値\n
        ・"next"：次のイベントの識別子
        '''
        print(f"called:update_setFlg({args})")

        # フラグセット
        # 仮実装
        print(f"FlgNo:{args['flgNo']} value:{args['value']}")

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_changeState(self, args) -> None:
        '''
        state変更コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"stateName"：変更するstateのENUM値。\n
        ・"next"；次のイベントの識別子
        '''
        print(f"called:update_changeState({args})")

        # state変更
        self.calledState.pushState(eval("State." + args.get("stateName")))

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_setPartyPosition(self, args) -> None:
        '''
        パーティー座標設定コマンド\n
        プレイヤーパーティーの座標を設定する。\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"position"：変更する座標をリストで指定\n
        ・"next"；次のイベントの識別子
        '''
        print(f"called:update_setPartyPosition({args})")

        playerParty.x = args.get("position")[0]
        playerParty.y = args.get("position")[1]

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def draw(self) -> None:
        '''
        画面描画処理
        '''
        # 画像表示
        pyxel.blt(self.DRAW_OFFSET_X + 15,
                  self.DRAW_OFFSET_Y + 15, 0, 0, 205, 50, 50)


eventhandler = eventHandler()
