# -*- coding: utf-8 -*-

#import module.const
import tkinter
#from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageChops
from PIL import Image, ImageTk, ImageDraw

"""
3D MAZE WRITE TEST
"""

# 方向
DIRECTION_NORTH = 0
DIRECTION_EAST = 1
DIRECTION_SOUTH = 2
DIRECTION_WEST = 3

# 方向に対する増分
vx = ( 0, 1, 0,-1)
vy = (-1, 0, 1, 0)

# 自分の位置と方向からマップのどこを参照するかを、参照順に定義
# 参照順のイメージは以下（上向きである前提、自分の位置はCとする）
# |0|1|2|3|4|
#   |5|6|7|
#   |8|9|A|
#   |B|C|D|
# ※正面(6)が壁の場合は5から処理
# ※正面(9)が壁の場合は8から処理
# ※上記以外の場合は0から処理
pos_x = (
    (-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0),
    ( 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
    ( 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0),
    (-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0)
)
pos_y = (
    (-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0),
    (-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0),
    ( 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
    ( 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0)
)

# 自分の最初の座標と方向
x = 1
y = 1
direction = DIRECTION_SOUTH

# マップ
# 0 = 通路
# 1 = 壁
# 外周は必ず壁とする
map = [
    [ 1, 1, 1, 1, 1],
    [ 1, 0, 1, 0, 1],
    [ 1, 0, 1, 0, 1],
    [ 1, 0, 0, 0, 1],
    [ 1, 1, 1, 1, 1]
]
""" map = [
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [ 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [ 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [ 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [ 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [ 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [ 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1],
    [ 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [ 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [ 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [ 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [ 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
 """

# 壁を描く
def drawWall(num, img):
    wall_front = ()
    wall_side = ()
    
    if num == 0:
        wall_front = (( 8, 40), (24, 40), (24, 56), ( 8, 56))
        wall_side = ((24, 40), (40, 48), (24, 56))
    elif num == 1:
        wall_front = ((24, 40), (40, 40), (40, 56), (24, 56))
        wall_side = ((40, 40), (48, 48), (40, 56))
    elif num == 2:
        wall_front = ((72, 40), (88, 40), (88, 56), (72, 56))
        wall_side = ((56, 40), (56, 56), (48, 48))
    elif num == 3:
        wall_front = ((56, 40), (72, 40), (72, 56), (56, 56))
        wall_side = ((56, 40), (56, 56), (48, 48))
    elif num == 4:
        wall_front = ((40, 40), (56, 40), (56, 56), (40, 56))
        wall_side = ()

    elif num == 5:
        wall_front = (( 0, 24), (24, 24), (24, 72), ( 0, 72))
        wall_side = ((24, 24), (40, 40), (40, 56), (24, 72))
    elif num == 6:
        wall_front = ((72, 24), (96, 24), (96, 72), (72, 72))
        wall_side = ((56, 40), (72, 24), (72, 72), (56, 56))
    elif num == 7:
        wall_front = ((24, 24), (72, 24), (72, 72), (24, 72))
        wall_side = ()

    elif num == 8:
        wall_front = (( 0,  8), ( 8,  8), ( 8, 88), ( 0, 88))
        wall_side = (( 8,  8), (24, 24), (24, 72), ( 8, 88))
    elif num == 9:
        wall_front = ((88,  8), (96,  8), (96, 88), (88, 88))
        wall_side = ((72, 24), (88,  8), (88, 88), (72, 72))
    elif num == 10:
        wall_front = (( 8,  8), (88,  8), (88, 88), ( 8, 88))
        wall_side = ()

    elif num == 11:
        wall_front = ()
        wall_side = (( 0,  0), ( 8,  8), ( 8, 88), ( 0, 96))
    elif num == 12:
        wall_front = ()
        wall_side = ((88,  8), (96,  0), (96, 96), (88, 88))
    elif num == 13:
        wall_front = (( 8,  8), (88,  8), (88, 88), ( 8, 88))
        wall_side = ()

    draw = ImageDraw.Draw(img)
    if len(wall_front) > 0:
        draw.polygon(wall_front, (0x00, 0xFF, 0xFF))
    if len(wall_side) > 0:
        draw.polygon(wall_side , (0x00, 0x00, 0xFF))


def main():
    root.after(50, main)


# テスト：ウィンドウに表示
SCREEN_WIDTH = 12
SCREEN_HEIGHT = 12

root = tkinter.Tk()
root.geometry(str(SCREEN_WIDTH * 8 * 4) + "x" + str(SCREEN_HEIGHT * 8 * 4))
root.title("3D MAZE")

# Canvas生成
canvas = tkinter.Canvas(width = (SCREEN_WIDTH * 8 * 4), height = (SCREEN_HEIGHT * 8 * 4))
canvas.pack()

# ベースとなる画像
img = Image.new("RGB", (SCREEN_WIDTH * 8, SCREEN_HEIGHT * 8), (0x00, 0x00, 0x00))
draw = ImageDraw.Draw(img)
draw.line((( 0, 48), (96, 48)), (0x00, 0x00, 0xFF), 1)
draw.line((( 0, 56), (96, 56)), (0x00, 0x00, 0xFF), 1)
draw.line((( 0, 72), (96, 72)), (0x00, 0x00, 0xFF), 1)
draw.line(((48, 48), ( 0, 96)), (0x00, 0x00, 0xFF), 1)
draw.line(((48, 48), (96, 96)), (0x00, 0x00, 0xFF), 1)

# テスト：マップデータを取得して描画
for i in range(14):
    map_x = x + pos_x[direction][i]
    map_y = y + pos_y[direction][i]
    if map_x < 0 or map_x > 15 or map_y < 0 or map_y > 15:
        data = 1
    else:
        data = map[map_y][map_x]

    if data == 1:
        drawWall(i, img)

    print("[" + str(i) + "]" + str(map_x) + ":" + str(map_y) + "=" + str(data))

img = img.resize((img.width * 4, img.height * 4), Image.NEAREST)


# PhotoImage生成
photoImage = ImageTk.PhotoImage(img)
canvas.create_image((img.width / 2, img.height / 2), image = photoImage, tag = "SCREEN")

# メイン処理
main()

# ウィンドウイベントループ実行
root.mainloop()
