# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLoginShare.py
from __future__ import absolute_import
import six_ex
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.comsys.activity.widget.GlobalAchievementWidget import GlobalAchievementWidget
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils

class ActivityLoginShare(ActivityTemplate):

    def on_init_panel(self):
        super(ActivityLoginShare, self).on_init_panel()
        self.widget_map = {}
        self.init_task_list()
        self.init_countdown_widget()
        self.refresh_data()

        @self.panel.btn_question.callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(602039, 610662)

    def on_finalize_panel(self):
        for widget in six_ex.values(self.widget_map):
            widget.on_finalize_panel()

        self.widget_map = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self.refresh_data,
           'receive_task_reward_succ_event': self.refresh_data
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_task_list(self):
        from logic.comsys.activity.widget.TaskListWithTagWidget import TaskListWithTagWidget
        self.widget_map['task_list'] = TaskListWithTagWidget(self.panel, self._activity_type)

    def init_countdown_widget(self):
        from logic.comsys.activity.widget.CountdownWidget import CountdownWidget
        self.widget_map['countdown'] = CountdownWidget(self.panel.lab_time, self._activity_type, {'completion': True})

    def refresh_data(self, *args):
        ui_data = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        conf = (
         (
          ui_data['login_task'], 907154, 907156),
         (
          ui_data['share_task'], 907155, 907157))
        for i, (reward_task_id, total_text, prog_text) in enumerate(conf):
            item = self.panel.list_item.GetItem(i)
            item_list = task_utils.get_task_reward_list(reward_task_id)
            item_id = item_list[0][0]
            from logic.gutils.item_utils import get_lobby_item_name
            reward_name = get_lobby_item_name(item_id)
            item.lab_name.SetString(reward_name)
            prog = global_data.player.get_task_prog(reward_task_id)
            max_prog = task_utils.get_total_prog(reward_task_id)
            item.lab_rule.SetString(get_text_by_id(total_text).format(max_prog))
            item.lab_rule2.SetString(get_text_by_id(860238) + ':' + reward_name)
            item.lab_sign.SetString(get_text_by_id(prog_text) + '%d/%d' % (prog, max_prog) + get_text_by_id(80998))
            has_receive = bool(global_data.player.has_receive_reward(reward_task_id))
            item.lab_sign.setVisible(not has_receive)
            item.img_tag.setVisible(has_receive)