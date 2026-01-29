# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAccumulateCharge.py
from __future__ import absolute_import
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_item_rare_degree, get_lobby_item_type, REWARD_RARE_COLOR, get_money_icon
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gcommon.item import lobby_item_type
from logic.gcommon.item import item_const
import logic.gcommon.const as gconst
import cc

class ActivityAccumulateCharge(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityAccumulateCharge, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()

    def on_finalize_panel(self):
        self.process_event(False)

    def init_parameters(self):
        task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.check_index = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={}).get('jump_tag_index', [])
        if not task_id:
            return
        else:
            self.cur_item_index = 0
            self.task_id = task_id
            self.task_conf = task_utils.get_task_conf_by_id(task_id)
            self.total_prog = self.task_conf.get('total_prog', 0)
            self.prog_rewards = self.task_conf.get('prog_rewards', [])
            self._prog_to_index = {}
            self.left_show_index = None
            self.right_show_index = None
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

    def on_init_panel(self):
        self.panel.PlayAnimation('show')
        act0 = cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('show'))
        act1 = cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))
        self.panel.runAction(cc.Sequence.create([act0, act1]))
        if not global_data.player:
            return
        self.panel.lits_item.SetInitCount(len(self.prog_rewards) + 1)
        item_widget = self.panel.lits_item.GetItem(0)
        item_widget.nd_content.setVisible(False)
        self._refresh_task_progress(True)

        @self.panel.btn_close_quick.unique_callback()
        def OnClick(btn, touch, *args):
            global_data.ui_mgr.close_ui('ActivityChargeMainUI')

        self.panel.lits_item.LocatePosByItem(self.cur_item_index)

        def OnScrollEvent(scrollview, event):
            self.show_arrow()

        self.panel.lits_item.addEventListener(OnScrollEvent)
        self.show_arrow()

        @self.panel.btn_get.btn_common_big.unique_callback()
        def OnClick(btn, touch):
            player = global_data.player
            if not player:
                return
            player.receive_all_task_prog_reward(self.task_id)

    def show_arrow(self):
        all_item = self.panel.lits_item.GetAllItem()
        if not all_item:
            self.panel.arrow_left.setVisible(False)
            self.panel.arrow_right.setVisible(False)
            return
        else:
            first_nd = all_item[0]
            last_nd = all_item[-1]
            first_show = first_nd and self.panel.lits_item.IsNodeVisible(first_nd)
            last_show = last_nd and self.panel.lits_item.IsNodeVisible(last_nd)
            self.panel.arrow_left.setVisible(not first_show)
            self.panel.arrow_right.setVisible(not last_show)
            l_index, r_index = self.panel.lits_item.GetVisibleRange()
            count = len(all_item)
            left_show_index = None
            right_show_index = None
            for index in self.check_index:
                if index < count:
                    nd = all_item[index]
                    if index > 0:
                        front_nd = all_item[index - 1]
                    show = nd and self.panel.lits_item.IsNodeVisible(nd)
                    front_show = front_nd and self.panel.lits_item.IsNodeVisible(front_nd)
                    if show and front_show:
                        continue
                    if index <= l_index:
                        if left_show_index is None:
                            left_show_index = index
                        else:
                            left_show_index = max(index, left_show_index)
                    elif index >= r_index:
                        if right_show_index is None:
                            right_show_index = index
                        else:
                            right_show_index = min(index, right_show_index)

            self.panel.btn_bubble1.setVisible(False)
            self.panel.btn_bubble2.setVisible(False)
            if left_show_index is not None and left_show_index > 0:
                _, reward_id = self.prog_rewards[left_show_index - 1]
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                if reward_list:
                    self.panel.btn_bubble1.setVisible(True)
                    item_no, item_num = reward_list[0]
                    init_tempate_mall_i_item(self.panel.btn_bubble1.temp_item1, item_no, item_num=item_num, show_tips=False)
                    if left_show_index != self.left_show_index:

                        @self.panel.btn_bubble1.unique_callback()
                        def OnClick(btn, touch, index=left_show_index):
                            self.panel.lits_item.LocatePosByItem(index)
                            self.show_arrow()

                    self.left_show_index = left_show_index
            if right_show_index is not None and right_show_index > 0:
                _, reward_id = self.prog_rewards[right_show_index - 1]
                reward_conf = confmgr.get('common_reward_data', str(reward_id))
                reward_list = reward_conf.get('reward_list', [])
                if reward_list:
                    self.panel.btn_bubble2.setVisible(True)
                    item_no, item_num = reward_list[0]
                    init_tempate_mall_i_item(self.panel.btn_bubble2.temp_item2, item_no, item_num=item_num, show_tips=False)
                    if right_show_index != self.right_show_index:

                        @self.panel.btn_bubble2.unique_callback()
                        def OnClick(btn, touch, index=right_show_index):
                            self.panel.lits_item.LocatePosByItem(index)
                            self.show_arrow()

                    self.right_show_index = right_show_index
            return

    def _refresh_task_progress(self, is_init=False):
        if not global_data.player:
            return
        is_receivable = False
        for i, prog_reward in enumerate(self.prog_rewards):
            result = self._update_task_ui(i, prog_reward, is_init)
            is_receivable = is_receivable or result

        self.panel.btn_get.btn_common_big.SetEnable(is_receivable)
        item_widget = self.panel.lits_item.GetItem(len(self.prog_rewards))
        progress_node = item_widget.progress_ing
        progress_node.setVisible(False)

    def receive_task_prog_reward(self, task_id, prog):
        if self.task_id != task_id:
            return
        self._refresh_task_progress()

    def task_prog_changed(self, changes):
        for change in changes:
            if self.task_id == change.task_id:
                self._refresh_task_progress()
                break

    def _update_task_ui(self, index, prog_reward, is_init):
        if not global_data.player:
            return False
        else:
            prog, reward_id = prog_reward
            task_cur_prog = global_data.player.get_task_prog(self.task_id)
            item_index = index + 1
            item_widget = self.panel.lits_item.GetItem(item_index)
            front_item_widget = self.panel.lits_item.GetItem(index)
            progress_node = front_item_widget.progress_ing
            show_lab_money_left = False
            if progress_node:
                if index > 0:
                    front_prog, _ = self.prog_rewards[index - 1]
                else:
                    front_prog = 0
                if task_cur_prog >= prog:
                    self.cur_item_index = index
                    percent = 100
                elif task_cur_prog < front_prog:
                    percent = 0
                else:
                    percent = 100 * (1 - (prog - task_cur_prog) * 1.0 / (prog - front_prog))
                    self.cur_item_index = index
                    show_lab_money_left = True
                if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
                    progress_node.SetPercentage(percent)
                else:
                    progress_node.SetPercent(percent)
                if show_lab_money_left:
                    if is_init:
                        item_widget.PlayAnimation('show2')
                        act0 = cc.DelayTime.create(item_widget.GetAnimationMaxRunTime('show2'))
                        act1 = cc.CallFunc.create(lambda : item_widget.PlayAnimation('loop2'))
                        item_widget.runAction(cc.Sequence.create([act0, act1]))
                    else:
                        item_widget.PlayAnimation('loop2')
                else:
                    item_widget.StopAnimation('loop2')
                item_widget.nd_lab.setVisible(show_lab_money_left)
                if G_IS_NA_USER:
                    item_widget.lab_money_left.SetString(get_text_by_id(12174).format(prog=max(prog - task_cur_prog, 0) * 10))
                else:
                    item_widget.lab_money_left.SetString(get_text_by_id(12160).format(prog=max(prog - task_cur_prog, 0)))
                if G_IS_NA_USER:
                    txt = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>%d' % (get_money_icon(gconst.SHOP_PAYMENT_YUANBAO), prog * 10)
                    item_widget.text_1.SetString(txt)
                    item_widget.text_1_sel.SetString(txt)
                else:
                    txt = '<size = 32>' + str(prog) + '</size><size = 28>' + get_text_by_id(12158) + '</size>'
                    item_widget.text_1.SetString(txt)
                    item_widget.text_1_sel.SetString(txt)
            reward_conf = confmgr.get('common_reward_data', str(reward_id))
            reward_list = reward_conf.get('reward_list', [])
            if not reward_list:
                return False
            show_ani = False
            is_receive = True
            show_tips = True
            is_receivable = False
            item_widget.btn_img_circle.SetEnable(True)
            item_widget.btn_progress_point.SetEnable(True)
            item_widget.img_light.setVisible(False)
            has_receive = global_data.player.has_receive_prog_reward(self.task_id, prog)
            item_widget.btn_click.UnBindMethod('OnClick')
            if has_receive:
                item_widget.btn_img_circle.SetEnable(False)
            elif global_data.player.is_prog_reward_receivable(self.task_id, prog):
                is_receivable = True
                show_ani = True
                show_tips = False
                if is_init:
                    item_widget.PlayAnimation('show_in')
                item_widget.img_light.setVisible(True)
                item_widget.btn_click.BindMethod('OnClick', lambda b, t, tid=self.task_id, prog=prog: global_data.player.receive_task_prog_reward(tid, prog))
            else:
                is_receive = False
                item_widget.btn_progress_point.SetEnable(False)
            item_widget.text_1.setVisible(not is_receive)
            item_widget.text_1_sel.setVisible(is_receive)
            if G_IS_NA_USER:
                self.panel.text_charge_num.SetString(get_text_by_id(12173).format(prog=task_cur_prog * 10))
            else:
                self.panel.text_charge_num.SetString(get_text_by_id(12159).format(prog=task_cur_prog))
            reward_items = item_widget.list_item
            reward_items.SetInitCount(len(reward_list))
            quality = item_const.RARE_DEGREE_4
            for i, reward_info in enumerate(reward_list):
                item_no, item_num = reward_info[0], reward_info[1]
                reward_item_widget = reward_items.GetItem(i)
                reward_item_widget.item_1.setScale(1.6)
                reward_item_widget.head_bg.setVisible(False)
                item_type = get_lobby_item_type(item_no)
                if item_type in [lobby_item_type.L_ITEM_TYPE_ROLE, lobby_item_type.L_ITEM_TYPE_ROLE_SKIN, lobby_item_type.L_ITEM_TYPE_MECHA,
                 lobby_item_type.L_ITEM_TYPE_MECHA_SKIN, lobby_item_type.L_ITEM_TYPE_HEAD_PHOTO]:
                    init_tempate_mall_i_item(reward_item_widget.item_1, item_no, item_num=item_num, show_tips=show_tips)
                    reward_item_widget.item_1.img_frame.setVisible(True)
                    reward_item_widget.item_1.nd_lock.setVisible(has_receive)
                    reward_item_widget.nd_got.setVisible(True)
                    reward_item_widget.cut_item_1.setVisible(False)
                    reward_item_widget.img_got.setVisible(has_receive)
                else:
                    init_tempate_mall_i_item(reward_item_widget.item_1, item_no, item_num=item_num, show_rare_degree=False, show_tips=show_tips)
                    reward_item_widget.item_1.img_frame.setVisible(False)
                    if item_type == lobby_item_type.L_ITEM_TYPE_HEAD_FRAME:
                        reward_item_widget.item_1.setScale(2.0)
                        reward_item_widget.head_bg.setVisible(True)
                    reward_item_widget.item_1.nd_lock.setVisible(False)
                    icon_path = get_lobby_item_pic_by_item_no(item_no)
                    reward_item_widget.cut_item_1.SetMaskFrameByPath('', icon_path)
                    reward_item_widget.nd_got.setVisible(has_receive)
                    reward_item_widget.cut_item_1.setVisible(has_receive)
                    reward_item_widget.img_got.setVisible(has_receive)
                reward_item_widget.lab_item_name.SetString(get_lobby_item_name(item_no))
                reward_item_widget.cut_lizi.setVisible(show_ani)
                quality = get_item_rare_degree(item_no)
                if is_init and show_ani:
                    reward_item_widget.PlayAnimation('show1')
                    reward_item_widget.PlayAnimation('loop1')
                elif show_ani:
                    reward_item_widget.PlayAnimation('loop1')
                else:
                    reward_item_widget.StopAnimation('loop1')
                    reward_item_widget.nd_content1.SetPosition('50%0', '50%0')

            color = REWARD_RARE_COLOR.get(quality, 'orange')
            floor_pic = 'gui/ui_res_2/charge/charge_bonus/img/img_%sfloor.png' % color
            floor2_pic = 'gui/ui_res_2/charge/charge_bonus/img/img_%sfloor2.png' % color
            light1_pic = 'gui/ui_res_2/charge/charge_bonus/img/img_%slight1.png' % color
            item_widget.btn_img_circle.SetFrames('', [floor_pic, floor_pic, floor2_pic], False, None)
            item_widget.img_vx_light.SetDisplayFrameByPath('', light1_pic)
            item_widget.img_light.SetDisplayFrameByPath('', light1_pic)
            return is_receivable