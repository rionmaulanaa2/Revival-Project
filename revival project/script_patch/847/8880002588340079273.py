# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityArtCollectionAccumulate.py
from __future__ import absolute_import
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.item_utils import get_item_rare_degree
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import REWARD_RARE_COLOR
from logic.gcommon.item import item_const
import cc

class ActivityArtCollectionAccumulate(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityArtCollectionAccumulate, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)
        self.panel.StopAnimation('loop')
        self.panel.StopAnimation('show')
        self.panel.stopAllActions()

    def init_parameters(self):
        task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        if not task_id:
            return
        self.cur_item_index = 0
        self.task_id = task_id
        self.task_conf = task_utils.get_task_conf_by_id(task_id)
        self.prog_rewards = self.task_conf.get('prog_rewards', [])
        self._prog_to_index = {}

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
        self.panel.temp_list.SetInitCount(int((len(self.prog_rewards) + 1) / 2))
        self._refresh_task_progress(True)
        self.panel.temp_list.LocatePosByItem(self.cur_item_index)
        end_item = self.panel.temp_list.GetItem(-1)
        if len(self.prog_rewards) % 2:
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
            player.receive_all_task_prog_reward(self.task_id)

        self.panel.lab_text_on.SetString(get_text_by_id(80834))
        self.panel.lab_text_off.SetString(get_text_by_id(80834))

    def set_btn_get_enable(self, enable):
        self.panel.btn_get.SetEnable(enable)

    def _refresh_task_progress(self, is_init=False):
        if not global_data.player:
            return
        is_receivable = False
        for i, prog_reward in enumerate(self.prog_rewards):
            result = self._update_task_ui(i, prog_reward, is_init)
            is_receivable = is_receivable or result

        self.set_btn_get_enable(is_receivable)
        self.panel.btn_get.vx_btn and self.panel.btn_get.vx_btn.setVisible(is_receivable)
        self.panel.btn_get.lab_text_on.setVisible(is_receivable)
        self.panel.btn_get.lab_text_off.setVisible(not is_receivable)
        if self.panel.vx_btn:
            self.panel.vx_btn.setVisible(is_receivable)
        if self.panel.img_btn_light:
            self.panel.img_btn_light.setVisible(is_receivable)
        task_cur_prog = global_data.player.get_task_prog(self.task_id)
        self.panel.lab_stage.SetString(get_text_by_id(82124).format(task_cur_prog))
        global_data.emgr.refresh_activity_redpoint.emit()
        self.update_lab_info(task_cur_prog)

    def update_lab_info(self, task_cur_prog):
        index = -1
        for i, prog_reward in enumerate(self.prog_rewards):
            cur_tag_num = prog_reward[0]
            if task_cur_prog >= cur_tag_num:
                index += 1
                continue
            else:
                break

        if index + 1 == len(self.prog_rewards):
            self.panel.lab_info.SetString(get_text_by_id(609644))
        else:
            self.panel.lab_info.SetString(get_text_by_id(609643).format(self.prog_rewards[index + 1][0] - task_cur_prog))

    def receive_task_prog_reward(self, task_id, prog):
        if self.task_id != task_id:
            return
        self._refresh_task_progress()

    def task_prog_changed(self, changes):
        for change in changes:
            if self.task_id == change.task_id:
                self._refresh_task_progress()
                break

    def _get_task_reward_list(self, task_id):
        reward_id = str(task_utils.get_task_reward(task_id))
        reward_list = confmgr.get('common_reward_data', reward_id, 'reward_list', default=[])
        if len(reward_list) <= 0:
            return []
        return reward_list

    def update_receive_img(self, sub_item_widget, has_receive, is_receivable):
        img_node_path = 'gui/ui_res_2/lottery/lottery_activity/activity_s2_new/activity_s2_new_bones/img_progresspoint2.png'
        if has_receive:
            img_node_path = 'gui/ui_res_2/lottery/lottery_activity/activity_s2_new/activity_s2_new_bones/img_progresspoint1.png'
        elif is_receivable:
            img_node_path = 'gui/ui_res_2/lottery/lottery_activity/activity_s2_new/activity_s2_new_bones/img_progresspoint3.png'
        sub_item_widget.img_node.SetDisplayFrameByPath('', img_node_path)

    def _update_task_ui(self, index, prog_reward, is_init=False):
        if not global_data.player:
            return False
        prog, reward_id = prog_reward
        task_cur_prog = global_data.player.get_task_prog(self.task_id)
        item_index = index // 2
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
                front_prog, _ = self.prog_rewards[index - 1]
            else:
                front_prog = 0
            if task_cur_prog >= prog:
                self.cur_item_index = item_index
                percent = 100
            elif task_cur_prog < front_prog:
                percent = 0
            else:
                percent = 100 * (1 - (prog - task_cur_prog) * 1.0 / (prog - front_prog))
                self.cur_item_index = item_index
            if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
                progress_node.SetPercentage(percent)
            else:
                progress_node.SetPercent(percent)
        temp_item_widget.lab_cell_name.SetString(get_text_by_id(82125).format(prog))
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        if not reward_list:
            return False
        is_receivable = False
        show_tips = True
        has_receive = global_data.player.has_receive_prog_reward(self.task_id, prog)
        temp_item_widget.btn_click.UnBindMethod('OnClick')
        if has_receive:
            pass
        elif global_data.player.is_prog_reward_receivable(self.task_id, prog):
            is_receivable = True
            show_tips = False
            temp_item_widget.btn_click.BindMethod('OnClick', lambda b, t, tid=self.task_id, prog=prog: global_data.player.receive_task_prog_reward(tid, prog))
        self.update_receive_img(sub_item_widget, has_receive, is_receivable)
        reward_items = temp_item_widget.lv_item
        reward_items.SetInitCount(len(reward_list))
        quality = item_const.RARE_DEGREE_4
        for i, reward_info in enumerate(reward_list):
            item_no, item_num = reward_info[0], reward_info[1]
            reward_item_widget = reward_items.GetItem(i)
            init_tempate_mall_i_item(reward_item_widget, item_no, item_num=item_num, show_rare_degree=True, show_tips=show_tips, show_all_num=True)
            reward_item_widget.nd_get.setVisible(has_receive)
            reward_item_widget.nd_get.img_get_bar.setVisible(has_receive)
            reward_item_widget.nd_get_tips.setVisible(is_receivable)
            quality = get_item_rare_degree(item_no)
            if is_receivable:
                reward_item_widget.PlayAnimation('get_tips')
            else:
                reward_item_widget.StopAnimation('get_tips')

        if temp_item_widget.img_item_light:
            color = REWARD_RARE_COLOR.get(quality, 'orange')
            img_path = 'gui/ui_res_2/lottery/lottery_activity/activity_02/img_%s.png'
            temp_item_widget.img_item_light.SetDisplayFrameByPath('', img_path % color)
        return is_receivable