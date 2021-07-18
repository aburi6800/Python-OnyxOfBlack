# -*- coding: utf-8 -*-
import pygame.mixer
import os

class MusicPlayer():
    '''
    ミュージックプレイヤークラス\n
    インスタンス生成時に指定されたファイルの再生の準備を行う。\n
    updateメソッド内でplayメソッドを呼ぶことでループ再生する。\n
    '''
    playStarted = False     # 再生実行したか
    playStopped = False     # 再生停止したか

    def __init__(self):
        '''
        初期化\n
        '''
        pygame.mixer.init()
    
    def load(self, musicFileName:str = "" ):
        '''
        音楽ファイルロード\n
        ファイルはsource/assets/mp3にあるものとする。
        '''
        filePath = os.path.normpath(os.path.join(
            os.path.dirname(__file__), "../assets/mp3/" + musicFileName))
        pygame.mixer.music.load(filePath)

        self.playStarted == False
        self.playStopped == False

    def play(self, loop:bool=False, looptime:float=0.0):
        '''
        音楽を再生する。\n
        引数にループ後の再生位置（時間）を指定することで、再生終了後に指定位置から繰り返し再生する。\n
        省略時は先頭から繰り返し再生する。
        '''
        # 現在再生中の位置を取得
        pos = pygame.mixer.music.get_pos()

        if int(pos) == -1: # 再生終了
            if loop: #ループ再生ありの場合
                pygame.mixer.music.play(-1, looptime)

            else: # ループ再生なしの場合
                if self.playStarted == False:
                    pygame.mixer.music.play()
                    self.playStarted = True
                    print("play start.")
                    
                else:
                    if self.playStopped == False:
                        pygame.mixer.music.stop()
                        self.playStopped = True
                        print("play stop.")

musicPlayer = MusicPlayer()
