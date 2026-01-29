# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/AppointmentUI.py
from __future__ import absolute_import
import ccui
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER
from common.const import uiconst
from common.const.property_const import U_ID, HEAD_FRAME, HEAD_PHOTO, C_NAME
from logic.gutils.role_head_utils import init_role_head, init_dan_info, set_role_dan
AGREE = 0
REFUSE = 1
IGNORE = 2
VALID_TIME = 30

class AppointmentUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/battle_invite'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {}
    UI_ACTION_EVENT = {'btn_refuse.btn_common.OnClick': 'on_click_refuse',
       'btn_agree.btn_common.OnClick': 'on_click_agree',
       'btn_close.OnClick': 'on_click_close'
       }

    def on_init_panel(self):
        self.cur_showing_appoint = None
        self.appointment_list = []
        self.slider_touching = False
        self.panel.slider.addTouchEventListener(self._on_touch_slider)
        self.panel.slider.addEventListener(self._on_slider_percent_changed)
        self._init_refuse_text = self.panel.btn_refuse.btn_common.GetText()
        self.count_down_timer = None
        return

    def _on_touch_slider(self, widget, event):
        if event == ccui.TOUCH_EVENT_ENDED:
            self.slider_touching = False
            self.handle_slider()
        elif event == ccui.TOUCH_EVENT_BEGAN:
            self.slider_touching = True

    def _on_slider_percent_changed(self, widget, event):
        if not self.slider_touching and event == ccui.SLIDER_PERCENTCHANGED:
            self.handle_slider()

    def handle_slider(self):
        percent = self.panel.slider.getPercent()
        if percent >= 100.0:
            if self.cur_showing_appoint:
                confirm_id, extra_info = self.cur_showing_appoint
                global_data.player.req_confirm(confirm_id, IGNORE)
                self.try_show_next_appointment()
        else:
            self.panel.slider.setPercent(0.0)

    def add_appointment(self, confirm_id, extra_info):
        uid = extra_info.get('uid', None)
        if self.appointment_list:
            for c, e in self.appointment_list:
                if uid == e.get('uid', None):
                    return

        if self.cur_showing_appoint:
            c, e = self.cur_showing_appoint
            if uid == e.get('uid', None):
                return
        self.appointment_list.append((confirm_id, extra_info))
        if not self.cur_showing_appoint:
            self.try_show_next_appointment()
        return

    def try_show_next_appointment(self):
        if not self.appointment_list:
            self.close()
            return
        else:
            self.panel.slider.setPercent(0.0)
            self.cur_showing_appoint = self.appointment_list.pop(0)
            confirm_id, extra_info = self.cur_showing_appoint
            uid = extra_info.get('uid', None)
            if not uid:
                self.try_show_next_appointment()
                return
            self.show_appointment(extra_info)
            return

    def show_appointment(self, extra_info):
        self.panel.name.SetString(extra_info.get('char_name', ''))
        init_role_head(self.panel.head, extra_info.get('head_frame', None), extra_info.get('head_photo', None))
        dan_info = extra_info.get('dan_info')
        last_season = extra_info.get('last_season', 0)
        if global_data.player:
            this_season = global_data.player.get_battle_season()
        else:
            from logic.gcommon.cdata import season_data
            this_season = season_data.get_cur_battle_season()
        is_settled = last_season == this_season
        set_role_dan(self.panel.temp_tier, dan_info, is_settled)
        self.panel.lab_tips.SetString(extra_info.get('msg', ''))
        self.panel.PlayAnimation('invite_show')
        if not self.count_down_timer:
            self.init_count_down_timer()
        return

    def on_finalize_panel(self):
        self.destroy_count_down_timer()

    def on_click_refuse(self, *args):
        confirm_id, extra_info = self.cur_showing_appoint
        global_data.player.req_confirm(confirm_id, REFUSE)
        self.try_show_next_appointment()

    def on_click_agree(self, *args):
        confirm_id, extra_info = self.cur_showing_appoint
        global_data.player.req_confirm(confirm_id, AGREE)
        self.appointment_list = []
        self.close()

    def on_click_close(self, *args):
        confirm_id, extra_info = self.cur_showing_appoint
        global_data.player.req_confirm(confirm_id, REFUSE)
        self.try_show_next_appointment()

    def init_count_down_timer(self):
        from common.utils.timer import CLOCK
        import time
        self.destroy_count_down_timer()
        self.count_down_timer = global_data.game_mgr.register_logic_timer(self.update_count_down, interval=1, times=-1, mode=CLOCK)
        self.update_count_down()

    def update_count_down(self):
        if not self.cur_showing_appoint:
            self.destroy_count_down_timer()
            return
        confirm_id, extra_info = self.cur_showing_appoint
        ts = extra_info.get('timestamp', 0)
        if not ts:
            self.destroy_count_down_timer()
            return
        from logic.gcommon.time_utility import get_server_time
        cur_time = get_server_time()
        left_time = VALID_TIME - int(cur_time - ts)
        if left_time <= 0:
            self.on_click_refuse()
            self.try_show_next_appointment()
        else:
            self.panel.btn_refuse.btn_common.SetText(self._init_refuse_text + '(%ds)' % left_time)

    def destroy_count_down_timer(self):
        if self.count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self.count_down_timer)
        self.count_down_timer = None
        return