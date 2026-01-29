# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComMechaNewAimHelper.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.client.com_human_logic.ComOpenAimHelper import ComOpenAimHelper
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from common.cfg import confmgr

class ComMechaNewAimHelper(ComOpenAimHelper):
    DYNAMIC_EVENT = {'G_SIGHTING_TARGET_POS': '_get_sighting_target_pos',
       'E_GUN_ATTACK': 'on_gun_attack',
       'E_TOUCH_SLIDE': 'on_touch_slide',
       'G_AIM_LOOK_AT_POS': 'get_aim_look_at_pos',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start',
       'E_ON_ENABLE_AIM_HELPER': 'on_enable_aim_helper'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComOpenAimHelper, self).init_from_dict(unit_obj, bdict)
        self.aim_helper_allowed = not (global_data.is_pc_mode or global_data.deviceinfo.is_emulator())
        self.aim_helper_enabled = global_data.player.get_setting(uoc.AIM_HELPER_KEY_1)
        self.want_to_tick = False
        self.cur_mecha_need_update = False
        return
        first_weapon_id = bdict.get('weapons', {}).get(PART_WEAPON_POS_MAIN1, {}).get('item_id', None)
        if first_weapon_id:
            if confmgr.get('firearm_aim_args', str(first_weapon_id)) or confmgr.get('fire_adsorb_args', str(first_weapon_id)):
                self.event_registered = False
                if self.aim_helper_allowed:
                    self._process_event(True)
                self.want_to_tick = True
                self.cur_mecha_need_update = True
        return

    def _refresh_tick_state(self):
        need_update = self.aim_helper_enabled and self.want_to_tick and self.cur_mecha_need_update
        if self.need_update ^ need_update:
            self.need_update = need_update
            self.update_aim_config()

    def get_weapon_config(self):
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return None
        else:
            return confmgr.get('firearm_config', str(obj_weapon.get_item_id()))

    def get_aim_config(self):
        obj_weapon = self.sd.ref_wp_bar_cur_weapon
        if not obj_weapon:
            return None
        else:
            return confmgr.get('firearm_aim_args', str(obj_weapon.get_item_id()))

    def on_leave_mecha_start(self):
        self.on_enable_aim_helper(False)