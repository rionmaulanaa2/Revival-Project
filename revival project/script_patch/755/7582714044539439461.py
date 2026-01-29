# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/widget/IndependentTaskWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.activity.widget.Widget import Widget
from .ActivityWidgetBase import ActivityWidgetBase
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.gutils.client_utils import post_ui_method
from logic.gutils.item_utils import get_lobby_item_name

class IndependentTaskWidget(Widget):

    def on_init_panel(self):
        super(IndependentTaskWidget, self).on_init_panel()
        conf = confmgr.get('c_activity_config', self._activity_type)
        self._task_info_list = conf.get('cUiData', {}).get('task_info', [])
        self.__process_event(True)
        self._init_list_item()
        self._on_update_task()

    def __process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self._on_update_task,
           'receive_task_reward_succ_event': self._on_update_task,
           'receive_task_prog_reward_succ_event': self._on_update_task
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_list_item(self):
        l = len(self._task_info_list)
        for i in range(l):
            item = self.panel.list_item.GetItem(i)
            task_id = self._task_info_list[i][0]

            @item.temp_btn.btn_common.unique_callback()
            def OnClick(btn, touch, _task_id=task_id, *args):
                prog = global_data.player.get_task_prog(_task_id)
                max_prog = task_utils.get_total_prog(_task_id)
                if prog >= max_prog and not bool(global_data.player.has_receive_reward(_task_id)):
                    global_data.player.receive_task_reward(_task_id)
                    item.temp_red.setVisible(False)

    @post_ui_method
    def _on_update_task(self, *args):
        for i, reward_task_info in enumerate(self._task_info_list):
            item = self.panel.list_item.GetItem(i)
            item_list = task_utils.get_task_reward_list(reward_task_info[0])
            item_id = item_list[0][0]
            reward_name = get_lobby_item_name(item_id)
            item.lab_name.SetString(reward_name)
            prog = global_data.player.get_task_prog(reward_task_info[0])
            max_prog = task_utils.get_total_prog(reward_task_info[0])
            item.lab_rule.SetString(item.lab_rule.GetString().format(max_prog))
            item.lab_rule2.SetString(get_text_by_id(860238) + ':' + reward_name)
            item.lab_sign.SetString(get_text_by_id(reward_task_info[1]).format(prog, max_prog))
            if prog >= max_prog:
                item.temp_btn.setVisible(True)
            has_receive = bool(global_data.player.has_receive_reward(reward_task_info[0]))
            if has_receive:
                text = 604029 if 1 else 604030
                item.temp_btn.btn_common.SetText(get_text_by_id(text))
                item.temp_btn.btn_common.SetEnable(not has_receive)
                item.lab_sign.setVisible(prog < max_prog)
                item.img_tag.setVisible(has_receive)
                item.temp_red.setVisible(prog >= max_prog and not has_receive)

    def on_finalize_panel(self):
        self.__process_event(False)
        super(IndependentTaskWidget, self).on_finalize_panel()