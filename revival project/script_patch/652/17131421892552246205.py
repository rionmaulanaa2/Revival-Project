# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/AddFriend.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
import time
from cocosui import cc, ccui, ccs
import common.const.uiconst
from common.const.property_const import *
from logic.gcommon import const
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.comsys.common_ui.InputBox as InputBox
import common.utilities
import logic.gcommon.const
from common.utils.path import get_neox_dir
from patch.patch_path import get_download_target_path
import math
from logic.gutils.role_head_utils import PlayerInfoManager, set_gray, set_gray_by_online_state
from logic.gutils import role_head_utils
from common.platform import channel_const
from logic.gcommon.common_const import chat_const
from logic.client.const import share_const
from common.platform.dctool import interface
from common.cfg import confmgr
import logic.gutils.share_utils
from logic.gutils import friend_utils
import game3d
from logic.gcommon.common_utils.text_utils import check_review_words
from logic.gutils.search_salog_utils import add_common_search_salog
RECOMMEND_TAB_NORMAL = 0
RECOMMEND_TAB_TEMP_TEAM = 1
RECOMMEND_TAB_PLATFORM = 2
RECOMMEND_TAB_COUNT = 3
TAB_MAP = {RECOMMEND_TAB_NORMAL: {'tab_name': 10270},RECOMMEND_TAB_TEMP_TEAM: {'tab_name': 10271},RECOMMEND_TAB_PLATFORM: {'tab_name': 10286}}
REQ_RECOMMEND_MIN_INTERVAL_TIME = 3.0

