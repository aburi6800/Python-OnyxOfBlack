# -*- coding: utf-8 -*-
from module.character import HumanPartyGenerator

if __name__ == "__main__":
    party = HumanPartyGenerator.generate(1)
    for human in party:
        print(human.name + ":LIFE=" + str(human.life) + "/EXP=" + str(human.exp) + "/WEAPON="+ human.weapon.name + "(" + str(human.weapon.attack) + ")/ARMOR=" + human.armor.name + "(" + str(human.armor.armor) + ")")
