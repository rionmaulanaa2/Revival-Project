# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/RoleBuffWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO, SHOP_PAYMENT_DIAMON
from logic.gutils import template_utils
from logic.gutils import mall_utils
import logic.gcommon.common_const.role_const as role_const
from common.utils import time_utils as tutil
from logic.gcommon import time_utility

class RoleBuffWidget(object):
    ROLE_LOBBY_BUFF_TYPE_IMG = {role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_TIME_EXP: 'gui/ui_res_2/main/buff_limit_time_exp.png',
       role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_TIME_MECH_EXP: 'gui/ui_res_2/main/buff_limit_time_mech_exp.png',
       role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_USE_EXP: 'gui/ui_res_2/main/buff_limit_use_exp.png',
       role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_USE_MECH_EXP: 'gui/ui_res_2/main/buff_limit_use_mech_exp.png',
       role_const.ROLE_LOBBY_BUFF_TYPE_MONTH_EXP_UP: 'gui/ui_res_2/main/buff_month_exp_up.png',
       role_const.ROLE_LOBBY_BUFF_TYPE_WEEK_EXP_UP: 'gui/ui_res_2/main/buff_month_exp_up.png',
       role_const.ROLE_LOBBY_BUFF_TYPE_RETURN_MECH_EXP_UP: 'gui/ui_res_2/main/buff_limit_time_mech_exp.png',
       role_const.ROLE_LOBBY_BUFF_TYPE_RETURN_EXP_UP: 'gui/ui_res_2/main/buff_limit_time_exp.png'
       }

    def __init__(self, parent, call_back=None):
        self.parent = parent
        self.panel = parent.panel
        self.call_back = call_back
        self.init_parameters()
        self.init_panel()
        self.init_event()

    def init_panel(self):
        self.describe_widget = global_data.uisystem.load_template_create('lobby/i_role_buff_list', parent=self.panel)
        self.describe_widget.setVisible(False)
        self.list_buff = self.panel.list_role_buff
        self._bind_node_touch_event(self.panel.btn_check_buff)
        self.refresh_role_buff()

    def _bind_node_touch_event(self, buff_node):

        @buff_node.unique_callback()
        def OnBegin(btn, touch):
            if not self.buff_in_effects:
                return
            self._refresh_buff_describe_text()
            wposition = touch.getLocation()
            template_utils.set_node_position_in_screen(self.describe_widget, self.panel, wposition)
            self.describe_widget.setVisible(True)

        @buff_node.unique_callback()
        def OnEnd(btn, touch):
            self.describe_widget and self.describe_widget.setVisible(False)
            self.refresh_role_buff()

    def on_finalize_panel(self):
        self.process_event(False)
        self.describe_widget = None
        self.buff_in_effects = None
        self.describe_list_buffs = None
        self.buff_type_getters.clear()
        return

    def init_parameters(self):
        self.buff_in_effects = []
        self.describe_list_buffs = []
        self.describe_widget = None
        self.buff_type_getters = {role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_TIME_EXP: self.get_time_exp_card_buff,
           role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_TIME_MECH_EXP: self.get_time_prof_card_buff,
           role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_USE_EXP: self.get_exp_card_buff,
           role_const.ROLE_LOBBY_BUFF_TYPE_LIMIT_USE_MECH_EXP: self.get_prof_card_buff,
           role_const.ROLE_LOBBY_BUFF_TYPE_MONTH_EXP_UP: self.get_month_card_buff,
           role_const.ROLE_LOBBY_BUFF_TYPE_WEEK_EXP_UP: self.get_week_card_buff,
           role_const.ROLE_LOBBY_BUFF_TYPE_RETURN_MECH_EXP_UP: self.get_return_mech_prof_buff,
           role_const.ROLE_LOBBY_BUFF_TYPE_RETURN_EXP_UP: self.get_return_exp_buff
           }
        return

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'role_add_card_attr_update_event': self._on_add_card_attr_change,
           'role_return_buff_update': self._on_role_return_buff_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_add_card_attr_change(self):
        self.refresh_role_buff()

    def _on_role_return_buff_update(self):
        self.refresh_role_buff()

    def refresh_role_buff(self):
        if global_data and global_data.player:
            self.buff_in_effects = self._get_role_buff_in_effect()
        buff_node_list = self.list_buff
        if not self.buff_in_effects:
            buff_node_list.setVisible(False)
            return
        else:
            buff_node_list.setVisible(True)
            buff_describe_list = self.describe_widget
            buff_describe_list.DeleteAllSubItem()
            buff_describe_list.SetInitCount(len(self.buff_in_effects))
            self.describe_list_buffs = []
            buff_describe_list.img_bg.ResizeAndPosition()
            buff_node_list.SetInitCount(len(self.buff_in_effects))
            for i, buff_data in enumerate(self.buff_in_effects):
                m_type, describe_text = buff_data
                buff_node = buff_node_list.GetItem(i)
                describe_node = buff_describe_list.GetItem(i)
                image_path = RoleBuffWidget.ROLE_LOBBY_BUFF_TYPE_IMG.get(m_type, None)
                if image_path:
                    buff_node.img_role_buff.SetDisplayFrameByPath('', image_path)
                    describe_node.img_role_buff.SetDisplayFrameByPath('', image_path)
                self.describe_list_buffs.append(m_type)
                describe_node.lab_describe.SetString(describe_text)
                buff_node.setVisible(True)

            w, h = buff_node_list.GetContentSize()
            self.panel.btn_check_buff.SetContentSize(w, h)
            return

    def _refresh_buff_describe_text(self):
        buff_describe_list = self.describe_widget
        size = len(self.describe_list_buffs)
        for i, m_type in enumerate(self.describe_list_buffs):
            buff_func = self.buff_type_getters.get(m_type, None)
            if not buff_func:
                continue
            in_effect, describe_text = buff_func(include_zero=True)
            if in_effect:
                describe_node = buff_describe_list.GetItem(size - i - 1)
                describe_node.lab_describe.SetString(describe_text)

        return

    def _get_role_buff_in_effect(self):
        buff_in_effects = []
        for m_type, buff_func in six.iteritems(self.buff_type_getters):
            in_effect, text = buff_func(include_zero=False)
            if in_effect:
                buff_in_effects.append((m_type, text))

        return buff_in_effects

    def get_time_exp_card_buff(self, include_zero=False):
        card_time = global_data.player.get_duo_exp_timestamp()
        return self._get_time_buff_card_result(card_time, 606040, include_zero)

    def _get_time_buff_card_result(self, card_time, format_text_id, include_zero=False):
        now = time_utility.get_server_time()
        if not card_time or card_time < now:
            return (False, None)
        else:
            delta = card_time - now
            if not include_zero and delta <= 0:
                return (False, None)
            day, hour, minute, seconds = tutil.get_readable_time_value(delta)
            if not include_zero and day == 0 and hour == 0 and minute == 0:
                return (False, None)
            return (True, get_text_by_id(format_text_id).format(day=day, hour=hour, min=minute))

    def get_exp_card_buff(self, include_zero=False):
        left_point = global_data.player.get_dup_exp_point()
        if left_point <= 0:
            return (False, None)
        else:
            return (
             True, get_text_by_id(606043).format(num=left_point))

    def get_month_card_buff(self, include_zero=False):
        card_time = global_data.player.get_yueka_time()
        return self._get_time_buff_card_result(card_time, 606041, include_zero)

    def get_week_card_buff(self, include_zero=False):
        card_time = global_data.player.get_weeklycard_time()
        if global_data.player.has_yueka():
            return (False, None)
        else:
            return self._get_time_buff_card_result(card_time, 608062, include_zero)

    def get_prof_card_buff(self, include_zero=False):
        left_point = global_data.player.get_duo_prof_point()
        if left_point <= 0:
            return (False, None)
        else:
            return (
             True, get_text_by_id(606042).format(num=left_point))

    def get_time_prof_card_buff(self, include_zero=False):
        card_time = global_data.player.get_duo_prof_timestamp()
        return self._get_time_buff_card_result(card_time, 606039, include_zero)

    def get_return_mech_prof_buff(self, include_zero=False):
        due_time = global_data.player.get_return_buff_due_time()
        return self._get_time_buff_card_result(due_time, 606174, include_zero)

    def get_return_exp_buff(self, include_zero=False):
        due_time = global_data.player.get_return_buff_due_time()
        return self._get_time_buff_card_result(due_time, 606175, include_zero)