class AddFriend(object):

    def __init__(self, main_panel, **kargs):
        panel_temp = global_data.uisystem.load_template_create('friend/i_add_friend', main_panel.panel, name='add_content')
        panel_temp.SetPosition('50%', '50%')
        self.main_panel = main_panel
        self.panel = main_panel.panel
        self._message_data = global_data.message_data
        self._init_tab_index = kargs.get('tab_index', None)
        self._cur_tab_index = 0
        self._tab_panels = {}
        self.tag_idnex = 0
        self._last_selected_role_id = 0
        self._player_info_manager = PlayerInfoManager()
        self.platform_item_temp = global_data.uisystem.load_template('friend/i_list_platform_item')
        global_data.player.req_recommend_friend()
        self._player_simple_inf_pos_y = panel_temp.getContentSize().height - 20
        self._player_simple_inf_pos_y = 0
        self.init_list()
        self.init_inputbox()
        self.qrcode_sprite = None

        def callback():
            self.init_qrcode()
            self.delay_exec_id = None
            return

        self.delay_exec_id = game3d.delay_exec(1, callback)
        self._apply_friends_ids = []
        self._message_data = global_data.message_data
        global_data.emgr.message_refresh_friend_recommend += self.refresh_recommend_friends
        global_data.emgr.message_refresh_friends += self.refresh_temp_team_friends
        global_data.emgr.message_refresh_friend_search += self.on_search_friends
        global_data.emgr.on_bind_channel_event += self.on_bind_channel
        img_red_dot = self.panel.add_content.nd_friend.nd_list.btn_apply_list.img_red_dot

        def callback():
            friends = self._message_data.get_apply_friends()
            if friends:
                img_red_dot.lab_num.SetString(str(len(friends)))

        self._apply_num_cb = callback
        global_data.redpoint_mgr.register_redpoint(img_red_dot, '4', callback)
        return

    def init_list(self):
        nd_list = self.panel.add_content.nd_friend.nd_list
        self._lv_friend = nd_list.list_friend
        list_tab = nd_list.nd_tab.list_tab
        list_tab.DeleteAllSubItem()
        from logic.gutils.share_utils import is_share_enable
        if interface.get_game_id() == 'g93' or not is_share_enable() or global_data.is_google_pc:
            tab_count = RECOMMEND_TAB_COUNT - 1
        else:
            tab_count = RECOMMEND_TAB_COUNT
        for tab_index in range(tab_count):
            panel = list_tab.AddTemplateItem()
            panel.btn_tab.SetText(get_text_by_id(TAB_MAP[tab_index]['tab_name']))
            self.add_touch_tab(panel, tab_index)

        if self._init_tab_index != None:
            self.touch_tab_by_index(self._init_tab_index)
        else:
            self.touch_tab_by_index(RECOMMEND_TAB_NORMAL)
        self._last_request_time = None

        @nd_list.btn_change.callback()
        def OnClick(*args):
            now = time.time()
            if self._last_request_time == None or now - self._last_request_time > REQ_RECOMMEND_MIN_INTERVAL_TIME:
                global_data.player.req_recommend_friend()
                self._last_request_time = now
            else:
                delay_time = REQ_RECOMMEND_MIN_INTERVAL_TIME - (now - self._last_request_time)
                global_data.player.notify_client_message((get_text_by_id(10273).format('%d' % math.ceil(delay_time)),))
            return

        @nd_list.btn_apply_list.callback()
        def OnClick(*args):
            from logic.comsys.message import HintLineUI
            HintLineUI.query_friend_apply_from_line(lambda : global_data.ui_mgr.show_ui('FriendApplyList', 'logic.comsys.message'))

        @nd_list.btn_platform_set.callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('ChannelSettingUI', 'logic.comsys.message')

        return

    def init_inputbox(self):
        nd_bottom = self.panel.add_content.nd_friend.nd_add.nd_bottom
        if global_data.is_pc_mode:

            def cb():
                if not nd_bottom.isValid():
                    return
                else:
                    if not nd_bottom.btn_search or not nd_bottom.btn_search.isValid():
                        return
                    search = nd_bottom.btn_search
                    if not search or not search.isValid():
                        return
                    btn = search.btn_common
                    if not btn or not btn.isValid():
                        return
                    btn.OnClick(None)
                    return

            send_callback = cb
        else:
            send_callback = None
        self._input_box = InputBox.InputBox(nd_bottom.input_box, placeholder=get_text_by_id(10026), send_callback=send_callback)
        self._input_box.set_rise_widget(self.panel)
        self.search_time = 0

        @nd_bottom.btn_search.btn_common.callback()
        def OnClick(*args):
            if not self._input_box:
                return
            text = self._input_box.get_text()
            if not text:
                return
            now = time.time()
            interval = now - self.search_time
            if interval < logic.gcommon.const.SEARCH_FRIEND_MIN_TIME:
                notify_text = get_text_by_id(10039, {'time': int(logic.gcommon.const.SEARCH_FRIEND_MIN_TIME - interval) + 1})
                global_data.player.notify_client_message((notify_text,))
                return
            self.search_time = now
            self._input_box.set_text('')
            if self.check_is_int(text):
                frd_uid = int(text)
                if not G_IS_NA_USER:
                    frd_uid += global_data.uid_prefix
                if frd_uid >= 18446744073709551616L:
                    return
                frd_name = ''
            else:
                frd_uid = 0
                frd_name = str(text)
                import common.utilities
                from logic.gcommon.const import NAME_MAX_BYTE_COUNT
                if common.utilities.get_byte_count(text) > NAME_MAX_BYTE_COUNT:
                    return
                flag, frd_name_review = check_review_words(frd_name)
                if not flag:
                    global_data.game_mgr.show_tip(get_text_by_id(10045))
                    add_common_search_salog(str(frd_name))
                    return
            if not global_data.player.search_friend(frd_uid, frd_name):
                global_data.game_mgr.show_tip(get_text_by_id(10044))

        return

    def check_is_int(self, text):
        try:
            int(text)
            return True
        except:
            return False

    def init_qrcode(self):
        import game3d
        import os
        import render
        self.qrcode_sprite = None
        nd_qr_code = self.panel.add_content.nd_friend.nd_add.nd_qr_code
        nd_qr_code.lab_name.setString(global_data.player.get_name())
        if G_IS_NA_USER:
            nd_qr_code.lab_id.setString('ID:' + str(global_data.player.uid))
        else:
            show_id = int(global_data.player.uid)
            show_id -= global_data.uid_prefix
            nd_qr_code.lab_id.setString('ID:' + str(show_id))
        if game3d.get_platform() != game3d.PLATFORM_WIN32 and not global_data.is_pc_mode:
            file_name = str(global_data.player.uid) + '_qrcode.png'
            file_path = get_neox_dir() + '/' + get_download_target_path('res/' + file_name)
            if os.path.exists(file_path):
                self.create_qrcode_pic(file_name)
            else:
                nd_qr_code.nd_bg.SetTimeOut(0.001, self.make_qrcode_img)

            @nd_qr_code.btn_scan.callback()
            def OnClick(*args):
                from logic.gutils.share_utils import huawei_permission_confirm
                permission = 'android.permission.CAMERA'
                huawei_permission_confirm(permission, 635574, self.do_btn_scan)

        else:
            self.panel.add_content.PlayAnimation('pc')

        @nd_qr_code.btn_copy.callback()
        def OnClick(*args):
            import game3d
            if G_IS_NA_USER:
                game3d.set_clipboard_text(str(global_data.player.uid))
            else:
                show_id = int(global_data.player.uid)
                show_id -= global_data.uid_prefix
                game3d.set_clipboard_text(str(show_id))
            global_data.game_mgr.show_tip(get_text_by_id(10053))

        if global_data.is_android_pc:
            nd_qr_code.btn_scan.setVisible(False)
        return

    def do_btn_scan(self, *args):

        def callback--- This code section failed: ---

 267       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'check_is_int'
           6  LOAD_ATTR             1  'global_data'
           9  BINARY_SUBSCR    
          10  CALL_FUNCTION_1       1 
          13  POP_JUMP_IF_FALSE    42  'to 42'

 268      16  LOAD_GLOBAL           1  'global_data'
          19  LOAD_ATTR             2  'player'
          22  LOAD_ATTR             3  'req_add_friend'
          25  LOAD_GLOBAL           4  'int'
          28  LOAD_GLOBAL           1  'global_data'
          31  BINARY_SUBSCR    
          32  CALL_FUNCTION_1       1 
          35  CALL_FUNCTION_1       1 
          38  POP_TOP          
          39  JUMP_FORWARD         25  'to 67'

 270      42  LOAD_GLOBAL           1  'global_data'
          45  LOAD_ATTR             2  'player'
          48  LOAD_ATTR             5  'notify_client_message'
          51  LOAD_GLOBAL           6  'get_text_by_id'
          54  LOAD_CONST            2  10067
          57  CALL_FUNCTION_1       1 
          60  BUILD_TUPLE_1         1 
          63  CALL_FUNCTION_1       1 
          66  POP_TOP          
        67_0  COME_FROM                '39'

