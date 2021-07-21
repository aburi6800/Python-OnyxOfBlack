# -*- coding: utf-8 -*-
import pygame.mixer
import os

class MusicPlayer():
    '''
    ミュージックプレイヤークラス\n
    インスタンス生成時に指定されたファイルの再生の準備を行う。\n
    updateメソッド内でplayメソッドを呼ぶことでループ再生する。\n
    '''
    PLAY_STOP = 0       # 停止中
    PLAY_PLAYING = 1    # 再生中
    PLAY_END = 2        # 再生終了

    # 再生の状態。初期値は停止中。
    playStatus = PLAY_STOP

    def __init__(self):
        '''
        初期化\n
        '''
        pygame.mixer.init(frequency = 44100)
    
    def load(self, musicFileName:str = "" ):
        '''
        音楽ファイルロード\n
        ファイルはsource/assets/mp3にあるものとする。
        '''
        filePath = os.path.normpath(os.path.join(
            os.path.dirname(__file__), "../assets/ogg/" + musicFileName))
        pygame.mixer.music.load(filePath)

        # 状態の初期化
        self.playStatus = self.PLAY_STOP

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
                if self.playStatus == self.PLAY_STOP: # 停止中の場合
                    pygame.mixer.music.play()
                    self.playStatus = self.PLAY_PLAYING
                    print("play start.")
                    
                elif self.playStatus == self.PLAY_PLAYING: # 再生中の場合
                    pygame.mixer.music.stop()
                    self.playStatus = self.PLAY_END
                    print("play stop.")

    def stop(self):
        '''
        音楽の再生を停止する。\n
        再生していない状態でも特にエラーとしない。\n
        '''
        if self.playStatus != self.PLAY_END:
            pygame.mixer.music.stop()
            self.playStatus = self.PLAY_END
            print("play stop.")

musicPlayer = MusicPlayer()
