# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComTrioClient.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.mecha_const import TRIO_STATE_M, TRIO_STATE_S, TRIO_STATE_R
from logic.gcommon.const import PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3
from logic.gcommon.time_utility import get_server_time
from common.utils.timer import CLOCK
STATE_TO_WEAPON_POS_MAP = {TRIO_STATE_M: PART_WEAPON_POS_MAIN1,
   TRIO_STATE_S: PART_WEAPON_POS_MAIN2,
   TRIO_STATE_R: PART_WEAPON_POS_MAIN3
   }
STATE_TO_ICON_INFO = {TRIO_STATE_M: (
                ('action1', 'gui/ui_res_2/battle/mech_main/icon_mech8009_1.png', 'show'),
                ('action2', 'gui/ui_res_2/battle/mech_main/icon_mech8009_1.png', 'show'),
                ('action3', 'gui/ui_res_2/battle/mech_main/icon_mech8009_1.png', 'show'),
                ('action4', 'gui/ui_res_2/battle/mech_main/icon_mech8009_5.png', '')),
   TRIO_STATE_S: {
                ('action1', 'gui/ui_res_2/battle/mech_main/icon_mech8009_2.png', 'show'),
                ('action2', 'gui/ui_res_2/battle/mech_main/icon_mech8009_2.png', 'show'),
                ('action3', 'gui/ui_res_2/battle/mech_main/icon_mech8009_2.png', 'show'),
                ('action4', 'gui/ui_res_2/battle/mech_main/icon_mech8009_6.png', '')},
   TRIO_STATE_R: {
                ('action1', 'gui/ui_res_2/battle/mech_main/icon_mech8009_3.png', 'show'),
                ('action2', 'gui/ui_res_2/battle/mech_main/icon_mech8009_3.png', 'show'),
                ('action3', 'gui/ui_res_2/battle/mech_main/icon_mech8009_3.png', 'show'),
                ('action4', 'gui/ui_res_2/battle/mech_main/icon_mech8009_7.png', '')},
   'FullForce': {
               ('action1', 'gui/ui_res_2/battle/mech_main/icon_mech8009_4.png', 'show'),
               ('action2', 'gui/ui_res_2/battle/mech_main/icon_mech8009_4.png', 'show'),
               ('action3', 'gui/ui_res_2/battle/mech_main/icon_mech8009_4.png', 'show')}
   }

class ComTrioClient(UnitCom):
    BIND_EVENT = {'E_ENABLE_BEHAVIOR': ('on_enable_behavior', 100),
       'E_TRIO_TRANS_STATE': 'trans_state',
       'G_TRIO_STATE': 'get_trio_state',
       'E_ENTER_FIREPOWER': 'enable_full_force',
       'G_FULL_FORCE_ENABLED_PARAM': 'get_full_force_enabled_param',
       'E_REFRESH_WEAPON_DATA': 'refresh_cur_weapon_data',
       'E_MECHA_CONTROL_MAIN_INIT_COMPLETE': 'refresh_mecha_control_button_icon',
       'E_REFRESH_MECHA_CONTROL_BUTTON_ICON': 'refresh_mecha_control_button_icon',
       'G_RECONNECT_SKILL_NEED_RECOVER': 'get_reconnect_skill_need_recover',
       'E_DELAY_CLEAR_ADVANCE_FULL_FORCE': 'delay_clear_advance_full_force'
       }

    def __init__(self):
        super(ComTrioClient, self).__init__()
        self.cur_state = TRIO_STATE_M
        self.full_force_enabled = False
        self.clear_advance_timer = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrioClient, self).init_from_dict(unit_obj, bdict)
        self.npc_id = bdict.get('npc_id', None)
        self.cur_state = bdict.get('trio_state', TRIO_STATE_M)
        self.full_force_enabled = bdict.get('trio_firepower', False)
        self.full_force_total_time = bdict.get('fp_total_time', 0)
        self.full_force_finish_timestamp = bdict.get('fp_finish_time', 0)
        return

    def on_init_complete(self):
        switch_id = '{}_{}'.format(self.npc_id, self.cur_state) if self.cur_state else str(self.npc_id)
        self.send_event('E_REFRESH_STATE_PARAM', switch_id)

    def refresh_cur_weapon_data(self):
        self.send_event('E_REFRESH_CUR_WEAPON_BULLET', STATE_TO_WEAPON_POS_MAP[self.cur_state])

    def refresh_mecha_control_button_icon(self, start_full_force=False):
        state = 'FullForce' if self.full_force_enabled or start_full_force else self.cur_state
        for action, icon_path, anim_name in STATE_TO_ICON_INFO[state]:
            self.send_event('E_SET_ACTION_ICON', action, icon_path, anim_name)

    def trans_state(self, state):
        self.cur_state = state
        self.send_event('E_SWITCH_LETTER_EFFECT', state)
        switch_id = '{}_{}'.format(self.npc_id, state) if state else str(self.npc_id)
        self.send_event('E_SHOW_WEAPON_SWITCH_PROCESS', switch_id)
        self.send_event('E_REFRESH_CUR_WEAPON_BULLET', STATE_TO_WEAPON_POS_MAP[state])
        self.refresh_mecha_control_button_icon()

    def get_trio_state(self):
        return self.cur_state

    def enable_full_force(self, flag, total_time, finish_timestamp):
        if self.full_force_enabled == flag and flag:
            return
        else:
            self.full_force_enabled = flag
            self.full_force_total_time = total_time
            self.full_force_finish_timestamp = finish_timestamp
            self.send_event('E_ACTIVE_FULL_FORCE', flag, total_time, finish_timestamp)
            self.refresh_mecha_control_button_icon()
            if flag and self.clear_advance_timer:
                global_data.game_mgr.unregister_logic_timer(self.clear_advance_timer)
                self.clear_advance_timer = None
            return

    def on_enable_behavior(self, *args):
        if self.full_force_enabled:
            self.send_event('E_ACTIVE_FULL_FORCE', True, self.full_force_total_time, self.full_force_finish_timestamp)

    def get_full_force_enabled_param(self):
        return (
         self.full_force_enabled, self.full_force_total_time, self.full_force_finish_timestamp)

    def get_reconnect_skill_need_recover(self):
        return self.full_force_finish_timestamp <= get_server_time()

    def get_is_slide_move(self):
        return self.full_force_enabled or str(self.sd.ref_low_body_anim).startswith('run')

    def delay_clear_advance_full_force(self):
        if self.clear_advance_timer:
            global_data.game_mgr.unregister_logic_timer(self.clear_advance_timer)

        def clear_func():
            from logic.gcommon.cdata.mecha_status_config import MC_DASH
            self.send_event('E_DISABLE_STATE', MC_DASH)
            self.clear_advance_timer = None
            return

        self.clear_advance_timer = global_data.game_mgr.register_logic_timer(clear_func, interval=2.0, times=1, mode=CLOCK)