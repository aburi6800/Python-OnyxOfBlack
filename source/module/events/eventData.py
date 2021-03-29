# -*- coding: utf-8 -*-

class eventData(object):

    # イベントデータの辞書
    events = {}

    def __init__(self) -> None:
        '''
        クラス初期化
        '''
        super().__init__()

        # イベント辞書の初期化処理を呼ぶ
        self.reset()

    def reset(self) -> None:
        '''
        イベント辞書の初期化処理
        '''
        self.events = {
            "CITY17040D": "self.draw_gate()",
            "CITY18040D": "self.draw_gate()",
            "CITY17030U": "playerParty.restoreCondition()",
            "CITY18030U": "playerParty.restoreCondition()",
            "CITY27073D": "self.draw_shieldshop()",
            "CITY26073U": "self.stateStack.push(State.SHIELDSHOP)",
            "CITY27061D": "self.draw_armorshop()",
            "CITY28061U": "self.stateStack.push(State.ARMORSHOP)",
            "CITY27081D": "self.draw_weaponshop()",
            "CITY28081U": "self.stateStack.push(State.WEAPONSHOP)",
            "CITY27101D": "self.draw_helmetshop()",
            "CITY28101U": "self.stateStack.push(State.HELMETSHOP)",
            "CITY27113D": "self.draw_barbar()",
            "CITY26113U": "self.stateStack.push(State.BARBAR)",
            "CITY16083D": "self.draw_donotenter()",
            "CITY21052D": "self.draw_inn()",
            "CITY23092D": "self.draw_physicker()",
            "CITY23100D": "self.draw_physicker_exit()",
            "CITY23103D": "self.draw_drugs()",
            "CITY22103U": "self.stateStack.push(State.DRUGS)",
            "CITY23101D": "self.draw_surgery()",
            "CITY24101U": "self.stateStack.push(State.SURGERY)",
            "CITY23111D": "self.draw_examinations()",
            "CITY24111U": "self.stateStack.push(State.EXAMINATIONS)",
            "CITY17141D": "self.draw_thewall()",
            "CITY18143D": "self.draw_thewall()",
            "CITY14050D": "self.draw_jail()",
            "CITY02023U": "self.startEvent('city_002.json')",
            "CITY18090D": "self.draw_directionmarket()",
            "CITY18092D": "self.draw_directionmarket()",
            "CITY21151D": "self.draw_cemetery()",
            "CITY22151D": "self.draw_cemetery()",
            "CITY25199U": "self.startEvent('city_003.json')",
            "CITY26199U": "self.startEvent('city_004.json')",
            "CITY25209U": "self.startEvent('city_005.json')",
            "CITY26209U": "self.startEvent('city_006.json')",
            "CITY17172D": "self.draw_temple()",
            "CITY18172D": "self.draw_temple()",
            "CITY19172D": "self.draw_temple()",
            "CITY17182U": "playerParty.restoreCondition()",
            "CITY18182U": "playerParty.restoreCondition()",
            "CITY19182U": "playerParty.restoreCondition()",
            "CITY15149U": "self.startEvent('city_001.json')",
            "CITY11079U": "self.startEvent('city_007.json')",
            "CEMETERY09069U": "self.update_to_city()",
            "CEMETERY10069U": "self.update_to_city()",
            "CEMETERY09079U": "self.update_to_city()",
            "CEMETERY10079U": "self.update_to_city()",
            "CEMETERY09069D": "self.draw_to_city()",
            "CEMETERY10069D": "self.draw_to_city()",
            "CEMETERY09079D": "self.draw_to_city()",
            "CEMETERY10079D": "self.draw_to_city()",
            "CEMETERY07129U": "self.update_fixed_encount_enemy()",
            "CEMETERY09139U": "self.update_fixed_encount_enemy()",
            "CEMETERY07149U": "self.update_fixed_encount_enemy()",
            "CEMETERY09159U": "self.update_fixed_encount_enemy()",
            "CEMETERY07109U": "self.update_fixed_encount_enemy()",
            "CEMETERY16169U": "self.update_fixed_encount_enemy()",
            "CEMETERY15159U": "self.update_fixed_encount_enemy()",
            "CEMETERY18169U": "self.update_fixed_encount_enemy()",
            "CEMETERY17159U": "self.update_fixed_encount_enemy()",
            "CEMETERY15189U": "self.update_fixed_encount_enemy()",
            "CEMETERY16199U": "self.update_fixed_encount_enemy()",
            "CEMETERY17189U": "self.update_fixed_encount_enemy()",
            "CEMETERY18199U": "self.update_fixed_encount_enemy()",
            "DUNGEONB103069U": "self.startEvent('dungeonb1_001.json')",
            "DUNGEONB118219U": "self.startEvent('dungeonb1_002.json')",
            "DUNGEONB218219U": "self.startEvent('dungeonb2_001.json')",
            "DUNGEONB216279U": "self.startEvent('dungeonb1_002.json')",
            "DUNGEONB229199U": "self.startEvent('dungeonb1_002.json')",
            "DUNGEONB226129U": "self.startEvent('dungeonb1_002.json')",
            "DUNGEONB316289U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB328199U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB326129U": "self.startEvent('dungeonb3_001.json')",
            "DUNGEONB306069U": "self.startEvent('dungeonb3_002.json')",
            "DUNGEONB406069U": "self.startEvent('dungeonb4_001.json')",
            "DUNGEONB424249U": "self.startEvent('dungeonb4_001.json')",
            "DUNGEONB510109U": "self.update_encount_kraken()",
            "DUNGEONB510109D": "self.draw_encount_kraken()",
            "WELLB110109U": "self.startEvent('wellb1_001.json')",
            "WELLB210109U": "self.startEvent('wellb2_001.json')",
            "WELLB310109U": "self.startEvent('wellb3_001.json')",
            "WELLB410109U": "self.startEvent('wellb4_001.json')",
        }

# インスタンスを生成
eventdata = eventData()
