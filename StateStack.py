import stateTitle
import stateCity
import stateWeaponShop
import stateArmorShop
#import stateShieldShop
#import stateHelmetShop
#import stateBarbar
#import stateBank
#import stateSurgery
#import stateDrug
#import stateExaminations

class StateStack():

	states = []
	stateDic = {
		"Title" : StateTitle(),
		"City" : stateCity(),
		"WeaponShop" : stateWeaponShop()
	}

	#
	# 現在先頭にあるstateのupdate処理を呼び出す
	#
	def update():

		pass

	#
	# 現在先頭にあるstateのrender処理を呼び出す
	# 
	def render():

		pass

	# 
	# stateを追加する(push)
	#
	def push(stateName, state);

		states{stateName} = state

	#
	# stateを削除する(pop)
	#
	def addState(stateName, state):

		pass
