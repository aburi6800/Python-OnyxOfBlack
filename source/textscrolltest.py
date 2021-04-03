import os
import sys

import pyxel

class App:

    def __init__(self):

        # 表示オブジェクト辞書データ
        # Key : フレーム数
        # Value : 横位置、種別("text", "img")、値の辞書データ("text"={"value", "col"}, "blt"={"img", "u", "v", "w", "h"})
        self.roll_objects = {
            60 : [80, "text", {"value":"PRODUCER", "color":pyxel.COLOR_CYAN}],
            100 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            160 : [80, "text", {"value":"MUSIC PRODUCER", "color":pyxel.COLOR_CYAN}],
            200 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            360 : [80, "text", {"value":"PROGRAM", "color":pyxel.COLOR_CYAN}],
            460 : [80, "text", {"value":"MAIN PROGRAM", "color":pyxel.COLOR_CYAN}],
            500 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            560 : [80, "text", {"value":"BATTLE PROGRAM", "color":pyxel.COLOR_CYAN}],
            600 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            660 : [80, "text", {"value":"UTILITIES", "color":pyxel.COLOR_CYAN}],
            700 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            860 : [80, "text", {"value":"DIRECTOR", "color":pyxel.COLOR_CYAN}],
            900 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            960 : [80, "text", {"value":"MUSIC DIRECTOR", "color":pyxel.COLOR_CYAN}],
            1000 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1060 : [80, "text", {"value":"SOUND DIRECTOR", "color":pyxel.COLOR_CYAN}],
            1100 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            1260 : [80, "text", {"value":"DESIGN", "color":pyxel.COLOR_CYAN}],
            1360 : [80, "text", {"value":"CHARACTER DESIGN", "color":pyxel.COLOR_CYAN}],
            1400 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1460 : [80, "text", {"value":"GRAPHIC DESIGN", "color":pyxel.COLOR_CYAN}],
            1500 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1560 : [80, "text", {"value":"SYSTEM DESIGN", "color":pyxel.COLOR_CYAN}],
            1600 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1660 : [80, "text", {"value":"MAP DESIGN", "color":pyxel.COLOR_CYAN}],
            1700 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            1860 : [80, "text", {"value":"STORY", "color":pyxel.COLOR_CYAN}],
            1900 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1960 : [80, "text", {"value":"SCRIPT", "color":pyxel.COLOR_CYAN}],
            2000 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            2160 : [80, "text", {"value":"MUSIC COMPOSED BY", "color":pyxel.COLOR_CYAN}],
            2200 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            2360 : [80, "text", {"value":"DEBUGGER", "color":pyxel.COLOR_CYAN}],
            2400 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            2600 : [51, "img", {"img":0, "u":0, "v":72, "w":152, "h":42}],
            2680 : [52, "img", {"img":0, "u":0, "v":120, "w":150, "h":62}],

            2960 : [80, "text", {"value":"PRESENTED BY", "color":pyxel.COLOR_CYAN}],
            3000 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
        }

        # 表示中オブジェクトリスト
        self.disp_objects = []

        # フレームカウント
        self.frame_count = 0

        # 終了フレーム数
        print(max(self.roll_objects))
        self.end_frame_count = max(self.roll_objects) + 500
        print(self.end_frame_count)

        # Pyxel初期化
        pyxel.init(256, 192)
        pyxel.load("../assets/onyxofblack.pyxres")
#        pyxel.image(0).load(0, 72, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../images/python.png")))
#        pyxel.image(0).load(0, 120, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../images/pyxel.png")))
        pyxel.image(0).load(0, 72, os.path.normpath(os.path.join(os.path.dirname(__file__), "../images/python.png")))
        pyxel.image(0).load(0, 120, os.path.normpath(os.path.join(os.path.dirname(__file__), "../images/pyxel.png")))
        pyxel.run(self.update, self.draw)

        # 画像をロード

    def update(self):

        # フレームカウントをインクリメント
        self.frame_count += 1

        # フレームカウントが終了フレーム数を超える場合は終了
        if self.frame_count > self.end_frame_count:
            sys.exit()
        
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

                # y座標 < -20 の場合、リストから除去
                if _item[0] < -20:
                    del self.disp_objects[_idx]

    def draw(self):

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

if __name__ == "__main__":
    '''
    アプリケーション実行
    '''
    App()
