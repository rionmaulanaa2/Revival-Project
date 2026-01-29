# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/FaceBookFriendList.py
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

class FaceBookFriendList(BasePanel):
    PANEL_CONFIG_NAME = 'friend/add_other_friend_list'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_window.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self, *args, **kargs):
        self._message_data = global_data.message_data
        self._list_add = self.panel.list_add
        self._list_add.DeleteAllSubItem()
        global_data.emgr.message_social_friends += self.refresh_facebook_friends
        global_data.emgr.net_login_reconnect_event += self.on_login_reconnect
        self.hide_main_ui()
        global_data.channel.query_fb_friend_info(1)
        self.refresh_facebook_friends()

    def on_click_close_btn(self, *args):
        self.close()

    def on_login_reconnect(self, *args):
        self.close()

    def refresh_facebook_friends(self):
        self._list_add.DeleteAllSubItem()
        social_friends = self._message_data.get_social_friends(friend_const.SOCIAL_ID_TYPE_FB)
        facebook_friendinfos = self._message_data.get_facebook_friends()
        count = 0
        for data in social_friends:
            if not self._message_data.is_friend(data.get('uid')):
                facebook_data = facebook_friendinfos.get(data.get('social_id'))
                self.add_facebook_friend_elem(data, facebook_data)
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

    def add_facebook_friend_elem(self, data, facebook_data):
        uid = data['uid']
        panel = self._list_add.AddTemplateItem()
        panel.lab_name.setString(facebook_data.get('nickname', ''))
        panel.lab_desc.setVisible(False)
        icon_url = facebook_data.get('icon', '')
        if icon_url:
            file_name = '%s.jpg' % self.get_str_md5(icon_url)
            icon_path = get_neox_dir() + '/' + get_download_target_path('res/' + file_name)
            if os.path.exists(icon_path):
                self.add_facebook_icon(panel, file_name)
            else:

                def load_callback():
                    self.add_facebook_icon(panel, file_name)

                self.download_facebook_icon(icon_url, load_callback)

        @panel.btn_add.callback()
        def OnClick(*args):
            self.on_touch_item(panel, uid)

    def add_facebook_icon(self, elem_panel, file_path):
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

    def on_finalize_panel(self):
        self.show_main_ui()

    def download_facebook_icon(self, url, callback):

        def http_callback--- This code section failed: ---

 127       0  LOAD_CONST            1  '%s.jpg'
           3  LOAD_DEREF            0  'self'
           6  LOAD_ATTR             0  'get_str_md5'
           9  LOAD_DEREF            1  'url'
          12  CALL_FUNCTION_1       1 
          15  BINARY_MODULO    
          16  STORE_FAST            1  'file_name'

 128      19  LOAD_GLOBAL           1  'get_neox_dir'
          22  CALL_FUNCTION_0       0 
          25  LOAD_CONST            2  '/'
          28  BINARY_ADD       
          29  LOAD_GLOBAL           2  'get_download_target_path'
          32  LOAD_CONST            3  'res/'
          35  LOAD_FAST             1  'file_name'
          38  BINARY_ADD       
          39  CALL_FUNCTION_1       1 
          42  BINARY_ADD       
          43  STORE_FAST            2  'file_path'

 129      46  LOAD_FAST             2  'file_path'
          49  LOAD_ATTR             3  'rfind'
          52  LOAD_CONST            2  '/'
          55  CALL_FUNCTION_1       1 
          58  STORE_FAST            3  'index'

 130      61  LOAD_FAST             2  'file_path'
          64  LOAD_CONST            4  ''
          67  LOAD_FAST             3  'index'
          70  SLICE+3          
          71  STORE_FAST            4  'dirs'

 131      74  LOAD_GLOBAL           4  'os'
          77  LOAD_ATTR             5  'path'
          80  LOAD_ATTR             6  'exists'
          83  LOAD_FAST             4  'dirs'
          86  CALL_FUNCTION_1       1 
          89  POP_JUMP_IF_TRUE    108  'to 108'

 132      92  LOAD_GLOBAL           4  'os'
          95  LOAD_ATTR             7  'makedirs'
          98  LOAD_FAST             4  'dirs'
         101  CALL_FUNCTION_1       1 
         104  POP_TOP          
         105  JUMP_FORWARD          0  'to 108'
       108_0  COME_FROM                '105'

 133     108  LOAD_GLOBAL           8  'open'
         111  LOAD_FAST             2  'file_path'
         114  LOAD_CONST            5  'wb'
         117  CALL_FUNCTION_2       2 
         120  STORE_FAST            5  'jpg_file'

 134     123  LOAD_FAST             5  'jpg_file'
         126  LOAD_ATTR             9  'write'
         129  LOAD_ATTR             4  'os'
         132  BINARY_SUBSCR    
         133  CALL_FUNCTION_1       1 
         136  POP_TOP          

 135     137  LOAD_FAST             5  'jpg_file'
         140  LOAD_ATTR            10  'close'
         143  CALL_FUNCTION_0       0 
         146  POP_TOP          

 136     147  LOAD_DEREF            2  'callback'
         150  POP_JUMP_IF_FALSE   163  'to 163'

 137     153  LOAD_DEREF            2  'callback'
         156  CALL_FUNCTION_0       0 
         159  POP_TOP          
         160  JUMP_FORWARD          0  'to 163'
       163_0  COME_FROM                '160'

Parse error at or near `BINARY_SUBSCR' instruction at offset 132

        common.http.request_v2(url, None, {}, http_callback)
        return

    def get_str_md5(self, url):
        import hashlib
        index = url.rfind('&ext=')
        url_enable = url[0:index]
        import six
        md5 = hashlib.md5(six.ensure_binary(url_enable)).hexdigest()
        return md5

    def on_touch_item(self, panel, uid):
        global_data.player.req_add_friend(uid)
        index = self._list_add.getIndexByItem(panel)
        self._list_add.DeleteItemIndex(index)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_ADD_VIA_FACEBOOK)

    def on_send_link(self):
        key_word = '%s=%s' % (share_const.DEEP_LINK_ADD_FRIEND, str(global_data.player.uid))
        logic.gutils.share_utils.web_share(key_word, share_const.APP_SHARE_FACEBOOK)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_SHARE_VIA_FACEBOOK)