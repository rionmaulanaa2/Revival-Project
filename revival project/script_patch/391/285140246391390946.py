# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202203/ActivityPulsarSevenDayLogin.py
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
from logic.gcommon.item.item_const import ITEM_RECEIVED, ITEM_UNRECEIVED, ITEM_UNGAIN
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
import cc

class ActivityPulsarSevenDayLogin(ActivityCollect):

    def init_parameters(self):
        super(ActivityPulsarSevenDayLogin, self).init_parameters()
        self.task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        children_tasks = task_utils.get_children_task(self.task_id)
        self._normal_task = children_tasks

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self._on_update_reward,
           'receive_task_prog_reward_succ_event': self._on_update_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def show_list(self):
        self._timer_cb[0] = lambda : self.refresh_time(None)
        self.refresh_time(None)
        conf = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        coupon_dict = conf.get('coupon_dict', {})
        max_discount_task = conf.get('max_discount_task', 1410634)
        from logic.gutils.mall_utils import item_has_owned_by_item_no
        self.panel.lab_get_coupon.SetString(610101)
        show_item_id = None
        for task_id in sorted(six_ex.keys(coupon_dict), reverse=False):
            if ITEM_RECEIVED != global_data.player.get_task_reward_status(task_id):
                self.panel.lab_get_coupon.SetString(610101)
                show_item_id = coupon_dict[task_id][1]
                break

        if show_item_id is None:
            show_item_id = coupon_dict.get(max_discount_task, [610207, 50101173])[1]
            self.panel.lab_get_coupon.SetString(coupon_dict.get(max_discount_task, [610207, 50101173])[0])
            self.panel.lab_get_coupon.SetColor(16776566)
        if show_item_id == coupon_dict.get(max_discount_task, [610207, 50101173])[1]:
            self.panel.btn_coupon.SetShowEnable(False)
        self.panel.btn_coupon.EnableCustomState(True)

        @self.panel.btn_coupon.unique_callback()
        def OnClick(btn, touch):
            x, y = btn.GetPosition()
            w, h = btn.GetContentSize()
            x += w * 0.5
            w_pos = btn.ConvertToWorldSpace(x, y)
            extra_info = {'show_jump': True}
            global_data.emgr.show_item_desc_ui_event.emit(show_item_id, None, w_pos, extra_info=extra_info)
            return

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            self.on_click_btn_question()

        self.panel.btn_see.setVisible(False)
        if global_data.player:
            mecha_open_info = global_data.player.read_mecha_open_info()
            if mecha_open_info['opened_order']:
                _open_mecha_lst = mecha_open_info['opened_order']
                from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
                item_no = mecha_lobby_id_2_battle_id('101008022')
                if int(item_no) in _open_mecha_lst:
                    self.panel.btn_see.setVisible(True)

        @self.panel.btn_see.unique_callback()
        def OnClick(btn, touch):
            jump_to_display_detail_by_item_no('101008022')

        children_tasks = task_utils.get_children_task(self.task_id)
        normal_task = self.reorder_task_list(children_tasks)
        self._normal_task = normal_task
        sub_act_list = self.panel.act_list
        sub_act_list.SetInitCount(0)
        sub_act_list.SetInitCount(len(normal_task))
        for idx, task_id in enumerate(normal_task):
            item_widget = sub_act_list.GetItem(idx).temp_common
            item_widget.lab_name.SetString(task_utils.get_task_name(task_id))
            reward_id = task_utils.get_task_reward(task_id)
            template_utils.init_common_reward_list(item_widget.list_reward, reward_id)

        self.refresh_list()
        self._init_get_all()
        return

    def refresh_list(self):
        sub_act_list = self.panel.act_list
        for i, task_id in enumerate(self._normal_task):
            item_widget = sub_act_list.GetItem(i).temp_common
            btn = item_widget.temp_btn_get.btn_common
            status = global_data.player.get_task_reward_status(task_id)
            self.update_receive_btn(status, item_widget)

            @btn.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    return
                global_data.player.receive_task_reward(task_id)
                btn.SetText(80866)
                btn.SetEnable(False)

    def update_receive_btn(self, status, ui_item):
        btn_receive = ui_item.nd_task.temp_btn_get
        if status == ITEM_RECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_RECEIVED)
        elif status == ITEM_UNGAIN:
            update_task_list_btn(btn_receive, BTN_ST_ONGOING)
        elif status == ITEM_UNRECEIVED:
            update_task_list_btn(btn_receive, BTN_ST_CAN_RECEIVE)

    def refresh_time(self, parent_task):
        left_time = task_utils.get_raw_left_open_time(self.task_id)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))

    def on_click_btn_question(self):
        desc_id = confmgr.get('c_activity_config', self._activity_type, 'cRuleTextID')
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(desc_id)))

    def _init_get_all(self):
        task_num = len(self._get_all_receivable_tasks())
        if task_num >= 2:
            self.panel.nd_get_all.setVisible(True)
            self.panel.img_num.setVisible(True)
            self.panel.lab_num.SetString(str(task_num))

            @self.panel.temp_get_all.btn_common_big.unique_callback()
            def OnClick(btn, touch):
                global_data.player.receive_all_task_reward(self.task_id)

        else:
            self.panel.nd_get_all.setVisible(False)
            self.panel.img_num.setVisible(False)

    def _get_all_receivable_tasks(self):
        can_receive_task = []
        for task_id in self._normal_task:
            status = global_data.player.get_task_reward_status(task_id)
            if status == ITEM_UNRECEIVED:
                can_receive_task.append(task_id)

        return can_receive_task