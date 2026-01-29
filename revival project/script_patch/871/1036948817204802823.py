# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/BlackList.py
from __future__ import absolute_import
import six
import cc
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray, set_gray_by_online_state
from common.const.property_const import *
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.const import FRD_KEY_BALCLIST
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.role_head_utils import init_dan_info
from logic.gutils.online_state_utils import is_not_online

def get_name_richtext(data, clr_str):
    return '<color={}>{}</color>'.format(clr_str, data.get(C_NAME, ''))


class BlackList(object):

    def __init__(self, main_panel, **kwargs):
        self.panel = panel_temp = global_data.uisystem.load_template_create('friend/i_blacklist', main_panel.panel, name='black_content')
        panel_temp.SetPosition('50%', '50%')
        self.main_panel = main_panel
        self._black_list = None
        self.player_info_manager = PlayerInfoManager()
        self.init_panel()
        self.init_event()
        return

    def init_panel(self):
        self._temp_list = self.panel.temp_list
        self.refresh_temp_black_list()

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'message_refresh_friends': self.refresh_temp_black_list,
           'message_friend_state': self.refresh_temp_black_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_temp_black_list(self):
        self._black_list = global_data.message_data.get_black_friends()
        black_count = len(self._black_list)
        self.panel.nd_empty.setVisible(black_count == 0)
        self._temp_list.SetInitCount(black_count)
        idx = 0
        for friend_id, data in six.iteritems(self._black_list):
            friend_id = data[U_ID]
            item_widget = self._temp_list.GetItem(idx)
            item_widget.btn_item.SetEnableCascadeOpacityRecursion(True)
            setattr(item_widget, 'panel_type', 'item')
            setattr(item_widget, 'data', data)
            if item_widget.btn_item.lab_name:
                item_widget.btn_item.lab_name.SetString(get_name_richtext(data, '0X363B51FF'))
            self.player_info_manager.add_head_item_auto(item_widget.btn_item.temp_head, friend_id, 0, data)
            self.player_info_manager.add_dan_info_item(item_widget.temp_tier, friend_id)
            init_dan_info(item_widget.temp_tier, friend_id)
            self.set_online_state(item_widget, data)
            item_widget.btn_item.btn_remove.btn_common_big.BindMethod('OnClick', lambda btn, touch, uid=friend_id: SecondConfirmDlg2().confirm(content=get_text_by_id(10010), confirm_callback=lambda : global_data.player.req_del_from_list(FRD_KEY_BALCLIST, uid)))
            item_widget.btn_item.btn_remove.btn_common_big.SetText(3213)

            @item_widget.temp_head.callback()
            def OnClick(btn, touch, uid=data[U_ID]):
                ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
                ui.refresh_by_uid(int(uid))
                ui.set_position(touch.getLocation())

            idx += 1

    def set_online_state(self, panel, data):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        from logic.comsys.effect import ui_effect
        import logic.gcommon.const as const
        friend_id = data[U_ID]
        friend_online_state = global_data.message_data.get_player_online_state()
        state = int(friend_online_state.get(int(friend_id), 0))
        text_id, color = ui_utils.get_online_inf(state)
        panel.lab_status.setString(get_text_by_id(text_id))
        panel.lab_status.SetColor(color)
        panel.btn_item.lab_name.SetString(get_name_richtext(data, '0X363B51FF'))
        panel.btn_item.SetShowEnable(not is_not_online(state))
        set_gray_by_online_state(panel.btn_item.temp_head, state)
        if is_not_online(state):
            panel.btn_item.lab_name.setOpacity(int(204.0))
        else:
            panel.btn_item.lab_name.setOpacity(255)
        panel.btn_invite.setVisible(False)
        return not is_not_online(state)

    def set_visible(self, flag):
        self.panel.setVisible(flag)

    def destroy(self):
        self.process_event(False)