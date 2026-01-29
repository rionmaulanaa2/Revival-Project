# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyTriggerGiftEntryWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import activity_utils
from logic.comsys.charge_ui.LeftTimeCountDownWidget import LeftTimeCountDownWidget
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id, get_cur_text_lang, LANG_CN
from logic.gutils import trigger_gift_utils
from logic.gcommon.common_const.shop_const import GIFTBOX_TRIGGER_TYPE

class LobbyTriggerGiftEntryWidget(BaseUIWidget):

    def __init__(self, panel_cls, panel, gift_info):
        super(LobbyTriggerGiftEntryWidget, self).__init__(panel_cls, panel)
        self._gift_info = gift_info
        self._gift_id = self._gift_info.get('id')
        self._template_name = self._gift_info.get('template_name', 'temp_btn_gifts_01')
        self.ui_node = getattr(self.panel, self._template_name)
        self._left_time_widget = None
        self.init_widget()
        return

    def destroy(self):
        self.panel.StopAnimation('loop_charge')
        super(LobbyTriggerGiftEntryWidget, self).destroy()
        self.ui_node.setVisible(False)
        if self._left_time_widget:
            self._left_time_widget.destroy()
            self._left_time_widget = None
        self.process_event(False)
        return

    def init_event(self):
        super(LobbyTriggerGiftEntryWidget, self).init_event()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def get_gift_id(self):
        return self._gift_info.get('id')

    def init_widget(self):
        if self._template_name == 'temp_btn_gifts_01':
            self._left_time_widget = trigger_gift_utils.init_template_lobby_btn_gifts(self.ui_node, self._gift_info)
        elif self._template_name == 'temp_btn_gifts_02':
            self._left_time_widget = trigger_gift_utils.init_template_lobby_btn_battle_pass(self.ui_node, self._gift_info)
        self.ui_node.setVisible(True)
        self._init_left_time_widget()

        @self.ui_node.btn_click.callback()
        def OnClick(b, t):
            self._on_entry_btn_click(b, t)

        self.process_event(True)

    def _init_left_time_widget(self):
        expire_time = self._gift_info.get('expire_time', 0)
        cash_only = self._gift_info.get('cash_only', 0)
        if cash_only:
            self.ui_node.nd_time.setVisible(False)
        else:
            self.ui_node.nd_time.setVisible(True)
        if expire_time > tutil.get_server_time():
            self._left_time_widget.begin_count_down_time(expire_time, self._time_up_callback, use_big_interval=False)

    def _time_up_callback(self):
        if global_data.player:
            if self._gift_info.get('gift_type') == GIFTBOX_TRIGGER_TYPE:
                global_data.player.on_trigger_gift_expire(self._gift_id)
            else:
                global_data.player.on_chance_gift_expire(self._gift_id)
        self.ui_node.setVisible(False)

    def _on_entry_btn_click(self, btn, touch):
        if global_data.player:
            if self._gift_info.get('gift_type') == GIFTBOX_TRIGGER_TYPE:
                global_data.player.show_trigger_gift_ui(self._gift_id)
            else:
                global_data.player.show_chance_gift_ui(self._gift_id)