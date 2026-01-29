# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/TwitterFriendList.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import time
import common.utils.timer as timer
import common.uisys.richtext
from cocosui import cc, ccui, ccs
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.const.property_const import *
import common.utilities
import logic.gcommon.const as const
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex, ccc4aFromHex
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils
import common.http
import game3d
import os
from patch.patch_path import get_download_target_path
from common.utils.path import get_neox_dir
from logic.client.const import share_const
import logic.gutils.share_utils
from logic.gcommon.common_const import friend_const
from logic.gutils import friend_utils
from common.const import uiconst

class TwitterFriendList(BasePanel):
    PANEL_CONFIG_NAME = 'friend/add_other_twitter_friend_list'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_window.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kargs):
        self._message_data = global_data.message_data
        self._list_add = self.panel.list_add
        self._list_add.DeleteAllSubItem()
        global_data.emgr.message_social_friends += self.refresh_friends
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        self.hide_main_ui()
        global_data.message_data.request_twitter_friendids()
        self.refresh_friends()

    def on_click_close_btn(self, *args):
        self.close()

    def on_login_reconnect(self, *args):
        self.close()

    def refresh_friends(self):
        self._list_add.DeleteAllSubItem()
        social_friends = self._message_data.get_social_friends(friend_const.SOCIAL_ID_TYPE_TW)
        twitter_friendinfos = self._message_data.get_twitter_friendinfos()
        count = 0
        for data in social_friends:
            if not self._message_data.is_friend(data.get('uid')):
                twitter_data = twitter_friendinfos.get(data.get('social_id'), {})
                self.add_twitter_friend_elem(data, twitter_data)
                count += 1
                if count > 50:
                    break

        if count == 0:
            self.panel.nd_empty.setVisible(True)
            self.panel.nd_content.setVisible(False)

            @self.panel.temp_btn_add_friend.btn_major.callback()
            def OnClick(*args):
                self.on_send_link()

        else:
            self.panel.nd_empty.setVisible(False)
            self.panel.nd_content.setVisible(True)

            @self.panel.temp_btn_other_friend.btn_major.callback()
            def OnClick(*args):
                self.on_send_link()

    def add_twitter_friend_elem(self, data, twitter_data):
        uid = data['uid']
        panel = self._list_add.AddTemplateItem()
        name = twitter_data.get('name', '')
        if not name:
            name = data.get('char_name', '')
        panel.lab_name.setString(name)
        res_path = role_head_utils.get_head_photo_res_path(data['head_photo'])
        panel.img_head.SetDisplayFrameByPath('', res_path)

        @panel.btn_add.callback()
        def OnClick(*args):
            self.on_touch_item(panel, uid)

    def on_finalize_panel(self):
        self.show_main_ui()

    def on_touch_item(self, panel, uid):
        global_data.player.req_add_friend(uid)
        index = self._list_add.getIndexByItem(panel)
        self._list_add.DeleteItemIndex(index)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_ADD_VIA_TWITTER)

    def on_send_link(self):
        key_word = '%s=%s' % (share_const.DEEP_LINK_ADD_FRIEND, str(global_data.player.uid))
        logic.gutils.share_utils.web_share(key_word, share_const.APP_SHARE_TWITTER)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_SHARE_VIA_TWITTER)