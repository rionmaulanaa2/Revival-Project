# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BulletReloadProgressUI.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mecha_utils
import cc
from common.const import uiconst

class BulletReloadProgressUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_reload_progress'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    HIDE_ACT = 180810
    HIDE_UI_LIST = mecha_utils.BULLET_RELOAD_HIDE_UI_LIST
    HOT_KEY_FUNC_MAP = {'cancel_action': 'cancel_btn_click'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'cancel_action': {'node': 'btn_cancel.temp_pc'}}

    def on_init_panel(self):
        self._timer = 0
        self.last_pass_time = 0
        self.reload_cost_time = 0
        self.reload_pass_time = 0
        self._reload_time_scale = 0.0
        self._begin_roll_time = 0
        self.disable_cancel_by_change_weapon = False
        self.panel.lab_hint.setVisible(False)
        self.init_event()
        self.cur_battle_progress_item_id = None
        self.cur_battle_progress_msg = None
        self.add_hide_count(self.__class__.__name__)
        self.add_shadow_richtext('')
        return

    def on_finalize_panel(self):
        self.unregister_timer()

    def init_event(self):
        emgr = global_data.emgr
        econf = {'on_wpbar_switch_cur_event': self.on_change_weapon,
           'on_reload_bullet_event': self.on_reload_bullet,
           'on_cancel_reload_event': self.on_cancel_progress,
           'on_begin_roll_event': self.on_begin_roll,
           'on_end_roll_event': self.on_roll_end,
           'scene_camera_player_setted_event': self.on_camera_player_setted,
           'disable_change_weapon_cancel_reload_ui_appearance': self.disable_change_weapon_cancel
           }
        emgr.bind_events(econf)

    def on_resolution_changed(self):
        self.set_hint_position()

    def do_show_panel(self):
        super(BulletReloadProgressUI, self).do_show_panel()
        self.hide_main_ui(self.HIDE_UI_LIST)

    def do_hide_panel(self):
        super(BulletReloadProgressUI, self).do_hide_panel()
        self.show_main_ui()

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.set_progress_time, interval=0.033, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def on_reload_bullet(self, reload_time, times, *args):
        from data import rush_arg
        left_time = time.time() - self._begin_roll_time
        if left_time > rush_arg.DEFAULT_ROLL_DURATION:
            left_time = 0
        left_time = max(0, left_time)
        if reload_time <= 0 and global_data.game_mode.is_pve():
            return
        else:
            self.show_battle_info_progress(reload_time + left_time, get_text_by_id(19113), None)
            return

    def on_begin_roll(self, *args):
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_reload():
            self._reload_time_scale = global_data.cam_lplayer.ev_g_attr_get('fRollReloadSpeedFactor', 0.0)
        self._begin_roll_time = time.time()

    def on_roll_end(self, *args):
        self._reload_time_scale = 0.0

    def on_change_weapon(self, *args):
        if not self.disable_cancel_by_change_weapon:
            self.on_cancel_progress()

    def on_cancel_progress(self, *args):
        self.disable_cancel_by_change_weapon = False
        self.cur_battle_progress_item_id = None
        self.cur_battle_progress_msg = None
        self.unregister_timer()
        if self.get_show_count(self.__class__.__name__) >= 0:
            self.add_hide_count(self.__class__.__name__)
        return

    def on_camera_player_setted(self):
        self.on_cancel_progress()

    def disable_change_weapon_cancel(self, disable):
        self.disable_cancel_by_change_weapon = disable

    def show_battle_info_progress(self, reload_time, progress_msg, item_id, cancel_callback=None):
        self.panel.btn_cancel.OnClick(None)
        if self.get_show_count(self.__class__.__name__) < 0:
            self.add_show_count(self.__class__.__name__)
        btn = self.panel.btn_cancel
        if cancel_callback:
            btn.setVisible(True)
        else:
            btn.setVisible(False)
        self.panel.nd.setVisible(True)

        @btn.unique_callback()
        def OnClick(btn, touch, item_id=item_id):
            if cancel_callback:
                cancel_callback()

        if progress_msg:
            self.panel.lab_hint_rich.setVisible(True)
            progress_msg = self.get_shadow_richtext_str(progress_msg)
            self.panel.lab_hint_rich.SetString(progress_msg)
        else:
            self.panel.lab_hint_rich.setVisible(False)
        self.cur_battle_progress_item_id = item_id
        self.cur_battle_progress_msg = progress_msg
        self.last_pass_time = time.time()
        self.reload_cost_time = reload_time
        self.reload_pass_time = 0
        self.register_timer()
        return

    def set_progress_time(self):
        from common import utilities
        tf_times = self.panel.lab_time
        nd_progress = self.panel.progress_reload
        now = time.time()
        pass_time = (now - self.last_pass_time) * (1.0 + self._reload_time_scale)
        self.last_pass_time = now
        self.reload_pass_time += pass_time
        left_time = self.reload_cost_time - self.reload_pass_time
        left_time = max(0, left_time)
        if tf_times:
            time_str = '%.1f%s' % (left_time, get_text_local_content(18534))
            tf_times.SetString(time_str)
        nd_progress.setPercentage(utilities.safe_percent(self.reload_pass_time, self.reload_cost_time))
        if left_time <= 0:
            self.on_cancel_progress()

    def cancel_battle_info_progress(self):
        self.on_cancel_progress()
        nd_progress = self.panel.progress_reload
        nd_progress.stopAllActions()

    def set_hint_position(self):
        item = getattr(self.panel, 'lab_hint_rich', None)
        if not item:
            return
        else:
            item.setPosition(self.panel.lab_hint.getPosition())
            item.setAnchorPoint(cc.Vec2(0.5, 0.5))
            item.SetHorizontalAlign(1)
            return

    def add_shadow_richtext(self, txt):
        txt = '<shadow=1>#SW{0}</color></shadow>'.format(txt)
        from common.uisys.uielment.CCRichText import CCRichText
        count_msg = CCRichText.Create(txt, 22, cc.Size(200, 30))
        self.panel.AddChild('lab_hint_rich', count_msg)
        self.set_hint_position()

    def get_shadow_richtext_str(self, txt):
        txt = '<shadow=1>#SW{0}</color></shadow>'.format(txt)
        return txt

    def cancel_btn_click(self, msg, keycode):
        self.panel.btn_cancel.OnClick(None)
        return