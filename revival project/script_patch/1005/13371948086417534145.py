# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/LineGameFriendList.py
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
from logic.gcommon.common_const import friend_const, chat_const
from logic.gutils import friend_utils

def get_str_md5--- This code section failed: ---

  26       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'hashlib'
           9  STORE_FAST            1  'hashlib'

  27      12  LOAD_FAST             0  'url'
          15  LOAD_ATTR             1  'rfind'
          18  LOAD_CONST            2  '&ext='
          21  CALL_FUNCTION_1       1 
          24  STORE_FAST            2  'index'

  28      27  STORE_FAST            1  'hashlib'
          30  LOAD_FAST             2  'index'
          33  SLICE+3          
          34  STORE_FAST            3  'url_enable'

  29      37  LOAD_CONST            1  ''
          40  LOAD_CONST            0  ''
          43  IMPORT_NAME           2  'six'
          46  STORE_FAST            4  'six'

  30      49  LOAD_FAST             1  'hashlib'
          52  LOAD_ATTR             3  'md5'
          55  LOAD_FAST             4  'six'
          58  LOAD_ATTR             4  'ensure_binary'
          61  LOAD_FAST             3  'url_enable'
          64  CALL_FUNCTION_1       1 
          67  CALL_FUNCTION_1       1 
          70  LOAD_ATTR             5  'hexdigest'
          73  CALL_FUNCTION_0       0 
          76  STORE_FAST            5  'md5'

  31      79  LOAD_FAST             5  'md5'
          82  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `STORE_FAST' instruction at offset 27


def get_file_path_from_url(url):
    file_name = '%s.jpg' % get_str_md5(url)
    icon_path = get_neox_dir() + '/' + get_download_target_path('res/' + file_name)
    return (
     file_name, icon_path)


def download_linegame_icon(url, callback):

    def http_callback--- This code section failed: ---

  40       0  LOAD_GLOBAL           0  'get_file_path_from_url'
           3  LOAD_DEREF            0  'url'
           6  CALL_FUNCTION_1       1 
           9  UNPACK_SEQUENCE_2     2 
          12  STORE_FAST            1  'file_name'
          15  STORE_FAST            2  'file_path'

  42      18  LOAD_FAST             2  'file_path'
          21  LOAD_ATTR             1  'rfind'
          24  LOAD_CONST            1  '/'
          27  CALL_FUNCTION_1       1 
          30  STORE_FAST            3  'index'

  43      33  LOAD_FAST             2  'file_path'
          36  LOAD_CONST            2  ''
          39  LOAD_FAST             3  'index'
          42  SLICE+3          
          43  STORE_FAST            4  'dirs'

  44      46  LOAD_GLOBAL           2  'os'
          49  LOAD_ATTR             3  'path'
          52  LOAD_ATTR             4  'exists'
          55  LOAD_FAST             4  'dirs'
          58  CALL_FUNCTION_1       1 
          61  POP_JUMP_IF_TRUE     80  'to 80'

  45      64  LOAD_GLOBAL           2  'os'
          67  LOAD_ATTR             5  'makedirs'
          70  LOAD_FAST             4  'dirs'
          73  CALL_FUNCTION_1       1 
          76  POP_TOP          
          77  JUMP_FORWARD          0  'to 80'
        80_0  COME_FROM                '77'

  46      80  LOAD_GLOBAL           6  'open'
          83  LOAD_FAST             2  'file_path'
          86  LOAD_CONST            3  'wb'
          89  CALL_FUNCTION_2       2 
          92  STORE_FAST            5  'jpg_file'

  47      95  LOAD_FAST             5  'jpg_file'
          98  LOAD_ATTR             7  'write'
         101  LOAD_ATTR             2  'os'
         104  BINARY_SUBSCR    
         105  CALL_FUNCTION_1       1 
         108  POP_TOP          

  48     109  LOAD_FAST             5  'jpg_file'
         112  LOAD_ATTR             8  'close'
         115  CALL_FUNCTION_0       0 
         118  POP_TOP          

  49     119  LOAD_DEREF            1  'callback'
         122  POP_JUMP_IF_FALSE   135  'to 135'

  50     125  LOAD_DEREF            1  'callback'
         128  CALL_FUNCTION_0       0 
         131  POP_TOP          
         132  JUMP_FORWARD          0  'to 135'
       135_0  COME_FROM                '132'

Parse error at or near `BINARY_SUBSCR' instruction at offset 104

    common.http.request_v2(url, None, {}, http_callback)
    return


