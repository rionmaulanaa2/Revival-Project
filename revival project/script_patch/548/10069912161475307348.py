# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/FriendApplyList.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
import time
from common.platform import channel_const
import common.utils.timer as timer
import common.uisys.richtext
from cocosui import cc, ccui, ccs
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const.property_const import *
import common.utilities
import logic.gcommon.const as const
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex, ccc4aFromHex
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.comsys.common_ui.InputBox as InputBox
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gcommon.common_const import chat_const, friend_const
from logic.gutils import role_head_utils
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class FriendApplyList(WindowMediumBase):
    PANEL_CONFIG_NAME = 'friend/add_friend_list'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_window'
    GLOBAL_EVENT = {'message_refresh_friend_apply': 'refresh_apply_friends',
       'message_refresh_friends': 'refresh_apply_friends',
       'net_login_reconnect_event': 'on_login_reconnect'
       }
    UI_ACTION_EVENT = {'btn_agree_all.btn_common.OnClick': 'on_accept_all',
       'btn_ignore_all.btn_common.OnClick': 'on_reject_all',
       'btn_shielding_all.btn_common.OnClick': 'on_shield_all',
       'btn_page_down.OnClick': 'on_page_down',
       'btn_page_up.OnClick': 'on_page_up'
       }

    def on_init_panel(self, *args, **kargs):
        super(FriendApplyList, self).on_init_panel()
        self._message_data = global_data.message_data
        self._list_apply = self.panel.list_apply
        self._list_apply.DeleteAllSubItem()
        self._one_page_max_count = 4
        self.cur_page_index = 0
        self.all_page_count = 0
        self.role_head_manager = PlayerInfoManager()
        self._apply_friends = None
        self._apply_friends_ids = None
        if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
            self.panel.temp_tips_warnning.setVisible(False)
        self.refresh_apply_friends()
        self.hide_main_ui()
        self.panel.PlayAnimation('show')
        return

    def on_click_close_btn(self, *args):
        self.close()

    def on_login_reconnect(self, *args):
        self.close()

    def refresh_apply_friends(self, data_sort=True):
        if data_sort:
            self._apply_friends = self._message_data.get_apply_friends()
            self._apply_friends_ids = sorted(six_ex.keys(self._apply_friends), key=lambda key: int(key))
        all_count = len(self._apply_friends_ids)
        if all_count == 0:
            all_page = 1
        else:
            all_page = int((len(self._apply_friends_ids) - 1) / self._one_page_max_count) + 1
        self.all_page_count = all_page
        if self.cur_page_index >= all_page:
            self.cur_page_index = all_page - 1
        panel = self.panel
        panel.lab_page.SetString('%d/%d' % (self.cur_page_index + 1, all_page))
        panel.list_apply.DeleteAllSubItem()
        for index in range(self._one_page_max_count):
            friend_index = int(self.cur_page_index * self._one_page_max_count + index)
            if friend_index < all_count:
                data = self._apply_friends[self._apply_friends_ids[friend_index]]
                self.add_apply_elem(data)
            else:
                break

        panel.nd_empty.setVisible(not all_count)
        panel.nd_content.setVisible(bool(all_count))
        panel.nd_page.setVisible(all_page != 1)

    def add_apply_elem(self, data):
        lv_apply = self.panel.list_apply
        panel = lv_apply.AddTemplateItem()
        panel.lab_name.SetString(data[C_NAME])
        uid = data[U_ID]
        self.role_head_manager.add_head_item_auto(panel.temp_head, uid, 0, data)
        role_head_utils.set_role_dan(panel.temp_tier, data.get('dan_info'))
        stat_visible = False
        if global_data.channel.is_bind_linegame():
            social_ids = data.get('social_ids', {}).get(friend_const.SOCIAL_ID_TYPE_LINEGAME, [])
            if social_ids:
                icon = '<img="{}",scale=0.9>'.format(chat_const.LINE_ICON)
                content = '#SW{}#n#DG{}:{}#n'.format(icon, get_text_by_id(609012), self._message_data.get_line_friend_name(social_ids[0]))
                panel.lab_status.SetString(content)
                stat_visible = True
        panel.lab_status.setVisible(stat_visible)

        @panel.btn_agree.callback()
        def OnClick(*args):
            global_data.player.agree_add_friend(data[U_ID])
            self._apply_friends_ids.remove(data[U_ID])
            self.refresh_apply_friends(False)

        @panel.btn_ignore.callback()
        def OnClick(*args):
            global_data.player.req_del_from_list(const.FRD_KEY_REQ, data[U_ID])
            self._apply_friends_ids.remove(data[U_ID])
            self.refresh_apply_friends(False)

        @panel.btn_shielding.callback()
        def OnClick(*args):
            global_data.player.req_del_from_list(const.FRD_KEY_REQ, data[U_ID])
            global_data.player.req_add_to_list(const.FRD_KEY_BALCLIST, data[U_ID])
            self._apply_friends_ids.remove(data[U_ID])
            self.refresh_apply_friends(False)

        @panel.temp_head.callback()
        def OnClick(*args):
            pos_x, pos_y = panel.temp_head.GetPosition()
            world_pos = panel.temp_head.ConvertToWorldSpace(pos_x, pos_y)
            size = panel.temp_head.getContentSize()
            world_pos = cc.Vec2(world_pos.x + size.width, world_pos.y + size.height)
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(data[U_ID]))
            ui.set_position(world_pos, cc.Vec2(0.0, 0.5))

    def on_page_down(self, *args):
        self.cur_page_index -= 1
        if self.cur_page_index < 0:
            self.cur_page_index = 0
            global_data.player.notify_client_message((get_text_by_id(10068),))
        self.refresh_apply_friends(False)

    def on_page_up(self, *args):
        self.cur_page_index += 1
        if self.cur_page_index >= self.all_page_count:
            self.cur_page_index = self.all_page_count - 1
            global_data.player.notify_client_message((get_text_by_id(10069),))
        self.refresh_apply_friends(False)

    def on_reject_all(self, *args):
        all_count = len(self._apply_friends_ids)
        for index in range(self._one_page_max_count):
            friend_index = self.cur_page_index * self._one_page_max_count + index
            if friend_index < all_count:
                friend_id = self._apply_friends_ids[friend_index]
                global_data.player.req_del_from_list(const.FRD_KEY_REQ, int(friend_id))
            else:
                break

    def on_accept_all(self, *args):
        all_count = len(self._apply_friends_ids)
        for index in range(self._one_page_max_count):
            friend_index = int(self.cur_page_index * self._one_page_max_count + index)
            if friend_index < all_count:
                friend_id = self._apply_friends_ids[friend_index]
                global_data.player.agree_add_friend(int(friend_id))
            else:
                break

    def on_shield_all(self, *args):
        all_count = len(self._apply_friends_ids)
        for index in range(self._one_page_max_count):
            friend_index = int(self.cur_page_index * self._one_page_max_count + index)
            if friend_index < all_count:
                friend_id = self._apply_friends_ids[friend_index]
                global_data.player.req_del_from_list(const.FRD_KEY_REQ, int(friend_id))
                global_data.player.req_add_to_list(const.FRD_KEY_BALCLIST, int(friend_id))
            else:
                break

    def on_finalize_panel(self):
        self.show_main_ui()