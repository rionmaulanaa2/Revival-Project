# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/PrivilegeChargeWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from re import template
from logic.gutils import item_utils, jump_to_ui_utils
from logic.gutils import template_utils
from logic.gutils.template_utils import init_tempate_mall_i_item, init_tempate_reward
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_type, get_money_icon, get_lobby_item_use_parms
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_LOBBY_SKY_BOX, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA, L_ITEM_MECHA_SFX
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils import task_utils, mall_utils
from logic.gcommon.cdata import privilege_data
from common.utils.ui_path_utils import PRIVILEGE_BADGE_TEMPLTE, PRIVILEGE_BAR_BADGE_LEVEL, PRIVILEGE_LEVEL_REWARD
from logic.gcommon.const import PRIVILEGE_LEVEL_TO_SETTING, SHOP_PAYMENT_YUANBAO, PRIVILEGE_SETTING_TO_RED_POINT
import cc
SHOW_DETAIL_TYPE = [
 L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_ROLE_SKIN]
PIC_EXTRA_OFFSET = {1: ('50%', '40%'),
   4: ('50%', '40%'),
   6: ('50%', '40%'),
   7: ('50%', '40%'),
   8: ('50%', '40%'),
   9: ('50%', '40%')
   }
OLD_PRIVILEGE_LEVEL_CAP = 8
EXTRA_PRIVILEGE_LEVEL = privilege_data.LV_CAP - OLD_PRIVILEGE_LEVEL_CAP