def set_linegame_icon(icon_url, callback):
    file_name, icon_path = get_file_path_from_url(icon_url)
    if os.path.exists(icon_path):
        callback(file_name)
    else:

        def load_callback():
            callback(file_name)

        download_linegame_icon(icon_url, load_callback)


from common.const import uiconst

class LineGameFriendList(BasePanel):
    PANEL_CONFIG_NAME = 'friend/add_other_friend_list'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_window.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kargs):
        self._message_data = global_data.message_data
        self._list_add = self.panel.list_add
        self._list_add.DeleteAllSubItem()
        global_data.emgr.message_social_friends += self.refresh_linegame_friends
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        self.hide_main_ui()
        self.panel.temp_window.lab_title.SetString(609012)
        self.panel.temp_btn_other_friend.btn_major.SetText(609013)
        self.panel.temp_btn_add_friend.btn_major.SetText(609013)
        if self._message_data.need_refresh_linegame_friends():
            global_data.channel.query_linegame_in_game_friends(self._message_data.get_linegame_friends_cursor() + 1)
        else:
            self.refresh_linegame_friends()

    def on_click_close_btn(self, *args):
        self.close()

    def on_login_reconnect(self, *args):
        self.close()

    def refresh_linegame_friends(self):
        self._list_add.DeleteAllSubItem()
        social_friends = self._message_data.get_social_friends(friend_const.SOCIAL_ID_TYPE_LINEGAME)
        linegame_friendinfos = self._message_data.get_linegame_friends()
        count = 0
        for data in social_friends:
            if not self._message_data.is_friend(data.get('uid')):
                linegame_data = linegame_friendinfos.get(data.get('social_id'))
                self.add_linegame_friend_elem(data, linegame_data)
                count += 1

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

    def add_linegame_friend_elem(self, data, linegame_data):
        uid = data['uid']
        panel = self._list_add.AddTemplateItem()
        panel.lab_name.SetString(data[C_NAME])
        panel.lab_desc.setVisible(True)
        icon = '<img="{}",scale=0.9>'.format(chat_const.LINE_ICON)
        content = '#SW{}#n#DG{}#n'.format(icon, linegame_data.get('nickname', ''))
        panel.lab_desc.SetString(content)
        panel.lab_name.SetPosition('50%-115', '50%+10')
        icon_url = linegame_data.get('avatar', '')
        if icon_url:
            set_linegame_icon(icon_url, lambda file_path: self.add_linegame_icon(panel, file_path, data))

        @panel.btn_add.callback()
        def OnClick(*args):
            self.on_touch_item(panel, data)

        @panel.btn_invite.callback()
        def OnClick(*args):
            self.on_touch_invite(panel, data)

        return panel

    def add_linegame_icon(self, elem_panel, file_path, data):
        if not elem_panel.isValid():
            return
        sprite = cc.Sprite.create(file_path)
        if not sprite:
            return
        sprite.setAnchorPoint(cc.Vec2(0.5, 0.5))
        size = elem_panel.img_head.getContentSize()
        sprite.setPosition(cc.Vec2(size.width * 0.5, size.height * 0.5))
        scale = size.width / sprite.getTextureRect().width
        sprite.setScale(scale)
        elem_panel.img_head.addChild(sprite)
        return sprite

    def on_finalize_panel(self):
        self.show_main_ui()

    def on_touch_item(self, panel, data):
        uid = data['uid']
        global_data.player.req_add_friend(uid)
        index = self._list_add.getIndexByItem(panel)
        self._list_add.DeleteItemIndex(index)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_ADD_VIA_LINEGAME)

    def on_touch_invite(self, panel, data):
        from logic.comsys.message import SendLineMessage
        SendLineMessage.SendLineMessageAddFriend(None, social_id=social_ids[0])
        return

    def on_send_link(self):
        key_word = '%s=%s' % (share_const.DEEP_LINK_ADD_FRIEND, str(global_data.player.uid))
        logic.gutils.share_utils.web_share(key_word, share_const.APP_SHARE_LINE)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_SHARE_VIA_LINEGAME)