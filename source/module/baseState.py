# -*- coding: utf-8 -*-
from os import name

import pyxel
from overrides import EnforceOverrides
from module.character import Character, Human, Monster, playerParty
from module.eventHandler import eventhandler
from module.messageHandler import messagehandler
from module.pyxelUtil import PyxelUtil


class BaseState(EnforceOverrides):
    '''
    各Stateクラス全ての基底クラス\n
    EnforceOverridesを継承
    '''
    # 経過時間
    tick = 0

    # stateStackへの参照
    stateStack = None

    # 描画の座標オフセット
    DRAW_OFFSET_X = 150
    DRAW_OFFSET_Y = 14

    def __init__(self, **kwargs):
        '''
        クラス初期化
        '''
        # stateStackへの参照を設定
        self.stateStack = kwargs.get("stateStack")
        if self.stateStack == None:
            raise ValueError("kwargs `stateStack' is not defined.")

        # 経過時間リセット
        self.tick = 0

    def update(self):
        '''
        各フレームの処理
        '''
        self.tick += 1

        # メッセージハンドラにキューが登録されてる場合は、メッセージハンドラのupdateメソッドを呼んで終了する
        if messagehandler.isEnqueued():
            messagehandler.update()
            return

        # イベントハンドラでイベントが実行中の場合は、イベントハンドラのupdateメソッドを呼んで終了する
        if eventhandler.isExecute:
            eventhandler.update()
            return

        self.update_execute()

    def update_execute(self):
        '''
        各フレームの個別処理\n
        子クラスで個別の処理があれば、このメソッドに実装する
        '''
        pass

    def draw(self):
        '''
        各フレームの描画処理\n
        各Stateで必ず必要な、画面の枠線とプレイヤーキャラクタ、ステータスの描画を行う
        '''
        pyxel.cls(pyxel.COLOR_BLACK)

        # 枠線
        pyxel.rectb(8, 8, 240, 126, pyxel.COLOR_DARKBLUE)
        pyxel.line(128, 8, 128, 132, pyxel.COLOR_DARKBLUE)
        pyxel.line(8, 96, 247, 96, pyxel.COLOR_DARKBLUE)

        # プレイヤーキャラクタの描画位置
        _x = [16, 36, 60, 84, 104]
        _y = [104, 108, 104, 108, 104]

        # プレイヤーキャラクタ描画
        for _idx, _member in enumerate(playerParty.memberList):
            _member = playerParty.memberList[_idx]
            # キャラクタグラフィック
            self.drawCharacter(_member, _x[_idx], _y[_idx])
            # 名前
            PyxelUtil.text(16,  (_idx + 1) * 16 - 2,
                           ["*" + f'{_idx + 1}:' + _member.name], pyxel.COLOR_WHITE)  
            # 体力最大値
            _maxlife_x = _member.maxlife if _member.maxlife <= 100 else 100
            pyxel.rect(16, (_idx + 1) * 16 + 6, _maxlife_x, 3,  pyxel.COLOR_RED)
            # 体力
            _life_x = _member.life if _member.life <= 100 else 100
            pyxel.rect(16, (_idx + 1) * 16 + 6, _life_x, 3,  pyxel.COLOR_DARKBLUE)
            # 経験値
            _exp_x = _member.exp // 2 if _member.exp <= 200 else 100
            pyxel.rect(16, (_idx + 1) * 16 + 9, 100, 1,  pyxel.COLOR_NAVY)
            pyxel.rect(16, (_idx + 1) * 16 + 9, _exp_x, 1,  pyxel.COLOR_LIGHTBLUE)

    def onEnter(self):
        '''
        状態開始時の処理
        '''
        # タイマーカウンタ初期化
        self.tick = 0

    def onExit(self):
        '''
        状態終了時の処理\n
        実装なし
        '''
        pass

    @staticmethod
    def drawCharacter(_chr: Character, _x: int, _y: int):
        '''
        キャラクターグラフィックの描画を行う。\n
        Characterクラスのインスタンスと、表示位置を渡すと装備等に合わせて描画する。\n
        Humanクラスの場合は装備を組み合わせたパターンを表示する。\n
        Monsterクラスの場合はパターンをそのまま表示する。
        '''
        if isinstance(_chr, Human):
            # 頭
            if _chr.helmet == None:
                _head_x = (_chr.head % 32) * 8
                _head_y = (_chr.head // 32) * 8
                _head_w = 8
                _head_h = 8
            else:
                _head_x = _chr.helmet.blt_x
                _head_y = _chr.helmet.blt_y
                _head_w = _chr.helmet.blt_w
                _head_h = _chr.helmet.blt_h
            pyxel.blt(_x + 8, _y, 1, _head_x, _head_y, _head_w, _head_h, 0)

            # 体
            if _chr.armor == None:
                _armor_x = 160 + _chr.body * 8
                _armor_y = 32
                _armor_w = 8
                _armor_h = 16
            else:
                _armor_x = _chr.armor.blt_x
                _armor_y = _chr.armor.blt_y
                _armor_w = _chr.armor.blt_w
                _armor_h = _chr.armor.blt_h
            pyxel.blt(_x + 8, _y + 8, 1, _armor_x, _armor_y, _armor_w, _armor_h, 0)

            # 武器
            if _chr.weapon != None:
                _weapon_x = _chr.weapon.blt_x
                _weapon_y = _chr.weapon.blt_y
                _weapon_w = _chr.weapon.blt_w
                _weapon_h = _chr.weapon.blt_h
                pyxel.blt(_x, _y, 1, _weapon_x, _weapon_y, _weapon_w, _weapon_h, 0)

            # 盾
            if _chr.shield != None:
                _shield_x = _chr.shield.blt_x
                _shield_y = _chr.shield.blt_y
                _shield_w = _chr.shield.blt_w
                _shield_h = _chr.shield.blt_h
                pyxel.blt(_x + 8, _y + 8, 1, _shield_x, _shield_y, _shield_w, _shield_h, 0)

        elif isinstance(_chr, Monster):
            pyxel.blt(_x, _y, 2, _chr.blt_x, _chr.blt_y, _chr.blt_w, _chr.blt_h, 0)
