# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/red_packet/ChatRedPacketSendUI.py
from __future__ import absolute_import
import six
from logic.gutils.red_packet_utils import get_red_packet_cover_info, init_red_packet_cover_item, get_all_display_red_packet_info, get_user_setting_red_packet_cover
from logic.gutils.item_utils import get_lobby_item_name
from .RedPacketSendSettingUI import RedPacketSendSettingUI
from logic.gcommon.common_const.red_packet_const import CAN_SEND_RED_PACKET_CHANNEL

class ChatRedPacketSendUI(object):
    GLOBAL_EVENT = {'change_red_packet_cover_succeed': 'refresh_red_packet_cover'
       }

    def __init__(self, panel, channel):
        self.panel = panel
        self.on_init_panel()
        global_data.emgr.change_red_packet_cover_succeed += self.refresh_red_packet_cover

    def on_init_panel(self, *args, **kwargs):
        self.choose_item = None
        self.choose_idx = -1
        self.cover_item_no = get_user_setting_red_packet_cover()
        self.init_red_packet_list_item()
        self.init_right_cover_item()
        return

    def init_red_packet_list_item(self):
        red_packet_info = get_all_display_red_packet_info()
        list_item = self.panel.list_item
        list_item.SetInitCount(len(red_packet_info))
        idx = 0
        for key, packet_item_info in six.iteritems(red_packet_info):
            packet_item = list_item.GetItem(idx)
            if not packet_item_info:
                continue
            packet_item.item.SetDisplayFrameByPath('', 'gui/ui_res_2/item/groceries/%s.png' % packet_item_info.get('cur_id', 50101101))
            packet_item.lab_name.SetString(packet_item_info.get('text_id', 2))
            packet_item.btn_choose.BindMethod('OnClick', lambda btn, touch, key=key, item=packet_item: self.on_click_choose_red_packet_type(key, packet_item))
            idx += 1

    def init_right_cover_item(self):
        self.refresh_red_packet_cover(self.cover_item_no)
        self.panel.temp_item.btn_choose.SetEnable(False)
        self.panel.temp_btn.btn_common.BindMethod('OnClick', self.on_click_change_red_packet_cover)

    def refresh_red_packet_cover(self, item_no):
        packet_cover_info = get_red_packet_cover_info(item_no)
        if not packet_cover_info:
            return
        cover_item = self.panel.temp_item
        init_red_packet_cover_item(cover_item, item_no, True)
        self.panel.lab_name.SetString(get_lobby_item_name(item_no))

    def on_click_choose_red_packet_type(self, i, item):
        if not global_data.player:
            return
        from logic.comsys.setting_ui.UnderageHelper import is_in_underage_mode
        if is_in_underage_mode():
            global_data.game_mgr.show_tip(get_text_by_id(635260))

            def click_goto():
                from logic.gutils import jump_to_ui_utils
                jump_to_ui_utils.jump_to_underage_mode_btn()

            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            SecondConfirmDlg2().confirm(content=get_text_by_id(635270), confirm_callback=click_goto)
            return
        if global_data.player.get_red_packet_day_create_count() >= global_data.player.get_red_packet_day_create_limit_count():
            global_data.game_mgr.show_tip(634361)
            return
        if self.channel not in CAN_SEND_RED_PACKET_CHANNEL:
            return
        send_setting_ui = RedPacketSendSettingUI(red_packet_type=i, channel=self.channel)
        from logic.client.const import game_mode_const
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
            send_setting_ui.set_skin_list_vis(False)
            send_setting_ui.set_remain_unusable(False)

    def on_click_change_red_packet_cover(self, *args):
        global_data.ui_mgr.show_ui('RedPacketCoverChangeUI', 'logic.comsys.red_packet')

    def get_is_visible(self):
        if not self.panel or not self.panel.isValid():
            return False
        return self.panel.isVisible()

    def update_send_channel(self, channel):
        self.channel = channel

    def destroy(self):
        self.panel = None
        global_data.emgr.change_red_packet_cover_succeed -= self.refresh_red_packet_cover
        return

    def set_show_close_tips(self, vis):
        self.panel.lab_close_tips.setVisible(vis)

    def set_cover_usable(self, usable):
        self.panel.temp_btn.btn_common.SetEnable(usable)