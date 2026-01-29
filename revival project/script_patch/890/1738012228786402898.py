# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/FriendChat.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import math
import time
from common.uisys.uielment.CCRichText import CCRichText
from cocosui import cc, ccui, ccs
from common.const.property_const import *
import common.const.uiconst
import common.utilities
import logic.comsys.common_ui.InputBox as InputBox
import game3d
import re
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.const as const
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex, ccc4aFromHex
import common.utilities
import logic.gutils.template_utils
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gcommon.common_const import chat_const
from logic.gcommon.common_utils import text_utils
from logic.gutils import role_head_utils, chat_utils
from logic.comsys.chat import chat_link
from logic.gcommon.cdata.privilege_data import COLOR_NAME, COLOR_FONT
from logic.gcommon.item import item_const
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gutils.item_utils import get_item_rare_degree
from logic.gutils.mall_utils import get_lottery_id_from_name, check_speaker
from logic.gutils.item_utils import get_skin_rare_path_by_rare
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITME_TYPE_GUNSKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_WEAPON_SFX
from logic.gcommon.common_const.chat_const import winning_streak_bgs
from logic.comsys.lottery.LotteryNew.LotteryResultUI import LotteryResultUI
from logic.gcommon.cdata.luck_score_config import NORMAL_LUCK_SCORE_EDGE, MIN_LUCK_SCORE_PERCENT, LOTTERY_COUNT_SHOW_BAODI
import six
RICHTEXT_CONTENT_EDGE = 10
RICHTEXT_BOTTOM_TRIANGLE_WIDTH = 13
MSG_WEIGHT = 350
SVIEW_WHITH = 664
FONT_COLOR_IDX = 2
ID_COLOR_IDX = 1
VOICE_BAR_WIDTH = 250
from common.utils.ui_utils import calc_pos

