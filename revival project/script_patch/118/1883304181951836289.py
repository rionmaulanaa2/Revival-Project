# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityLuckScore.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.comsys.activity.ActivityCollect import ActivityBase
from logic.gutils import task_utils
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityLuckScore(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityLuckScore, self).__init__(dlg, activity_type)
        self.init_parameters()

    def on_init_panel(self):
        super(ActivityLuckScore, self).on_init_panel()
        self.init_luck_prog_widget()
        self.init_luck_score_lab()
        self.init_receive_all_btn()
        self.process_event(True)

    def on_finalize_panel(self):
        self.process_event(False)
        super(ActivityLuckScore, self).on_finalize_panel()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.receive_task_prog_reward,
           'task_prog_changed': self.task_prog_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        self.task_id = conf.get('cTask', '')
        self.lottery_reward_id = conf.get('cUiData', {}).get('lottery_reward_id')

    def init_luck_prog_widget(self):
        prog_rewards = task_utils.get_task_prog_rewards(self.task_id)
        reward_cnt = len(prog_rewards)
        self.panel.temp_list.SetInitCount(reward_cnt)
        self.refresh_luck_prog_widget()

    def refresh_luck_prog_widget(self):
        player = global_data.player
        prog_rewards = task_utils.get_task_prog_rewards(self.task_id)
        reward_cnt = len(prog_rewards)
        cur_prog = player.get_task_prog(self.task_id)
        last_prog = 0
        last_reward_item = None
        is_btn_get_enable = False
        for idx, (prog, reward_id) in enumerate(prog_rewards):
            reward_item = self.panel.temp_list.GetItem(idx)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            item_no, item_num = reward_list[0]
            can_recevie = player.is_prog_reward_receivable(self.task_id, prog) and not player.has_receive_prog_reward(self.task_id, prog)
            is_btn_get_enable = can_recevie or is_btn_get_enable
            has_receive = player.has_receive_prog_reward(self.task_id, prog)
            show_tips = not can_recevie
            init_tempate_mall_i_item(reward_item.temp_item, item_no, item_num=item_num, show_rare_degree=True, show_tips=show_tips, show_all_num=True)
            reward_item.lab_value.SetString(get_text_by_id(635443).format(prog))
            if prog > cur_prog:
                icon_dot_pat = 'gui/ui_res_2/lottery/lottery_activity/common/icon_lottery_dot_0.png'
            elif can_recevie:
                icon_dot_pat = 'gui/ui_res_2/lottery/lottery_activity/common/icon_lottery_dot_2.png'
            else:
                icon_dot_pat = 'gui/ui_res_2/lottery/lottery_activity/common/icon_lottery_dot_1.png'
            reward_item.icon_dot.SetDisplayFrameByPath('', icon_dot_pat)
            if idx != 0:
                reward_item.bar_prog.setVisible(False)
            if idx == reward_cnt - 1:
                reward_item.bar_prog_2.setVisible(False)
            if idx == 0:
                prog_item = reward_item.bar_prog.prog
            else:
                prog_item = last_reward_item.bar_prog_2.prog
            if cur_prog >= prog:
                prog_item.SetPercentage(100)
            elif last_prog < cur_prog < prog:
                percent = 1.0 * (cur_prog - last_prog) / (prog - last_prog) * 100
                prog_item.SetPercentage(percent)
            else:
                prog_item.SetPercentage(0)
            reward_item.temp_item.nd_get.setVisible(has_receive)
            reward_item.temp_item.nd_get.img_get_bar.setVisible(has_receive)
            reward_item.temp_item.nd_get_tips.setVisible(can_recevie)
            if can_recevie:
                reward_item.temp_item.btn_choose.BindMethod('OnClick', lambda b, t, tid=self.task_id, pg=prog: player.receive_task_prog_reward(tid, pg))
            if can_recevie:
                reward_item.temp_item.PlayAnimation('get_tips')
            else:
                reward_item.temp_item.StopAnimation('get_tips')
            last_reward_item = reward_item
            last_prog = prog

        self.set_btn_get_enable(is_btn_get_enable)
        return

    def init_receive_all_btn(self):

        @self.panel.btn_get.unique_callback()
        def OnClick(*args):
            self.on_click_receive_all_btn()

    def on_click_receive_all_btn(self):
        global_data.player.receive_all_task_prog_reward(self.task_id)

    def set_btn_get_enable(self, enable):
        self.panel.btn_get.SetEnable(enable)

    def init_luck_score_lab(self):
        total_luck = global_data.player.get_total_luck_by_reward_id(self.lottery_reward_id)
        luck_score = total_luck.get('luck_score', 0)
        self.panel.lab_value.SetString(get_text_by_id(635442).format(luck_score))

    def task_prog_changed(self, changes):
        for change in changes:
            if self.task_id == change.task_id:
                self.refresh_luck_prog_widget()
                break

    def receive_task_prog_reward(self, task_id, prog):
        if self.task_id != task_id:
            return
        self.refresh_luck_prog_widget()