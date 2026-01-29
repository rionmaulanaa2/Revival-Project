# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivitySakuganDayLogin.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gutils import activity_utils
from logic.gutils import template_utils
from logic.comsys.activity.ActivityCollect import ActivityCollect
from logic.gcommon.time_utility import get_day_hour_minute_second, get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc

class ActivitySakuganDayLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivitySakuganDayLogin, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.prog_2_reward_id = task_utils.get_prog_rewards_in_dict(self._task_id)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_update_reward(self, *args):
        global_data.player.read_activity_list(self._activity_type)
        self.show_list()

    def on_init_panel(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        btn_question = self.panel.btn_question
        if btn_question:

            @btn_question.unique_callback()
            def OnClick(btn, touch):
                dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
                dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(conf.get('cDescTextID', '')))
                x, y = btn_question.GetPosition()
                wpos = btn_question.GetParent().ConvertToWorldSpace(x, y)
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.5, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        text_time = '2021.11.11-11.25'
        self.panel.lab_time.SetString(text_time)
        self.show_list()
        self.panel.PlayAnimation('show')

    def reorder_prog_list(self, progs):
        ret_list = sorted(progs)
        return ret_list

    def show_list(self):
        self._timer_cb[0] = lambda : self.refresh_time(self._task_id)
        self.refresh_time(self._task_id)
        sub_act_list = self.panel.list_items
        sub_act_list.SetInitCount(len(self.prog_2_reward_id))
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        for idx, prog in enumerate(prog_list):
            item_widget = sub_act_list.GetItem(idx)
            reward_id = self.prog_2_reward_id.get(prog)
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = r_list[0]
            item_name = get_lobby_item_name(item_no)
            item_widget.lab_sign.SetString(item_name)
            item_path = get_lobby_item_pic_by_item_no(item_no)
            item_widget.temp_items.item.SetDisplayFrameByPath('', item_path)
            item_widget.temp_items.lab_quantity.setVisible(True)
            item_widget.temp_items.lab_quantity.SetString(str(item_num))

        self.refresh_list()
        self._init_get_all()

    def refresh_list(self):
        pic0 = 'gui/ui_res_2/activity/activity_202111/sakugan_7days/bar_week_02.png'
        pic1 = 'gui/ui_res_2/activity/activity_202111/sakugan_7days/bar_week_01.png'
        player = global_data.player
        sub_act_list = self.panel.list_items
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        for idx, prog in enumerate(prog_list):
            day = idx + 1
            item_widget = sub_act_list.GetItem(idx)
            reward_id = self.prog_2_reward_id.get(prog)
            text_day = get_text_by_id(604004).format(day)
            item_widget.lab_days.SetString(text_day)
            btn = item_widget.temp_items.btn_choose
            btn_bar = item_widget.btn_bar
            can_receive = player.is_prog_reward_receivable(self._task_id, prog) and not player.has_receive_prog_reward(self._task_id, prog)
            is_received = player.has_receive_prog_reward(self._task_id, prog)
            if is_received:
                blue_check = True
                blue_pic = True
            elif can_receive:
                blue_check = False
                blue_pic = False
            else:
                blue_check = False
                blue_pic = True
            lab_quantity = item_widget.temp_items.lab_quantity
            if blue_pic:
                from common.utils.cocos_utils import ccc4FromHex
                lab_quantity.SetColor('#SW')
                lab_quantity.EnableOutline(ccc4FromHex(3218954), 1, 150, 3)
                btn_bar.SetFrames('', [pic0, pic0, pic0], False, None)
            else:
                lab_quantity.SetColor('#SK')
                lab_quantity.EnableOutline(0, 0, 0, 0)
                btn_bar.SetFrames('', [pic0, pic0, pic1], False, None)
            lab_quantity.SetString(lab_quantity._rstr)
            btn_bar.SetEnable(False)
            item_widget.img_blue_check.setVisible(blue_check)

            @btn.unique_callback()
            def OnClick(btn, touch, reward_id=reward_id):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                extra_info = {'show_jump': False}
                r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                item_no, item_num = r_list[0]
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos, extra_info=extra_info, item_num=item_num)
                return

        return

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(parent_task)
        if left_time > 0:
            day, _, _, _ = get_day_hour_minute_second(left_time)
            day = day + 1
            day_text = '<fontname=gui/fonts/fzdys.ttf><size=24><color=0XF9DD49FF>{}</color></size></fontname>'.format(day)
            self.panel.lab_rest_time.SetString(get_text_by_id(607969).format('20', '0XFFFFFFFF', day_text))
        else:
            close_left_time = 0
            self.panel.lab_rest_time.SetString(get_readable_time(close_left_time))

    def _init_get_all(self):
        player = global_data.player
        if not player:
            return
        has_unreceived = False
        all_received = True
        for prog in six_ex.keys(self.prog_2_reward_id):
            can_receive = player.is_prog_reward_receivable(self._task_id, prog) and not player.has_receive_prog_reward(self._task_id, prog)
            is_received = player.has_receive_prog_reward(self._task_id, prog)
            if can_receive:
                has_unreceived = True
            if not is_received:
                all_received = False

        self.panel.StopAnimation('loop')
        self.panel.vx_mask.setVisible(False)
        if has_unreceived:
            self.panel.lab_get.SetString(get_text_by_id(604030))
            self.panel.btn_get.SetEnable(True)

            @self.panel.btn_get.unique_callback()
            def OnClick(btn, touch):
                player.receive_all_task_prog_reward(self._task_id)

            self.panel.PlayAnimation('loop')
            self.panel.vx_mask.setVisible(True)
        elif all_received:
            self.panel.lab_get.SetString(get_text_by_id(80866))
            self.panel.btn_get.SetEnable(False)
        else:
            self.panel.lab_get.SetString(get_text_by_id(606046))
            self.panel.btn_get.SetEnable(False)