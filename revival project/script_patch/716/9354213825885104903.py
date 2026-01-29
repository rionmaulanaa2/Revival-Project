# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFairyland/ActivityFairylandCalendar.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from .ActivityFairylandCalendarMainUI import ActivityFairylandCalendarBase
from common.cfg import confmgr

class ActivityFairylandCalendar(ActivityTemplate):

    def on_init_panel(self):
        self.calendar_widget = ActivityFairylandCalendarTabPage(self.panel, self._activity_type)

    def on_finalize_panel(self):
        super(ActivityFairylandCalendar, self).on_finalize_panel()
        self.calendar_widget.on_finalize_panel()


class ActivityFairylandCalendarTabPage(ActivityFairylandCalendarBase):

    def __init__(self, panel, activity_type):
        super(ActivityFairylandCalendarTabPage, self).__init__(panel)
        self.process_event(True)
        self.share_task_id = confmgr.get('c_activity_config', activity_type, 'cTask', default='')
        self.refresh_share()

    def play_show_animation(self):
        super(ActivityFairylandCalendarTabPage, self).play_show_animation()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.refresh_share,
           'receive_task_reward_succ_event': self.refresh_share
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_share(self, *args):
        reward_recv = global_data.player.has_receive_reward(self.share_task_id)
        self.panel.img_share.setVisible(not reward_recv)
        global_data.emgr.refresh_activity_redpoint.emit()

    def init_panel(self):
        super(ActivityFairylandCalendarTabPage, self).init_panel()
        if global_data.is_pc_mode:
            self.panel.nd_share.setVisible(False)
            return

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.ShareUI import ShareUI
            share_ui = ShareUI(parent=self.panel)

            def init_cb():
                if share_ui and share_ui.is_valid():
                    share_ui.set_share_content_raw(self._share_content.get_render_texture(), need_scale=True, share_content=self._share_content)

                    def share_inform_func():
                        import cc
                        if global_data.player:
                            act = [cc.DelayTime.create(0.3),
                             cc.CallFunc.create(lambda : global_data.player.share_activity('activity_10601')),
                             cc.CallFunc.create(lambda : global_data.player.share())]
                            self.panel.runAction(cc.Sequence.create(act))
                        self.refresh_share()

                    share_ui.set_share_inform_func(share_inform_func)

            if not getattr(self, '_share_content', None):
                from logic.comsys.share.FairylandCalendarShareCreator import FairylandCalendarShareCreator
                self._share_content = FairylandCalendarShareCreator()
                self._share_content.create(parent=None, init_cb=init_cb)
            else:
                init_cb()
            return

    def on_video_ready(self):
        self.panel.SetTimeOut(0.1, lambda : self.panel.img_bg.setVisible(False))

    def on_finalize_panel(self):
        self.process_event(False)