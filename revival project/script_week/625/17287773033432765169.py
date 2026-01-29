# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BulletReloadUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.client.const import pc_const
from logic.gutils import pc_utils
from logic.gcommon.cdata import status_config
from common.const import uiconst

class BulletReloadUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_bullet_reload'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'reload_button.OnClick': 'on_click_reload_button'
       }
    HOT_KEY_FUNC_MAP = {'human_reload': 'keyboard_reload'}
    HOT_KEY_FUNC_MAP_SHOW = {'human_reload': {'node': 'temp_pc'}}
    GLOBAL_EVENT = {'pc_hotkey_hint_display_option_changed': '_on_pc_hotkey_hint_display_option_changed',
       'pc_hotkey_hint_switch_toggled': '_on_pc_hotkey_hint_switch_toggled',
       'pc_hotkey_try_reload': 'try_reload'
       }

    def on_init_panel(self):
        self._timer = 0
        self.cur_weapon_pos = None
        self.last_pass_time = 0
        self.reload_cost_time = 0
        self.reload_pass_time = 0
        self._reload_time_scale = 0.0
        self._begin_roll_time = 0
        self.init_events()
        self.init_custom_com()
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_events(self):
        self.process_event(True)

    def on_finalize_panel(self):
        self.unregister_timer()
        self.process_event(False)
        self.destroy_widget('custom_ui_com')

    def on_hot_key_state_opened(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def on_hot_key_state_closed(self):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_display_option_changed(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(pc_utils.get_pc_hotkey_hint_switch(), now, pc_utils.is_pc_control_enable())

    def _on_pc_hotkey_hint_switch_toggled(self, old, now):
        self._update_pc_key_hint_related_uis_visibility(now, pc_utils.get_hotkey_hint_display_option(), pc_utils.is_pc_control_enable())

    def _update_pc_key_hint_related_uis_visibility(self, hint_switch, display_option, pc_op_mode):
        show = pc_utils.should_pc_key_hint_related_uis_show(pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_ICON, hint_switch, display_option, pc_op_mode)
        if show:
            self.add_show_count(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION)
        else:
            self.add_hide_count(pc_const.PANEL_HIDE_REASON_DUE_TO_PC_HOTKEY_HINT_DISPLAY_OPTION)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.set_progress_time, interval=0.033, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_wpbar_switch_cur_event': self.on_change_weapon,
           'on_reload_bullet_event': self.on_reload_bullet,
           'on_cancel_reload_event': self.on_cancel_reload,
           'on_begin_roll_event': self.on_begin_roll,
           'on_end_roll_event': self.on_roll_end,
           'scene_camera_player_setted_event': self.on_camera_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_begin_roll(self, *args):
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_reload():
            self._reload_time_scale = global_data.cam_lplayer.ev_g_attr_get('fRollReloadSpeedFactor', 0.0)
        self._begin_roll_time = time.time()

    def on_roll_end(self, *args):
        self._reload_time_scale = 0.0

    def on_reload_bullet(self, reload_time, times, *args):
        import cc
        from data import rush_arg
        self.panel.reload_shield.setVisible(True)
        self.panel.reload_button.SetEnableTouch(False)
        self.last_pass_time = time.time()
        left_time = self.last_pass_time - self._begin_roll_time
        if left_time > rush_arg.DEFAULT_ROLL_DURATION:
            left_time = 0
        left_time = max(0, left_time)
        self.reload_cost_time = reload_time + left_time
        self.reload_pass_time = 0
        self.register_timer()

    def set_progress_time(self):
        from common import utilities
        now = time.time()
        pass_time = (now - self.last_pass_time) * (1.0 + self._reload_time_scale)
        self.last_pass_time = now
        self.reload_pass_time += pass_time
        left_time = self.reload_cost_time - self.reload_pass_time
        left_time = max(0, left_time)
        time_str = '%.1fs' % left_time
        self.panel.reload_time.SetString(time_str)
        self.panel.progress_reload.SetPercentage(utilities.safe_percent(self.reload_pass_time, self.reload_cost_time))
        if left_time <= 0:
            self.on_cancel_reload()

    def on_change_weapon(self, *args):
        self.on_cancel_reload()
        if global_data.cam_lplayer:
            self.cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
        self.check_need_show_reload_ui()

    def on_cancel_reload(self, *args):
        self.panel.reload_shield.setVisible(False)
        self.panel.reload_button.SetEnableTouch(True)
        self.unregister_timer()

    def on_camera_player_setted(self):
        if global_data.cam_lplayer:
            self.cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos
            self.check_need_show_reload_ui()

    def check_need_show_reload_ui(self):
        from logic.gcommon import const
        if self.cur_weapon_pos in const.MAIN_WEAPON_LIST:
            self.panel.reload_layer.setVisible(True)
        else:
            self.panel.reload_layer.setVisible(False)

    def on_click_reload_button(self, btn, touch):
        self.try_reload()

    def _update_weapon_pos(self):
        if global_data.cam_lplayer:
            self.cur_weapon_pos = global_data.cam_lplayer.share_data.ref_wp_bar_cur_pos

    def try_reload(self):
        self._update_weapon_pos()
        if not global_data.is_key_mocking_ui_event:
            self.panel.PlayAnimation('reload_click')
        weapon_pos = self.cur_weapon_pos
        from logic.gcommon import const
        if global_data.cam_lplayer:
            lplayer = global_data.cam_lplayer
        else:
            lplayer = None
        if not lplayer:
            return
        else:
            if not lplayer.ev_g_status_check_pass(status_config.ST_RELOAD):
                return
            if weapon_pos in const.MAIN_WEAPON_LIST:
                weapon_data = lplayer.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
                if weapon_data is None:
                    weapon_data = None if 1 else weapon_data.get_data()
                    return weapon_data or None
                cur_bullet_num = weapon_data.get('iBulletNum', 0)
                wp = lplayer.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
                if wp:
                    max_bullet = wp.get_bullet_cap()
                    if cur_bullet_num != max_bullet:
                        lplayer.send_event('E_TRY_RELOAD')
            return

    def keyboard_reload(self, msg, keycode):
        self.on_click_reload_button(None, None)
        return