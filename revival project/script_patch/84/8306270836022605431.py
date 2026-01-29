# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202305/Activity520Login.py
from __future__ import absolute_import
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from common.cfg import confmgr
from logic.gutils.common_ui_utils import show_game_rule
from logic.gutils.global_data_utils import get_global_data
from logic.gutils import activity_utils
from logic.gutils.new_template_utils import update_task_list_btn
from logic.gcommon.item.item_const import BTN_ST_CAN_RECEIVE, BTN_ST_ONGOING, BTN_ST_RECEIVED, ITEM_RECEIVED, ITEM_UNGAIN, ITEM_UNRECEIVED
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_pic_by_item_no
from logic.gcommon.common_const.battle_const import PLAY_TYPE_CHICKEN
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import jump_to_ui_utils

class Activity520Login(ActivityTemplate):

    def init_parameters(self):
        super(Activity520Login, self).init_parameters()

    def get_activity_conf(self):
        return confmgr.get('c_activity_config', self._activity_type)

    def get_task_list(self):
        activity_conf = self.get_activity_conf()
        children_task = confmgr.get('task/task_data', activity_conf['cTask'], 'children_task')
        return children_task

    def on_init_panel(self):
        super(Activity520Login, self).on_init_panel()
        self.init_btn_describe()
        self.init_reward_list()

    def init_btn_describe(self):
        btn_describe = self.panel.btn_describe
        if btn_describe:
            activity_conf = self.get_activity_conf()
            act_name_id = activity_conf['cNameTextID']
            rule_text_id = activity_conf.get('cRuleTextID', '')

            @btn_describe.unique_callback()
            def OnClick(btn, touch):
                show_game_rule(get_text_by_id(act_name_id), get_text_by_id(rule_text_id))

    def process_event(self, is_bind):
        emgr = get_global_data().emgr
        econf = {'receive_task_reward_succ_event': self.on_receive_task_reward
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_receive_task_reward(self, task_id):
        self.update_reward_list()

    def init_reward_list(self):
        self.update_reward_list()

    def update_reward_list(self):
        task_list = self.get_task_list()
        list_item = self.panel.list_item
        for index, task_id in enumerate(task_list):
            widget = list_item.GetItem(index)
            self.update_one_reward_widget_by_id(widget, task_id)

    def update_one_reward_widget_by_id(self, widget, task_id):
        task_prog = get_global_data().player.get_task_prog(task_id)
        total_prog = confmgr.get('task/task_data', task_id, 'total_prog')
        total_prog = total_prog if total_prog is not None else 1
        widget.lab_prog.SetString('/'.join((str(task_prog), str(total_prog))))
        reward_id = task_utils.get_task_reward(task_id)
        r_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        item_no, item_num = r_list[0]
        item_name = get_lobby_item_name(item_no)
        widget.lab_name.SetString(item_name)
        pic = get_lobby_item_pic_by_item_no(item_no)
        widget.img_item.SetDisplayFrameByPath('', pic)
        self.update_task_btn(widget.temp_btn, task_id)
        return

    def transfer_task_reward_status_to_btn_status(self, task_reward_status):
        status_map = {ITEM_RECEIVED: BTN_ST_RECEIVED,
           ITEM_UNGAIN: BTN_ST_ONGOING,
           ITEM_UNRECEIVED: BTN_ST_CAN_RECEIVE
           }
        return status_map[task_reward_status]

    def update_task_btn(self, nd_btn, task_id, extra_args=None):
        status_dict = {BTN_ST_CAN_RECEIVE: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_major.png','text_color': 7616256,'btn_text': 604030},BTN_ST_ONGOING: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_unlock.png','text_color': 14674164,'btn_text': 906672},BTN_ST_RECEIVED: {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','btn_text': 604029,'enable': False,'text_color': 14674164}}
        not_open_status_dict = {'btn_frame': 'gui/ui_res_2/common/button/btn_secondary_useless.png','btn_text': 604026,'text_color': 14674164}
        task_reward_status = get_global_data().player.get_task_reward_status(task_id)
        status = self.transfer_task_reward_status_to_btn_status(task_reward_status)
        if status not in status_dict:
            return
        else:
            if not extra_args:
                extra_args = {}
            selected_status_dict = status_dict[status] if task_utils.is_task_open(task_id) else not_open_status_dict
            text_color = selected_status_dict.get('text_color')
            extra_btn_text = extra_args.get('btn_text', '')
            btn_text = extra_btn_text if extra_btn_text else selected_status_dict.get('btn_text', '')
            nd_btn.btn_common.SetText(btn_text)
            text_color and nd_btn.btn_common.SetTextColor(text_color, text_color, text_color)
            btn_frame = selected_status_dict['btn_frame']
            nd_btn.btn_common.SetFrames('', [btn_frame, btn_frame, btn_frame], False, None)
            extra_enable = extra_args.get('enable')
            if extra_enable is not None:
                nd_btn.btn_common.SetEnable(extra_enable)
            else:
                nd_btn.btn_common.SetEnable(selected_status_dict.get('enable', True))
            btn_common = nd_btn.btn_common

            @btn_common.unique_callback()
            def OnClick(btn, touch, task_id=task_id):
                if not activity_utils.is_activity_in_limit_time(self._activity_type):
                    get_global_data().game_mgr.show_tip(get_text_by_id(634195))
                    return
                if status == BTN_ST_ONGOING:
                    return
                if status == BTN_ST_RECEIVED:
                    return
                get_global_data().player.receive_task_reward(task_id)

            return