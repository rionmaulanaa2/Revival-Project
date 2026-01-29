# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityRedCliff/ActivityRedCliffCharge.py
from __future__ import absolute_import
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.template_utils import init_template_mall_i_lottery_prog_item
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_name
from logic.gcommon.item import item_const
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_HEAD
import cc
from logic.gcommon.time_utility import get_readable_time, ONE_DAY_SECONDS
from logic.gcommon.common_utils.local_text import get_text_by_id

class ActivityRedCliffCharge(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityRedCliffCharge, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel.StopAnimation('loop')
        self.panel.StopAnimation('show')
        self.panel.stopAllActions()
        self.unregister_timer()

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', str(self._activity_type), default={})
        task_id = conf.get('cTask', None)
        if not task_id:
            return
        else:
            ui_conf = conf.get('cUiData', {})
            self.charge_task_id = task_id
            task_conf = task_utils.get_task_conf_by_id(task_id)
            self.charge_prog_rewards = task_conf.get('prog_rewards', [])
            self._timer = 0
            self._init_head_x = 0
            self._init_head_y = 0
            return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.receive_task_prog_reward,
           'task_prog_changed': self.task_prog_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def get_progress_bg(self, nd_item):
        if nd_item.progress_bg:
            return nd_item.progress_bg
        else:
            return nd_item.nd_cut.progress_bg

    def play_show_anim(self):
        self.panel.StopAnimation('loop')
        self.panel.PlayAnimation('show')
        act0 = cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show'))
        act1 = cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))
        self.panel.runAction(cc.Sequence.create([act0, act1]))

    def on_init_panel(self):
        self.play_show_anim()
        if not global_data.player:
            return
        self.panel.temp_list.SetInitCount((len(self.charge_prog_rewards) + 1) / 2)
        self._refresh_charge_task_progress(True)
        end_item = self.panel.temp_list.GetItem(-1)
        if len(self.charge_prog_rewards) % 2:
            end_item.nd_item1.setVisible(False)
            progress_bg = self.get_progress_bg(end_item.nd_item0)
            progress_bg.setVisible(False)
        else:
            progress_bg = self.get_progress_bg(end_item.nd_item1)
            progress_bg.setVisible(False)

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            from logic.gutils import jump_to_ui_utils
            jump_to_ui_utils.jump_to_charge(tab_idx=0)

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch, *args):
            desc_id = confmgr.get('c_activity_config', self._activity_type, 'cDescTextID')
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

        self.register_timer()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.panel.temp_list.PlayAnimation('show_common')

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_left_time, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def refresh_left_time(self):
        left_time = task_utils.get_raw_left_open_time(self.charge_task_id)
        if left_time > 0:
            self.panel.lab_title.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = ONE_DAY_SECONDS + left_time
            self.panel.lab_title.SetString(get_text_by_id(607014).format(get_readable_time(close_left_time)))

    def _refresh_charge_task_progress(self, is_init=False):
        if not global_data.player:
            return
        if global_data.player.is_task_finished(self.charge_task_id):
            self.panel.lab_info and self.panel.lab_info.SetString(609976)
        show_lab_rules = False
        task_cur_prog = global_data.player.get_task_prog(self.charge_task_id)
        self.panel.lab_tips.SetString(get_text_by_id(610216).format(str(task_cur_prog * 10)))
        reached_max_index = -1
        for index, prog_reward in enumerate(self.charge_prog_rewards):
            prog, reward_id = prog_reward
            if task_cur_prog >= prog:
                reached_max_index = index

        for i, prog_reward in enumerate(self.charge_prog_rewards):
            self._update_charge_task_ui(i, prog_reward, i == reached_max_index, is_init)
            prog, reward_id = prog_reward
            if not show_lab_rules and task_cur_prog < prog:
                show_prog = prog - task_cur_prog
                self._refresh_charge_lab_rules(show_prog, reward_id)
                show_lab_rules = True

        max_prog = self.charge_prog_rewards[-1][0]
        if task_cur_prog >= max_prog:
            self.panel.lab_text_on.SetString(get_text_by_id(610541))

    def _refresh_charge_lab_rules(self, need_prog, reward_id):
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        if not reward_list:
            return
        item_no, item_num = reward_list[0]
        params = (need_prog * 10, get_lobby_item_name(item_no))
        self.panel.lab_info.SetString(get_text_by_id(609972).format(*params))

    def receive_task_prog_reward(self, task_id, prog):
        if self.charge_task_id == task_id:
            self._refresh_charge_task_progress()
            global_data.emgr.refresh_activity_redpoint.emit()

    def task_prog_changed(self, changes):
        refreshed = False
        for change in changes:
            if self.charge_task_id == change.task_id:
                self._refresh_charge_task_progress()
                refreshed = True

        if refreshed:
            global_data.emgr.refresh_activity_redpoint.emit()

    def update_receive_img(self, sub_item_widget, has_receive, is_receivable):
        if has_receive:
            img_node_path = 'gui/ui_res_2/lottery/lottery_activity/red_cliff/icon_red_cliff_collection_dot_2.png'
        elif is_receivable:
            img_node_path = 'gui/ui_res_2/lottery/lottery_activity/red_cliff/icon_red_cliff_collection_dot_3.png'
        else:
            img_node_path = 'gui/ui_res_2/lottery/lottery_activity/red_cliff/icon_red_cliff_collection_dot_1.png'
        sub_item_widget.img_node.SetDisplayFrameByPath('', img_node_path)

    def _update_charge_task_ui(self, index, prog_reward, is_max_reached_prog, is_init=False):
        if not global_data.player:
            return
        else:
            prog, reward_id = prog_reward
            task_cur_prog = global_data.player.get_task_prog(self.charge_task_id)
            item_index = index / 2
            sub_item_index = index % 2
            item_widget = self.panel.temp_list.GetItem(item_index)
            if is_init:
                item_widget.PlayAnimation('show_common')
            if item_index != 0 and sub_item_index == 0:
                item_widget.progress_bg0.setVisible(False)
            if index == 0:
                sub_item_widget = item_widget.nd_item0
                progress_node = item_widget.progress_bar0
                item_widget.progress_bg0.setVisible(True)
            elif sub_item_index == 0:
                sub_item_widget = item_widget.nd_item0
                front_item_widget = self.panel.temp_list.GetItem(item_index - 1)
                progress_bg = self.get_progress_bg(front_item_widget.nd_item1)
                progress_node = progress_bg.progress_bar
            else:
                sub_item_widget = item_widget.nd_item1
                progress_bg = self.get_progress_bg(item_widget.nd_item0)
                progress_node = progress_bg.progress_bar
            temp_item_widget = sub_item_widget.temp_item
            if progress_node:
                if index > 0:
                    front_prog, _ = self.charge_prog_rewards[index - 1]
                else:
                    front_prog = 0
                if task_cur_prog >= prog:
                    percent = 100
                elif task_cur_prog < front_prog:
                    percent = 0
                else:
                    percent = 100 * (1 - (prog - task_cur_prog) * 1.0 / (prog - front_prog))
                if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
                    progress_node.SetPercentage(percent)
                else:
                    progress_node.SetPercent(percent)
            temp_item_widget.lab_cell_name.SetString(get_text_by_id(82125).format(prog))
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            if not reward_list:
                return
            is_receivable = False
            show_tips = True
            has_receive = global_data.player.has_receive_prog_reward(self.charge_task_id, prog)
            temp_item_widget.btn_click.UnBindMethod('OnClick')
            if has_receive:
                pass
            elif global_data.player.is_prog_reward_receivable(self.charge_task_id, prog):
                is_receivable = True
                show_tips = False
                temp_item_widget.btn_click.BindMethod('OnClick', lambda b, t, tid=self.charge_task_id, prog=prog: global_data.player.receive_task_prog_reward(tid, prog))
            self.update_receive_img(sub_item_widget, has_receive, is_receivable)
            reward_items = temp_item_widget.lv_item
            show_prog = prog
            temp_item_widget.lab_cell_name.SetString(str(show_prog * 10))
            reward_items.SetInitCount(len(reward_list))
            for i, reward_info in enumerate(reward_list):
                item_no, item_num = reward_info[0], reward_info[1]
                reward_item_widget = reward_items.GetItem(i)
                frame_path = 'gui/ui_res_2/activity/activity_202109/kizuna/charge/bar_kizuna_charge_item.png'
                show_name = False
                if index == len(self.charge_prog_rewards) - 1:
                    frame_path = 'gui/ui_res_2/activity/activity_202109/kizuna/charge/bar_kizuna_charge_item3.png'
                elif get_lobby_item_type(item_no) == L_ITEM_TYPE_HEAD:
                    show_name = True
                    frame_path = 'gui/ui_res_2/activity/activity_202109/kizuna/charge/bar_kizuna_charge_item2.png'
                init_template_mall_i_lottery_prog_item(reward_item_widget, item_no, item_num=item_num, show_name=show_name, show_rare_degree=True, show_tips=show_tips, show_all_num=True, img_frame_path=None)
                if index == len(self.charge_prog_rewards) - 1:
                    reward_item_widget.nd_cut.setVisible(False)
                    if is_init:
                        nd_parent = reward_item_widget.nd_vx
                        nd_parent.DestroyChild('nd_head_vx')
                        nd_vx = global_data.ui_mgr.uis.load_template_create('head/i_vx_30290014', nd_parent, name='nd_head_vx')
                        nd_vx.PlayAnimation('show_head')
                        nd_vx.setScale(0.26)
                    reward_item_widget.setScale(1.3)
                    reward_item_widget.SetPosition(self._init_head_x - 15, self._init_head_y + 20)
                    reward_item_widget.img_frame.ResizeAndPosition(include_self=True)
                reward_item_widget.nd_get.img_get_bar.setVisible(has_receive)
                reward_item_widget.nd_get.setVisible(has_receive)
                reward_item_widget.nd_get_tips.setVisible(is_receivable)
                if is_receivable:
                    reward_item_widget.PlayAnimation('get_tips')
                else:
                    reward_item_widget.StopAnimation('get_tips')

            return