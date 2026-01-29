# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGrossCharge68New.py
from __future__ import absolute_import
from logic.gutils import activity_utils
from logic.comsys.activity.ActivityTemplate import ActivityBase
TO_GET = 1
CAN_GET = 2
GOT = 3

class ActivityGrossCharge68New(ActivityBase):
    DELAY_LOOP_TAG = 31415926
    VIDEO_PATH = 'video/activity_wind_new.mp4'

    def __init__(self, dlg, activity_type):
        ActivityBase.__init__(self, dlg, activity_type)
        self._need_bg = False

    def on_init_panel(self):
        self._init_data()
        self._init_view()
        self._refresh_view()
        self.init_event()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        global_data.video_player.play_video(self.VIDEO_PATH, None, {}, 0, None, True, disable_sound_mgr=False)
        if G_IS_NA_USER:
            self.panel.lab_sub_title.SetString(607373)
        else:
            self.panel.lab_sub_title.SetString(607342)
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(activity_type, self.__class__.__name__)
        return

    def on_finalize_panel(self):
        self.process_event(False)
        if global_data.video_player.video_name == self.VIDEO_PATH:
            global_data.video_player.stop_video()
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(activity_type, self.__class__.__name__)

    def _init_data(self):
        activity_type = self._activity_type
        self._d_item_id = activity_utils.get_activity_conf_ui_data(activity_type, 'display_item_id')
        self._task_id = activity_utils.get_activity_conf_ui_data(activity_type, 'task_id')
        self._money = activity_utils.get_activity_conf_ui_data(activity_type, 'money')
        self._mecha_id = activity_utils.get_activity_conf_ui_data(activity_type, 'mecha_id')
        self._state = TO_GET

    def _init_view(self):
        from logic.comsys.mecha_display.MechaDisplay import MechaDisplay
        MechaDisplay.refresh_mecha_tag_list(self.panel.temp_list_tab, self._mecha_id)

    def init_event(self):
        self.process_event(True)

        @self.panel.btn_buy.btn_buy.unique_callback()
        def OnClick(btn, touch):
            if self._state == TO_GET:
                from logic.gutils.jump_to_ui_utils import jump_to_charge
                from logic.comsys.charge_ui.ChargeUINew import ACTIVITY_GROWTH_FUND
                jump_to_charge(ACTIVITY_GROWTH_FUND)
                from logic.gutils.ui_salog_utils import add_uiclick_salog_lobby
                add_uiclick_salog_lobby('charge68_new_jump_to_charge')
            elif self._state == CAN_GET:
                if self._task_id and self._money:
                    global_data.player and global_data.player.receive_task_prog_reward(self._task_id, self._money)

        @self.panel.btn_more.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
            jump_to_display_detail_by_item_no(self._d_item_id)

    def _refresh_view(self):
        state = self._get_state()
        self._state = state
        if state == TO_GET:
            text_id = 80961
        elif state == CAN_GET:
            text_id = 80930
        elif state == GOT:
            text_id = 604029
        else:
            text_id = 80961
        btn = self.panel.btn_buy.btn_buy
        lab = self.panel.btn_buy.lab_text
        lab.SetString(text_id)
        btn.SetEnable(state != GOT)
        global_data.video_player.play_video(self.VIDEO_PATH, None, {}, 0, None, True, disable_sound_mgr=False)
        return

    def refresh_panel(self):
        self._refresh_view()

    def _get_state(self):
        if activity_utils.has_got_gross_charge_68_reward():
            return GOT
        else:
            if activity_utils.is_gross_charge_68_receivable():
                return CAN_GET
            return TO_GET

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_task_reward_received
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _is_task_id_of_interest(self, task_id):
        return bool(self._task_id) and self._task_id == task_id

    def _on_task_progress_updated(self, task_id, *args):
        if not self._is_task_id_of_interest(task_id):
            return
        self._refresh_view()
        global_data.emgr.refresh_activity_redpoint.emit()

    def _on_task_reward_received(self, task_id, *args):
        if not self._is_task_id_of_interest(task_id):
            return
        self._refresh_view()
        global_data.emgr.refresh_activity_redpoint.emit()