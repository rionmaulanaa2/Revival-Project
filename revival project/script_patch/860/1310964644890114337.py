# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonSevenDayLoginTask.py
from __future__ import absolute_import
import cc
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.comsys.activity.widget import widget
from logic.gutils import task_utils
from logic.gutils.client_utils import post_method
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no

@widget('AsyncAllReceiveTaskListWidget', 'DescribeWidget')
class ActivityCommonSevenDayLoginTask(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCommonSevenDayLoginTask, self).__init__(dlg, activity_type)
        conf = confmgr.get('c_activity_config', self._activity_type, default={})
        ui_data = conf.get('cUiData', {})
        self._fixed_task_id = conf.get('cTask', '')
        self._collect_task = ui_data.get('change_task', '1410655')
        self._desc_item_no = ui_data.get('desc_item_no')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._refresh_gun_progress,
           'receive_task_prog_reward_succ_event': self._refresh_gun_progress
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.process_event(False)
        super(ActivityCommonSevenDayLoginTask, self).on_finalize_panel()

    def on_init_panel(self):
        super(ActivityCommonSevenDayLoginTask, self).on_init_panel()
        self.process_event(True)
        self._init_gun_progress()
        self._refresh_gun_progress()

    def refresh_panel(self):
        super(ActivityCommonSevenDayLoginTask, self).refresh_panel()
        self._refresh_gun_progress()

    def _init_gun_progress(self):

        @self.panel.btn_gun_see.unique_callback()
        def OnClick(btn, touch):
            if self._desc_item_no:
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(self._desc_item_no, None, directly_world_pos=position)
            return

        prog_rewards = task_utils.get_prog_rewards(self._collect_task)
        self.panel.list_item.SetInitCount(len(prog_rewards))
        for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            progress, reward_id = prog_rewards[idx]
            if idx == 0:
                self._min_progress = progress
            self._max_progress = progress
            node = getattr(self.panel, 'lab_number_{}'.format(int(idx) + 1))
            node.SetString(str(progress))
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = reward_list[0]
            item_path = get_lobby_item_pic_by_item_no(item_no)
            ui_item.item.SetDisplayFrameByPath('', item_path)
            ui_item.lab_quantity.setVisible(True)
            ui_item.lab_quantity.SetString(str(item_num))
            ui_item._reward_data = (progress, item_no, item_num)

    @post_method
    def _refresh_gun_progress(self, *args):
        if not global_data.player or not self.panel:
            return
        player = global_data.player
        for idx, ui_item in enumerate(self.panel.list_item.GetAllItem()):
            progress, item_no, item_num = ui_item._reward_data
            can_receive = player.is_prog_reward_receivable(self._collect_task, progress) and not player.has_receive_prog_reward(self._collect_task, progress)
            is_received = player.has_receive_prog_reward(self._collect_task, progress)
            if is_received:
                ui_item.nd_get.setVisible(True)
                ui_item.nd_lock.setVisible(True)
                ui_item.btn_choose.SetSelect(False)
            elif can_receive:
                ui_item.btn_choose.SetSelect(True)
            else:
                ui_item.btn_choose.SetSelect(False)

            @ui_item.btn_choose.unique_callback()
            def OnClick(btn, touch, progress=progress, item_no=item_no, item_num=item_num, can_receive=can_receive):
                if can_receive:
                    global_data.player.receive_task_prog_reward(self._collect_task, progress)
                else:
                    x, y = btn.GetPosition()
                    w, h = btn.GetContentSize()
                    x += w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    extra_info = {'show_jump': False}
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

        now_prog = global_data.player.get_task_prog(self._collect_task)
        min_progress = 8
        if now_prog <= self._min_progress:
            self.panel.prog_inside.SetPercentage(float(now_prog) / self._min_progress * min_progress)
        else:
            self.panel.prog_inside.SetPercentage(float(now_prog - self._min_progress) / (self._max_progress - self._min_progress) * (100 - min_progress) + min_progress)
        if hasattr(self.panel, 'lab_prog') and self.panel.lab_prog:
            self.panel.lab_prog.SetString(get_text_by_id(634532, {'num': now_prog}))
        TIMER_TAG = 220427
        if player.has_receive_prog_reward(self._collect_task, 100):
            self.panel.bar_tips_get.setVisible(True)
            self.panel.stopActionByTag(TIMER_TAG)
            self.panel.bar_tips_count_down.setVisible(False)
            self.panel.bar_tips_riko.setVisible(False)
        elif player.has_receive_prog_reward(self._collect_task, 1):
            self.panel.bar_tips_count_down.setVisible(True)
            task_left_time = task_utils.get_raw_left_open_time(self._fixed_task_id)
            if task_left_time <= 86400:
                action_list = [cc.CallFunc.create(lambda : self.panel and self.panel.bar_tips_count_down.setVisible(False)),
                 cc.CallFunc.create(lambda : self.panel and self.panel.bar_tips_riko.setVisible(True)),
                 cc.DelayTime.create(5),
                 cc.CallFunc.create(lambda : self.panel and self.panel.bar_tips_riko.setVisible(False)),
                 cc.CallFunc.create(lambda : self.panel and self.panel.bar_tips_count_down.setVisible(True))]
                act = self.panel.runAction(cc.Sequence.create(action_list))
                act.setTag(TIMER_TAG)