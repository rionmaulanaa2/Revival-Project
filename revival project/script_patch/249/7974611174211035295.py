# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySummer/ActivitySummerCalendar2022.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from common.cfg import confmgr
from .ActivitySummerCalendar2022MainUI import ActivitySummerCalendar2022Base

class ActivitySummerCalendar2022(ActivityTemplate):

    def on_init_panel(self):
        self.calendar_widget = ActivitySummerCalendar2022TabPage(self.panel, self._activity_type)

    def on_finalize_panel(self):
        super(ActivitySummerCalendar2022, self).on_finalize_panel()
        self.calendar_widget.on_finalize_panel()


class ActivitySummerCalendar2022TabPage(ActivitySummerCalendar2022Base):

    def __init__(self, panel, activity_type):
        self.ACTIVITY_ID = activity_type
        super(ActivitySummerCalendar2022TabPage, self).__init__(panel)
        self.process_event(True)
        self.refresh_share()

    def play_show_animation(self):
        super(ActivitySummerCalendar2022TabPage, self).play_show_animation()
        self.panel.nd_content.setVisible(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.refresh_share
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def need_alt_btn(self):
        return global_data.channel.is_steam_channel()

    def refresh_share(self, *args):
        if not global_data.player:
            return
        if global_data.player.has_unreceived_task_reward(self.SHARE_TASK_ID):
            global_data.player.receive_task_reward(self.SHARE_TASK_ID)
        self._refresh_share_btn(global_data.player.has_receive_reward(self.SHARE_TASK_ID))

    def init_panel(self):
        super(ActivitySummerCalendar2022TabPage, self).init_panel()

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.ShareUI import ShareUI
            share_ui = ShareUI(parent=self.panel)

            def init_cb():
                if share_ui and share_ui.is_valid():
                    share_ui.set_share_content_raw(self._share_content.get_render_texture(), need_scale=True, share_content=self._share_content)

                    def share_inform_func():
                        if global_data.player:
                            global_data.player.share_activity(self.share_id)
                            global_data.player.share()
                        self.refresh_share()

                    share_ui.set_share_inform_func(share_inform_func)

            if not getattr(self, '_share_content', None):
                from logic.comsys.share.SummerCalendar2022ShareCreator import SummerCalendar2022ShareCreator
                self._share_content = SummerCalendar2022ShareCreator(self.ACTIVITY_ID)
                conf = confmgr.get('c_activity_config', str(self.ACTIVITY_ID), 'cUiData', default={})
                share_templ = conf.get('share_templ')
                self._share_content.create(parent=None, init_cb=init_cb, tmpl=share_templ)
            else:
                init_cb()
            return

    def on_finalize_panel(self):
        self.process_event(False)

    def _refresh_share_btn(self, has_shared):
        self.panel.btn_share1 and self.panel.btn_share1.setVisible(not has_shared)
        self.panel.btn_share2 and self.panel.btn_share2.setVisible(has_shared)