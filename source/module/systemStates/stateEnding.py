import os

import pyxel
from module.systemStates.baseSystemState import BaseSystemState
from overrides import overrides


class StateEnding(BaseSystemState):
    '''
    エンディングクラス\n
    BaseSystemStateを継承。\n
    エンディング画面、スタッフロールの表示を行い、タイトルに戻す。
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # スタッフロールのカウンタ
        self.cnt = 0

        # 表示オブジェクト辞書データ
        # Key : フレーム数
        # Value : 横位置、種別("text", "img")、値の辞書データ("text"={"value", "col"}, "blt"={"img", "u", "v", "w", "h"})
        self.roll_objects = {
            self.getCnt(40) : [80, "text", {"value":"THE ONYX OF BLACK", "color":pyxel.COLOR_RED}],

            self.getCnt(40) : [80, "text", {"value":"STAFF", "color":pyxel.COLOR_RED}],

            self.getCnt(100) : [80, "text", {"value":"PRODUCER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"DIRECTOR", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(80) : [80, "text", {"value":"GAME DIRECTOR", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"ART DIRECTOR", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"SOUND AND MUSIC DIRECTOR", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"PROGRAM", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(80) : [80, "text", {"value":"MAIN PROGRAMMER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"BATTLE PROGRAMMER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"EVENT PROGRAMMER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"DESIGN", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(80) : [80, "text", {"value":"SYSTEM DESIGNNER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"MAP DESIGNNER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"GRAPHIC DESIGNNER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"CHARACTER DESIGNNER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"FONT DESIGNNER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"SCENARIO", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(80) : [80, "text", {"value":"SCREENPLAY BY", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"SCRIPT BY", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"MUSIC AND SOUND", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(80) : [80, "text", {"value":"MUSIC COMPOSER", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            self.getCnt(80) : [80, "text", {"value":"SOUND EFFECTS", "color":pyxel.COLOR_YELLOW}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"MANUAL WRITTEN BY", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"DEBUGGER", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"DEBUGGER", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"SPECIAL THANKS TO", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(40) : [140, "text", {"value":"@doc100", "color":pyxel.COLOR_WHITE}],
            self.getCnt(40) : [124, "text", {"value":"@info_ymcat", "color":pyxel.COLOR_WHITE}],
            self.getCnt(40) : [132, "text", {"value":"@hiromasa", "color":pyxel.COLOR_WHITE}],
            self.getCnt(40) : [120, "text", {"value":"@feilong5000", "color":pyxel.COLOR_WHITE}],

            self.getCnt(100) : [80, "text", {"value":"CAST", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":96, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [148, "text", {"value":"WOLF", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":0, "v":0, "w":16, "h":8}],
            self.getCnt(8) : [152, "text", {"value":"BAT", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":16, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [140, "text", {"value":"KOBOLD", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":48, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [140, "text", {"value":"ZOMBIE", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":32, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [136, "text", {"value":"SKELTON", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":80, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [140, "text", {"value":"GOBLIN", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":64, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"AZTEC", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":112, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [148, "text", {"value":"LION", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":192, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"MUMMY", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":176, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [152, "text", {"value":"ORC", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":128, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"SLIME", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":144, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [140, "text", {"value":"SPIDER", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":160, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"GHOUL", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":96, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"COBRA", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":224, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"BLAAB", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":32, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [136, "text", {"value":"VAMPIRE", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":208, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [148, "text", {"value":"OGRE", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":240, "v":0, "w":16, "h":16}],
            self.getCnt(8) : [128, "text", {"value":"HOBGOBLIN", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":48, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [140, "text", {"value":"WIRKAT", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":112, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"BEAST", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":144, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"HIDER", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":80, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"DEMON", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":64, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"GHOST", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":128, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [144, "text", {"value":"TROLL", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":160, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [148, "text", {"value":"MIER", "color":pyxel.COLOR_WHITE}],
            self.getCnt(50) : [80, "img", {"img":2, "u":176, "v":16, "w":16, "h":16}],
            self.getCnt(8) : [140, "text", {"value":"WRAITH", "color":pyxel.COLOR_WHITE}],
            self.getCnt(60) : [80, "img", {"img":2, "u":192, "v":16, "w":32, "h":32}],
            self.getCnt(8) : [140, "text", {"value":"TAURUS", "color":pyxel.COLOR_WHITE}],
            self.getCnt(60) : [80, "img", {"img":2, "u":216, "v":16, "w":32, "h":32}],
            self.getCnt(8) : [144, "text", {"value":"GIANT", "color":pyxel.COLOR_WHITE}],
            self.getCnt(70) : [80, "img", {"img":2, "u":0, "v":16, "w":32, "h":32}],
            self.getCnt(8) : [140, "text", {"value":"KRAKEN", "color":pyxel.COLOR_WHITE}],

            self.getCnt(300) : [89, "img", {"img":0, "u":0, "v":72, "w":76, "h":21}],
            self.getCnt(100) : [89, "img", {"img":0, "u":0, "v":120, "w":75, "h":31}],

            self.getCnt(300) : [80, "text", {"value":"PRESENTED BY", "color":pyxel.COLOR_ORANGE}],
            self.getCnt(40) : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_YELLOW}],
        }

        # 表示中オブジェクトリスト
        self.disp_objects = []

        # フレームカウント
        self.frame_count = 0

        # 終了フレーム数算出
        self.end_frame_count = max(self.roll_objects) + 500
        print(str(self.end_frame_count))

        # イメージロード
        pyxel.image(0).load(0, 72, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/png/python.png")))
        pyxel.image(0).load(0, 120, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../assets/png/pyxel.png")))

    def getCnt(self, value:int = 0) -> int:
        '''
        スタッフロールのリストに設定するカウントを取得する
        '''
        self.cnt = self.cnt + value
        return self.cnt

    @overrides
    def update_execute(self):
        '''
        各フレームの個別処理
        '''
        # フレームカウントをインクリメント
        self.frame_count += 1

        # フレームカウントが終了フレーム数を超える場合は終了
        if self.frame_count > self.end_frame_count:
            pyxel.quit()
        
        # フレームカウントをキーに表示オブジェクト辞書をサーチ
        if self.roll_objects.get(self.frame_count) != None:
            # ヒットしたら表示中オブジェクトリストに登録
            # 初期のy座標は193とする
            _obj = [193] + self.roll_objects[self.frame_count]
            self.disp_objects.append(_obj)

        # 表示中オブジェクトリスト全件に対して処理
        for _idx, _item in enumerate(self.disp_objects):

            if pyxel.frame_count % 2 == 0:
                # y座標をデクリメント
                _item[0] -= 1

                # y座標 < -100 の場合、リストから除去
                if _item[0] < -100:
                    del self.disp_objects[_idx]

    @overrides
    def draw(self):
        '''
        各フレームの描画処理
        '''
        # 画面消去
        pyxel.cls(pyxel.COLOR_BLACK)

        # 表示中オブジェクトリスト全件に対して処理
        for _item in self.disp_objects:
            # 表示オブジェクトの情報を取得
            _x = _item[1]
            _cmd = _item[2]
            _value = _item[3]

            #  "text" = 文字列を指定色で表示
            if _cmd == "text":
                pyxel.text(_x, _item[0], _value["value"], _value["color"])

            #  "img"  = イメージバンクの指定座標のイメージを表示
            elif _cmd == "img":
                pyxel.blt(_x, _item[0], _value["img"], _value["u"], _value["v"], _value["w"], _value["h"])
