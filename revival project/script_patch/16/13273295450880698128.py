# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202209/ActivityUnlockByTimeTask.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityCollect import ActivityCollect
from common.cfg import confmgr
from logic.gutils import template_utils
from logic.gutils import activity_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gutils import task_utils
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import item_utils
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, BTN_ST_INACTIVE
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
import cc

class ActivityUnlockByTimeTask(ActivityCollect):

    def __init__(self, dlg, activity_type):
        super(ActivityUnlockByTimeTask, self).__init__(dlg, activity_type)
        self.conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = self.conf.get('cUiData', {})
        self.task_list = task_utils.get_children_task(self.conf['cTask'])

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_init_panel(self):
        act_name_id = self.conf.get('cNameTextID', '')
        self.panel.lab_tdescribe and self.panel.lab_tdescribe.SetString(get_text_by_id(self.conf.get('cDescTextID', '')))
        btn_question = self.panel.btn_question
        if btn_question:

            @btn_question.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(self.conf.get('cRuleTextID', '')))
                x, y = btn.GetPosition()
                wpos = btn.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.show_list()

        @self.panel.btn_go.unique_callback()
        def OnClick(btn, touch):
            widget_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.emgr.trigger_activity_main_close_btn.emit(widget_type)
            from logic.gutils.jump_to_ui_utils import jump_to_mode_choose
            from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
            jump_to_mode_choose(PLAY_TYPE_CHICKEN)

    def show_list(self):
        player = global_data.player
        if not player:
            return
        if self.panel.lab_time:
            self._timer_cb[0] = lambda : self.refresh_time(self.conf['cTask'])
            self.refresh_time(self.conf['cTask'])
        cur_task_idx = global_data.player.get_task_children_idx(self.conf['cTask'])
        for i, task_id in enumerate(self.task_list):
            nd = getattr(self.panel, 'temp_item_%d' % (i + 1))
            if not nd:
                continue
            reward_id = task_utils.get_task_reward(task_id)
            if reward_id:
                import common.cfg.confmgr as confmgr
                from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                if not reward_conf:
                    continue
                reward_list = reward_conf.get('reward_list', [])
                if not reward_list:
                    continue
                item_no, item_num = reward_list[0]
                reward_item = nd.item
                item_path = get_lobby_item_pic_by_item_no(item_no)
                reward_item.SetDisplayFrameByPath('', item_path)
                time_txt = task_utils.get_task_start_time_str(task_id, format='%m.%d')
                is_open = task_utils.is_task_open(task_id)
                if not is_open:
                    status = -1
                else:
                    status = player.get_task_reward_status(task_id)
                is_in_progress = cur_task_idx >= i
                is_lock = status in (-1, ) or not is_in_progress
                nd.bar_tips.setVisible(is_lock)
                if status == ITEM_RECEIVED:
                    nd.bar_day.EnableCustomState(False)
                    nd.bar_day.SetShowEnable(False)
                    nd.bar_item.EnableCustomState(False)
                    nd.bar_item.SetShowEnable(False)
                else:
                    nd.bar_day.EnableCustomState(True)
                    nd.bar_day.SetSelect(status != -1)
                    nd.bar_item.SetSelect(status != -1)
                if status == ITEM_UNRECEIVED:
                    nd.nd_get_tips.setVisible(True)
                    nd.PlayAnimation('get_tips')
                else:
                    nd.nd_get_tips.setVisible(False)
                    nd.StopAnimation('get_tips')
                nd.nd_got.setVisible(status == ITEM_RECEIVED)
                nd.bar_day.SetText(time_txt)

                @nd.bar_item.unique_callback()
                def OnClick(btn, touch, task_id=task_id, item_no=item_no, item_num=item_num, status=status):
                    if status == ITEM_UNRECEIVED:
                        if not activity_utils.is_activity_in_limit_time(self._activity_type):
                            return
                        _total_times = task_utils.get_total_prog(task_id)
                        _cur_times = global_data.player.get_task_prog(task_id)
                        jump_conf = task_utils.get_jump_conf(task_id)
                        if _cur_times < _total_times and jump_conf.get('unreach_text', ''):
                            item_utils.exec_jump_to_ui_info(jump_conf)
                        else:
                            global_data.player.receive_task_reward(task_id)
                    else:
                        x, y = btn.GetPosition()
                        w, h = btn.GetContentSize()
                        x += w * 0.5
                        wpos = btn.ConvertToWorldSpace(x, y)
                        extra_info = {'show_jump': True}
                        global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                    return

    def refresh_time(self, parent_task):
        if not self.panel or not self.panel.lab_time:
            return
        task_left_time = task_utils.get_raw_left_open_time(self.conf['cTask'])
        if task_left_time > 0:
            if task_left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(task_left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(task_left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(close_left_time)))