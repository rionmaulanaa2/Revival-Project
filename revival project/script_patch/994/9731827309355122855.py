# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComDeathBattleGuide.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.comsys.guide_ui.GuideUI import GuideUI
from logic.client.const import game_mode_const
from mobile.common.IdManager import IdManager
from data.c_guide_data import GetDeathGuide, get_death_guide_params
from common.utils.timer import CLOCK

class ComDeathBattleGuide(UnitCom):
    BIND_EVENT = {'E_DEATH': 'destroy_death_guide'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComDeathBattleGuide, self).init_from_dict(unit_obj, bdict)
        self._in_death_guide = False
        self._death_battle_key = None
        self._death_battle_value = None
        self._play_rule_timer = None
        return

    @property
    def _guide_ui(self):
        return GuideUI()

    def on_init_complete(self, *_):
        player = global_data.player
        if player.in_local_battle():
            return
        else:
            if player.is_remote_death_guide_flag():
                return
            if player.is_in_global_spectate():
                return
            if self.ev_g_is_in_spectate():
                return
            if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATH):
                return
            if self.ev_g_is_in_spectate():
                return
            data = player.get_death_battle_data()
            total_cnt = player.get_death_total_cnt()
            if total_cnt < 3:
                if not self._guide_ui:
                    return
                self._in_death_guide = True
                key = IdManager.id2str(player.battle_id)
                self._death_battle_key = key
                if data is None or key not in data:
                    data = {key: []}
                self._death_battle_value = data
                self.init_death_guide()
            elif data:
                player.save_death_battle_data(None)
                player.update_remote_death_guide_flag(True)
            return

    def init_death_guide--- This code section failed: ---

  69       0  LOAD_GLOBAL           0  'GetDeathGuide'
           3  CALL_FUNCTION_0       0 
           6  STORE_FAST            1  'info'

  70       9  SETUP_LOOP           79  'to 91'
          12  LOAD_FAST             1  'info'
          15  GET_ITER         
          16  FOR_ITER             71  'to 90'
          19  STORE_FAST            2  'handler_name'

  71      22  LOAD_FAST             2  'handler_name'
          25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             1  '_death_battle_value'
          31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             2  '_death_battle_key'
          37  BINARY_SUBSCR    
          38  COMPARE_OP            6  'in'
          41  POP_JUMP_IF_FALSE    50  'to 50'

  72      44  CONTINUE             16  'to 16'
          47  JUMP_FORWARD          0  'to 50'
        50_0  COME_FROM                '47'

  73      50  LOAD_GLOBAL           3  'getattr'
          53  LOAD_GLOBAL           1  '_death_battle_value'
          56  LOAD_ATTR             4  'format'
          59  LOAD_FAST             2  'handler_name'
          62  CALL_FUNCTION_1       1 
          65  CALL_FUNCTION_2       2 
          68  STORE_FAST            3  'func'

  74      71  LOAD_FAST             3  'func'
          74  POP_JUMP_IF_FALSE    16  'to 16'

  75      77  LOAD_FAST             3  'func'
          80  CALL_FUNCTION_0       0 
          83  POP_TOP          
          84  JUMP_BACK            16  'to 16'
          87  JUMP_BACK            16  'to 16'
          90  POP_BLOCK        
        91_0  COME_FROM                '9'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 65

    def save_death_guide(self, guide):
        self._death_battle_value[self._death_battle_key].append(guide)
        global_data.player.save_death_battle_data(self._death_battle_value)

    def destroy_death_guide(self, *_):
        if self._in_death_guide:
            self._in_death_guide = False
            if self._play_rule_timer:
                global_data.game_mgr.unregister_logic_timer(self._play_rule_timer)
                self._play_rule_timer = None
            global_data.emgr.death_count_down_over -= self.death_guide_choose_weapon
            global_data.emgr.death_count_down_over -= self.death_guide_play_rule
            self.unit_obj.unregist_event('E_DEATH_GUIDE_CHOOSE_WEAPON_UI', self.death_guide_choose_weapon_final)
            self.unit_obj.unregist_event('E_DEATH_GUIDE_REVIVE', self.death_guide_revive)
        return

    def init_death_guide_choose_weapon(self):
        global_data.emgr.death_count_down_over += self.death_guide_choose_weapon
        if global_data.ui_mgr.get_ui('DeathBeginCountDown'):
            return
        self.death_guide_choose_weapon()

    def death_guide_choose_weapon(self):
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            return
        global_data.emgr.death_count_down_over -= self.death_guide_choose_weapon
        guide = 'death_guide_choose_weapon'
        if not global_data.ui_mgr.get_ui('DeathBeginCountDown'):
            param = get_death_guide_params(guide)
            self._guide_ui.show_death_choose_weapon(*param)
            self.unit_obj.regist_event('E_DEATH_GUIDE_CHOOSE_WEAPON_UI', self.death_guide_choose_weapon_final)
        self.save_death_guide(guide)

    def death_guide_choose_weapon_final(self):
        self.unit_obj.unregist_event('E_DEATH_GUIDE_CHOOSE_WEAPON_UI', self.death_guide_choose_weapon_final)
        self._guide_ui.hide_death_choose_weapon()

    def init_death_guide_play_rule(self):
        global_data.emgr.death_count_down_over += self.death_guide_play_rule
        if global_data.ui_mgr.get_ui('DeathBeginCountDown'):
            return
        self.death_guide_play_rule()

    def death_guide_play_rule(self):
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            return
        global_data.emgr.death_count_down_over -= self.death_guide_play_rule

        def _():
            guide = 'death_guide_play_rule'
            param = get_death_guide_params(guide)
            text_id, time_out, v1, v2 = param
            self._guide_ui.show_death_play_rule(text_id, time_out, (v1, v2))
            self.save_death_guide(guide)

        self._play_rule_timer = global_data.game_mgr.register_logic_timer(lambda : _(), interval=10, times=1, mode=CLOCK)

    def init_death_guide_revive(self):
        self.unit_obj.regist_event('E_DEATH_GUIDE_REVIVE', self.death_guide_revive)

    def death_guide_revive(self):
        if global_data.ui_mgr.get_ui('DeathBeginCountDown'):
            return
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            return
        self.unit_obj.unregist_event('E_DEATH_GUIDE_REVIVE', self.death_guide_revive)
        guide = 'death_guide_revive'
        param = get_death_guide_params(guide)
        self._guide_ui.show_death_choose_weapon(*param)
        self.save_death_guide(guide)
        self.unit_obj.unregist_event('E_DEATH_GUIDE_CHOOSE_WEAPON_UI', self.death_guide_choose_weapon_final)
        self.unit_obj.regist_event('E_DEATH_GUIDE_CHOOSE_WEAPON_UI', self.death_guide_choose_weapon_final)