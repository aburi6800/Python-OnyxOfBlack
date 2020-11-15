# -*- coding: utf-8 -*-
from module.character import HumanPartyGenerator
from module.character import PlayerParty
from module.character import Human

if __name__ == "__main__":
    party = HumanPartyGenerator.generate()
    for human in party:
        print(human.name + ":LIFE=" + str(human.life) + "/EXP=" + str(human.exp) + "/WEAPON="+ human.weapon.name + "/ARMOR=" + human.armor.name)
