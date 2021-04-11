import os
import sys

import pyxel

class App:

    def __init__(self):

        # 表示オブジェクト辞書データ
        # Key : フレーム数
        # Value : 横位置、種別("text", "img")、値の辞書データ("text"={"value", "col"}, "blt"={"img", "u", "v", "w", "h"})
        self.roll_objects = {
            10 : [80, "text", {"value":"THE ONYX OF BLACK", "color":pyxel.COLOR_RED}],
            110 : [80, "text", {"value":"STAFF", "color":pyxel.COLOR_ORANGE}],
            210 : [80, "text", {"value":"PRODUCER", "color":pyxel.COLOR_YELLOW}],
            240 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            310 : [80, "text", {"value":"MUSIC PRODUCER", "color":pyxel.COLOR_YELLOW}],
            340 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            440 : [80, "text", {"value":"PROGRAM", "color":pyxel.COLOR_ORANGE}],
            540 : [80, "text", {"value":"MAIN PROGRAM", "color":pyxel.COLOR_YELLOW}],
            570 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            640 : [80, "text", {"value":"BATTLE PROGRAM", "color":pyxel.COLOR_YELLOW}],
            670 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            740 : [80, "text", {"value":"UTILITIES", "color":pyxel.COLOR_YELLOW}],
            770 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            870 : [80, "text", {"value":"DIRECTOR", "color":pyxel.COLOR_YELLOW}],
            900 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            970 : [80, "text", {"value":"MUSIC DIRECTOR", "color":pyxel.COLOR_YELLOW}],
            1000 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1070 : [80, "text", {"value":"SOUND DIRECTOR", "color":pyxel.COLOR_YELLOW}],
            1100 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            1200 : [80, "text", {"value":"DESIGN", "color":pyxel.COLOR_ORANGE}],
            1300 : [80, "text", {"value":"CHARACTER DESIGN", "color":pyxel.COLOR_YELLOW}],
            1330 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1400 : [80, "text", {"value":"GRAPHIC DESIGN", "color":pyxel.COLOR_YELLOW}],
            1430 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1500 : [80, "text", {"value":"SYSTEM DESIGN", "color":pyxel.COLOR_YELLOW}],
            1530 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1600 : [80, "text", {"value":"MAP DESIGN", "color":pyxel.COLOR_YELLOW}],
            1630 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            1730 : [80, "text", {"value":"STORY", "color":pyxel.COLOR_YELLOW}],
            1760 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],
            1830 : [80, "text", {"value":"SCRIPT", "color":pyxel.COLOR_YELLOW}],
            1860 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            1960 : [80, "text", {"value":"MUSIC COMPOSED BY", "color":pyxel.COLOR_YELLOW}],
            1990 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            2060 : [80, "text", {"value":"DEBUGGER", "color":pyxel.COLOR_YELLOW}],
            2090 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_WHITE}],

            2160 : [80, "text", {"value":"SPECIAL THANKS", "color":pyxel.COLOR_YELLOW}],
            2190 : [124, "text", {"value":"@info_ymcat", "color":pyxel.COLOR_WHITE}],

            2390 : [80, "text", {"value":"CAST", "color":pyxel.COLOR_ORANGE}],
            2490 : [80, "img", {"img":2, "u":96, "v":0, "w":16, "h":16}],
            2498 : [148, "text", {"value":"WOLF", "color":pyxel.COLOR_WHITE}],
            2540 : [80, "img", {"img":2, "u":0, "v":0, "w":16, "h":8}],
            2548 : [152, "text", {"value":"BAT", "color":pyxel.COLOR_WHITE}],
            2590 : [80, "img", {"img":2, "u":16, "v":0, "w":16, "h":16}],
            2598 : [140, "text", {"value":"KOBOLD", "color":pyxel.COLOR_WHITE}],
            2640 : [80, "img", {"img":2, "u":48, "v":0, "w":16, "h":16}],
            2648 : [140, "text", {"value":"ZOMBIE", "color":pyxel.COLOR_WHITE}],
            2690 : [80, "img", {"img":2, "u":32, "v":0, "w":16, "h":16}],
            2698 : [136, "text", {"value":"SKELTON", "color":pyxel.COLOR_WHITE}],
            2740 : [80, "img", {"img":2, "u":80, "v":0, "w":16, "h":16}],
            2748 : [140, "text", {"value":"GOBLIN", "color":pyxel.COLOR_WHITE}],
            2790 : [80, "img", {"img":2, "u":64, "v":0, "w":16, "h":16}],
            2798 : [144, "text", {"value":"AZTEC", "color":pyxel.COLOR_WHITE}],
            2840 : [80, "img", {"img":2, "u":112, "v":0, "w":16, "h":16}],
            2848 : [148, "text", {"value":"LION", "color":pyxel.COLOR_WHITE}],
            2890 : [80, "img", {"img":2, "u":192, "v":0, "w":16, "h":16}],
            2898 : [144, "text", {"value":"MUMMY", "color":pyxel.COLOR_WHITE}],
            2940 : [80, "img", {"img":2, "u":176, "v":0, "w":16, "h":16}],
            2948 : [152, "text", {"value":"ORC", "color":pyxel.COLOR_WHITE}],
            2990 : [80, "img", {"img":2, "u":128, "v":0, "w":16, "h":16}],
            2998 : [144, "text", {"value":"SLIME", "color":pyxel.COLOR_WHITE}],
            3040 : [80, "img", {"img":2, "u":144, "v":0, "w":16, "h":16}],
            3048 : [140, "text", {"value":"SPIDER", "color":pyxel.COLOR_WHITE}],

            3400 : [89, "img", {"img":0, "u":0, "v":72, "w":76, "h":21}],
            3460 : [89, "img", {"img":0, "u":0, "v":120, "w":75, "h":31}],

            3700 : [80, "text", {"value":"PRESENTED BY", "color":pyxel.COLOR_ORANGE}],
            3730 : [132, "text", {"value":"ABURI6800", "color":pyxel.COLOR_YELLOW}],
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
#        pyxel.image(0).load(0, 72, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../assets/python.png")))
#        pyxel.image(0).load(0, 120, os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../assets/pyxel.png")))
        pyxel.image(0).load(0, 72, os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/python.png")))
        pyxel.image(0).load(0, 120, os.path.normpath(os.path.join(os.path.dirname(__file__), "../assets/pyxel.png")))
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

                # y座標 < -100 の場合、リストから除去
                if _item[0] < -100:
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
