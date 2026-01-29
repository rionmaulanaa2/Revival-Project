# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryTaskUI.py
from __future__ import absolute_import
import six
import six_ex
from functools import cmp_to_key
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils import task_utils
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.client.const import mall_const
from common.uisys.basepanel import BasePanel
from logic.gcommon.time_utility import get_readable_time
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from cocosui import cc, ccui, ccs

class LotteryTaskUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/premium_lottery_task'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'close'
       }
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, activity_type):
        self._activity_type = activity_type
        self.init_parameters()
        self.init_event()
        self.register_timer()
        self.panel.PlayAnimation('show')
        self.init_widget()

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()

    def init_parameters(self):
        self._timer = 0
        self._timer_cb = {}

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def _on_update_reward(self, task_id):
        global_data.player.read_activity_list(self._activity_type)
        self.show_list()

    def init_widget(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        act_name_id = conf['cNameTextID']
        self.panel.lab_describe_2.SetString(get_text_by_id(conf.get('cDescTextID', '')))
        btn_describe = self.panel.btn_describe

        @btn_describe.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(conf.get('cRuleTextID', '')))
            x, y = btn_describe.GetPosition()
            wpos = btn_describe.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]

        def callback--- This code section failed: ---

 111       0  LOAD_GLOBAL           0  'task_utils'
           3  LOAD_ATTR             1  'get_left_open_time'
           6  LOAD_DEREF            0  'parent_task'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            0  'left_time'

 112      15  LOAD_DEREF            1  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_ATTR             3  'lab_time_2'
          24  LOAD_ATTR             4  'SetString'
          27  LOAD_GLOBAL           5  'get_readable_time'
          30  LOAD_FAST             0  'left_time'
          33  CALL_FUNCTION_1       1 
          36  CALL_FUNCTION_1       1 
          39  POP_TOP          

 114      40  POP_TOP          
          41  POP_TOP          
          42  POP_TOP          
          43  COMPARE_OP            0  '<'
          46  POP_JUMP_IF_FALSE    63  'to 63'

 115      49  LOAD_DEREF            1  'self'
          52  LOAD_ATTR             6  'close'
          55  CALL_FUNCTION_0       0 
          58  POP_TOP          

 116      59  LOAD_CONST            0  ''
          62  RETURN_END_IF    
        63_0  COME_FROM                '46'

Parse error at or near `POP_TOP' instruction at offset 40

        self._timer_cb[0] = callback
        callback()
        self.show_list()

    def reorder_task_list(self, tasks):

        def cmp_func(task_id_a, task_id_b):
            has_rewarded_a = global_data.player.has_receive_reward(task_id_a)
            has_rewarded_b = global_data.player.has_receive_reward(task_id_b)
            if has_rewarded_a != has_rewarded_b:
                if has_rewarded_a:
                    return 1
                if has_rewarded_b:
                    return -1
            return six_ex.compare(int(task_id_a), int(task_id_b))

        ret_list = sorted(tasks, key=cmp_to_key(cmp_func))
        return ret_list

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        parent_task = task_list[0]
        children_tasks = task_utils.get_children_task(parent_task)
        children_tasks = self.reorder_task_list(children_tasks)
        self._children_tasks = children_tasks
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(children_tasks))
        ui_data = conf.get('cUiData', {})
        for i, task_id in enumerate(children_tasks):
            item_widget = sub_act_list.GetItem(i)
            item_widget.lab_task_name.SetString(task_utils.get_task_name(task_id))
            if ui_data.get('lab_name_color'):
                color = int(ui_data.get('lab_name_color'), 16)
                item_widget.lab_task_name.SetColor(color)
            if ui_data.get('lab_num_color'):
                color = int(ui_data.get('lab_num_color'), 16)
                item_widget.lab_task_progress.SetColor(color)
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list_simple(item_widget.list_award, reward_id, show_tips=False)

        self.refresh_list()

    def refresh_list(self):
        from common import utilities
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._children_tasks):
            item_widget = sub_act_list.GetItem(i)
            total_times = task_utils.get_total_prog(task_id)
            jump_conf = task_utils.get_jump_conf(task_id)
            cur_times = global_data.player.get_task_prog(task_id)
            if total_times >= 1:
                item_widget.lab_task_progress.SetString('{}'.format(cur_times))
                item_widget.lab_task_progress_2.SetString('/{}'.format(total_times))
                item_widget.progress_task.SetPercentage(utilities.safe_percent(cur_times, total_times))
            else:
                item_widget.lab_task_progress.SetString('')
                item_widget.lab_task_progress_2.SetString('')
            btn = item_widget.temp_btn_get.btn_common
            item_widget.nd_get.setVisible(False)

            def check_btn(btn=btn):
                has_rewarded = global_data.player.has_receive_reward(task_id)
                if has_rewarded:
                    item_widget.nd_get.setVisible(True)
                    btn.setVisible(False)
                elif cur_times < total_times:
                    btn.setVisible(True)
                    text_id = jump_conf.get('unreach_text', '')
                    if text_id:
                        btn.SetText(text_id)
                        btn.SetEnable(True)
                    else:
                        btn.SetEnable(False)
                else:
                    btn.setVisible(True)
                    btn.SetEnable(True)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                _total_times = task_utils.get_total_prog(task_id)
                _cur_times = global_data.player.get_task_prog(task_id)
                jump_conf = task_utils.get_jump_conf(task_id)
                if _cur_times < _total_times and jump_conf.get('unreach_text', ''):
                    item_utils.exec_jump_to_ui_info(jump_conf)
                else:
                    global_data.player.receive_task_reward(task_id)
                    btn.SetText(80866)
                    btn.SetEnable(False)

            check_btn()