Parse error at or near `BINARY_SUBSCR' instruction at offset 9

        global_data.channel.present_qrcode_scanner('', 0, callback)

    def make_qrcode_img(self):
        import game3d
        import os
        import C_file
        file_name = str(global_data.player.uid) + '_qrcode.png'
        file_path = get_neox_dir() + '/' + get_download_target_path('res/' + file_name)
        index = file_path.rfind('/')
        dirs = file_path[0:index]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        try:
            common.utilities.make_qrcode(global_data.player.uid, file_path)
            C_file.set_fileloader_enable('patch', True)
            self.create_qrcode_pic(file_name)
        except IOError as e:
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            NormalConfirmUI2().set_content_string(get_text_by_id(177))

    def create_qrcode_pic(self, file_name):
        self.qrcode_sprite = cc.Sprite.create(file_name)
        if not self.qrcode_sprite:
            return
        if self.qrcode_sprite.getTextureRect().width == 0:
            return
        self.qrcode_sprite.setAnchorPoint(cc.Vec2(0.5, 0.5))
        nd_bg = self.panel.add_content.nd_friend.nd_add.nd_qr_code.nd_bg
        size = nd_bg.getContentSize()
        self.qrcode_sprite.setPosition(cc.Vec2(size.width * 0.5, size.height * 0.5))
        scale = float(200) / self.qrcode_sprite.getTextureRect().width
        self.qrcode_sprite.setScale(scale)
        nd_bg.addChild(self.qrcode_sprite)

    def add_touch_tab(self, panel, tab_index):
        self._tab_panels[tab_index] = panel
        panel.btn_tab.EnableCustomState(True)

        @panel.btn_tab.callback()
        def OnClick(*args):
            self.touch_tab_by_index(tab_index)

        if tab_index == RECOMMEND_TAB_PLATFORM and global_data.channel.is_guest():
            panel.img_award.setVisible(True)
        else:
            panel.img_award.setVisible(False)

    def touch_tab_by_index(self, tab_index):
        tab_panel = self._tab_panels.get(self._cur_tab_index)
        if tab_panel:
            tab_panel.btn_tab.SetSelect(False)
            tab_panel.PlayAnimation('unclick')
            tab_panel.img_vx.setVisible(False)
        tab_panel = self._tab_panels.get(tab_index)
        if tab_panel:
            tab_panel.btn_tab.SetSelect(True)
            tab_panel.img_vx.setVisible(True)
            tab_panel.PlayAnimation('click')
        self._cur_tab_index = tab_index
        if self._cur_tab_index == RECOMMEND_TAB_NORMAL:
            self.refresh_recommend_friends()
        elif self._cur_tab_index == RECOMMEND_TAB_TEMP_TEAM:
            self.refresh_temp_team_friends()
        else:
            self.refresh_platfrom()
        self.panel.add_content.nd_friend.nd_list.btn_change.setVisible(self._cur_tab_index == RECOMMEND_TAB_NORMAL)
        btn_platform_visible = global_data.channel.is_bind_linegame() and self._cur_tab_index == RECOMMEND_TAB_PLATFORM
        self.panel.add_content.nd_friend.nd_list.btn_platform_set.setVisible(btn_platform_visible)

    def refresh_recommend_friends(self):
        if self._cur_tab_index != RECOMMEND_TAB_NORMAL:
            return
        self._lv_friend.DeleteAllSubItem()
        friends = self._message_data.get_recommend_friends()
        if friends:
            for data in friends:
                self.add_friend_elem(data)

            self.panel.add_content.nd_empty.setVisible(False)
        else:
            self.panel.add_content.nd_empty.setVisible(True)

    def refresh_temp_team_friends(self):
        if self._cur_tab_index != RECOMMEND_TAB_TEMP_TEAM:
            return
        self._lv_friend.DeleteAllSubItem()
        friends = self._message_data.get_team_friends()
        for data in six.itervalues(friends):
            if not self._message_data.is_friend(data[U_ID]):
                self.add_friend_elem(data)

        nd_empty_flag = friends or True if 1 else False
        self.panel.add_content.nd_empty.setVisible(nd_empty_flag)

    def refresh_platfrom(self):
        if self._cur_tab_index != RECOMMEND_TAB_PLATFORM:
            return
        self.panel.add_content.nd_empty.setVisible(False)
        self._lv_friend.DeleteAllSubItem()
        panel = self._lv_friend.AddItem(self.platform_item_temp, bRefresh=True)
        panel.icon.SetDisplayFrameByPath('', chat_const.FACEBOOK_ICON)
        bind_types = global_data.channel.get_bind_types()
        is_bind_facebook = True if str(channel_const.AUTH_TYPE_FACEBOOK) in bind_types else False
        panel.icon_tick.setVisible(is_bind_facebook)
        if is_bind_facebook:
            panel.lab.setString(get_text_by_id(81024))
        else:
            panel.lab.setString(get_text_by_id(10287))

        @panel.btn_item.callback()
        def OnClick(*args):
            bind_types = global_data.channel.get_bind_types()
            is_bind_facebook = True if str(channel_const.AUTH_TYPE_FACEBOOK) in bind_types else False
            if is_bind_facebook:
                pass
            else:
                global_data.channel.set_prop_str('BIND_TYPE', '1')
                global_data.channel.set_prop_str('AUTH_CHANNEL', 'facebook')
                global_data.channel.guest_bind()
                friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_ADD_BIND_FACEBOOK)

        panel = self._lv_friend.AddItem(self.platform_item_temp, bRefresh=True)
        panel.icon.SetDisplayFrameByPath('', chat_const.TWITTER_ICON)
        is_bind_twitter = True if str(channel_const.AUTH_TYPE_TWITTER) in bind_types else False
        panel.icon_tick.setVisible(is_bind_twitter)
        if is_bind_twitter:
            panel.lab.setString(get_text_by_id(10290))
        else:
            panel.lab.setString(get_text_by_id(10288))

        @panel.btn_item.callback()
        def OnClick(*args):
            bind_types = global_data.channel.get_bind_types()
            is_bind_twitter = True if str(channel_const.AUTH_TYPE_TWITTER) in bind_types else False
            if is_bind_twitter:
                global_data.ui_mgr.show_ui('TwitterFriendList', 'logic.comsys.message')
            else:
                global_data.channel.set_prop_str('BIND_TYPE', '1')
                global_data.channel.set_prop_str('AUTH_CHANNEL', 'twitter')
                global_data.channel.guest_bind()
                friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_ADD_BIND_TWITTER)

        panel = self._lv_friend.AddItem(self.platform_item_temp, bRefresh=True)
        panel.icon.SetDisplayFrameByPath('', chat_const.MESSENGER_ICON)
        panel.icon_tick.setVisible(True)
        panel.lab.setString(get_text_by_id(81260))

        @panel.btn_item.callback()
        def OnClick(*args):
            key_word = '%s=%s' % (share_const.DEEP_LINK_ADD_FRIEND, str(global_data.player.uid))
            logic.gutils.share_utils.web_share(key_word, share_const.APP_SHARE_MESSENGER)

        if global_data.feature_mgr.is_linegame_ready():
            panel = self._lv_friend.AddItem(self.platform_item_temp, bRefresh=True)
            panel.icon.SetDisplayFrameByPath('', chat_const.LINE_ICON)
            is_bind_linegame = global_data.channel.is_bind_linegame()
            panel.icon_tick.setVisible(is_bind_linegame)
            if is_bind_linegame:
                panel.lab.setString(get_text_by_id(609015))
            else:
                panel.lab.setString(get_text_by_id(609014))

            @panel.btn_item.callback()
            def OnClick(*args):
                from logic.comsys.message import HintLineUI
                _is_bind_linegame = global_data.channel.is_bind_linegame()
                if _is_bind_linegame:
                    HintLineUI.check_hint_line(lambda : global_data.ui_mgr.show_ui('LineGameFriendList', 'logic.comsys.message'))
                else:
                    global_data.channel.bind_linegame()
                    friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_ADD_BIND_LINEGAME)

    def add_friend_elem(self, data):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        panel = self._lv_friend.AddTemplateItem()
        name = data.get(C_NAME, '')
        setattr(panel, 'data', data)
        if panel.btn_item.lab_name:
            panel.btn_item.lab_name.setString(name)
        uid = data.get(U_ID)
        role_id = data.get(ROLE_ID, u'11')
        if self._cur_tab_index == RECOMMEND_TAB_TEMP_TEAM:
            friend_online_state = self._message_data.get_player_online_state()
            state = int(friend_online_state.get(int(uid), 0))
            self._player_info_manager.add_head_item_auto(panel.btn_item.temp_head, uid, 0, data)
            set_gray_by_online_state(panel.btn_item.temp_head, state)
        else:
            state = int(data.get('st', 1))
            self._player_info_manager.add_head_item_auto(panel.btn_item.temp_head, uid, 0, data)
        role_head_utils.set_role_dan(panel.temp_tier, data.get('dan_info'))
        text_id, color = ui_utils.get_online_inf(state)
        panel.lab_status.setString(get_text_by_id(text_id))
        panel.lab_status.SetColor(color)
        tag = self.tag_idnex
        panel.setTag(tag)
        self.tag_idnex += 1
        panel.btn_follow.setVisible(True)

        @panel.btn_follow.callback()
        def OnClick(*args):
            global_data.player.req_add_friend(data[U_ID])
            global_data.message_data.del_recommend_friend(data[U_ID])
            self._lv_friend.DeleteItemByTag(tag)

        panel.btn_follow.SetSwallowTouch(False)
        panel.red_dot_1.setVisible(False)

        @panel.temp_head.callback()
        def OnClick(*args):
            pos_x, pos_y = panel.GetPosition()
            world_pos = panel.ConvertToWorldSpace(pos_x, pos_y)
            size = panel.getContentSize()
            show_pos_x = world_pos.x + size.width
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            ui.refresh_by_uid(int(data[U_ID]))
            ui.set_position(cc.Vec2(show_pos_x, self._player_simple_inf_pos_y))

        panel.temp_head.SetSwallowTouch(False)

        @panel.btn_item.callback()
        def OnClick(*args):
            for item in self._lv_friend.GetAllItem():
                cur_role_id = item.data.get(ROLE_ID, u'11')

            self._last_selected_role_id = role_id

        panel.btn_item.SetSwallowTouch(False)

    def on_bind_channel(self, *args):
        self.refresh_platfrom()
        btn_platform_visible = global_data.channel.is_bind_linegame() and self._cur_tab_index == RECOMMEND_TAB_PLATFORM
        self.panel.add_content.nd_friend.nd_list.btn_platform_set.setVisible(btn_platform_visible)

    def on_search_friends(self, *args):
        global_data.ui_mgr.show_ui('FriendSearchList', 'logic.comsys.message')

    def set_visible(self, visible):
        self.panel.add_content.setVisible(visible)

    def hide_inputbox(self):
        if self._input_box:
            self._input_box.hide()

    def destroy(self):
        if self.delay_exec_id:
            game3d.cancel_delay_exec(self.delay_exec_id)
            self.delay_exec_id = None
        self._apply_num_cb = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        if self.qrcode_sprite:
            self.qrcode_sprite.isValid() and self.qrcode_sprite.removeFromParent()
            self.qrcode_sprite = None
        global_data.emgr.message_refresh_friend_recommend -= self.refresh_recommend_friends
        global_data.emgr.message_refresh_friends -= self.refresh_temp_team_friends
        global_data.emgr.message_refresh_friend_search -= self.on_search_friends
        global_data.emgr.on_bind_channel_event -= self.on_bind_channel
        return

    def get_friend_list(self):
        return self._lv_friend