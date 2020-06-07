# -*- coding: utf-8 -*-
import stateStack

# stateStackのテスト
sStack = stateStack.StateStack()

sStack.push(sStack.STATE_TITLE)
sStack.update()
sStack.render()
sStack.push(sStack.STATE_CITY)
sStack.update()
sStack.render()
sStack.push(sStack.STATE_WEAPONSHOP)
sStack.update()
sStack.render()
sStack.pop()
sStack.update()
sStack.render()

