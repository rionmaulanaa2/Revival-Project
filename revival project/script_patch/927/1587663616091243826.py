# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMatchTeammate.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
import cc
from common.cfg import confmgr
import logic.gcommon.time_utility as tutil
from logic.gutils.jump_to_ui_utils import ACTIVITY_MAIN_UI

class ActivityMatchTeammate(ActivityTemplate):
    TIMER_TAG = 0

    def __init__(self, dlg, activity_type):
        super(ActivityMatchTeammate, self).__init__(dlg, activity_type)
        widget_type = confmgr.get('c_activity_config', activity_type, 'cWidgetType', default='None')
        self.main_ui = ACTIVITY_MAIN_UI.get(widget_type, {}).get('ui_name', None)
        return

    def on_init_panel(self):
        self.panel.PlayAnimation('show')
        act0 = cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show'))
        act1 = cc.CallFunc.create(lambda : self.panel.PlayAnimation('btn_loop'))
        self.panel.runAction(cc.Sequence.create([act0, act1]))

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch, *args):
            ui = global_data.ui_mgr.get_ui('LobbyUI')
            ui.on_click_add_player()
            global_data.ui_mgr.close_ui(self.main_ui)

        global_data.player.call_server_method('attend_activity', (self._activity_type,))
        self.refresh_time()
        self.refresh_reward()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.refresh_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(self.refresh_time)]))
        self.panel.runAction(act)
        act.setTag(self.TIMER_TAG)

    def unregister_timer(self):
        self.panel.stopActionByTag(self.TIMER_TAG)

    def get_end_time(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        return conf.get('cEndTime', 0)

    def refresh_time(self):
        end_time = self.get_end_time()
        if end_time:
            server_time = tutil.get_server_time()
            left_time = end_time - server_time
            if left_time > 0:
                self.panel.lab_date.SetString(get_text_by_id(607014).format(tutil.get_readable_time_2(left_time)))
            else:
                self.panel.lab_date.SetString(81796)
        else:
            self.panel.lab_date.SetString(81796)

    def refresh_reward(self, *args, **kwargs):
        from logic.gutils import task_utils, template_utils
        task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask')
        if not task_id:
            return
        item_id, item_num = task_utils.get_task_reward_list(task_id)[0]
        template_utils.init_tempate_reward(self.panel.temp_item, item_id, item_num)
        if global_data.player.has_receive_reward(task_id):
            self.panel.btn_sign.SetEnable(False)
            self.panel.btn_sign.SetText(80866)
        elif global_data.player.is_task_reward_receivable(task_id):
            self.panel.btn_sign.SetEnable(True)
            self.panel.btn_sign.SetText(80930)

            @self.panel.btn_sign.callback()
            def OnClick(*args):
                global_data.player.receive_task_reward(task_id)

        else:
            self.panel.btn_sign.SetEnable(False)
            self.panel.btn_sign.SetText(80930)