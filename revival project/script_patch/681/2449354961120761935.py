# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityGranbelmShare.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_const import activity_const
from logic.comsys.activity.ActivityTemplate import ActivityGlobalTemplate
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.new_template_utils import CommonItemReward, GranbelmItemReward
from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
from logic.gutils import task_utils
from logic.gutils import activity_utils
import random
from logic.gcommon.item.item_const import ITEM_UNGAIN, ITEM_RECEIVED, ITEM_UNRECEIVED
from logic.gcommon import time_utility

class ActivityGranbelmShare(ActivityGlobalTemplate):
    GLOBAL_EVENT = {'message_update_global_stat': 'up_tick_goal_num',
       'message_update_global_reward_receive': '_update_gl_receive_state',
       'receive_task_reward_succ_event': 'on_task_data_changed'
       }
    GLOBAL_SHARE_PCT_CFG = (35, 60, 85, 100)
    SOLO_SHARE_PCT_CFG = (0, 35, 60, 85, 100)

    def __init__(self, dlg, activity_type):
        super(ActivityGranbelmShare, self).__init__(dlg, activity_type)
        self.init_widget()
        self.init_ui_event()

    def init_parameters(self):
        super(ActivityGranbelmShare, self).init_parameters()
        self.share_cnt_task_id = self.ui_data.get('share_cnt_task_id', None)
        self.day_task_id = self.ui_data.get('day_task_id', None)
        self.des_num_list = []
        self._screen_capture_helper = None
        for achieve_id in self._achieve_id_lst:
            des_num = confmgr.get('global_achieve_data', str(achieve_id), 'iCondValue')
            self.des_num_list.append(des_num)

        return

    def init_ui_event(self):

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(609100))

        cur_param_index = 0
        nRet, text_id = self.exec_custom_condition(cur_param_index)

        @self.panel.nd_share.temp_btn_share.btn_major.unique_callback()
        def OnClick(btn, touch):
            if global_data.is_pc_mode:
                global_data.game_mgr.show_tip(get_text_by_id(607929))
                return
            from logic.comsys.share.GranbelmGlobalShareCreator import GranbelmGlobalShareCreator
            share_creator = GranbelmGlobalShareCreator()
            share_creator.create()
            share_content = share_creator
            from logic.comsys.share.ShareUI import ShareUI
            ShareUI().set_share_content_raw(share_content.get_render_texture(), share_content=share_content)
            share_ui = global_data.ui_mgr.get_ui('ShareUI')
            if share_ui:

                def share_inform_func():
                    if global_data.player:
                        global_data.player.share_activity('activity_10203')

                share_ui.set_share_inform_func(share_inform_func)

    def init_widget(self):
        self.update_personal_share()
        self.panel.PlayAnimation('loop1')
        self.panel.PlayAnimation('loop2')
        self.panel.PlayAnimation('loop3')

    def get_achieve_reward_nodes(self):
        ret = []
        for x in range(1, len(self._achieve_id_lst) + 1):
            nd_reward = getattr(self.panel, 'nd_reward_%s' % x)
            ret.append([getattr(nd_reward, 'temp_reward'), getattr(nd_reward, 'lab_num')])

        return ret

    def _init_global_achieve_base(self):
        for x in range(0, len(self._achieve_id_lst)):
            achieve_id = self._achieve_id_lst[x]
            des_num = confmgr.get('global_achieve_data', str(achieve_id), 'iCondValue')
            reward_id = confmgr.get('global_achieve_data', str(achieve_id), 'iRewardID')
            reward_nd, num_nd = self._achieve_nodes[x]
            box_widget = GranbelmItemReward(reward_nd, reward_id, self.on_click_achieve_reward, (x, achieve_id))
            self._gl_box_widget[achieve_id] = box_widget
            num_nd.SetString(str(des_num))

        self._update_gl_receive_state()
        self.up_tick_goal_num()

    def update_personal_share(self):
        prog = global_data.player.get_task_prog(self.share_cnt_task_id)
        total_prog = task_utils.get_total_prog(self.share_cnt_task_id)
        idx = min(prog, len(self.SOLO_SHARE_PCT_CFG) - 1)
        self.panel.nd_prog.progress_exp_solo.SetPercent(self.SOLO_SHARE_PCT_CFG[idx])

    def init_left_time(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        start_time = conf.get('cBeginTime', 0)
        end_time = conf.get('cEndTime', 0)
        if start_time and end_time:
            start_dt = time_utility.get_utc8_datetime(start_time)
            end_dt = time_utility.get_utc8_datetime(end_time)
            start_str = time_utility.datetime_to_time_str(start_dt, '%Y.%m.%d')
            end_str = time_utility.datetime_to_time_str(end_dt, '%Y.%m.%d')
            self.panel.lab_time.SetString('{0}-{1}'.format(start_str, end_str))
        self.register_timer()
        self.second_callback()

    def on_task_data_changed(self, task_id):
        if task_id == self.share_cnt_task_id:
            self._update_gl_receive_state()
            self.update_personal_share()

    def on_click_achieve_reward(self, item_no, position, idx, achieve_id):
        if global_data.player.get_task_prog(self.share_cnt_task_id) <= idx:
            global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
            return
        else:
            global_stat = global_data.player.get_gl_reward_receive_state(achieve_id)
            if global_stat == ITEM_UNGAIN:
                global_data.game_mgr.show_tip(get_text_by_id(608417))
                return
            if global_stat == ITEM_RECEIVED:
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
                return
            global_data.player.try_get_global_achieve(achieve_id)
            return

    def up_tick_goal_num(self, *args):
        global_stat_data = global_data.player or None if 1 else global_data.player.get_global_stat_data()
        if global_stat_data is None:
            return
        else:
            latest_num = global_stat_data.get(str(self._parent_achieve), {}).get(self._achieve_name, 0)
            if latest_num < 0:
                return
            if self._is_first_open:
                last_cache = global_data.player or 0 if 1 else global_data.player.get_simulate_cache(self._achieve_name)
                if last_cache >= latest_num:
                    last_cache = latest_num
                self._tick_now_num = max(int(last_cache), int(latest_num * 0.99))
                random_num = random.uniform(5000, 15000)
                if latest_num - random_num > 0:
                    self._tick_now_num = max(self._tick_now_num, random_num)
                self._is_first_open = False
            if self._tick_goal_num == latest_num:
                return
            self._tick_goal_num = latest_num
            self._tick_now_num = min(self._tick_goal_num, self._tick_now_num)
            self._second_tick_increase_num = max(1, (self._tick_goal_num - self._tick_now_num) / self.SIMULATE_TIMES)
            return

    def second_callback(self):
        self.second_simulate_up()
        self._times += 1
        if self._times > self.INTERVAL_TIMES:
            self.interval_update()
            self._times = 0

    def second_simulate_up(self, *args):
        if self._tick_goal_num is None or self._tick_now_num is None:
            self.panel.nd_num.lab_num.SetString('0')
            return
        else:
            self._tick_now_num += self._second_tick_increase_num
            if self._tick_now_num >= self._tick_goal_num:
                self._tick_now_num = self._tick_goal_num
            self.panel.nd_num.lab_num.SetString(str(int(self._tick_now_num)))
            des_num_list = self.des_num_list
            des_num_list.append(5000000)
            if self._tick_goal_num >= 5000000:
                self.panel.nd_content.nd_reward.nd_prog.progress_exp.SetPercent(100)
            else:
                for idx, des_num in enumerate(des_num_list):
                    if self._tick_now_num < des_num:
                        if idx == 0:
                            base_p = 0
                            base_num = 0
                        else:
                            base_p = self.GLOBAL_SHARE_PCT_CFG[idx - 1]
                            base_num = self.des_num_list[idx - 1]
                        intv_p = self.GLOBAL_SHARE_PCT_CFG[idx] - base_p
                        intv_num = des_num - base_num
                        percent = base_p + (self._tick_now_num - base_num) * 1.0 * intv_p / intv_num
                        self.panel.nd_content.nd_reward.nd_prog.progress_exp.SetPercent(percent)
                        break

            self._update_gl_receive_state()
            return

    def _update_gl_receive_state(self):
        is_lock = False
        global_data.player.read_activity_list(self._activity_type)
        task_prog = global_data.player.get_task_prog(self.share_cnt_task_id)
        for idx, a_id in enumerate(self._achieve_id_lst):
            global_stat = global_data.player.get_gl_reward_receive_state(a_id)
            if task_prog <= idx:
                global_stat = ITEM_UNGAIN
                is_lock = True
            else:
                is_lock = False
            box_widget = self._gl_box_widget.get(a_id, None)
            if box_widget:
                box_widget.update_nd_lock_state(is_lock)
                box_widget.update_nd_get_tips_state(global_stat == ITEM_UNRECEIVED)
                box_widget.update_nd_get_state(global_stat == ITEM_RECEIVED)
                nd_reward = getattr(self.panel, 'nd_reward_%s' % (idx + 1))
                if global_stat != ITEM_UNGAIN and nd_reward:
                    nd_reward.img_received.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202004/img_gear_choose.png')

        return