# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityCommon/ActivityCommonCharge.py
from __future__ import absolute_import
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.template_utils import init_template_mall_i_lottery_prog_item
from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_name
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_HEAD
from logic.gcommon.time_utility import get_readable_time, ONE_DAY_SECONDS
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc

class ActivityCommonCharge(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityCommonCharge, self).__init__(dlg, activity_type)
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
        ui_data = conf.get('cUiData', {})
        self.can_receive_task_cnt = 0
        self.special_prog_list = ui_data.get('special_prog_list', [])
        self.special_template = ui_data.get('special_template', '')
        self.special_name = ui_data.get('special_name', None)
        task_id = conf.get('cTask', None)
        if not task_id:
            return
        else:
            self.charge_task_id = task_id
            task_conf = task_utils.get_task_conf_by_id(task_id)
            self.charge_prog_rewards = task_conf.get('prog_rewards', [])
            head_frame_reward = self.charge_prog_rewards[-1][-1]
            reward_list = confmgr.get('common_reward_data', str(head_frame_reward), 'reward_list', default=[])
            head_frame_item_no = reward_list[0][0]
            self.head_frame_vx = 'head/i_vx_%s' % head_frame_item_no
            self._timer = 0
            self._init_head_x = 0
            self._init_head_y = 0
            self.panel.txt_title.SetString(get_text_by_id(conf.get('cNameTextID')))
            return

    def init_event(self):
        self.process_event(True)

    def _update_get_all_reward(self):
        if not self.panel.btn_get_all:
            return
        if self.can_receive_task_cnt > 1:
            self.panel.btn_get.setVisible(False)
            self.panel.btn_get_all.setVisible(True)

            @self.panel.btn_get_all.unique_callback()
            def OnClick(btn, touch):
                global_data.player.receive_tasks_reward([self.charge_task_id])

        else:
            self.panel.btn_get.setVisible(True)
            self.panel.btn_get_all.setVisible(False)

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
        self.panel.temp_list.SetInitCount((len(self.charge_prog_rewards) + 1) // 2)
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
        self.refresh_left_time()

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0

    def refresh_left_time(self):
        if not self.panel or not self.panel.lab_title:
            return
        left_time = task_utils.get_raw_left_open_time(self.charge_task_id)
        if left_time > 0:
            self.panel.lab_title.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = ONE_DAY_SECONDS + left_time
            self.panel.lab_title.SetString(get_text_by_id(607014).format(get_readable_time(close_left_time)))

    def _refresh_charge_task_progress(self, is_init=False):
        self.can_receive_task_cnt = 0
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
        self._update_get_all_reward()

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
            img_node_path = 'gui/ui_res_2/activity/activity_bp_purchase_1_1/icon_bp_purchase_dot_1.png'
        elif is_receivable:
            img_node_path = 'gui/ui_res_2/activity/activity_bp_purchase_1_1/icon_bp_purchase_dot_3.png'
        else:
            img_node_path = 'gui/ui_res_2/activity/activity_bp_purchase_1_1/icon_bp_purchase_dot_2.png'
        sub_item_widget.img_node.SetDisplayFrameByPath('', img_node_path)

    def _update_charge_task_ui(self, index, prog_reward, is_max_reached_prog, is_init=False):
        if not global_data.player:
            return
        else:
            prog, reward_id = prog_reward
            task_cur_prog = global_data.player.get_task_prog(self.charge_task_id)
            item_index = index // 2
            sub_item_index = index % 2
            item_widget = self.panel.temp_list.GetItem(item_index)
            is_special = prog in self.special_prog_list
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
                self.can_receive_task_cnt += 1
                is_receivable = True
                show_tips = False
                temp_item_widget.btn_click.BindMethod('OnClick', lambda b, t, tid=self.charge_task_id, prog=prog: global_data.player.receive_task_prog_reward(tid, prog))
            self.update_receive_img(sub_item_widget, has_receive, is_receivable)
            reward_items = temp_item_widget.lv_item
            if is_special:
                temp_item_widget.lab_cell_name.SetString(str(prog * 10))
                temp_item_widget.DestroyChild('lv_item')
                reward_item_widget = global_data.ui_mgr.uis.load_template_create(self.special_template, temp_item_widget, name='lv_item')
                item_no, item_num = reward_list[0]
                init_template_mall_i_lottery_prog_item(reward_item_widget, item_no, item_num=item_num, show_name=True, show_rare_degree=False, show_tips=show_tips, show_all_num=False, img_frame_path=None)
                self.special_name and reward_item_widget.lab_name.SetString(self.special_name)
                reward_item_widget.nd_get.img_get_bar.setVisible(has_receive)
                reward_item_widget.nd_get.setVisible(has_receive)
                reward_item_widget.nd_get_tips.setVisible(is_receivable)
                if is_receivable:
                    reward_item_widget.PlayAnimation('get_tips')
                else:
                    reward_item_widget.StopAnimation('get_tips')
            else:
                temp_item_widget.lab_cell_name.SetString(str(prog * 10))
                reward_items.SetInitCount(len(reward_list))
                is_last_reward = index == len(self.charge_prog_rewards) - 1
                for i, reward_info in enumerate(reward_list):
                    item_no, item_num = reward_info[0], reward_info[1]
                    reward_item_widget = reward_items.GetItem(i)
                    if is_last_reward:
                        show_all_num = False
                    else:
                        show_all_num = True
                    init_template_mall_i_lottery_prog_item(reward_item_widget, item_no, item_num=item_num, show_name=False, show_rare_degree=True, show_tips=show_tips, show_all_num=show_all_num, img_frame_path=None)
                    if is_last_reward:
                        reward_item_widget.nd_cut.setVisible(False)
                        if is_init:
                            nd_parent = reward_item_widget.nd_vx
                            nd_parent.DestroyChild('nd_head_vx')
                            nd_vx = global_data.ui_mgr.uis.load_template_create(self.head_frame_vx, nd_parent, name='nd_head_vx')
                            nd_vx.PlayAnimation('show_head')
                            nd_vx.setScale(0.26)
                            nd_vx.pnl_bg.setVisible(False)
                        reward_item_widget.setScale(2)
                        reward_item_widget.nd_get_tips.img_tips.setScale(0.5)
                        reward_item_widget.nd_get_tips.img_tips.SetPosition('50%32', '50%32')
                        reward_item_widget.nd_get_tips.img_get_tips_bar.SetContentSize('100%30', '100%50')
                        reward_item_widget.SetPosition(self._init_head_x + 63, self._init_head_y - 40)
                        reward_item_widget.img_frame.setVisible(False)
                        reward_item_widget.btn_choose.setScale(0.9)
                        temp_item_widget.lab_cell_name.SetPosition(225, -115)
                        temp_item_widget.btn_click.setScale(1.2)
                        temp_item_widget.btn_click.SetPosition(220, 0)
                    reward_item_widget.nd_get.img_get_bar.setVisible(has_receive)
                    reward_item_widget.nd_get.setVisible(has_receive)
                    reward_item_widget.nd_get_tips.setVisible(is_receivable)
                    if is_receivable:
                        reward_item_widget.PlayAnimation('get_tips')
                    else:
                        reward_item_widget.StopAnimation('get_tips')

            if is_last_reward:
                temp_item_widget.vx_cut.setVisible(False)
            return