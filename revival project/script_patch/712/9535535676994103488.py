# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/GMHelperUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.cdata.status_config import ST_SWIM
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_const.battle_const as battle_const
from data import hot_key_def
import math3d
from logic.gcommon.common_const import mecha_const
import time
ADJUST_WATER_Y_OFFSET = 3 * NEOX_UNIT_SCALE
from common.const import uiconst
MIN_REQUEST_INTERVAL = 0.5
last_request_time = 0

class GMHelperBaseUI(BasePanel):
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'help_button.OnClick': 'on_click_help'
       }
    HOT_KEY_FUNC_MAP = {hot_key_def.GM_HELPER: 'on_click_help'
       }
    HOT_KEY_FUNC_MAP_SHOW = {hot_key_def.GM_HELPER: {'node': 'temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        self._reason = kwargs.get('reason', battle_const.TRY_TELE_POS_REASON_DEFAULT)
        self._is_in_close_space = kwargs.get('in_close_space', False)
        self.panel.help_button.setVisible(True)
        self.panel.PlayAnimation('help')
        self.init_custom_com()
        if global_data.ex_scene_mgr_agent.check_settle_scene_active() or self.check_is_in_lobby():
            self.hide()

    def on_finalize_panel(self):
        self.destroy_widget('custom_ui_com')
        if global_data.player:
            player = global_data.player.logic
            if player:
                player.send_event('E_SET_IS_ENABLE_TEST_POS', True)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def is_in_close_space(self):
        return self._is_in_close_space

    def check_is_in_lobby(self):
        if global_data.player:
            return not global_data.player.is_in_battle()
        return True

    def on_click_help(self, *args):
        global last_request_time
        if not global_data.player or not global_data.player.logic:
            self.close()
            return
        player = global_data.player.logic
        if not self._is_in_close_space and player.ev_g_get_state(ST_SWIM):
            char_ctrl = player.sd.ref_character
            if char_ctrl and char_ctrl.isActive():
                char_ctrl.unLimitLowerHeight()
                char_ctrl.unlimitHeight()
            physical_position = player.ev_g_phy_position()
            direction = math3d.vector(0, -50 * NEOX_UNIT_SCALE, 0)
            start_position = math3d.vector(physical_position)
            start_position.y = 30 * NEOX_UNIT_SCALE
            col_result = char_ctrl.sweepTest(start_position, direction)
            is_hit = col_result[0]
            hit_position = col_result[1]
            hit_normal = col_result[2]
            move_len = col_result[3]
            if is_hit:
                player.send_event('E_FOOT_POSITION', hit_position)
            else:
                foot_pos = self.ev_g_foot_position()
                foot_pos.y = foot_pos.y + ADJUST_WATER_Y_OFFSET
                player.send_event('E_FOOT_POSITION', foot_pos)
        else:
            cur_time = time.time()
            pass_time = cur_time - last_request_time
            if pass_time >= MIN_REQUEST_INTERVAL:
                last_request_time = cur_time
                control_target = player.ev_g_control_target()
                if control_target and control_target.logic.__class__.__name__ == 'LMechaTrans':
                    pattern = control_target.logic.ev_g_pattern()
                    is_vehicle = pattern == mecha_const.MECHA_TYPE_VEHICLE
                    if is_vehicle:
                        control_target.logic.send_event('E_TRY_TRANSFORM')
                player.send_event('E_CALL_SYNC_METHOD', 'try_teleport_to_top', (self._reason,))
        player.send_event('E_USE_GM_HLEP')
        self.close()


class GMHelperUI(GMHelperBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_temporary'