class PrivilegeChargeWidget(object):

    def on_init_panel(self, panel):
        self.panel = panel
        self.panel.SetPosition('45%', '50%')
        self.init_paramaters()
        self.init_widget()
        self.init_event()
        self.process_event(True)
        global_data.ui_mgr.show_ui('PrivilegeWeekRewardPreviewUI', 'logic.comsys.reward')

    def init_paramaters(self):
        self._level = global_data.player.get_privilege_level() or 1
        self._cur_item_idx = 0
        self._task_cur_prog = 0
        self.task_id = privilege_data.PAY_TASK_ID
        self.max_level = privilege_data.LV_CAP
        self.privilege_prog_rewards = privilege_data.data
        self.privilege_display_rewards = privilege_data.display_reward_data
        self._other_rewards = {}
        self._prog_to_level = {}
        self._level_reward_type = {}
        self._prog_to_item = {}
        for level, reward in six.iteritems(self.privilege_prog_rewards):
            prog, _ = reward
            self._prog_to_level[prog] = level

        self.temp_badge = None
        self.old_prog_rewards = task_utils.get_prog_rewards(self.task_id)
        self.old_reward_len = len(self.old_prog_rewards)
        self.show_reward_item_num = self.old_reward_len + EXTRA_PRIVILEGE_LEVEL
        self.show_reward_list = []
        for idx in range(self.show_reward_item_num):
            if idx < self.old_reward_len:
                self.show_reward_list.append(self.old_prog_rewards[idx])
            else:
                prog, reward = self.privilege_prog_rewards[idx - self.old_reward_len + 1 + OLD_PRIVILEGE_LEVEL_CAP]
                self.show_reward_list.append([prog, reward])

        self.prog_list = [ prog for prog, _ in self.show_reward_list ]
        self.prog_list.sort()
        return

    def init_widget(self):
        for i in range(self.max_level):
            dot_icon = self.panel.list_dot.AddTemplateItem()
            dot_icon.img_list_dot.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/charge_reward/img_recharge_reward_dot0.png')

        self.panel.list_dot.setVisible(True)
        self._update_task_progress()
        self._init_reward_list()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self.update_recharge_level_reward_item(self._level, True)

    def init_event(self):
        self.panel.btn_left.BindMethod('OnClick', lambda btn, touch: self.on_btn_change_level(-1))
        self.panel.btn_right.BindMethod('OnClick', lambda btn, touch: self.on_btn_change_level(1))

        @self.panel.btn_charge.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_charge
            from logic.comsys.charge_ui.ChargeUINew import ACTIVITY_CHARGE_TYPE
            jump_to_charge(ACTIVITY_CHARGE_TYPE)

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            global_data.player.receive_all_task_prog_reward(str(self.task_id))
            global_data.player.call_server_method('receive_all_privilege_lv_reward')

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            if G_IS_NA_USER:
                dlg.set_show_rule(610214, 610290)
            else:
                dlg.set_show_rule(610214, 610289)

    def update_recharge_level_reward_item(self, level, is_init=False):
        if level < 1 or level > self.max_level:
            return
        if is_init:
            for idx in range(self.show_reward_item_num):
                prog, reward_id = self.show_reward_list[idx]
                temp_level = self._prog_to_level.get(prog)
                if temp_level:
                    reward_lst = template_utils.get_reward_list_by_reward_id(reward_id)
                    item_no, _ = reward_lst[0]
                    item_type = get_lobby_item_type(item_no)
                    if item_type in SHOW_DETAIL_TYPE:
                        self._level_reward_type[temp_level] = (
                         1, item_no)
                    else:
                        self._level_reward_type[temp_level] = (
                         0, item_no)

            _, last_reward_id = self.privilege_prog_rewards[8]
            six_reward_no, _ = self.privilege_display_rewards[6][1]
            item_no, _ = template_utils.get_reward_list_by_reward_id(last_reward_id)[0]
            self._level_reward_type[8] = (1, item_no)
            self._level_reward_type[6] = (1, six_reward_no)
            self._level_reward_type[10] = (L_ITEM_TYPE_LOBBY_SKY_BOX, 208000001)
            self._level_reward_type[11] = (1, 603000019)
            self._level_reward_type[12] = (1, 201009851)

            @self.panel.btn_look.unique_callback()
            def OnClick(btn, touch):
                item_type, item_no = self._level_reward_type[self._level]
                if item_type == L_ITEM_TYPE_LOBBY_SKY_BOX:
                    from logic.gutils.jump_to_ui_utils import jump_to_lobby_sky_box_preview
                    jump_to_lobby_sky_box_preview(item_no=item_no)
                if item_type != 0:
                    jump_to_ui_utils.jump_to_display_detail_by_item_no(item_no, {'role_info_ui': True})

        core_reward_pic = PRIVILEGE_LEVEL_REWARD[level]
        level_pic = PRIVILEGE_BAR_BADGE_LEVEL[level]
        frame_template = PRIVILEGE_BADGE_TEMPLTE[int(level)]
        priv_badge = self.panel.temp_badge.priv_badge
        if priv_badge:
            priv_badge.Destroy()
        priv_badge = global_data.uisystem.load_template_create(frame_template, parent=self.panel.temp_badge, name='priv_badge')
        priv_badge.img_num_level.SetDisplayFrameByPath('', level_pic)
        self.panel.img_item.SetDisplayFrameByPath('', core_reward_pic)
        self.panel.list_item.DeleteAllSubItem()
        self.panel.lab_tag.SetString(get_text_by_id(610213).format(level))
        level_prog, reward_id = self.privilege_prog_rewards[level]
        if reward_id != 0:
            privilege_reward_list = self.privilege_display_rewards[level]
            for i in range(len(privilege_reward_list)):
                item = self.panel.list_item.AddTemplateItem()
                item_no, item_num = privilege_reward_list[i]
                _show_tips = i != 0
                init_tempate_mall_i_item(item, item_no, item_num=item_num, show_rare_degree=False, show_tips=_show_tips)
                if not _show_tips:

                    @item.btn_choose.unique_callback()
                    def OnClick(btn, touch, _item_no=item_no):
                        self.on_click_week_reward_box_item(btn, _item_no)

                item.lab_name.setVisible(True)

        type_state, item_no = self._level_reward_type[level]
        self.panel.bar_level.setVisible(True)
        if type_state != 0:
            self.panel.btn_look.setVisible(True)
            item_name = get_lobby_item_name(item_no)
            self.panel.lab_item_name.SetString(item_name)
            item_rare_icon = item_utils.get_skin_rare_degree_icon(item_no)
        else:
            if level == 1:
                self.panel.lab_item_name.SetString(610282)
            elif level == 4:
                self.panel.lab_item_name.SetString(610283)
            else:
                self.panel.lab_item_name.SetString(610284)
            self.panel.btn_look.setVisible(False)
            item_rare_icon = item_utils.RARE_DEGREE_ICON[item_utils.RARE_DEGREE_4]
        self.panel.temp_level.bar_level.SetDisplayFrameByPath('', item_rare_icon)
        self.change_left_reward_text(level)
        act = [
         cc.DelayTime.create(0.14),
         cc.CallFunc.create(lambda : priv_badge.isValid() and priv_badge.PlayAnimation('show')),
         cc.CallFunc.create(lambda : priv_badge.isValid() and priv_badge.PlayAnimation('loop'))]
        if not is_init:
            act[0] = cc.CallFunc.create(lambda : self.panel and self.panel.PlayAnimation('switch'))
        self.panel.runAction(cc.Sequence.create(act))
        if level == 1:
            self.panel.btn_left.setVisible(False)
        elif level == self.max_level:
            self.panel.btn_right.setVisible(False)
        else:
            self.panel.btn_right.setVisible(True)
            self.panel.btn_left.setVisible(True)
        old_dot_icon = self.panel.list_dot.GetItem(self._level - 1)
        old_dot_icon.img_list_dot.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/charge_reward/img_recharge_reward_dot0.png')
        new_dot_icon = self.panel.list_dot.GetItem(level - 1)
        new_dot_icon.img_list_dot.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/charge_reward/img_recharge_reward_dot2.png')
        self._level = level
        self.update_btn_preview_state()
        self.locate_item_pos_by_level(level)

    def change_left_reward_text(self, level):
        level_prog, _ = self.privilege_prog_rewards[level]
        priv_reward_record = global_data.player.get_privilege_reward_record()
        if self._task_cur_prog < level_prog:
            if G_IS_NA_USER:
                txt = get_text_by_id(610212).format((level_prog - self._task_cur_prog) * 10)
                self.panel.lab_tips.SetString(txt)
            else:
                txt = get_text_by_id(610211).format(level_prog - self._task_cur_prog)
                self.panel.lab_tips.SetString(txt)
            self.panel.lab_tips.setVisible(True)
        elif priv_reward_record.is_record(level):
            self.panel.lab_tips.SetString(get_text_by_id(80451))
        else:
            self.panel.lab_tips.SetString(get_text_by_id(81708))

    def locate_item_pos_by_level(self, level):
        prog, _ = self.privilege_prog_rewards[level]
        item_idx = self.prog_list.index(prog) if prog in self.prog_list else None
        if item_idx is not None:
            self.panel.list_reward.LocatePosByItem(item_idx)
        self.panel.list_reward.scroll_Load()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.receive_task_prog_reward,
           'receive_privilege_level_reward_succ': self.receive_privilege_level_reward,
           'unlock_privilege_settings': self.unlock_privilege_setting,
           'player_leave_visit_scene_event': self.update_btn_preview_state,
           'player_enter_visit_scene_event': self.update_btn_preview_state
           }
        if is_bind:
            global_data.emgr.bind_events(econf)
        else:
            global_data.emgr.unbind_events(econf)

    def _init_reward_list(self):
        self.panel.list_reward.BindMethod('OnCreateItem', self._create_reward_item)
        self.panel.list_reward.DeleteAllSubItem()
        self.panel.list_reward.SetInitCount(self.show_reward_item_num)
        self.panel.list_reward.scroll_Load()

    def _create_reward_item(self, lv, idx, item):
        prog, reward_id = self.show_reward_list[idx]
        level = self._prog_to_level.get(prog, 0)
        item.data = (prog, reward_id, level)
        self._prog_to_item[prog] = item
        item.nd_item1.nd_cut.progress_bg.progress_bar.setPercent(0)
        reward_lst = template_utils.get_reward_list_by_reward_id(reward_id)
        if reward_lst:
            list_len = len(reward_lst)
            item_no, item_num = reward_lst[0]
            item_type = get_lobby_item_type(item_no)
            if item_type == L_ITEM_TYPE_MECHA_SKIN or item_type == L_ITEM_TYPE_ROLE_SKIN or item_type == L_ITEM_TYPE_MECHA or level:
                item.nd_reward_1.temp_item.setVisible(False)
                item.nd_reward_2.setVisible(False)
                item.nd_cut.setVisible(True)
                if level:
                    reward_pic = PRIVILEGE_LEVEL_REWARD[level]
                    if level == self.max_level:
                        item.nd_item1.nd_cut.setVisible(False)
                else:

                    @item.btn_reward.unique_callback()
                    def OnClick(btn, touch):
                        x, y = btn.GetPosition()
                        w, h = btn.GetContentSize()
                        x += w * 0.5
                        wpos = btn.ConvertToWorldSpace(x, y)
                        extra_info = {'show_jump': True,'btn_text': get_text_by_id(80706)}
                        global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                        return True

                    reward_pic = 'gui/ui_res_2/battle_mech_call_pic/201800641.png'
                    item.img_item.SetPosition('80%', '50%')
                item.img_item.SetDisplayFrameByPath('', reward_pic)
                pic_extra_offset = PIC_EXTRA_OFFSET.get(level, None)
                if pic_extra_offset:
                    item.img_item.SetPosition(*pic_extra_offset)
            elif list_len == 1:
                init_tempate_mall_i_item(item.nd_reward_1.temp_item, item_no, item_num=item_num, show_tips=True)
            else:
                item.nd_reward_1.setVisible(False)
                item.nd_reward_2.setVisible(True)
                item_no2, item_num2 = reward_lst[1]
                init_tempate_mall_i_item(item.nd_reward_2.temp_item, item_no, item_num=item_num, show_tips=True)
                init_tempate_mall_i_item(item.nd_reward_2.temp_item_2, item_no2, item_num=item_num2, show_tips=True)
            if not level:
                item.btn_get.setVisible(False)
                item.img_tag.setVisible(False)
            else:
                item.btn_get.SetText(get_text_by_id(610213).format(level))
                item.lab_tag.SetString(get_text_by_id(610214))

            @item.btn_get.unique_callback()
            def OnClick(btn, touch):
                self._on_click_progress_reward(prog, item)

            if level:

                @item.btn_reward.unique_callback()
                def OnClick(*args):
                    self.update_recharge_level_reward_item(level)

        item.RecordAnimationNodeState('show_01')
        item.PlayAnimation('show')
        item.PlayAnimation('show_01')
        self._update_reward_item_state(item)
        self._update_task_ui(idx, item)
        return

    def _update_reward_item_state(self, item):
        prog, _, level = item.data
        if not global_data.player:
            is_received, can_receive = False, False
        else:
            player = global_data.player
            privilege_reward_record = player.get_privilege_reward_record()
            is_received_task = player.has_receive_prog_reward(str(self.task_id), prog) if task_utils.has_prog_reward(str(self.task_id), prog) else True
            if level != 0:
                is_received_privilege = privilege_reward_record.is_record(level)
                can_receive_privilege = bool(self._task_cur_prog >= prog)
            else:
                is_received_privilege = True
                can_receive_privilege = False
            is_received = is_received_privilege and is_received_task
            can_receive_task = player.is_prog_reward_receivable(str(self.task_id), prog)
            can_receive = can_receive_task or can_receive_privilege
        if is_received:
            item.nd_got.setVisible(True)
            item.bar_item.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/charge_reward/img_recharge_reward_item0.png')
            item.btn_get.SetEnable(False)
            item.StopAnimation('show_01')
            item.RecoverAnimationNodeState('show_01')
            level = self._prog_to_level.get(prog)
            item.btn_get.SetSelect(False)
            if level:
                item.btn_get.SetText(get_text_by_id(610213).format(level))
                item.lab_tag.SetString(get_text_by_id(610214))
            else:
                item.btn_get.setVisible(False)
        elif can_receive:
            item.bar_item.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/charge_reward/img_recharge_reward_item2.png')
            item.btn_get.SetText(get_text_by_id(80930))
            item.btn_get.SetSelect(True)
            item.btn_get.setVisible(True)
        else:
            item.btn_get.SetEnable(False)
            item.btn_get.SetSelect(False)
            item.bar_item.SetDisplayFrameByPath('', 'gui/ui_res_2/charge/charge_reward/img_recharge_reward_item0.png')

    def receive_task_prog_reward(self, task_id, prog):
        if task_id != str(self.task_id) or not self._prog_to_item.get(prog, False):
            return
        self._update_reward_item_state(self._prog_to_item[prog])

    def receive_privilege_level_reward(self, priv_lv, lv_rewards):
        for level in range(1, priv_lv + 1):
            prog, _ = self.privilege_prog_rewards[level]
            if not self._prog_to_item.get(prog, False):
                continue
            self._update_reward_item_state(self._prog_to_item[prog])
            self.change_left_reward_text(level)

    def unlock_privilege_setting(self, priv_lv):
        priv_settings = PRIVILEGE_LEVEL_TO_SETTING.get(priv_lv, [])
        for setting in priv_settings:
            red_point_name = PRIVILEGE_SETTING_TO_RED_POINT[setting] + str(global_data.player.uid)
            setting_point_name = setting + str(global_data.player.uid)
            if global_data.achi_mgr.get_cur_user_archive_data(red_point_name, -1) == -1:
                global_data.achi_mgr.set_cur_user_archive_data(red_point_name, 0)
                global_data.emgr.update_setting_btn_red_point.emit()
                global_data.achi_mgr.set_cur_user_archive_data(setting_point_name, True)
                global_data.player.update_privilege_setting(setting, True)
                global_data.emgr.update_privilege_state.emit()
                ui = global_data.ui_mgr.get_ui('PrivilegeSettingTips')
                if not ui:
                    global_data.ui_mgr.show_ui('PrivilegeSettingTips', 'logic.comsys.privilege')

    def _update_task_progress(self):
        if not global_data.player:
            return False
        self._task_cur_prog = global_data.player.get_task_prog(str(self.task_id))
        if G_IS_NA_USER:
            self.panel.lab_tips_charge.SetString(get_text_by_id(610216).format(self._task_cur_prog * 10))
        else:
            self.panel.lab_tips_charge.SetString(get_text_by_id(610215).format(self._task_cur_prog))

    def _update_task_ui(self, idx, item_widget):
        if not global_data.player:
            return False
        item_idx = idx
        prog, _ = self.show_reward_list[item_idx]
        res_idx = 0
        item_widget.nd_item0.setVisible(False)
        if item_idx != 0 and item_idx != self.show_reward_item_num - 1:
            progress_node = item_widget.nd_item1.nd_cut.progress_bg.progress_bar
            next_prog, _ = self.show_reward_list[item_idx + 1]
            if self._task_cur_prog >= prog and self._task_cur_prog < next_prog:
                percent = 100 * (1 - (next_prog - self._task_cur_prog) * 1.0 / (next_prog - prog))
                res_idx = 2
            elif self._task_cur_prog < prog:
                percent = 0
                res_idx = 0
            else:
                percent = 100
                res_idx = 3
            progress_node.setPercent(percent)
        elif item_idx == 0:
            item_widget.nd_item0.setVisible(True)
            next_prog, _ = self.show_reward_list[item_idx + 1]
            if self._task_cur_prog < prog:
                percent0 = 100 * (1 - (prog - self._task_cur_prog) * 1.0 / prog)
                percent1 = 0
                res_idx = 0
            elif self._task_cur_prog >= prog and self._task_cur_prog < next_prog:
                percent0 = 100
                percent1 = 100 * (1 - (next_prog - self._task_cur_prog) * 1.0 / (next_prog - prog))
                res_idx = 2
            else:
                percent0 = 100
                percent1 = 100
                res_idx = 3
            progress_node0 = item_widget.nd_item0.nd_cut.progress_bg.progress_bar
            progress_node0.setPercent(percent0)
            progress_node1 = item_widget.nd_item1.nd_cut.progress_bg.progress_bar
            progress_node1.setPercent(percent1)
        elif self._task_cur_prog >= prog:
            res_idx = 3
        else:
            res_idx = 0
        node_pic = 'gui/ui_res_2/charge/charge_reward/prog_recharge_reward_dot_%s.png' % res_idx
        item_widget.img_node.SetDisplayFrameByPath('', node_pic)
        if G_IS_NA_USER:
            txt = '<color=0XFFFFFFFF></color>%d<img ="%s",scale=0.0>' % (prog * 10, get_money_icon(SHOP_PAYMENT_YUANBAO))
            item_widget.lab_price.SetString(txt)
        else:
            txt = str(prog) + get_text_by_id(12158)
            item_widget.lab_price.SetString(txt)
        item_widget.setVisible(True)

    def on_btn_change_level(self, change_value):
        next_level = self._level + change_value
        if next_level <= 0 or next_level > self.max_level:
            return
        self.update_recharge_level_reward_item(next_level)

    def _on_click_progress_reward(self, prog, item):
        if not global_data.player:
            return
        can_receive = global_data.player.is_prog_reward_receivable(str(self.task_id), prog)
        if can_receive:
            global_data.player.receive_task_prog_reward(str(self.task_id), prog)
        level = self._prog_to_level.get(prog, 0)
        if level != 0:
            global_data.player.call_server_method('receive_privilege_lv_reward', (level,))

    def on_finalize_panel(self):
        self.panel.list_item.DeleteAllSubItem()
        self.panel.list_dot.DeleteAllSubItem()
        self.panel.list_reward.DeleteAllSubItem()
        self.process_event(False)
        self.panel = None
        global_data.ui_mgr.close_ui('PrivilegeWeekRewardPreviewUI')
        global_data.emgr.refresh_activity_redpoint.emit()
        return

    def set_show(self, show):
        self.panel.setVisible(show)

    def on_click_week_reward_box_item(self, btn, item_no):
        x, y = btn.GetPosition()
        w, h = btn.GetContentSize()
        x += w * 0.5
        wpos = btn.ConvertToWorldSpace(x, y)
        reward_id = get_lobby_item_use_parms(item_no, {}).get('reward_id')
        if reward_id:
            reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            global_data.emgr.show_priv_week_reward_preview_event.emit(reward_list, wpos)

    def update_btn_preview_state(self, *args):
        if global_data.player and global_data.player.is_in_visit_mode():
            if self._level == 10:
                self.panel.btn_look.setVisible(False)
                return
        self.panel.btn_look.setVisible(True)

    def jump_to_priv_level(self, level):
        self.update_recharge_level_reward_item(level, True)