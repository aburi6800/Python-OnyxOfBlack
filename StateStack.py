# -*- coding: utf-8 -*-

import stateTitle
import stateCity
import stateWeaponShop
#import StateArmorShop
#import stateShieldShop
#import stateHelmetShop
#import stateBarbar
#import stateBank
#import stateSurgery
#import stateDrug
#import stateExaminations

class StateStack():

	STATE_TITLE = "Title"
	STATE_CITY = "City"
	STATE_WEAPONSHOP = "WeaponShop"

	#
	# クラス初期化
	#
	def __init__(self):
		self.states = []
		self.stateDic = {
			self.STATE_TITLE : stateTitle.StateTitle(),
			self.STATE_CITY : stateCity.StateCity(),
			self.STATE_WEAPONSHOP : stateWeaponShop.StateWeaponShop()
		}


	#
	# 現在先頭にあるstateのupdate処理を呼び出す
	#
	def update(self):

		state = self.states[0]
		state.update()


	#
	# 現在先頭にあるstateのrender処理を呼び出す
	# 
	def render(self):

		state = self.states[0]
		state.render()


	# 
	# stateを追加する(push)
	#
	def push(self, stateName):		

		self.states.insert(0, self.stateDic[stateName])
		self.states[0].onEnter()


	#
	# stateを削除する(pop)
	#
	def pop(self):

		self.states[0].onExit()
		self.states.pop(0)

