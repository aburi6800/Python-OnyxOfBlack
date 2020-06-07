# -*- coding: utf-8 -*-

class State():

	#
	# クラス初期化
	#
	def __init__(self):

		self.stateName = "(none)"

	#
	# 各フレームの処理
	#
	def update(self):

		print(self.stateName + ":update")

	#
	# 各フレームの画面描画処理
	#
	def render(self):

		print(self.stateName + ":render")

	#
	# 状態開始時の処理
	#
	def onEnter(self):

		print(self.stateName + ":onEnter")

	#
	# 状態終了時の処理
	#
	def onExit(self):

		print(self.stateName + ":onExit")

