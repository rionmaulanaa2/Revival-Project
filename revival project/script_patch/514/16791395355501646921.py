# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAIConcert/ActivityKizunaDayLogin.py
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
PIC0 = 'gui/ui_res_2/activity/activity_202110/seven_login/img_bar_week_unchecked.png'
PIC1 = 'gui/ui_res_2/activity/activity_202110/seven_login/img_bar_week_checked_new_2.png'

class ActivityKizunaDayLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityKizunaDayLogin, self).init_parameters()
        self._task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.prog_2_reward_id = task_utils.get_prog_rewards_in_dict(self._task_id)
        self.panel.RecordAnimationNodeState('btn_loop')

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
                dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 1.0))
                template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        self.show_list()
        if self.panel.HasAnimation('show'):
            self.panel.PlayAnimation('show')

    def reorder_prog_list(self, progs):
        ret_list = sorted(progs)
        return ret_list

    def show_list(self):
        activity_type = self._activity_type
        conf = confmgr.get('c_activity_config', activity_type)
        if not conf['cTask']:
            return
        task_list = activity_utils.parse_task_list(conf['cTask'])
        if len(task_list) <= 0:
            return
        self._timer_cb[0] = lambda : self.refresh_time(self._task_id)
        self.refresh_time(self._task_id)
        sub_act_list = self.panel.list_items
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(self.prog_2_reward_id))
        ui_data = conf.get('cUiData', {})
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
        player = global_data.player
        sub_act_list = self.panel.list_items
        prog_list = self.reorder_prog_list(six_ex.keys(self.prog_2_reward_id))
        for idx, prog in enumerate(prog_list):
            day = idx + 1
            item_widget = sub_act_list.GetItem(idx)
            reward_id = self.prog_2_reward_id.get(prog)
            r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
            item_no, item_num = r_list[0]
            item_name = get_lobby_item_name(item_no)
            btn = item_widget.temp_items.btn_choose
            btn_bar = item_widget.btn_bar
            day_text_1 = '<fontname=gui/fonts/fzdys.ttf><size=28><color=0X854B20FF>{}</color></size></fontname>'.format(day)
            day_text_2 = '<fontname=gui/fonts/fzdys.ttf><size=28><color=0XFFFFFFFF>{}</color></size></fontname>'.format(day)
            lab_day_text_1 = '<color=0X924F1EFF>{}</color>'.format(day)
            lab_day_text_2 = '<color=0XFFFFFFFF>{}</color>'.format(day)

            def check_btn(btn=btn_bar):
                can_receive = player.is_prog_reward_receivable(self._task_id, prog) and not player.has_receive_prog_reward(self._task_id, prog)
                is_received = player.has_receive_prog_reward(self._task_id, prog)
                if is_received:
                    item_widget.lab_kaiqi.SetString('<color=0X4F536AFF>{}</color>'.format(get_text_by_id(604010)))
                    item_widget.img_blue_check.setVisible(True)
                    btn.SetFrames('', [PIC0, PIC0, PIC0], False, None)
                    btn.SetEnable(False)
                    item_widget.lab_days.SetString(get_text_by_id(609889).format(day_text_2))
                    item_widget.img_triangle.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202110/seven_login/img_week_seventh.png')
                    item_widget.lab_num.SetString(lab_day_text_2)
                elif can_receive:
                    item_widget.lab_kaiqi.SetString('<color=0X82694AFF>{}</color>'.format(get_text_by_id(607961)))
                    item_widget.img_blue_check.setVisible(False)
                    btn.SetFrames('', [PIC0, PIC0, PIC1], False, None)
                    btn.SetEnable(False)
                    item_widget.lab_days.SetString(get_text_by_id(609888).format(day_text_1))
                    item_widget.img_triangle.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202110/seven_login/img_week_checked.png')
                    item_widget.lab_num.SetString(lab_day_text_1)
                else:
                    item_widget.lab_kaiqi.SetString('<color=0X4F536AFF>{}</color>'.format(get_text_by_id(604026)))
                    item_widget.img_blue_check.setVisible(False)
                    btn.SetFrames('', [PIC0, PIC0, PIC0], False, None)
                    btn.SetEnable(False)
                    item_widget.lab_days.SetString(get_text_by_id(609889).format(day_text_2))
                    item_widget.img_triangle.SetDisplayFrameByPath('', 'gui/ui_res_2/activity/activity_202110/seven_login/img_week_seventh.png')
                    item_widget.lab_num.SetString(lab_day_text_2)
                return

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

            check_btn()

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

        if has_unreceived:
            self.panel.btn_get.SetText(get_text_by_id(604030))
            self.panel.img_btn_light.setVisible(True)
            self.panel.btn_get.SetEnable(True)

            @self.panel.btn_get.unique_callback()
            def OnClick(btn, touch):
                player.receive_all_task_prog_reward(self._task_id)

            if self.panel.HasAnimation('btn_loop'):
                self.panel.PlayAnimation('btn_loop')
        elif all_received:
            self.panel.btn_get.SetText(get_text_by_id(80866))
            self.panel.img_btn_light.setVisible(False)
            self.panel.btn_get.SetEnable(False)
            self.panel.StopAnimation('btn_loop')
            self.panel.RecoverAnimationNodeState('btn_loop')
        else:
            self.panel.btn_get.SetText(get_text_by_id(606046))
            self.panel.img_btn_light.setVisible(False)
            self.panel.btn_get.SetEnable(False)
            self.panel.StopAnimation('btn_loop')
            self.panel.RecoverAnimationNodeState('btn_loop')