class FriendChat(object):

    def __init__(self, main_panel):
        self._message_data = global_data.message_data
        self.main_panel = main_panel
        self.panel = main_panel.panel.chat_content
        self._my_uid = global_data.player.uid
        self._chat_uid = None
        self._chat_data = None
        self._chat_lv = 0
        self._chat_cid = -1
        self._chat_char_name = ''
        self._last_send_time = time.time()
        self._template_data = {}
        self._player_info_manager = PlayerInfoManager()
        self._chat_emote_ui = None
        self._sview_data_index = 0
        self._cur_msg_data = []
        self._ignore_filter_pattern = []
        self._lv_chat = self.panel.nd_chat.lv_chat
        self._lv_chat.DeleteAllSubItem()
        self.show_empty()
        self.reload_all_template_format()
        self.init_touch()
        self.init_input()
        self.check_voice_btn_show()
        self.save_nd_chat_pos_y = self.main_panel.panel.GetPosition()[1]
        self.panel.nd_chat.setVisible(False)
        self.panel.nd_empty.setVisible(True)
        global_data.emgr.message_receive_friend_msg += self.refresh_one_msg
        global_data.emgr.player_join_team_event += self.check_voice_btn_show
        global_data.emgr.player_leave_team_event += self.check_voice_btn_show
        global_data.emgr.message_refresh_contact_group += self.on_refresh_contact
        return

    def init_touch(self):
        self._is_check_sview = False

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self._lv_chat.SetTimeOut(0.021, self.check_sview)

        self._lv_chat.addEventListener(scroll_callback)

        @self.panel.nd_empty.btn_add.btn_common.callback()
        def OnClick(*args):
            from logic.comsys.message.MainFriend import FRIEND_TAB_ADDFRIEND
            self.main_panel.touch_tab_by_index(FRIEND_TAB_ADDFRIEND)

    def read_format_inf(self, template):
        data = {}
        data['size'] = template['size']
        data['msg_pos'] = {'x': 0,'y': 0}
        remove_child = None
        for child in template['child_list']:
            if child.get('name') == 'lab_msg':
                pos = child['pos']
                pos['x'] = calc_pos(pos['x'], data['size']['width'])
                pos['y'] = calc_pos(pos['y'], data['size']['height'])
                data['msg_pos'] = pos
                remove_child = child

        if remove_child:
            template['child_list'].remove(remove_child)
        self._template_data[id(template)] = data
        return

    def init_input(self):
        panel = self.panel
        input_box = panel.nd_bottom.input_box

        def max_input_cb(length, max_length):
            global_data.game_mgr.show_tip(get_text_by_id(19150, {'num': max_length}))

        def send_cb(*args, **kwargs):
            panel.btn_send.btn_common.OnClick(None)
            return

        self._input_box = InputBox.InputBox(input_box, max_input_cb=max_input_cb, send_callback=send_cb, detach_after_enter=False)
        self._input_box.set_rise_widget(self.main_panel)

        @panel.btn_emote.callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('ChatEmote', 'logic.comsys.chat')
            self._chat_emote_ui = ui
            ui.set_input_box(self._input_box, panel.btn_send.btn_common)
            ui.set_close_callback(self.panel_recover)
            panel_offset = (self.main_panel.panel.getContentSize().height - self.panel.nd_friend.getContentSize().height) * 0.5
            height_offset = ui.get_bg_height() - panel_offset + 5
            if height_offset < 0:
                height_offset = 0
            self.panel_up_move(height_offset)

        @panel.btn_send.btn_common.callback()
        def OnClick(*args, **kargs):
            do_not_check_msg = kargs.get('do_not_check_msg')
            msg = do_not_check_msg or self._input_box.get_text()
            self.send_msg(self._chat_data, msg, do_not_check_msg)

        def send_msg(msg, do_not_check_msg=False):
            if not msg:
                global_data.player.notify_client_message((get_text_by_id(11055),))
                return
            if do_not_check_msg:
                check_code = 0
                check_result = text_utils.CHECK_WORDS_PASS
            else:
                check_code, check_result, msg = text_utils.check_review_words_chat(msg)
                if check_result == text_utils.CHECK_WORDS_NO_PASS:
                    global_data.player.notify_client_message((get_text_by_id(11009),))
                    global_data.player.sa_log_forbidden_msg(chat_const.CHAT_FRIEND, msg, check_code, self._chat_uid, self._chat_lv)
                    return
                self._input_box.set_text('')
            if self._chat_uid:
                if global_data.message_data.is_black_friend(self._chat_uid):
                    global_data.game_mgr.show_tip(get_text_by_id(10021))
                    return
                chat_name = self._chat_data.get(C_NAME, '')
                lv = self._chat_data.get(U_LV, 1)
                self._message_data.recv_to_friend_msg(self._chat_uid, chat_name, msg, lv)
                if check_result == text_utils.CHECK_WORDS_PASS:
                    global_data.player.req_friend_msg(self._chat_uid, self._chat_lv, self._chat_cid, msg)
                else:
                    global_data.player.sa_log_forbidden_msg(chat_const.CHAT_FRIEND, msg, check_code, self._chat_uid, self._chat_lv)

        self.voice_operate = logic.gutils.template_utils.voiceOperate(self, panel.btn_voice)

    def check_voice_btn_show(self, *args):
        from common.audio.ccmini_mgr import LOBBY_TEAM_SPEAKER, LOBBY_TEAM_MIC
        flag = global_data.player.is_in_team() and global_data.message_data.get_seting_inf(LOBBY_TEAM_MIC)
        self.panel.btn_voice.setVisible(not flag)

    def get_send_voice_callback(self):
        chat_data = self._chat_data

        def send_voice_msg_callback(msg_str, voice_str):
            self.send_voice_msg(chat_data, msg_str, voice_str)

        return send_voice_msg_callback

    def send_voice_msg(self, chat_data, msg_str, voice_str):
        cur_time = time.time()
        if cur_time - self._last_send_time < 0.5:
            return
        self._last_send_time = cur_time
        if not chat_data:
            return
        if msg_str == '':
            last_time, _ = voice_str.split('\n', 1)
            if float(last_time) < chat_const.VOICE_NONE_MAX_TIME:
                global_data.player.notify_client_message((get_text_by_id(11055),))
                return
        chat_uid = chat_data.get(U_ID, 0)
        chat_name = chat_data.get(C_NAME, '')
        chat_cid = chat_data.get(CLAN_ID, -1)
        lv = chat_data.get(U_LV, 1)
        check_code, check_result, msg_str = text_utils.check_review_words_chat(msg_str)
        if check_result == text_utils.CHECK_WORDS_NO_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            global_data.player.sa_log_forbidden_msg(chat_const.CHAT_FRIEND, msg_str, check_code, chat_uid, lv)
            return
        if not self.check_send_non_friend_msg(chat_uid):
            return
        self._message_data.recv_to_friend_msg(chat_uid, chat_name, msg_str, lv, voice_str)
        if check_result == text_utils.CHECK_WORDS_PASS:
            global_data.player.req_friend_msg(chat_uid, lv, chat_cid, msg_str, voice_str)
        else:
            global_data.player.sa_log_forbidden_msg(chat_const.CHAT_FRIEND, msg_str, check_code, chat_uid, lv)

    def get_voice_text_callback(self):
        chat_data = self._chat_data

        def send_text_msg_callback(msg, do_not_check_msg=False):
            self.send_msg(chat_data, msg, do_not_check_msg)

        return send_text_msg_callback

    def send_msg(self, chat_data, msg, do_not_check_msg=False):
        if not msg:
            global_data.player.notify_client_message((get_text_by_id(11055),))
            return
        else:
            if chat_data is None:
                return
            chat_uid = chat_data.get(U_ID, 0)
            chat_name = chat_data.get(C_NAME, '')
            chat_lv = chat_data.get(U_LV, 1)
            chat_cid = chat_data.get(CLAN_ID, -1)
            if do_not_check_msg:
                check_code = 0
                check_result = text_utils.CHECK_WORDS_PASS
            else:
                check_code, check_result, msg = text_utils.check_review_words_chat(msg)
                if check_result == text_utils.CHECK_WORDS_NO_PASS:
                    global_data.player.notify_client_message((get_text_by_id(11009),))
                    global_data.player.sa_log_forbidden_msg(chat_const.CHAT_FRIEND, msg, check_code, chat_uid, chat_lv)
                    return
                self._input_box and self._input_box.set_text('')
            if chat_uid:
                if global_data.message_data.is_black_friend(chat_uid):
                    global_data.game_mgr.show_tip(get_text_by_id(10021))
                    return
                if not self.check_send_non_friend_msg(chat_uid):
                    return
                self._message_data.recv_to_friend_msg(chat_uid, chat_name, msg, chat_lv)
                if check_result == text_utils.CHECK_WORDS_PASS:
                    global_data.player.req_friend_msg(chat_uid, chat_lv, chat_cid, msg)
                else:
                    global_data.player.sa_log_forbidden_msg(chat_const.CHAT_FRIEND, msg, check_code, chat_uid, chat_lv)
            return

    def refresh_one_msg(self, chat_uid, index_move, data):
        if self._chat_uid == chat_uid:
            self.add_msg(data)
            self._lv_chat._container._refreshItemPos()
            self._lv_chat._refreshItemPos()
            self._lv_chat.ScrollToBottom()
            self._sview_data_index += index_move

    def on_refresh_contact(self):
        if str(self._chat_uid) not in global_data.message_data._chat_friend:
            self.show_empty()

    def show_empty(self):
        self.panel.nd_chat.setVisible(False)
        self.panel.nd_empty.setVisible(True)
        if self._message_data.get_friends():
            self.panel.nd_empty.lab_empty.setString(get_text_by_id(10263))
        else:
            self.panel.nd_empty.lab_empty.setString(get_text_by_id(10281))
        self._friends = global_data.message_data.get_friends()
        self.panel.nd_empty.btn_add.setVisible(not self._friends)

    def is_ignore_filter_message(self, msg):
        if not self._ignore_filter_pattern:
            self._ignore_filter_pattern = [re.compile('<link=\\d+,.+>.*</link>'),
             re.compile('<emote=\\d+,\\d{1,3}>')]
        for sub_pattern in self._ignore_filter_pattern:
            if sub_pattern.match(msg) is not None:
                return True

        return

    def filter_history_message(self, chat_data):
        chat_record_list = chat_data.get('chat_record_list', [])
        filtered_result = []
        for data in chat_record_list:
            if 'msg' in data:
                msg = data['msg']
                if self.is_ignore_filter_message(msg):
                    filtered_result.append(data)
                    continue
                check_code, check_result, regulize_msg = text_utils.check_review_words_chat(data['msg'], False)
                if check_result == text_utils.CHECK_WORDS_NO_PASS:
                    continue
                data['msg'] = regulize_msg
            filtered_result.append(data)

        return filtered_result

    def censor_chat_data(self, chat_data):
        if 'msg' not in chat_data:
            return chat_data
        msg = chat_data['msg']
        if self.is_ignore_filter_message(msg):
            return chat_data
        check_code, check_result, regulize_msg = text_utils.check_review_words_chat(msg, False)
        if check_result == text_utils.CHECK_WORDS_NO_PASS:
            regulize_msg = '***'
        chat_data['msg'] = regulize_msg
        return chat_data

    def refresh_friend_chat(self, friend_data):
        self.panel.nd_chat.setVisible(True)
        self.panel.nd_empty.setVisible(False)
        self._lv_chat.DeleteAllSubItem()
        self._chat_uid = friend_data[U_ID]
        self._chat_lv = friend_data[U_LV]
        self._chat_cid = friend_data.get(CLAN_ID, -1)
        self._chat_char_name = friend_data.get(C_NAME)
        self._chat_data = friend_data
        self._cur_msg_data = self._message_data.get_chat_data(friend_data[U_ID]).get('chat_record_list', [])
        last_20_msg = self._cur_msg_data[-20:]
        for msg_data in last_20_msg:
            msg = msg_data.get('msg', '')
            uid = msg_data.get('uid', 0)
            if global_data.player and uid != global_data.player.uid and chat_utils.anti_spoofing_check(msg) and not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel():
                self.panel.temp_tips_warnning.setVisible(True)
                self.panel.lv_chat.SetContentSize(650, 430)
                break
        else:
            self.panel.temp_tips_warnning.setVisible(False)
            self.panel.lv_chat.SetContentSize(650, 455)

        intimacy_data = global_data.player.intimacy_data.get(str(self._chat_uid), [])
        if (not intimacy_data or intimacy_data[3] < 1) and not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel():
            self.panel.temp_tips_warnning.setVisible(True)
            self.panel.lv_chat.SetContentSize(650, 430)
        self._sview_data_index = 0
        data_count = len(self._cur_msg_data)
        sview_height = self._lv_chat.getContentSize().height
        all_height = 0
        index = 0
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            data = self._cur_msg_data[data_count - index - 1]
            if data_count - index - 2 < 0:
                up_data = None
            else:
                up_data = self._cur_msg_data[data_count - index - 2]
            chat_pnl = self.add_msg(data, False, -1, up_data)
            if chat_pnl is None:
                del self._cur_msg_data[data_count - index - 1]
                data_count -= 1
                continue
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._sview_data_index = data_count - 1
        self._lv_chat._container._refreshItemPos()
        self._lv_chat._refreshItemPos()
        self._lv_chat.ScrollToBottom()
        self.panel.nd_chat.nd_title.lab_name.SetString(friend_data[C_NAME])
        player_data = self._message_data.get_player_detail_inf(self._chat_uid)
        if not player_data:
            player_data = {}
        priv_settings = player_data.get('priv_settings', {})
        priv_purple_id = player_data.get('priv_purple_id', False)
        if priv_purple_id and priv_settings.get(const.PRIV_SHOW_PURPLE_ID):
            self.panel.nd_chat.nd_title.lab_name.SetColor(COLOR_NAME)
        else:
            self.panel.nd_chat.nd_title.lab_name.SetColor('#BC')
        return

    def add_msg(self, data, is_back_item=True, index=-1, up_data=None):
        notify_type = data.get('extra', {}).get('notify_type')
        if notify_type:
            from logic.gcommon.common_const.notice_const import NOTICE_WINNING, NOTICE_REWARD
            if notify_type == NOTICE_WINNING:
                panel = self.add_winning_broadcast_msg(data, is_back_item)
            elif notify_type == NOTICE_REWARD:
                panel = self.add_lottery_broadcast_msg(data, is_back_item)
            else:
                panel = None
        elif data[U_ID]:
            if data.get('voice', ''):
                panel = self.add_voice_msg(data, is_back_item)
            else:
                panel = self.add_text_msg(data, is_back_item)
        else:
            panel = self.add_sys_msg(data, is_back_item)
        return panel

    def add_lottery_broadcast_msg(self, data, is_back_item=True, is_new=False):
        from logic.gutils.mecha_skin_utils import is_s_skin_that_can_upgrade
        from logic.gcommon.common_const import friend_const
        init_text = data['msg']
        tid, args = unpack_text_data(init_text)
        item_no = args['itemtype']
        quality = args.get('quality') or get_item_rare_degree(item_no, ignore_imporve=True)
        item_type = get_lobby_item_type(item_no)
        if item_type == L_ITEM_TYPE_WEAPON_SFX:
            from logic.gutils.dress_utils import get_weapon_sfx_skin_show_mount_item_no
            mount_item_no = get_weapon_sfx_skin_show_mount_item_no(item_no)
            if not is_s_skin_that_can_upgrade(mount_item_no):
                template_name = 'chat/i_chat_pigeon_item_ex'
            else:
                template_name = 'chat/i_chat_pigeon_item_splus'
        elif quality in (item_const.RARE_DEGREE_4, item_const.RARE_DEGREE_6):
            template_name = 'chat/i_chat_pigeon_item_s'
        elif quality in (item_const.RARE_DEGREE_5, item_const.RARE_DEGREE_7):
            template_name = 'chat/i_chat_pigeon_item_ss'
        else:
            template_name = 'chat/i_chat_pigeon_item_s'
        panel = global_data.uisystem.load_template_create(template_name)
        enable_blessing = True
        if data.get('uid') == global_data.player.uid:
            enable_blessing = True
        reward_key = data['extra'].get('reward_key')
        import logic.gcommon.time_utility as tutil
        now = tutil.time()
        if not reward_key or int(reward_key) + friend_const.BLESSING_MSG_PRESERVE_DURATION < now:
            enable_blessing = False
        if is_back_item:
            self._lv_chat.AddControl(panel, bRefresh=True)
        else:
            self._lv_chat.AddControl(panel, index=0, bRefresh=True)
        if is_new:
            panel.PlayAnimation('show')
        panel.PlayAnimation('loop')
        uid = args['_uid']
        activity_name = args.get('activityname', None)
        jump_shop = args.get('jump_shop', 0)
        if jump_shop:
            goods_id = args.get('goods_id', None)
        else:
            goods_id = None
        lottery_id = get_lottery_id_from_name(activity_name)
        args.pop('_uid')
        text = get_text_by_id(tid, args)
        textlist = text.split('|')
        msg = textlist[0]
        item_name = ''
        if len(textlist) > 1:
            item_name = textlist[1]
        panel.lab_name.SetString(11007)

        def touch_callback(_msg, ele, touch, touch_event):
            chat_link.link_touch_callback(_msg, uid)

        msg = chat_link.linkstr_to_richtext(msg)
        lab_width = panel.lab_msg.getContentSize().width
        panel.lab_msg.SetStringWithAdapt(msg, (lab_width, 92))
        img_height = panel.img_item.getContentSize().height
        panel_size = panel.getContentSize()
        panel.lab_kind_name.SetString(item_name)
        height = max(img_height + 37, panel_size.height)
        if enable_blessing:
            height = height + 30
        panel.SetContentSize(panel_size.width, height)
        panel.ChildResizeAndPosition()
        if enable_blessing:
            template_name = 'chat/i_chat_blessing'
            blessing_ui = global_data.uisystem.load_template_create(template_name)
            panel.AddChild('blessing', blessing_ui)
            blessing_ui.setPosition(cc.Vec2(0, -30))
            blessing_ui.setAnchorPoint(cc.Vec2(0, 0))
            blessed = data.get('blessed')

            def blessing_touch_callback(_msg, ele, touch, touch_event):
                chat_link.link_touch_callback(_msg, data, blessing_ui)

            blessing_msg = get_text_by_id(633749)
            blessing_msg = chat_link.linkstr_to_richtext(blessing_msg)
            lab_blessing = blessing_ui.lab_blessing
            lab_blessing.SetString(blessing_msg)
            if blessed:
                blessing_ui.icon_got.setVisible(True)
            else:
                blessing_ui.icon_got.setVisible(False)
                lab_blessing.SetCallback(blessing_touch_callback)
        panel.lab_msg.SetStringWithAdapt(msg, (lab_width, 92))
        if global_data.player.uid != uid:
            panel.lab_msg.SetCallback(touch_callback)
        if quality in (item_const.RARE_DEGREE_6, item_const.RARE_DEGREE_7):
            panel.temp_kind and panel.temp_kind.SetDisplayFrameByPath('', get_skin_rare_path_by_rare(quality))
        panel.nd_mech.setVisible(False)
        item_type = get_lobby_item_type(item_no)
        show_item_no = item_no
        if item_type in (L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_MECHA):
            nd = panel.nd_mech
            nd_img = panel.nd_mech.img_skin
        elif item_type in (L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_ROLE):
            nd = panel.nd_people
            nd_img = panel.nd_people.img_skin
        elif item_type == L_ITME_TYPE_GUNSKIN:
            nd = nd_img = panel.nd_weapon
        elif item_type == L_ITEM_TYPE_WEAPON_SFX:
            from logic.gutils.dress_utils import get_weapon_sfx_skin_show_mount_item_no
            mount_item_no = get_weapon_sfx_skin_show_mount_item_no(item_no)
            nd = panel.nd_mech
            nd_img = panel.nd_mech.img_skin
            show_item_no = mount_item_no
        else:
            nd = nd_img = panel.nd_others
        nd.setVisible(True)
        nd_img.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(show_item_no))

        @panel.btn_goto.unique_callback()
        def OnClick(*args):
            from logic.gutils.item_utils import chat_jump_to_ui
            if chat_jump_to_ui(item_no, activity_name):
                return
            from logic.gutils.jump_to_ui_utils import jump_to_lottery
            jump_to_lottery(lottery_id=lottery_id, show_model_id=item_no, exchange_shop_goods_id=goods_id)

        return panel

    def add_winning_broadcast_msg(self, data, is_back_item):
        template_name = 'chat/i_chat_pigeon_item_data'
        init_text = data['msg']
        tid, args = unpack_text_data(init_text)
        item_no = args['itemtype']
        panel = global_data.uisystem.load_template_create(template_name)
        if is_back_item:
            self._lv_chat.AddControl(panel, bRefresh=True)
        else:
            self._lv_chat.AddControl(panel, index=0, bRefresh=True)
        text = get_text_by_id(tid, args)
        textlist = text.split('|')
        msg = textlist[0]
        winning_tag = ''
        if len(textlist) > 1:
            winning_tag = textlist[1]
        uid = args['_uid']
        args.pop('_uid')
        panel.lab_name.SetString(11007)

        def touch_callback(_msg, ele, touch, touch_event):
            chat_link.link_touch_callback(_msg, uid)

        msg = chat_link.linkstr_to_richtext(msg)
        lab_width = panel.lab_msg.getContentSize().width
        panel.lab_msg.SetStringWithAdapt(msg, (lab_width, 92))
        img_height = panel.img_item.getContentSize().height
        panel_size = panel.getContentSize()
        panel.lab_kind_name.SetString(winning_tag)
        height = max(img_height + 37, panel_size.height)
        panel.SetContentSize(panel_size.width, height)
        panel.ChildResizeAndPosition()
        panel.lab_msg.SetStringWithAdapt(msg, (lab_width, 92))
        if global_data.player.uid != uid:
            panel.lab_msg.SetCallback(touch_callback)
        show_item_no = item_no
        nd = panel.nd_mech
        nd_img = panel.nd_mech.img_skin
        nd.setVisible(True)
        nd_img.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(show_item_no))
        winning_info = args.get('winning_info', {})
        winning_streak = winning_info.get('winning_streak', 0)
        bgs = winning_streak_bgs.get(str(winning_streak)) or winning_streak_bgs['20']
        panel.img_item.img_item_s.SetDisplayFrameByPath('', bgs[0])
        panel.nd_show.btn_goto.SetFrames('', [bgs[1], bgs[1], bgs[1]])
        panel.lab_num.SetString(str(winning_streak))

        @panel.btn_goto.unique_callback()
        def OnClick(*args):
            tmp_ui = global_data.ui_mgr.show_ui('WinningStreakUI', 'logic.comsys.homeland')
            tmp_ui.set_winning_info(winning_info, uid, data)

        return panel

    def add_sys_msg(self, data, is_back_item=True, up_data=None):
        if is_back_item:
            chat = self._lv_chat.AddItem(self.chat_sys_temp, bRefresh=True)
        else:
            chat = self._lv_chat.AddItem(self.chat_sys_temp, 0, bRefresh=True)
        offset = 0
        time_rt_msg = None
        if data.get('is_show_time', False):
            time_str = '#BC%s</color>' % common.utilities.get_time_str_chat(data['time'])
            time_rt_msg = CCRichText.Create(time_str, 24, cc.Size(SVIEW_WHITH, 0))
            time_rt_msg.setAnchorPoint(cc.Vec2(0.5, 1.0))
            time_rt_msg.setHorizontalAlign(1)
            time_rt_msg.formatText()
            chat.AddChild(None, time_rt_msg)
            offset = time_rt_msg.getVirtualRendererSize().height
        msg_str = '#BC%s</color>' % data['msg']
        rt_msg = CCRichText.Create(msg_str, 20, cc.Size(SVIEW_WHITH, 0))
        rt_msg.setAnchorPoint(cc.Vec2(0.5, 0.5))
        rt_msg.setHorizontalAlign(1)
        rt_msg.formatText()
        chat.AddChild('msg', rt_msg)
        size = rt_msg.getVirtualRendererSize()
        rt_msg.SetPosition('50%0', '50%0')
        rt_width = self.get_max_line_width(rt_msg.getLineWidths())
        pnl_size = chat.getContentSize()
        bottom_height = size.height + RICHTEXT_CONTENT_EDGE * 2
        if bottom_height < pnl_size.height:
            bottom_height = pnl_size.height
        if time_rt_msg:
            time_rt_msg.SetPosition(SVIEW_WHITH * 0.5, bottom_height + offset)
        chat.SetContentSize(pnl_size.width, bottom_height + offset)
        return chat

    def add_voice_msg(self, data, is_back_item=True, up_data=None):
        data = self.censor_chat_data(data)
        if self._my_uid == data[U_ID]:
            conf = self.chat_me_voice
            anchor_x = 1.0
            align = 2
            scale = 1
            is_me = True
        else:
            conf = self.chat_friend_voice
            anchor_x = 0.0
            align = 0
            data['msg'] = '#SC%s</color>' % data['msg']
            scale = -1
            is_me = False
        chat, msg_pos, size, rt_width, time_msg_offset = self.make_chat_message(conf, is_back_item, data, anchor_x, align, is_me)
        if data.get('isread', 1) == 0:
            chat.img_redpoint.setVisible(True)
        else:
            chat.img_redpoint.setVisible(False)
        time, arm_key = data['voice'].split('\n', 1)
        time = float(time)

        @chat.btn_voice.callback()
        def OnClick(*args):
            global_data.voice_mgr.play_voice_msg(arm_key)
            if data.get('isread', 1) == 0:
                data['isread'] = 1
                chat.img_redpoint.setVisible(False)
                self._message_data.write_data(self._chat_uid)

        voice_width = VOICE_BAR_WIDTH * 0.4 + (time / 60.0) ** 0.5 * VOICE_BAR_WIDTH * 0.6
        if rt_width < voice_width + RICHTEXT_CONTENT_EDGE * 2:
            rt_width = voice_width + RICHTEXT_CONTENT_EDGE * 2
        chat.btn_voice.SetContentSize(voice_width, chat.btn_voice.getContentSize().height)
        chat.btn_voice.lab_time.SetPosition(voice_width / 2, chat.btn_voice.lab_time.getPosition().y)
        s = "%d''" % math.ceil(time)
        chat.btn_voice.lab_time.SetString(s)
        chat.btn_voice.img_icon.SetPosition(voice_width - 20, chat.btn_voice.img_icon.getPosition().y)
        if chat.img_redpoint.isVisible():
            pos = chat.img_redpoint.getPosition()
            red_point_size = chat.img_redpoint.getContentSize()
            chat.img_redpoint.setPosition(cc.Vec2(voice_width - red_point_size.width * 0.5, pos.y))
        self.adjust_chat_panel(chat, msg_pos, scale, rt_width, size, time_msg_offset)
        return chat

    def add_text_msg(self, data, is_back_item=True, up_data=None):
        data = self.censor_chat_data(data)
        if self._my_uid == data[U_ID]:
            conf = self.chat_me_temp
            anchor_x = 1.0
            align = 2
            scale = 1
            is_me = True
        else:
            if data.get('msg', '') and chat_utils.anti_spoofing_check(data['msg']) and not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel():
                self.panel.temp_tips_warnning.setVisible(True)
                self.panel.lv_chat.SetContentSize(650, 430)
            conf = self.chat_friend_temp
            anchor_x = 0.0
            align = 0
            data['msg'] = unpack_text(data['msg'])
            scale = -1
            is_me = False
        ret = self.make_chat_message(conf, is_back_item, data, anchor_x, align, is_me)
        if not ret:
            return None
        else:
            chat, msg_pos, size, rt_width, time_msg_offset = ret
            self.adjust_chat_panel(chat, msg_pos, scale, rt_width, size, time_msg_offset)
            return chat

    def make_chat_message(self, conf, is_back_item, data, anchor_x, align, is_me=True, color=None):
        from logic.gcommon.common_const import rank_const
        format_data = self._template_data[id(conf)]
        uid = data[U_ID]
        if is_back_item:
            chat = self._lv_chat.AddItem(conf, bRefresh=True)
        else:
            chat = self._lv_chat.AddItem(conf, 0, bRefresh=True)
        setattr(chat, 'uid', data[U_ID])
        from logic.gutils.chat_utils import load_chat_background
        load_chat_background(chat, data.get('chat_background', 0), is_me)
        time_msg_offset = 0
        time_rt_msg = None
        if data.get('is_show_time', False):
            time_str = '#BC%s</color>' % common.utilities.get_time_str_chat(data['time'])
            time_rt_msg = CCRichText.Create(time_str, 24, cc.Size(SVIEW_WHITH, 0))
            time_rt_msg.setAnchorPoint(cc.Vec2(0.5, 1.0))
            time_rt_msg.setHorizontalAlign(1)
            time_rt_msg.formatText()
            chat.AddChild(None, time_rt_msg)
            time_msg_offset = time_rt_msg.getVirtualRendererSize().height
            time_rt_msg.SetPosition(SVIEW_WHITH * 0.5, chat.getContentSize().height + time_msg_offset)
        if not global_data.player:
            return
        else:
            if is_me:
                name_str = global_data.player.get_name() if 1 else self._chat_char_name
                chat.lab_name.SetString(name_str)
                if is_me:
                    title_type = global_data.player.rank_use_title_type
                    rank_info = global_data.player.rank_use_title_dict.get(global_data.player.rank_use_title_type, None)
                    player_data = global_data.player.get_privilege_data()
                    default_color = '#BC'
                else:
                    default_color = '#SC'
                    player_data = self._message_data.get_player_simple_inf(uid)
                    player_data = player_data if player_data else {}
                    rank_use_title_dict = player_data.get('rank_use_title_dict', {})
                    title_type = rank_const.get_rank_use_title_type(rank_use_title_dict)
                    rank_info = rank_const.get_rank_use_title(rank_use_title_dict)
                logic.gutils.template_utils.init_rank_title(chat.temp_title, title_type, rank_info)
                channel = chat_const.CHAT_CHANNEL_NAME.get(chat_const.CHAT_FRIEND)
                wrapper_data = dict(data)
                wrapper_data.update({'channel': channel})
                chat.temp_head.SetSwallowTouch(False)
                self._player_info_manager.add_head_item_auto(chat.temp_head, uid, 0, wrapper_data, show_tips=True)
                self._player_info_manager.add_dan_info_item(chat.temp_tier, uid)
                role_head_utils.init_dan_info(chat.temp_tier, uid)
                role_head_utils.init_privilege_name_color_and_badge(chat.lab_name, chat.temp_head, player_data, '#BC')
                msg_pos = format_data['msg_pos']
                from logic.gutils.chat_utils import has_extra_msg
                content = has_extra_msg(data) or chat_link.linkstr_to_richtext(data['msg'])

                def touch_callback(msg, ele, touch, touch_event):
                    chat_link.link_touch_callback(msg)

                rt_msg = CCRichText.Create(content, 24, cc.Size(MSG_WEIGHT, 0))
                rt_msg.SetCallback(touch_callback)
                rt_msg.setVerticalAlign(30)
                rt_msg.setAnchorPoint(cc.Vec2(anchor_x, 1.0))
                rt_msg.setHorizontalAlign(0)
                rt_msg.formatText()
                rt_width = self.get_max_line_width(rt_msg.getLineWidths())
                offset_x = 0
                if align == 2:
                    offset_x = MSG_WEIGHT - rt_width
                chat.AddChild(None, rt_msg)
                size = rt_msg.getVirtualRendererSize()
                rt_msg.setPosition(cc.Vec2(msg_pos['x'] + offset_x, msg_pos['y']))
                privilege_font_color = COLOR_FONT
                priv_settings = player_data.get('priv_settings', {})
                priv_colorful_font = player_data.get('priv_colorful_font', False)
                if priv_colorful_font and priv_settings.get(const.PRIV_SHOW_COLORFUL_FONT, False):
                    rt_msg.SetColor(privilege_font_color)
                else:
                    rt_msg.SetColor(default_color)
                rt_msg.SetString(content)
                return (
                 chat, msg_pos, size, rt_width, time_msg_offset)
            content, size, content_width = self._add_extra_msg(data, is_me)
            if content:
                content.setPosition(cc.Vec2(msg_pos['x'], msg_pos['y']))
                chat.temp_bar.setVisible(False)
                chat.AddChild('content', content)
            if size is None:
                size = chat.getContentSize()
                content_width = size.width
            return (chat, msg_pos, size, content_width, time_msg_offset)
            return

    def adjust_chat_panel(self, chat, msg_pos, scale, rt_width, size, time_msg_offset):
        pnl_size = chat.getContentSize()
        img_item = None
        if getattr(chat, 'img_item'):
            img_item = chat.img_item
        elif getattr(chat, 'temp_bar'):
            img_item = chat.temp_bar.chat_bar
            img_item = chat.temp_bar
        if img_item:
            img_item_pos = img_item.getPosition()
            img_item_size = img_item.getContentSize()
            x_diff = img_item_pos.x - msg_pos['x']
            richtext_bottom_width = x_diff * scale + rt_width + RICHTEXT_CONTENT_EDGE + RICHTEXT_BOTTOM_TRIANGLE_WIDTH
            richtext_bottom_height = img_item_pos.y - msg_pos['y'] + size.height + RICHTEXT_CONTENT_EDGE
            img_item.setContentSize(cc.Size(richtext_bottom_width, richtext_bottom_height))
            bottom_height = pnl_size.height - img_item_size.height + richtext_bottom_height + RICHTEXT_CONTENT_EDGE
            img_item.ChildResizeAndPosition()
        else:
            bottom_height = pnl_size.height - msg_pos['y'] + size.height + RICHTEXT_CONTENT_EDGE
        if bottom_height < pnl_size.height:
            bottom_height = pnl_size.height
        chat.setContentSize(cc.Size(pnl_size.width, bottom_height))
        offset = bottom_height - pnl_size.height
        for child in chat.getChildren():
            pos = child.getPosition()
            child.setPosition(cc.Vec2(pos.x, pos.y + offset))

        if time_msg_offset != 0:
            chat.setContentSize(cc.Size(pnl_size.width, bottom_height + time_msg_offset))
        return

    def get_max_line_width(self, line_widths):
        max_width = None
        for width in line_widths:
            if not max_width:
                max_width = width
            elif max_width < width:
                max_width = width

        return max_width

    def reload_all_template_format(self):
        self.release_template_format()
        self.load_template_format()

    def load_template_format(self):
        self.chat_me_temp = global_data.uisystem.load_template('chat/chat_me_item')
        self.chat_friend_temp = global_data.uisystem.load_template('chat/chat_other_item')
        self.chat_sys_temp = global_data.uisystem.load_template('friend/chat_sys_item')
        self.chat_me_voice = global_data.uisystem.load_template('chat/voice_me_item')
        self.chat_friend_voice = global_data.uisystem.load_template('chat/voice_other_item')
        self.chat_lucky_lottery_temp = global_data.uisystem.load_template('chat/i_chat_pigeon_item_lucky_lottery')
        self.read_format_inf(self.chat_me_temp)
        self.read_format_inf(self.chat_friend_temp)
        self.read_format_inf(self.chat_me_voice)
        self.read_format_inf(self.chat_friend_voice)
        self.read_format_inf(self.chat_lucky_lottery_temp)

    def release_template_format(self):
        global_data.uisystem.unload_template('chat/chat_me_item')
        global_data.uisystem.unload_template('chat/chat_other_item')
        global_data.uisystem.unload_template('friend/chat_sys_item')
        global_data.uisystem.unload_template('chat/voice_me_item')
        global_data.uisystem.unload_template('chat/voice_other_item')
        global_data.uisystem.unload_template('chat/i_chat_pigeon_item_lucky_lottery')

    def set_visible(self, visible):
        self.panel.setVisible(visible)

    def is_right_visible(self):
        return self.panel.nd_right.isVisible()

    def check_sview(self):
        msg_count = len(self._cur_msg_data)
        self._sview_data_index = self._lv_chat.AutoAddAndRemoveItem_chat(self._sview_data_index, self._cur_msg_data, msg_count, self.add_msg, 300, 400)
        self._is_check_sview = False

    def panel_up_move(self, height):
        x, _ = self.main_panel.panel.GetPosition()
        self.main_panel.panel.SetPosition(x, self.save_nd_chat_pos_y + height)

    def panel_recover(self):
        x, _ = self.main_panel.panel.GetPosition()
        self.main_panel.panel.SetPosition(x, self.save_nd_chat_pos_y)
        self._chat_emote_ui = None
        return

    def hide_inputbox(self):
        if self._input_box:
            self._input_box.hide()

    def check_send_non_friend_msg(self, frd_uid):
        if not global_data.message_data.is_friend(frd_uid):
            if global_data.player.get_lv() < chat_const.SEND_NON_FRD_MSG_MIN_LV:
                global_data.game_mgr.show_tip(get_text_by_id(603015).format(lv=chat_const.SEND_NON_FRD_MSG_MIN_LV))
                return False
        return True

    def _add_extra_msg(self, data, is_me):
        msg_func_dict = {chat_const.MSG_TYPE_CLAN_CARD: self._make_clan_card_msg,
           chat_const.MSG_TYPE_SKIN_DEFINE: self._make_skin_define_msg,
           chat_const.MSG_TYPE_VIDEO_SHARE: self._make_video_share_msg,
           chat_const.MSG_TYPE_FRIEND_SEASON_MEMORY: self._make_friend_season_memory,
           chat_const.MSG_TYPE_LUCKY_LOTTERY: self._make_lucky_lottery_msg
           }
        extra_msg_type = data['extra'].get('type', None)
        if extra_msg_type in msg_func_dict:
            deal_func = msg_func_dict[extra_msg_type]
            return deal_func(data, is_me)
        else:
            return (None, None, None)
            return

    def _make_clan_card_msg(self, data, is_me):
        from logic.gutils.template_utils import init_clan_card_msg
        tem_name = 'chat/chat_crew_me_item' if is_me else 'chat/chat_crew_other_item'
        content = global_data.uisystem.load_template_create(tem_name)
        extra_data = data['extra']
        init_clan_card_msg(content, extra_data)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width)

    def _make_skin_define_msg(self, data, is_me):
        from logic.gutils.template_utils import init_skin_define_msg
        tem_name = 'chat/i_chat_define_me_item' if is_me else 'chat/i_chat_define_other_item'
        content = global_data.uisystem.load_template_create(tem_name)
        extra_data = data['extra']
        init_skin_define_msg(content, extra_data)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width)

    def _make_video_share_msg(self, data, is_me):
        from logic.gutils.template_utils import init_video_share_msg
        tem_name = 'chat/chat_video_me_item' if is_me else 'chat/chat_video_others_item'
        content = global_data.uisystem.load_template_create(tem_name)
        extra_data = data['extra']
        init_video_share_msg(content, extra_data, is_friend=True)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width)

    def _make_friend_season_memory(self, data, is_me):
        from logic.gutils.template_utils import init_friend_memory_msg
        tem_name = 'chat/chat_me_item_memory' if is_me else 'chat/chat_other_item_memory'
        content = global_data.uisystem.load_template_create(tem_name)
        extra_data = data['extra']
        msg_sender_uid = extra_data.get('sender_uid', '')
        msg_rev_uid = extra_data.get('rev_uid', '')
        if is_me:
            rev_uid = self._chat_uid
            rev_name = self._chat_char_name
            sender_uid = self._my_uid
            send_name = global_data.player.get_name()
        else:
            rev_uid = self._my_uid
            rev_name = global_data.player.get_name()
            sender_uid = self._chat_uid
            send_name = self._chat_char_name
        msg = data['msg']
        init_friend_memory_msg(content, extra_data, is_me, msg, rev_uid, rev_name, sender_uid, send_name)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width)

    def _make_lucky_lottery_msg(self, data, is_me):
        tem_name = 'chat/i_chat_pigeon_item_lucky_lottery_me' if is_me else 'chat/i_chat_pigeon_item_lucky_lottery_others'
        content = global_data.uisystem.load_template_create(tem_name)
        size = content.getContentSize()
        content_width = size.width
        extra_data = data.get('extra', {})
        item_list = extra_data.get('item_list', {})
        luck_score_extra_info = extra_data.get('extra_info', {})
        luck_score = luck_score_extra_info.get('luck_score')
        luck_intervene_weight = luck_score_extra_info.get('luck_intervene_weight')
        luck_exceed_percent = luck_score_extra_info.get('luck_exceed_percent')
        lottery_id = extra_data.get('lottery_id')
        player_data = {'uid': data.get('uid'),
           'name': data.get('char_name', ''),
           'frame_no': data.get('head_frame'),
           'photo_no': data.get('head_photo')
           }
        item_no = extra_data.get('item_no')
        if item_no == -1:
            nd = content.img_alpha
        else:
            item_type = get_lobby_item_type(item_no)
            show_item_no = item_no
            if item_type in (L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_MECHA):
                nd = content.nd_mech
                nd_img = content.nd_mech.img_skin
            elif item_type in (L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_ROLE):
                nd = content.nd_people
                nd_img = content.nd_people.img_skin
            elif item_type == L_ITME_TYPE_GUNSKIN:
                nd = nd_img = content.nd_weapon
            elif item_type == L_ITEM_TYPE_WEAPON_SFX:
                from logic.gutils.dress_utils import get_weapon_sfx_skin_show_mount_item_no
                mount_item_no = get_weapon_sfx_skin_show_mount_item_no(item_no)
                nd = content.nd_mech
                nd_img = content.nd_mech.img_skin
                show_item_no = mount_item_no
            else:
                nd = nd_img = content.nd_others
            nd_img.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(show_item_no))
        content.nd_mech.setVisible(False)
        nd.setVisible(True)
        if luck_score >= NORMAL_LUCK_SCORE_EDGE:
            content.nd.lab_msg.setString(get_text_by_id(634668))
        else:
            lottery_str = get_text_by_id(extra_data.get('text_id'))
            content.nd.lab_msg.setString(get_text_by_id(634669).format(activityname=lottery_str))
        lab_value_lucky = content.lab_value_lucky
        lab_value_lucky.setString(str(int(luck_score)))
        lab_rank = lab_value_lucky.nd_auto_fit.lab_rank
        if luck_intervene_weight:
            value = next(iter(luck_intervene_weight.values()))
            if value <= LOTTERY_COUNT_SHOW_BAODI:
                lab_rank.setString(get_text_by_id(634637).format(value))
                lab_rank.setVisible(True)
            elif value > LOTTERY_COUNT_SHOW_BAODI or luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
                lab_rank.setString(get_text_by_id(634753).format(luck_exceed_percent))
                lab_rank.setVisible(True)
            else:
                lab_rank.setVisible(False)
        elif luck_exceed_percent >= MIN_LUCK_SCORE_PERCENT:
            lab_rank.setString(get_text_by_id(634753).format(luck_exceed_percent))
            lab_rank.setVisible(True)
        else:
            lab_rank.setVisible(False)

        @content.btn_goto.unique_callback()
        def OnClick(*args):
            reward_list = [ reward_info for reward_info in six.itervalues(item_list) ]
            lottery_result_ui = LotteryResultUI(is_my=False)
            lottery_result_ui.set_box_items(reward_list, {}, luck_score_extra_info, lottery_id, player_data)

        return (
         content, size, content_width)

    def destroy(self):
        if self._chat_emote_ui:
            global_data.ui_mgr.close_ui('ChatEmote')
            self._chat_emote_ui = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        self.voice_operate.destroy()
        self._lv_chat.DeleteAllSubItem()
        global_data.emgr.message_receive_friend_msg -= self.refresh_one_msg
        global_data.emgr.player_join_team_event -= self.check_voice_btn_show
        global_data.emgr.player_leave_team_event -= self.check_voice_btn_show
        global_data.emgr.message_refresh_contact_group -= self.on_refresh_contact
        self.release_template_format()
        return