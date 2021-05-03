import json
import os

import pyxel

from module.character import playerParty
from module.messageHandler import messageCommand, messagehandler
from module.state import State # update_pushState で使用
from module.direction import Direction # update_setPartyPosition で使用


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

    # 画像ロード済フラグ
    isPictureLoaded = False

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
        filePath = os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/json/" + eventFileName))
        if __debug__:
            print(f"load json file:{filePath}")

        # イベントのjsonファイルオープン
        f = open(filePath, 'r')

        # イベントのjsonファイルロード
        self.eventData = json.load(f)

        # イベントの最初（キーが"init"）のデータをエントリセクションデータに設定
        self.setNextSection("init")

        # イベント発生中フラグをTrueにする
        self.isExecute = True

        # 画像ロード済フラグをFalseにする
        self.isPictureLoaded = False

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
            if self.eventData.get(key, None) == None:
                if __debug__:
                    print("section key " + key + " not found.")
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
        if __debug__:
            print("called : eventHandler.update")
        
        # イベントセクションデータのコマンドと引数から、各updateメソッドを呼び出す
        eval("self.update_" +
             self.eventSection["command"])(self.eventSection["args"])

    def update_end(self, *args: dict) -> None:
        '''
        イベント終了コマンド\n
        引数は不要。
        '''
        if __debug__:
            print("called : update_end()")

        # イベント発生中フラグをFalseにする
        self.isExecute = False

    def update_judgeFlg(self, args: dict) -> None:
        '''
        フラグ判定コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"flgNo" : フラグNo\n
        ・"on" : フラグがONのときに実行するセクション名\n
        ・"off" : フラグがOFFのときに実行するセクション名
        '''
        if __debug__:
            print(f"called : update_judgeFlg({args})")

        # プラグ判定
        if playerParty.eventFlg[args.get("flgNo")] == 1:
            # 次のセクションデータをセット
            self.eventSection = self.getEventSection(args.get("on"))
        else:
            # 次のセクションデータをセット
            self.eventSection = self.getEventSection(args.get("off"))

    def update_loadPicture(self, args: dict) -> None:
        '''
        画像ロードコマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"fileName" : ロードするファイル名
        ・"next"：次のイベント識別子
        '''
        if __debug__:
            print(f"called : update_loadPicture({args})")

        # 画像ロード
        # ここではロードするファイル名を表示するのみとする
        fileName = os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/png/" + args.get("fileName")))
        print(f"loadPicture:{fileName}")
        pyxel.image(0).load(0, 205, fileName)

        # 画像ロード済フラグをTrueに設定
        self.isPictureLoaded = True

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_printMessage(self, args: dict) -> None:
        '''
        メッセージ表示コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"message"：リスト形式で、１要素目にメッセージ種別、２要素目に選択キー、メッセージ、選択肢を指定する。複数指定可能。\n
        　　　　　　　　　　　　　　　　種別"M"の場合：メッセージ（文字列 or リスト）を指定する。\n
        　　　　　　　　　　　　　　　　種別"C"の場合：メッセージ（文字列 or リスト）と選択キー、イベント定義jsonファイルの遷移先セクション名を指定する。\n
        ・"next"：イベント定義jsonファイルの次のセクション名。選択肢があるメッセージの場合は設定不要。
        '''
        if __debug__:
            print(f"called : update_printMessage({args})")

        # メッセージ表示コマンドクラスのインスタンス生成
        cmd = messageCommand()

        # "message"の内容すべてに対してループ処理する
        for m in args["message"]:
            # 種別
            _type = m[0]

            # メッセージ内容
            _message = m[1]

            # メッセージ色、指定がない場合（=リストの長さ<2）の場合は白を指定する。
            if len(m) < 3:
                _color = pyxel.COLOR_WHITE
            else:
                _color = eval(m[2])

            # 通常のメッセージ
            if _type == "M":
                cmd.addMessage(_message, _color)

            # 選択メッセージ
            if _type == "C":
                # 選択キー
                _chooseKey = eval(m[2])
                # 遷移先のセクション名からコールバックを生成する
                _next = (self.setNextSection, m[3])

                cmd.addChoose(_message, _chooseKey, _next)

        # メッセージキューに登録
        # このあと、messagequeueに制御が移る
        messagehandler.enqueue(cmd)

        # 次のエントリーデータをセットする。
        # messagequeueの処理が終了した後、ここで設定されたentryDataの処理から再開される。
        self.eventSection = self.getEventSection(args.get("next", None))

    def update_setFlg(self, args: dict) -> None:
        '''
        フラグ設定コマンド\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"flgNo"：設定対象のフラグNo\n
        ・"value"：フラグ設定値\n
        ・"next"：次のイベントの識別子
        '''
        if __debug__:
            print(f"called : update_setFlg({args})")

        # フラグセット
        print("FlgNo:" + str(args.get("flgNo")) + " value:" + str(args.get("value")))
        playerParty.eventFlg[args.get("flgNo")] = args.get("value")

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_pushState(self, args: dict) -> None:
        '''
        state変更コマンド(push)\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"stateName"：変更するstateのENUM値。\n
        ・"next"；次のイベントの識別子
        '''
        if __debug__:
            print(f"called : update_pushState({args})")

        # stateのpush
        self.calledState.stateStack.push(eval("State." + args.get("stateName")))

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_popState(self, args: dict) -> None:
        '''
        state変更コマンド(pop)\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"next"；次のイベントの識別子
        '''
        if __debug__:
            print(f"called : update_popState({args})")

        # stateのpop
        self.calledState.stateStack.pop()

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_setPartyPosition(self, args: dict) -> None:
        '''
        パーティー座標設定コマンド\n
        プレイヤーパーティーの座標を設定する。\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"position"：変更する座標をリストで指定（x座標、y座標の順）\n
        ・"direction"：省略可能。変更する方向をNORTH,SOUTH,WEST,EASTの文字列で指定\n
        ・"next"；次のイベントの識別子
        '''
        if __debug__:
            print(f"called : update_setPartyPosition({args})")

        playerParty.saveCondition()
        playerParty.x = args.get("position")[0]
        playerParty.y = args.get("position")[1]
        if args.get("direction") != None:
            playerParty.direction = eval("Direction." + args.get("direction"))

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def update_encountMonster(self, args: dict) -> None:
        '''
        モンスターと遭遇するコマンド\n
        モンスターパーティーを生成し、呼び出し元のStateのisEncountをtrueに設定する。\n
        呼び出し元のStateではstateBattleがpushされ、戦闘中はこのクラスのupdateメソッドは呼び出されなくなる。\n
        戦闘が終了すると、呼び出し元StateのisEncountがFalseとなり、イベントハンドラでの処理が再開される。\n
        引数は以下の要素を設定した辞書型とする。\n
        ・"monsterName"：モンスターのEnum値、省略された場合はモンスターのリスト(各Stateのenemy_set)からランダムで指定される
        ・"next"：次のイベントの識別子
        '''
        if __debug__:
            print(f"called : update_encountMonster({args})")

        _monsterName = args.get("monsterName")
        if _monsterName == None or _monsterName == "":
            self.calledState.encount_enemy()
        else:
            self.calledState.encount_enemy(_monsterName)

        # 次のエントリーデータをセット
        self.eventSection = self.getEventSection(args.get("next"))

    def draw(self) -> None:
        '''
        画面描画処理
        '''
        # 画像ロード済の場合、画像を表示
        if self.isPictureLoaded:
            pyxel.blt(self.DRAW_OFFSET_X + 15,
                    self.DRAW_OFFSET_Y + 15, 0, 0, 205, 50, 50)


eventhandler = eventHandler()
