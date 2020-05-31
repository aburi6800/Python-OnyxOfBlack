# -*- coding: utf-8 -*-
import const

"""
3D MAZE WRITE TEST
"""

# 方向
const.DIRECTION_NORTH = 0
const.DIRECTION_EAST = 1
const.DIRECTION_SOUTH = 2
const.DIRECTION_WEST = 3

# 方向に対する増分
vx = ( 0, 1, 0,-1)
vy = (-1, 0, 1, 0)

# 自分の位置と方向からマップのどこを参照するかを、参照順に定義
# 参照順のイメージは以下（上向きである前提、自分の位置は9とする）
# |0|1|2|3|4|
#   |5|6|7|
#   |8|9|A|
# ※正面（6）が壁の場合は5から処理
# ※正面（6）が壁でない場合は0から処理
pos_x = (
    (-2,-1, 0, 1, 2,-1, 0, 1,-1, 0, 1),
    ( 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0),
    ( 2, 1, 0,-1,-2, 1, 0,-1, 1, 0,-1),
    ( 2,-2,-2,-2,-2,-1,-1,-1, 0, 0, 0)
)
pos_y = (
    (-2,-2,-2,-2,-2,-1,-1,-1, 0, 0, 0),
    (-2,-1, 0, 1, 2,-1, 0, 1,-1, 0, 1),
    ( 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0),
    ( 2, 1, 0,-1,-2, 1, 0,-1, 1, 0,-1)
)

# 自分の最初の座標と方向
x = 1
y = 1
direction = const.DIRECTION_SOUTH

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

# テスト：表示元となるデータを画面に表示
for i in range(0, 11):
    map_x = x + pos_x[direction][i]
    map_y = y + pos_y[direction][i]
    if map_x < 0 or map_x > 15 or map_y < 0 or map_y > 15:
        data = "1"
    else:
        data = map[map_y][map_x]

    print(str(map_x) + ":" + str(map_y) + "=" + str(data))
    

