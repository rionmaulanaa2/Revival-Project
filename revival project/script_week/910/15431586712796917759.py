# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/MainChat.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
import time
import math
import copy
import common.const.uiconst
import logic.gutils.template_utils
import logic.gcommon.time_utility as tutil
import logic.comsys.common_ui.InputBox as InputBox
import logic.comsys.message.message_data as message_data
from cocosui import cc, ccui, ccs
from common.cfg import confmgr
from common.const.property_const import *
from common.uisys.uielment.CCRichText import CCRichText
from common.uisys.basepanel import BasePanel
from logic.comsys.chat import chat_link
from logic.gcommon.common_const import chat_const
from logic.gcommon.common_utils import text_utils
from logic.gcommon.common_const.team_const import TEAM_SUMMON_VALID_TIME
from logic.gcommon.common_utils.local_text import get_text_by_id, get_server_text
from logic.gutils.role_head_utils import PlayerInfoManager
from logic.gutils import role_head_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_type, get_lobby_chat_item_pic_by_item_no
from logic.gcommon.item.lobby_item_type import L_ITME_TYPE_GUNSKIN, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_WEAPON_SFX
from logic.gutils.mall_utils import get_lottery_id_from_name, check_speaker, get_lottery_turntable_item_data, get_lobby_item_name
from logic.gcommon.common_const.lang_data import *
from logic.gcommon.common_utils.local_text import get_cur_text_lang
from .TeamQuickChat import TeamQuickChat
from logic.gcommon.item.item_const import DEFAULT_HEAD_CHAT_FRAME
from logic.gcommon.item.item_const import DEFAULT_EMOTE_PACK
from logic.gcommon.item import item_const
from logic.gutils.item_utils import get_skin_rare_path_by_rare
from common.platform.dctool import interface
from logic.gutils import chat_utils
from logic.gutils.item_utils import get_item_rare_degree, get_rare_degree_name
from logic.gutils import item_utils
from exception_hook import post_stack
import re
from common.utils.ui_utils import calc_pos
from logic.gcommon.const import PRIV_SHOW_COLORFUL_FONT
from logic.gcommon.cdata.privilege_data import COLOR_FONT
from logic.gcommon.common_const.chat_const import winning_streak_bgs
from logic.gcommon.common_const.rank_const import get_rank_use_title_type, get_rank_use_title
from logic.gutils.red_packet_utils import init_chat_red_packet, get_red_packet_danmu_text, init_red_packet_cover_item, get_red_packet_info
from logic.comsys.red_packet.RedPacketUI import RedPacketUI
from logic.gcommon.common_const.red_packet_const import RED_PACKET_MESSAGE_NEW_PACKET, RED_PACKET_MESSAGE_DANMU, CAN_SEND_RED_PACKET_CHANNEL, RED_PACKET_MESSAGE_CLAIM
from logic.comsys.red_packet.ChatRedPacketSendUI import ChatRedPacketSendUI
from logic.gcommon.common_const.ui_operation_const import BAN_RED_PACKET_DAMMU
from logic.comsys.lottery.LotteryNew.LotteryResultUI import LotteryResultUI
from logic.gcommon.cdata.luck_score_config import NORMAL_LUCK_SCORE_EDGE, MIN_LUCK_SCORE_PERCENT, LOTTERY_COUNT_SHOW_BAODI
from logic.gcommon.common_const.red_packet_const import PRIV_RED_PACKET
from logic.gcommon.common_const.battle_const import PLAY_TYPE_PVE, PLAY_TYPE_PVE_EDIT, DEFAULT_DEATH_TID, DEFAULT_BATTLE_TID, DEFAULT_PVE_TID
from logic.gcommon.common_const.pve_const import DIFFICULTY_TEXT_LIST
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_utils.battle_utils import get_mode_name
chat_stage_hide = 0
chat_stage_open = 1
chat_stage_moving = 2
RICHTEXT_CONTENT_EDGE = 17
RICHTEXT_BOTTOM_TRIANGLE_WIDTH = 2
RICHTEXT_CONTENT_WIDTH = 450
MaxLength = 50
VOICE_BAR_WIDTH = 300
auto_img_n_path = 'gui/ui_res_2/common/button/btn_multi_select_n.png'
auto_img_s_path = 'gui/ui_res_2/common/button/btn_multi_select_s.png'
UI_WORLD_INDEX = 0
UI_TEAM_INDEX = 1
UI_CLAN_INDEX = 2
UI_ROOM_INDEX = 3
UI_SYS_INDEX = 4
UI_PIGEON_INDEX = 5
UI_VISIT_INDEX = 6
UI_ROOM_SHARE_INDEX = 7
TAB_INDEX_TO_CHANNEL = {UI_WORLD_INDEX: (
                  chat_const.CHAT_WORLD, 11004),
   UI_TEAM_INDEX: (
                 chat_const.CHAT_TEAM, 11005),
   UI_CLAN_INDEX: (
                 chat_const.CHAT_CLAN, 800001),
   UI_ROOM_INDEX: (
                 chat_const.CHAT_ROOM, 80634),
   UI_SYS_INDEX: (
                chat_const.CHAT_SYS, 11007),
   UI_PIGEON_INDEX: (
                   chat_const.CHAT_PIGEON, 11051),
   UI_VISIT_INDEX: (
                  chat_const.CHAT_VISIT, 611571),
   UI_ROOM_SHARE_INDEX: (
                       chat_const.CHAT_ROOM_SHARE, 80634)
   }
TAB_CHANNEL_TO_INDEX = {ch[0]:idx for idx, ch in six.iteritems(TAB_INDEX_TO_CHANNEL)}
VALID_CHANNEL = {ch[0] for ch in six.itervalues(TAB_INDEX_TO_CHANNEL)}
CHANNEL_INDEX_TO_CHANNEL_CHN_NAME = {chat_const.CHAT_WORLD: '\xe4\xb8\x96\xe7\x95\x8c',
   chat_const.CHAT_TEAM: '\xe9\x98\x9f\xe4\xbc\x8d',
   chat_const.CHAT_CLAN: '\xe6\x9c\xba\xe5\x8a\xa8\xe5\x9b\xa2',
   chat_const.CHAT_ROOM: '\xe6\x88\xbf\xe9\x97\xb4',
   chat_const.CHAT_SYS: '\xe7\xb3\xbb\xe7\xbb\x9f',
   chat_const.CHAT_PIGEON: '\xe5\xa4\xa7\xe5\x96\x87\xe5\x8f\xad',
   chat_const.CHAT_VISIT: '\xe5\xae\xb6\xe5\x9b\xad',
   chat_const.CHAT_ROOM_SHARE: '\xe6\x88\xbf\xe9\x97\xb4\xe5\x88\x86\xe4\xba\xab'
   }
FILTER_FIGHT_MODES = [
 0,
 DEFAULT_PVE_TID,
 DEFAULT_DEATH_TID,
 DEFAULT_BATTLE_TID]
ALL_LANG_ROOM_LIST = [
 (
  chat_const.CHAT_WORLD_EN, 81036),
 (
  chat_const.CHAT_WORLD_TW, 11076),
 (
  chat_const.CHAT_WORLD_JP, 81035),
 (
  chat_const.CHAT_WORLD_TH, 11077),
 (
  chat_const.CHAT_WORLD_ID, 11078),
 (
  chat_const.CHAT_WORLD_KO, 11079),
 (
  chat_const.CHAT_WORLD_OTHER, 11080)]
LANG_TO_ROOM_MAP = {LANG_CN: chat_const.CHAT_WORLD_TW,
   LANG_EN: chat_const.CHAT_WORLD_EN,
   LANG_ZHTW: chat_const.CHAT_WORLD_TW,
   LANG_JA: chat_const.CHAT_WORLD_JP,
   LANG_KO: chat_const.CHAT_WORLD_KO,
   LANG_TH: chat_const.CHAT_WORLD_TH,
   LANG_ID: chat_const.CHAT_WORLD_ID
   }
CHANGE_LANG_ROOM_CD = 10.0
CHANGE_MATCH_MODE_CD = 1.0
FONT_COLOR_IDX = 2
ID_COLOR_IDX = 1
richtext_pattern = re.compile('<(.*?)>')
enable_patterns = [
 re.compile('<emote=\\d{5,6},1>')]
TEXT_INPUT_BOX_MAX_LEN = 50
TEXT_INPUT_BOX_MAX_LEN_JUDGEMENT = 150

def check_show_msg(text):
    replace_strs = []
    all_msg = richtext_pattern.findall(text)
    for msg in all_msg:
        new_msg = '<' + msg + '>'
        for sub_pattern in enable_patterns:
            if sub_pattern.match(new_msg) is not None:
                replace_strs.append(msg)
                break

    text = text.replace('<', '\xef\xbc\x9c')
    text = text.replace('>', '\xef\xbc\x9e')
    for rp_str in replace_strs:
        old_str = '\xef\xbc\x9c' + rp_str + '\xef\xbc\x9e'
        new_str = '<' + rp_str + '>'
        text = text.replace(old_str, new_str)

    return text


class MainChat(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    PANEL_CONFIG_NAME = 'chat/main_chat'
    UI_ACTION_EVENT = {'btn_chat.OnClick': 'on_main_chat_ui'
       }
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    GLOBAL_EVENT = {'on_switch_scene_capture_event': 'switch_lobby_scene_capture',
       'player_item_update_event': 'on_item_update',
       'show_top_chat_pigeon': '_show_top_chat_pigeon',
       'on_refresh_red_packet_info': 'on_refresh_red_packet_info',
       'claim_red_packet_succeed': 'on_claim_red_packet_succeed',
       'send_red_packet_succeed': 'on_send_red_packet_succeed',
       'on_open_pve_main_ui': 'on_open_pve_main_ui',
       'on_close_pve_main_ui': 'on_close_pve_main_ui',
       'player_underage_mode_changed_event': 'underage_mode_changed'
       }

    def on_init_panel(self, *args, **kargs):
        self._emote_dict = confmgr.get('emote', 'emote')
        self._chat_emote_info = confmgr.get('chat_emoji', default={})
        self._my_uid = global_data.player.uid
        self._message_data = global_data.message_data
        self.top_chat_pigeon_show = False
        self.top_chat_pigeon_msg_data = None
        self._touch_children_list = {}
        self._need_block_all_click = False
        self._need_show_btn = True
        self._need_show_btn_list = [
         self.panel.btn_chat, self.panel.btn_emote,
         self.panel.btn_red_packet, self.panel.btn_speaker_2]
        self._message_data.set_main_chat_ui(self)
        self._cur_msg_data = []
        self._sview_data_index = 0
        self._is_msg_lock = False
        self._unread_msg_count = 0
        self._player_info_manager = PlayerInfoManager()
        self._lv_chat = self.panel.lv_chat
        self.init_touch_event()
        self.release_template_format()
        self.init_template_format()
        self.init_top_chat_pigeon()
        self._chat_width = self.panel.layer_chat.getContentSize().width
        self._widget_pos = self.panel.layer_chat.getPosition()
        self._chat_pnl_stage = chat_stage_hide
        self.panel.layer_chat.setPosition(cc.Vec2(self._widget_pos.x - self._chat_width, self._widget_pos.y))
        self.panel.layer_chat.setVisible(False)
        self._is_chat_open = False
        self._channel_index = -1
        self._tab_index = -1
        self._btn_tab = {}
        self._is_check_sview = False
        self._channel_redpoint_map = {channel:0 for channel in six_ex.keys(CHANNEL_INDEX_TO_CHANNEL_CHN_NAME)}
        self._last_send_time = time.time()
        self._chat_record_ui = None
        self.is_btn_voice_touch = True
        self._input_box = None
        self._speaker_input_box = None
        self._rich_test = None
        self._is_auto_voice = self._message_data.get_seting_inf('auto_voice')
        self.update_auto_voice_data_structure()
        self._auto_voice_list = []
        self._unplay_voice = set()
        self._voice_key_to_widget = {}
        self._last_change_lang_room_time = 0.0
        self._cur_match_battle_type_filter = 0
        self._last_change_match_mode_time = 0.0
        self._tab_index_list = six_ex.keys(TAB_INDEX_TO_CHANNEL)
        self._preview_tab_channel = None
        self._default_tab_index = UI_WORLD_INDEX
        self._team_quick_chat = None
        x = self.panel.layer_chat.getContentSize().width + 20
        y = self.panel.getContentSize().height - 20
        self._player_simple_inf_pos = cc.Vec2(x, y)
        self._cur_red_packet_info = {}
        self._ban_red_packet_dammu = False
        if global_data.achi_mgr.get_cur_user_archive_data(BAN_RED_PACKET_DAMMU, False) or global_data.player and global_data.player.get_setting_2(BAN_RED_PACKET_DAMMU):
            self._ban_red_packet_dammu = True
        self.refresh_red_packet_ban_dammu()
        self.panel.btn_red_packet.temp_reddot.setVisible(not global_data.achi_mgr.get_cur_user_archive_data('ban_red_packet_dammu_red_point', False))
        self.send_red_packet_widget = ChatRedPacketSendUI(self.panel.temp_red_packet, self._channel_index)

        @self.panel.temp_red_packet.nd_touch.callback()
        def OnClick(*args):
            if self.send_red_packet_widget and self.send_red_packet_widget.get_is_visible():
                self.panel.PlayAnimation('hide_red_packet')
                return

        @self.panel.callback()
        def OnClick(*args):
            if self.send_red_packet_widget and self.send_red_packet_widget.get_is_visible():
                self.panel.PlayAnimation('hide_red_packet')
                return
            self.chat_close()
            self.refresh_team_quick_chat()
            self.refresh_base_panel_touch_status()

        @self.panel.layer_chat.btn_back.callback()
        def OnClick(*args):
            if self.send_red_packet_widget and self.send_red_packet_widget.get_is_visible():
                self.panel.PlayAnimation('hide_red_packet')
            self.chat_close()
            self.refresh_base_panel_touch_status()

        self.panel.layer_chat.img_bg.btn_top.setVisible(False)

        @self.panel.layer_chat.img_bg.btn_top.callback()
        def OnClick(*args):
            self.panel.layer_chat.img_bg.btn_top.setVisible(False)
            self.change_channel()

        @self.panel.btn_speaker_2.callback()
        def OnClick(*args):
            if check_speaker():
                ui = global_data.ui_mgr.show_ui('ChatPigeonInput', 'logic.comsys.chat')
                ui._input_box.on_input_change(self._input_box.get_text())

        self.underage_mode_changed()

        @self.panel.btn_red_packet.callback()
        def OnClick(*args):
            if self.send_red_packet_widget and self.send_red_packet_widget.get_is_visible():
                self.panel.PlayAnimation('hide_red_packet')
            else:
                from logic.comsys.setting_ui.UnderageHelper import is_in_underage_mode
                if is_in_underage_mode():
                    global_data.game_mgr.show_tip(get_text_by_id(635260))

                    def click_goto():
                        from logic.gutils import jump_to_ui_utils
                        jump_to_ui_utils.jump_to_underage_mode_btn()

                    SecondConfirmDlg2().confirm(content=get_text_by_id(635270), confirm_callback=click_goto)
                    return
            if self._channel_index in CAN_SEND_RED_PACKET_CHANNEL:
                self.panel.PlayAnimation('show_red_packet')
            global_data.achi_mgr.set_cur_user_archive_data('ban_red_packet_dammu_red_point', True)
            self.panel.btn_red_packet.temp_reddot.setVisible(not global_data.achi_mgr.get_cur_user_archive_data('ban_red_packet_dammu_red_point', False))

        def scroll_callback(sender, eventType):
            if not self.is_in_touch:
                return
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.SetTimeOut(0.021, self.check_sview)
            in_height = sender.getInnerContainerSize().height
            out_height = sender.getContentSize().height
            if in_height != out_height:
                posy = sender.getInnerContainer().getPositionY()
                if posy > 0 and self._sview_data_index == len(self._cur_msg_data) - 1:
                    self._is_msg_lock = False
                    self._unread_msg_count = 0
                    self.set_btn_lock(self._is_msg_lock)
                    self.panel.layer_chat.img_bg.btn_top.setVisible(False)
                elif posy < 0:
                    self._is_msg_lock = True
                    self.set_btn_lock(self._is_msg_lock)

        self._lv_chat.addEventListener(scroll_callback)
        self.init_botom()
        self.init_left()
        self.init_top()
        self.init_team_chat_quick()
        self.refresh_base_panel_touch_status()
        self.on_item_update()
        def_txt = get_text_by_id(11001)
        self.panel.lab_chat.SetString(def_txt)
        self.panel.lab_chat.setEnableFontSizeAutoShrink(False, 12)
        global_data.emgr.chat_add_channel_msg += self.on_add_channel_msg
        global_data.emgr.chat_add_channel_msg += self.on_add_msg
        global_data.emgr.chat_history_msg += self.on_history_msg
        global_data.emgr.message_receive_self_msg += self.clean_input_box_msg
        global_data.emgr.chat_voice_empty += self.on_voice_empty
        global_data.emgr.player_join_team_event += self.on_team_change
        global_data.emgr.player_leave_team_event += self.on_team_change
        global_data.emgr.player_join_team_event += self.check_voice_btn_show
        global_data.emgr.player_leave_team_event += self.check_voice_btn_show
        global_data.emgr.create_clan_success += self._success_in_clan
        global_data.emgr.create_join_success += self._success_in_clan
        global_data.emgr.need_show_room_ui_event += self.init_left
        global_data.emgr.leave_custom_room += self.init_left
        global_data.emgr.on_show_room_ui_event += self.adjust_text_input_box_length
        global_data.emgr.leave_custom_room += self.reset_text_input_box_length
        global_data.emgr.refresh_item_red_point += self.update_chat_emote_rp
        global_data.emgr.update_lobby_puppet_count += self.update_lobby_puppet_count
        if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
            self.panel.temp_tips_warnning.setVisible(False)
        return

    def on_item_update(self, *args):
        if not global_data.player:
            return
        item_amount = global_data.player.get_item_num_by_no(chat_const.CHAT_PIGEON_COST_ITEM_NO)
        self.panel.btn_speaker_2.lab_speaker_num.SetString(str(item_amount))
        self.panel.nd_speaker_input.lab_speaker_num.SetString(str(item_amount))
        self.panel.speaker_btn_send.btn_common.SetShowEnable(item_amount > 0)

    def init_top_chat_pigeon(self):
        self.panel.top_chat_pigeon.setVisible(False)
        self.panel.top_chat_pigeon.lab_msg.setEnableFontSizeAutoShrink(False, 18)
        if self.panel.top_red_packet_pigeon:
            self.panel.top_red_packet_pigeon.setVisible(False)
            self.panel.top_chat_pigeon.lab_msg.setEnableFontSizeAutoShrink(False, 18)

    def _show_top_chat_pigeon(self, show, msg_data=None, is_change_channel=False):
        if not msg_data:
            return
        self.top_chat_pigeon_show = show
        self.top_chat_pigeon_msg_data = msg_data
        if msg_data['pigeon_type'] == chat_const.PIGEON_NORMAL:
            self.init_normal_top_pigeon(is_change_channel)
        elif msg_data['pigeon_type'] == chat_const.PIGEON_RED_PACKET:
            self.init_red_packet_top_pigeon(is_change_channel)

    def init_normal_top_pigeon(self, is_change_channel=False):
        top_chat_pigeon = self.panel.top_chat_pigeon
        top_chat_pigeon.StopAnimation('show')
        top_chat_pigeon.StopAnimation('show_01')
        top_chat_pigeon.StopAnimation('disappear')
        if not top_chat_pigeon:
            return
        else:
            if self._channel_index != chat_const.CHAT_WORLD:
                top_chat_pigeon.setVisible(False)
                return
            if self.top_chat_pigeon_show:
                top_chat_pigeon.setVisible(True)
                if is_change_channel:
                    top_chat_pigeon.PlayAnimation('show_01')
                else:
                    top_chat_pigeon.PlayAnimation('show')
                sender_info = self.top_chat_pigeon_msg_data.get('sender_info', None)
                if sender_info:
                    top_chat_pigeon.lab_name.SetString('[%s]:' % sender_info[C_NAME])
                    top_chat_pigeon.lab_msg.SetString(get_server_text(self.top_chat_pigeon_msg_data['msg']))
                    uid = sender_info.get(U_ID, 0)
                    self._player_info_manager.add_head_item_auto(top_chat_pigeon.temp_head, uid, 0, sender_info)
                else:
                    top_chat_pigeon.lab_name.SetString('')
                    top_chat_pigeon.lab_msg.SetString(get_server_text(self.top_chat_pigeon_msg_data['msg']))
            else:
                top_chat_pigeon.PlayAnimation('disappear')
                delay = self.panel.GetAnimationMaxRunTime('disappear')

                def _hide():
                    top_chat_pigeon.setVisible(False)

                top_chat_pigeon.SetTimeOut(delay, _hide)
            return

    def init_red_packet_top_pigeon(self, is_change_channel=False):
        top_chat_pigeon = self.panel.top_red_packet_pigeon
        top_chat_pigeon.StopAnimation('show')
        top_chat_pigeon.StopAnimation('show_01')
        top_chat_pigeon.StopAnimation('disappear')
        top_chat_pigeon.StopAnimation('hongbaotishi_loop')
        top_chat_pigeon.StopAnimation('loop_fire')
        if not top_chat_pigeon:
            return
        else:
            if self._channel_index != chat_const.CHAT_WORLD:
                top_chat_pigeon.setVisible(False)
                return
            if self.top_chat_pigeon_show:
                top_chat_pigeon.setVisible(True)
                if is_change_channel:
                    top_chat_pigeon.PlayAnimation('show_01')
                else:
                    top_chat_pigeon.PlayAnimation('show')
                top_chat_pigeon.PlayAnimation('hongbaotishi_loop')
                sender_info = self.top_chat_pigeon_msg_data.get('sender_info', None)
                if sender_info:
                    top_chat_pigeon.lab_name.SetString('[%s]:' % sender_info[C_NAME])
                    top_chat_pigeon.lab_msg.SetString(get_server_text(self.top_chat_pigeon_msg_data['msg']))
                    uid = sender_info.get(U_ID, 0)
                    self._player_info_manager.add_head_item_auto(top_chat_pigeon.temp_head, uid, 0, sender_info)
                    red_packet_info = sender_info.get('red_packet_info', {})
                    coin_type = red_packet_info.get('coin_type', 3)
                    red_packet_type_info = get_red_packet_info(coin_type)
                    if coin_type == PRIV_RED_PACKET:
                        top_chat_pigeon.PlayAnimation('loop_fire')
                        top_chat_pigeon.lab_msg.SetString(get_text_by_id(634768).format(sender_info[C_NAME], '<color=00F6FFFF> {} </color>'.format(get_text_by_id(red_packet_type_info.get('text_id')))))
                    else:
                        top_chat_pigeon.lab_msg.SetString(get_text_by_id(634391).format(sender_info[C_NAME], '<color=00F6FFFF> {} </color>'.format(get_text_by_id(red_packet_type_info.get('text_id')))))
                    top_chat_pigeon.icon_gender.setVisible(False)
                    role_head_utils.set_role_dan(top_chat_pigeon.temp_tier, sender_info.get('dan_info'))
                    init_red_packet_cover_item(top_chat_pigeon.temp_item, red_packet_info.get('extra_info', {}).get('skin_id', 80000001))
                    top_chat_pigeon.nd_red_packet.BindMethod('OnClick', lambda btn, touch, pid=red_packet_info.get('pid', -1): self.on_open_choose_red_packet(pid))
                else:
                    top_chat_pigeon.nd_red_packet.UnBindMethod('OnClick')
                    top_chat_pigeon.lab_name.SetString('')
                    top_chat_pigeon.lab_msg.SetString(get_server_text(self.top_chat_pigeon_msg_data['msg']))
            else:
                top_chat_pigeon.nd_red_packet.UnBindMethod('OnClick')
                top_chat_pigeon.PlayAnimation('disappear')
                delay = self.panel.GetAnimationMaxRunTime('disappear')

                def _hide():
                    top_chat_pigeon.setVisible(False)

                top_chat_pigeon.SetTimeOut(delay, _hide)
            return

    def init_top(self):
        self._cur_channel_btn_tab = None
        self._cur_mode_btn_tab = None

        @self.panel.btn_invite.callback()
        def OnClick(*args):
            from logic.comsys.lobby.TeamHall import TeamReleaseUI

            def callback():
                self.touch_channel_btn(chat_const.CHAT_TEAM)

            ui = TeamReleaseUI.TeamReleaseUI(None)
            ui.set_send_callback(callback)
            return

        self.panel.btn_invite.SetSwallowTouch(False)
        self.init_fight_mode_filter()

        @self.panel.btn_change_chat_frame.callback()
        def OnClick(*args):
            from logic.comsys.role.ChangeHeadUI import ChangeHeadUI
            ChangeHeadUI(tab_index=2)

        self.panel.btn_change_chat_frame.SetSwallowTouch(False)

        @self.panel.node_voice.callback()
        def OnClick(*args):
            self._is_auto_voice[self._channel_index] = 0 if self._is_auto_voice[self._channel_index] else 1
            self._message_data.set_seting_inf('auto_voice', copy.copy(self._is_auto_voice))
            self.refresh_auto_img_state()

        self.panel.temp_channel.channel_list.DeleteAllSubItem()
        for room_info in ALL_LANG_ROOM_LIST:
            btn_tab = self.panel.temp_channel.channel_list.AddTemplateItem()
            self.add_room_btn(btn_tab, room_info)

        @self.panel.btn_channel.callback()
        def OnClick(*args):
            visible = self.panel.temp_channel.isVisible()
            self.panel.temp_channel.setVisible(not visible)
            self.panel.img_icon.setRotation(0 if visible else 180)

        @self.panel.temp_channel.out_side_nd.callback()
        def OnClick(*args):
            self.panel.temp_channel.setVisible(False)

        @self.panel.temp_red_packet.node_ban_msg.callback()
        def OnClick(*args):
            self._ban_red_packet_dammu = True if self._ban_red_packet_dammu == False else False
            global_data.achi_mgr.set_cur_user_archive_data(BAN_RED_PACKET_DAMMU, self._ban_red_packet_dammu)
            if global_data.player:
                global_data.player.write_setting_2(BAN_RED_PACKET_DAMMU, self._ban_red_packet_dammu, True)
            self.refresh_red_packet_ban_dammu()

        @self.panel.temp_red_packet.btn_describe.callback()
        def OnClick(*args):
            dlg = global_data.ui_mgr.show_ui('GameDescCenterUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(634463), get_text_by_id(634462))

        return

    def init_fight_mode_filter(self):

        @self.panel.btn_mode.callback()
        def OnClick(*args):
            visible = self.panel.temp_mode.isVisible()
            self.show_mode_tap(not visible)

        self.panel.btn_mode.SetSwallowTouch(False)
        self.panel.temp_mode.channel_list.DeleteAllSubItem()
        for battle_type in FILTER_FIGHT_MODES:
            btn_item = self.panel.temp_mode.channel_list.AddTemplateItem()
            self.add_mode_filtr_item(btn_item, battle_type)

    def show_mode_tap(self, visible):
        if self.panel.temp_mode and self.panel.btn_mode:
            self.panel.temp_mode.setVisible(visible)
            self.panel.btn_mode.img_icon.setRotation(180 if visible else 0)

    def filter_team_mode(self):
        for btn_tab in self.panel.temp_mode.channel_list.GetAllItem():
            if btn_tab.data_channel_room == self._cur_channel_room:
                btn_tab.btn_mode.SetSelect(True)
            else:
                btn_tab.btn_mode.SetSelect(False)

    def add_mode_filtr_item(self, btn_item, battle_type):
        mode_str = get_text_by_id(900022) if battle_type == 0 else get_mode_name(battle_type)
        btn_item.btn_channel.SetText(mode_str)
        btn_item.lab_num.setVisible(False)

        @btn_item.btn_channel.callback()
        def OnClick(btn, touch, _battle_type=battle_type):
            self.panel.btn_mode.img_icon.setRotation(0)
            self.panel.temp_mode.setVisible(False)
            now = time.time()
            if now - self._last_change_match_mode_time > CHANGE_MATCH_MODE_CD:
                _mode_str = get_text_by_id(900022) if _battle_type == 0 else get_mode_name(_battle_type)
                self._last_change_match_mode_time = now
                self.panel.btn_mode.SetText(_mode_str)
                if self._cur_mode_btn_tab:
                    self._cur_mode_btn_tab.btn_channel.SetSelect(False)
                self._cur_mode_btn_tab = btn_item
                self._cur_mode_btn_tab.btn_channel.SetSelect(True)
                self._cur_match_battle_type_filter = _battle_type
                self.change_channel()
            else:
                global_data.game_mgr.show_tip(get_text_by_id(11081, (int(CHANGE_MATCH_MODE_CD - (now - self._last_change_match_mode_time)),)))

        if battle_type == 0:
            OnClick(btn_item.btn_channel, None, battle_type)
        return

    def add_room_btn(self, btn_tab, room_data):
        btn_tab.btn_channel.SetText(get_text_by_id(room_data[1]))
        btn_tab.lab_num.setVisible(False)

        @btn_tab.btn_channel.callback()
        def OnClick(*args):
            self.panel.img_icon.setRotation(0)
            self.panel.temp_channel.setVisible(False)
            now = time.time()
            if now - self._last_change_lang_room_time > CHANGE_LANG_ROOM_CD:
                self._last_change_lang_room_time = now
                global_data.player.req_switch_world_chat_lang(room_data[0])
                self.panel.btn_channel.SetText(get_text_by_id(room_data[1]))
                if self._cur_channel_btn_tab:
                    self._cur_channel_btn_tab.btn_channel.SetSelect(False)
                self._cur_channel_btn_tab = btn_tab
                self._cur_channel_btn_tab.btn_channel.SetSelect(True)
            else:
                global_data.game_mgr.show_tip(get_text_by_id(11081, (int(CHANGE_LANG_ROOM_CD - (now - self._last_change_lang_room_time)),)))

        cur_channel_room = LANG_TO_ROOM_MAP.get(get_cur_text_lang(), chat_const.CHAT_WORLD_OTHER)
        if cur_channel_room == room_data[0]:
            OnClick()

    def refresh_channel_room_status(self):
        for btn_tab in self.panel.temp_channel.channel_list.GetAllItem():
            if btn_tab.data_channel_room == self._cur_channel_room:
                btn_tab.btn_channel.SetSelect(True)
            else:
                btn_tab.btn_channel.SetSelect(False)

    def init_team_chat_quick(self):
        self._team_quick_chat = TeamQuickChat(self)
        self._team_quick_chat.set_visible(False)
        self.panel.btn_chat_quick.SetSelect(False)
        self.panel.btn_chat_quick.setVisible(global_data.player.is_in_team())

        @self.panel.btn_chat_quick.callback()
        def OnClick(*args):
            flag = self._team_quick_chat.is_visible()
            self._team_quick_chat.set_visible(not flag)
            self.panel.btn_chat_quick.SetSelect(not flag)
            self.refresh_base_panel_touch_status()

    def release_template_format(self):
        global_data.uisystem.unload_template('chat/chat_me_item')
        global_data.uisystem.unload_template('chat/chat_other_item')
        global_data.uisystem.unload_template('chat/voice_me_item')
        global_data.uisystem.unload_template('chat/voice_other_item')
        global_data.uisystem.unload_template('chat/sys_item')
        global_data.uisystem.unload_template('chat/speaker_me_item')
        global_data.uisystem.unload_template('chat/speaker_other_item')

    def init_template_format(self):
        self.chat_me_temp = global_data.uisystem.load_template('chat/chat_me_item', force_json=True)
        self.chat_other_temp = global_data.uisystem.load_template('chat/chat_other_item', force_json=True)
        self.voice_me_temp = global_data.uisystem.load_template('chat/voice_me_item', force_json=True)
        self.voice_other_temp = global_data.uisystem.load_template('chat/voice_other_item', force_json=True)
        self.sys_item_temp = global_data.uisystem.load_template('chat/sys_item', force_json=True)
        self.speaker_chat_me_temp = global_data.uisystem.load_template('chat/speaker_me_item', force_json=True)
        self.speaker_chat_other_temp = global_data.uisystem.load_template('chat/speaker_other_item', force_json=True)
        self.redpacket_me_temp = global_data.uisystem.load_template('chat/red_packet/i_chat_red_packet_me_item', force_json=True)
        self.redpacket_other_temp = global_data.uisystem.load_template('chat/red_packet/i_chat_red_packet_other_item', force_json=True)
        self.redpacket_open = global_data.uisystem.load_template('chat/red_packet/i_chat_red_packet_got_info', force_json=True)
        self.anti_spoofing = global_data.uisystem.load_template('chat/i_chat_tips_warnning', force_json=True)
        self._template_data = {}
        self.read_format_inf(self.chat_me_temp)
        self.read_format_inf(self.chat_other_temp)
        self.read_format_inf(self.voice_me_temp)
        self.read_format_inf(self.voice_other_temp)
        self.read_format_inf(self.sys_item_temp)
        self.read_format_inf(self.speaker_chat_me_temp)
        self.read_format_inf(self.speaker_chat_other_temp)
        self.read_format_inf(self.redpacket_me_temp)
        self.read_format_inf(self.redpacket_other_temp)
        self.read_format_inf(self.redpacket_open)
        self.special_temp_conf = {}

    def check_voice_btn_show(self, *args):
        from common.audio.ccmini_mgr import LOBBY_TEAM_SPEAKER, LOBBY_TEAM_MIC
        flag = global_data.player and global_data.player.is_in_team() and global_data.message_data.get_seting_inf(LOBBY_TEAM_MIC)
        self.panel.btn_voice.setVisible(not flag)

    def get_special_temp_conf(self, file_name):
        temp_conf = self.special_temp_conf.get(file_name, None)
        if not temp_conf:
            temp_conf = global_data.uisystem.load_template('chat/%s' % file_name)
            self.special_temp_conf[file_name] = temp_conf
        return temp_conf

    def read_format_inf(self, template):
        data = {}
        data['size'] = template['size']
        data['msg_pos'] = {'x': 0,'y': 0}
        data['voice_pos'] = {'x': 0,'y': 0}
        remove_child = None
        for child in template['child_list']:
            if child.get('name') == 'lab_msg':
                pos = child['pos']
                pos['x'] = calc_pos(pos['x'], data['size']['width'])
                pos['y'] = calc_pos(pos['y'], data['size']['height'])
                data['msg_pos'] = pos
                data['color'] = child.get('color', '#SW')
                remove_child = child
            elif child.get('name') == 'btn_voice':
                pos = child['pos']
                pos['x'] = calc_pos(pos['x'], data['size']['width'])
                pos['y'] = calc_pos(pos['y'], data['size']['height'])
                data['voice_pos'] = pos

        if remove_child:
            template['child_list'].remove(remove_child)
        self._template_data[id(template)] = data
        return

    def init_left(self):
        self._btn_tab = {}
        lv_tab = self.panel.nd_left.tab_list
        lv_tab.DeleteAllSubItem()
        self._tab_index_list = six_ex.keys(TAB_INDEX_TO_CHANNEL)
        tmp_player = global_data.player
        if tmp_player and tmp_player.is_in_room():
            self._default_tab_index = UI_ROOM_INDEX
            self._preview_tab_channel = chat_const.CHAT_ROOM
            self._tab_index_list.pop(UI_ROOM_SHARE_INDEX)
        else:
            if UI_ROOM_INDEX in self._tab_index_list:
                self._tab_index_list.remove(UI_ROOM_INDEX)
            if UI_ROOM_SHARE_INDEX not in self._tab_index_list:
                self._tab_index_list.append(UI_ROOM_SHARE_INDEX)
            self._default_tab_index = UI_WORLD_INDEX
            self._preview_tab_channel = None
        lobby_puppet_count = len(tmp_player.get_all_lobby_puppet())
        if not tmp_player or not tmp_player.is_in_visit_mode() or lobby_puppet_count < 1:
            if UI_VISIT_INDEX in self._tab_index_list:
                self._tab_index_list.remove(UI_VISIT_INDEX)
        self._tab_index_list.sort()
        for tab_index in self._tab_index_list:
            btn_tab = lv_tab.AddTemplateItem()
            self._btn_tab[tab_index] = btn_tab
            channel_type, text_id = TAB_INDEX_TO_CHANNEL[tab_index]
            btn_tab.lab_main.setString(get_text_by_id(text_id))
            btn_tab.lab_main.SetColor('#DD')
            self.add_channel_btn(tab_index, btn_tab)

        self.touch_channel_btn(self._default_tab_index, False)
        self._tab_index = self._default_tab_index
        self.refresh_left_redpoint()
        return

    def show_btn_tab_by_index_list(self, index_list):
        for tab_index, btn_tab in self._btn_tab.items():
            if tab_index in index_list:
                btn_tab.setVisible(True)
            else:
                btn_tab.setVisible(False)

    def get_channel_redpoint_count(self, channel):
        if channel == chat_const.CHAT_CLAN:
            if not global_data.player or not global_data.player.is_in_clan():
                return 0
            return self._channel_redpoint_map[channel] + self._message_data.get_clan_unread_history_msg_count() + global_data.player.get_new_clan_intro_msg_cnt()
        return 0

    def reset_channel_redpoint_count(self, channel):
        if channel == chat_const.CHAT_CLAN:
            self._message_data.save_readed_clan_msg_time()
            global_data.player and global_data.player.confirm_new_clan_intro_msg()
        self._channel_redpoint_map[channel] = 0

    def refresh_left_redpoint(self):
        total_count = 0
        lv_tab = self.panel.nd_left.tab_list
        for i, tab_index in enumerate(self._tab_index_list):
            info = TAB_INDEX_TO_CHANNEL[tab_index]
            channel, _ = info
            btn_tab = lv_tab.GetItem(i)
            count = self.get_channel_redpoint_count(channel)
            btn_tab.img_red.setVisible(count > 0)
            total_count += count

        if total_count > 0:
            self.panel.PlayAnimation('new_mesg')
        else:
            self.panel.StopAnimation('new_mesg')

    def on_main_chat_ui(self, *args):
        self._on_main_chat_ui()
        if global_data.player and global_data.player.is_in_team():
            self.touch_channel_btn(chat_const.CHAT_TEAM)

    def _on_main_chat_ui(self, on_shown_cb=None):
        self.chat_open(on_shown_cb=on_shown_cb)
        self.refresh_base_panel_touch_status()

    def on_add_msg(self, is_msg_move, channel, data):
        if channel not in VALID_CHANNEL:
            return
        else:
            if self._preview_tab_channel is None or channel == self._preview_tab_channel:
                msg_color = message_data.CHANNEL_COLOR.get(data['chnl'], '0xf0ffffff')
                channel_name = message_data.get_channel_name_by_chid(data['chnl'])
                name = ''
                sender_info = data.get('sender_info', {})
                if sender_info and 'notify_type' not in sender_info:
                    remark = global_data.player._frds_remark.get(int(data['sender_info'][U_ID]), '')
                    name = data['sender_info'][C_NAME]
                    if remark:
                        name = '%s(%s)' % (name, remark)
                if 'red_packet_flag' in sender_info:
                    flag = sender_info['red_packet_flag']
                    if flag == RED_PACKET_MESSAGE_NEW_PACKET:
                        global_data.emgr.on_add_red_packet_msg.emit(sender_info.get('red_packet_info'))
                        global_data.player.update_new_red_packet_info(sender_info.get('red_packet_info', {}).get('pid', -1))
                        htmltext = '<color=%s>[%s]%s:</color><color=0xf12c5eff>%s</color>' % (msg_color, channel_name, name, get_text_by_id(634425))
                    else:
                        htmltext = '<color=%s>[%s]%s:%s</color>' % (msg_color, channel_name, name, get_server_text(data['msg']))
                else:
                    htmltext = '<color=%s>[%s]%s:%s</color>' % (msg_color, channel_name, name, get_server_text(data['msg']))
                self.panel.lab_chat.SetString(htmltext)
            if not self._is_chat_open or self._channel_index != channel:
                self._channel_redpoint_map[channel] += 1
                self.refresh_left_redpoint()
            return

    def add_channel_btn(self, index, btn):

        @btn.btn.callback()
        def OnClick(*args):
            self.touch_channel_btn(index)

        btn.btn.SetSwallowTouch(False)

    def touch_channel_btn(self, index, is_need_refresh=True):
        if self._tab_index != index:
            panel = self._btn_tab.get(self._tab_index)
            self.panel.btn_top.setVisible(False)
            if panel:
                panel.lab_main.SetColor('#DD')
                panel.lab_main.setScale(1.0)
                panel.btn.SetSelect(False)
            panel = self._btn_tab.get(index)
            if panel:
                panel.lab_main.SetColor('#SW')
                panel.lab_main.setScale(1.2)
                panel.btn.SetSelect(True)
            if is_need_refresh:
                self.change_channel(index)
        else:
            panel = self._btn_tab.get(self._tab_index)
            if panel:
                panel.lab_main.SetColor('#SW')
                panel.lab_main.setScale(1.2)
                panel.btn.SetSelect(True)

    def change_channel(self, index=None):
        if index == None:
            index = self._tab_index
        else:
            if self._tab_index != index:
                self._auto_voice_list = []
            self._tab_index = index
        self._channel_index, text_id = TAB_INDEX_TO_CHANNEL[self._tab_index]
        if self.top_chat_pigeon_show:
            self._show_top_chat_pigeon(self.top_chat_pigeon_show, self.top_chat_pigeon_msg_data, is_change_channel=True)
        self.panel.StopAnimation('show_speaker')
        self.panel.StopAnimation('hide_speaker')
        animation = 'show_speaker' if self._channel_index == chat_const.CHAT_WORLD else 'hide_speaker'
        self.panel.PlayAnimation(animation)
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime(animation)),
         cc.CallFunc.create(lambda : self._input_box and self._input_box.change_input_width())]))
        self._voice_key_to_widget = {}
        self.check_voice_btn_show()
        channel, _ = TAB_INDEX_TO_CHANNEL[index]
        self.reset_channel_redpoint_count(channel)
        self.refresh_left_redpoint()
        self.panel.btn_invite.setVisible(self._channel_index == chat_const.CHAT_TEAM or self._channel_index == chat_const.CHAT_WORLD)
        self._lv_chat.DeleteAllSubItem()
        self._lv_chat.setVisible(True)
        self.panel.layer_chat.img_bg.nd_empty.setVisible(False)
        self._cur_msg_data = self._message_data.get_channel_msg(self._channel_index)
        data_count = len(self._cur_msg_data)
        sview_height = self._lv_chat.getContentSize().height
        if self.send_red_packet_widget:
            if self.send_red_packet_widget.get_is_visible():
                self.panel.PlayAnimation('hide_red_packet')
            if self._channel_index in CAN_SEND_RED_PACKET_CHANNEL:
                self.send_red_packet_widget.update_send_channel(self._channel_index)
        all_height = 0
        index = 0
        while all_height < sview_height + 200:
            if data_count - index <= 0:
                break
            data = self._cur_msg_data[data_count - index - 1]
            is_ignore = self.is_ignore_msg(data)
            if is_ignore:
                index += 1
                continue
            chat_pnl = self.add_msg(data, False)
            if chat_pnl is None:
                del self._cur_msg_data[data_count - index - 1]
                data_count -= 1
                continue
            all_height += chat_pnl.getContentSize().height
            index += 1

        self._lv_chat._container._refreshItemPos()
        self._lv_chat._refreshItemPos()
        self._lv_chat.ScrollToBottom()
        self._sview_data_index = len(self._cur_msg_data) - 1
        self._is_msg_lock = False
        self.set_btn_lock(self._is_msg_lock)
        self._unread_msg_count = 0
        self.panel.layer_chat.nd_bottom.nd_input.btn_lock.SetSelect(self._is_msg_lock)
        if self._channel_index in (chat_const.CHAT_TEAM, chat_const.CHAT_WORLD, chat_const.CHAT_ROOM):
            self.refresh_auto_img_state()
            self.panel.layer_chat.nd_top.nd_auto_voice.setVisible(True)
        else:
            self.panel.layer_chat.nd_top.nd_auto_voice.setVisible(False)
        if self._channel_index == chat_const.CHAT_CLAN:
            if global_data.player and global_data.player.is_in_clan():
                self.panel.nd_notice.setVisible(True)
                self.panel.nd_notice.lab_notice.setString(get_text_by_id(80161) + ':' + global_data.player.get_clan_intro())
        else:
            self.panel.nd_notice.setVisible(False)
        self.panel.nd_speaker_input.setVisible(False)
        if self._channel_index == chat_const.CHAT_SYS or self._channel_index == chat_const.CHAT_ROOM_SHARE or self._channel_index == chat_const.CHAT_TEAM and not global_data.player.get_team_info():
            self.panel.nd_forbidden.setVisible(True)
            self.panel.nd_input.setVisible(False)
            if self._channel_index == chat_const.CHAT_SYS or self._channel_index == chat_const.CHAT_ROOM_SHARE:
                self.panel.nd_forbidden.lab_forbidden.SetString(get_text_by_id(2132))
            else:
                self.panel.nd_forbidden.lab_forbidden.SetString(get_text_by_id(2133))
        else:
            self.panel.nd_forbidden.setVisible(False)
            self.panel.nd_input.setVisible(True)
        if self._channel_index == chat_const.CHAT_PIGEON:
            self.panel.nd_input.setVisible(False)
            self.panel.layer_chat.nd_top.nd_auto_voice.setVisible(False)
            self.panel.nd_speaker_input.setVisible(True)
            return
        else:
            if self._channel_index == chat_const.CHAT_CLAN:
                is_in_clan = global_data.player or False if 1 else global_data.player.is_in_clan()
                self._lv_chat.setVisible(is_in_clan)
                self.panel.nd_forbidden.setVisible(not is_in_clan)
                self.panel.nd_forbidden.lab_forbidden.SetString(get_text_by_id(800046))
                self.panel.nd_input.setVisible(is_in_clan)
                self.panel.layer_chat.img_bg.nd_empty.setVisible(not is_in_clan)
            self.panel.btn_channel.setVisible(self._channel_index == chat_const.CHAT_WORLD and not interface.is_mainland_package())
            self.panel.btn_mode.setVisible(self._channel_index in [chat_const.CHAT_TEAM])
            self.panel.btn_reply.setVisible(self._channel_index == chat_const.CHAT_TEAM)
            self.show_mode_tap(False)
            return

    def refresh_red_packet_info(self, red_pids=[]):
        if not global_data.player:
            return
        if not red_pids:
            for channel in CAN_SEND_RED_PACKET_CHANNEL:
                cur_msg_data = self._message_data.get_channel_msg(channel)
                for idx in range(len(cur_msg_data)):
                    data = cur_msg_data[idx]
                    sender_info = data.get('sender_info', {})
                    if sender_info and 'red_packet_flag' in sender_info:
                        flag = sender_info['red_packet_flag']
                        if flag == RED_PACKET_MESSAGE_NEW_PACKET:
                            red_packet_info = sender_info.get('red_packet_info')
                            if red_packet_info['pid'] not in self._cur_red_packet_info:
                                self._cur_red_packet_info[red_packet_info['pid']] = {}

            red_pids = six_ex.keys(self._cur_red_packet_info)
            if red_pids:
                self._need_wait_red_packet_msg = True
        global_data.player.search_red_packet_info(red_pids)

    def on_refresh_red_packet_info(self, infos):
        for pid, info in six.iteritems(infos):
            if not self._cur_red_packet_info.get(pid):
                self._cur_red_packet_info[pid] = {}
            self._cur_red_packet_info[pid].update({'red_packet_status': info})
            self.on_refresh_red_packet_chat_item(pid)

    def on_claim_red_packet_succeed(self, flag, pid, count, item_no, packet_info):
        if not self._cur_red_packet_info.get(pid):
            return
        self._cur_red_packet_info[pid].update({'red_packet_status': packet_info})
        self.on_refresh_red_packet_chat_item(pid)

    def on_refresh_red_packet_chat_item(self, pid):
        if not global_data.player:
            return
        packet_info = self._cur_red_packet_info[pid]
        red_packet_widget = packet_info.get('red_packet_widget')
        if not red_packet_widget or not red_packet_widget.isValid() or not red_packet_widget.temp_red_packet:
            return
        red_packet_sender_info = packet_info.get('red_packet_sender_info', {})
        if red_packet_sender_info.get('red_packet_info', {}).get('overdue_time', 0) < tutil.time():
            red_packet_widget.temp_red_packet.img_lock.setVisible(True)
            red_packet_widget.temp_red_packet.lab_name.SetString(81137)
            return
        red_packet_status = packet_info.get('red_packet_status', {})
        if not red_packet_status:
            return
        split_count = red_packet_sender_info.get('red_packet_info', {}).get('split_count', 0)
        if str(global_data.player.uid) in red_packet_status.get('avt_info_dict', {}):
            red_packet_widget.temp_red_packet.img_lock.setVisible(True)
            red_packet_widget.temp_red_packet.lab_name.SetString(604029)
        elif len(red_packet_status.get('avt_info_dict', {})) == split_count:
            red_packet_widget.temp_red_packet.img_lock.setVisible(True)
            red_packet_widget.temp_red_packet.lab_name.SetString(634424)
        else:
            red_packet_widget.temp_red_packet.lab_name.SetString(81708)

    def on_send_red_packet_succeed(self):
        if self.send_red_packet_widget and self.send_red_packet_widget.get_is_visible():
            self.panel.PlayAnimation('hide_red_packet')

    def on_history_msg(self, channel):
        if self._channel_index == channel:
            if channel in TAB_CHANNEL_TO_INDEX:
                self.change_channel(TAB_CHANNEL_TO_INDEX[channel])

    def init_botom(self):
        panel = self.panel

        def send_cb(*args, **kwargs):
            panel.btn_send.btn_common.OnClick(None)
            return

        def max_input_cb(length, max_length):
            global_data.game_mgr.show_tip(get_text_by_id(19150, {'num': max_length}))

        self._input_box = InputBox.InputBox(panel.input_box, max_length=TEXT_INPUT_BOX_MAX_LEN, max_input_cb=max_input_cb, send_callback=send_cb, detach_after_enter=False)
        self._input_box.set_rise_widget(self.panel)
        self._input_box.enable_input(self._is_chat_open)

        def speaker_send_cb(*args, **kwargs):
            panel.speaker_btn_send.btn_common.OnClick(None)
            return

        def speaker_max_input_cb(length, max_length):
            global_data.game_mgr.show_tip(get_text_by_id(19150, {'num': max_length}))

        from logic.comsys.chat import ChatPigeonInput
        self._speaker_input_box = InputBox.InputBox(panel.speaker_input_box, max_length=ChatPigeonInput.MaxLength, max_input_cb=speaker_max_input_cb, send_callback=speaker_send_cb, detach_after_enter=False)
        self._speaker_input_box.set_rise_widget(self.panel)
        self._speaker_input_box.enable_input(self._is_chat_open)
        panel.btn_send.btn_common.SetText(get_text_by_id(80137))

        @panel.btn_send.btn_common.callback()
        def OnClick(*args, **kargs):
            cur_time = time.time()
            if cur_time - self._last_send_time < 0.5:
                return
            self._last_send_time = cur_time
            do_not_check_msg = kargs.get('do_not_check_msg')
            msg = do_not_check_msg or self._input_box.get_text()
            self.send_msg(self._channel_index, msg, do_not_check_msg, from_input_box=True)

        @panel.speaker_btn_send.btn_common.callback()
        def OnClick(*args, **kargs):
            cur_time = time.time()
            if cur_time - self._last_send_time < 0.5:
                return
            self._last_send_time = cur_time
            chat_utils.send_pigeon_msg(self._speaker_input_box)

        @panel.btn_lock.callback()
        def OnClick(*args):
            if self._is_msg_lock:
                self._is_msg_lock = False
                panel.btn_top.setVisible(False)
                self.change_channel()
            else:
                self._is_msg_lock = True
            self.set_btn_lock(self._is_msg_lock)

        @panel.btn_join.btn_common.unique_callback()
        def OnClick(*args):
            global_data.ui_mgr.show_ui('ClanJoinMainUI', 'logic.comsys.clan')

        @panel.btn_emote.callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('ChatEmote', 'logic.comsys.chat')
            ui.set_input_box(self._input_box, panel.btn_send.btn_common)
            ui.set_close_callback(self.panel_recover)
            self.panel_up_move(ui.get_bg_height())

        @panel.btn_reply.callback()
        def OnClick(*args):
            ui = global_data.ui_mgr.show_ui('ChatReply', 'logic.comsys.chat')
            ui.set_input_box(self._input_box)
            ui.set_close_callback(self.panel_recover)
            self.panel_up_move(ui.get_bg_height())

        self.voice_operate = logic.gutils.template_utils.voiceOperate(self, panel.btn_voice)
        self.check_voice_btn_show()

    def adjust_text_input_box_length(self, *args):
        room_ui = global_data.ui_mgr.get_ui('RoomUINew')
        if not room_ui or not room_ui.room_info:
            return
        if not room_ui.is_judgement():
            return
        if self._input_box:
            self._input_box.set_max_length(TEXT_INPUT_BOX_MAX_LEN_JUDGEMENT)

    def reset_text_input_box_length(self, *args):
        if self._input_box:
            self._input_box.set_max_length(TEXT_INPUT_BOX_MAX_LEN)

    def show_main_chat_ui(self, channel=None, on_shown_cb=None):
        if not self._is_chat_open:
            self._on_main_chat_ui(on_shown_cb=on_shown_cb)
        if channel is not None:
            self.touch_channel_btn(channel)
        return

    def show_chat_emote_panel(self):
        ui = global_data.ui_mgr.get_ui('ChatEmote')
        if not ui:
            self.panel.btn_emote.OnClick(None)
        return

    def update_chat_emote_rp(self):
        if not self._chat_emote_info:
            return
        else:
            show_rp = False
            for item_id in six_ex.keys(self._chat_emote_info):
                if item_id not in DEFAULT_EMOTE_PACK:
                    if chat_utils.check_has_split_emote(item_id):
                        emote_list = chat_utils.get_all_split_emote(item_id)
                        conf = confmgr.get('chat_all_emotes')
                        for emote in emote_list:
                            emote_item_id = conf[str(emote)].get('iItemId', None)
                            if emote_item_id and global_data.lobby_red_point_data.get_rp_by_no(emote_item_id):
                                show_rp = True
                                break

                    else:
                        show_rp = global_data.lobby_red_point_data.get_rp_by_no(item_id)
                else:
                    show_rp = False
                if show_rp:
                    break

            self.panel.btn_emote.temp_reddot.setVisible(show_rp)
            return

    def update_lobby_puppet_count(self, count):
        self.init_left()

    def send_msg(self, channel, msg, do_not_check_msg=False, from_input_box=False):
        if msg == '':
            global_data.player.notify_client_message((get_text_by_id(11055),))
            return
        if channel == chat_const.CHAT_WORLD and global_data.player.get_lv() < chat_const.SEND_WORLD_MSG_MIN_LV:
            global_data.player.notify_client_message((get_text_by_id(11063).format(lv=chat_const.SEND_WORLD_MSG_MIN_LV),))
            return
        from logic.gcommon.common_const import ui_operation_const as uoc
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            global_data.player.notify_client_message((get_text_by_id(635715),))
            return
        if do_not_check_msg:
            check_code = 0
            check_result = text_utils.CHECK_WORDS_PASS
        else:
            check_code, check_result, msg = text_utils.check_review_words_chat(msg)
            if check_result == text_utils.CHECK_WORDS_NO_PASS:
                global_data.player.notify_client_message((get_text_by_id(11009),))
                global_data.player.sa_log_forbidden_msg(channel, msg, check_code)
                return
            if from_input_box:
                self._input_box.set_text_no_refresh(msg)
            if channel == chat_const.CHAT_TEAM and not global_data.player.get_team_info():
                if from_input_box:
                    self._input_box.set_text('')
                global_data.player.notify_client_message((get_text_by_id(11019),))
                return
        if check_result == text_utils.CHECK_WORDS_PASS:
            self.refresh_rich_test(msg)
            global_data.player.send_msg(channel, msg, code=check_code)
        elif check_result == text_utils.CHECK_WORDS_ONLY_SELF:
            self._message_data.add_only_self_msg(channel, msg)
            global_data.player.sa_log_forbidden_msg(channel, msg, check_code)
        self.show_chat_msg_on_head(msg, channel)

    def on_send_msg_by_other_panel(self, channel, msg):
        cur_time = time.time()
        if cur_time - self._last_send_time < 0.5:
            return
        self._last_send_time = cur_time
        self.send_msg(channel, msg)

    def refresh_rich_test(self, msg):
        if self._rich_test:
            self._rich_test.Destroy()
            self._rich_test = None
        self._rich_test = CCRichText.Create(msg, 24, cc.Size(RICHTEXT_CONTENT_WIDTH, 0), fontTrans=False)
        self._rich_test.setAnchorPoint(cc.Vec2(0, 1.0))
        self._rich_test.setHorizontalAlign(0)
        self._rich_test.formatText()
        self.panel.AddChild('rich_test', self._rich_test)
        self._rich_test.setVisible(True)
        return

    def set_btn_lock(self, flag):
        if flag:
            self.panel.img_control.SetPosition('50%-19', '50%')
        else:
            self.panel.img_control.SetPosition('50%19', '50%')

    def get_send_voice_callback(self):
        channel_index = self._channel_index

        def voice_msg_callback(msg_str, voice_str):
            self.send_voice_msg(channel_index, msg_str, voice_str)

        return voice_msg_callback

    def send_voice_msg(self, channel, msg_str, voice_str):
        cur_time = time.time()
        if cur_time - self._last_send_time < 0.5:
            return
        self._last_send_time = cur_time
        if msg_str == '':
            last_time, _ = voice_str.split('\n', 1)
            if float(last_time) < chat_const.VOICE_NONE_MAX_TIME:
                global_data.player.notify_client_message((get_text_by_id(11055),))
                return
        if channel == chat_const.CHAT_WORLD and global_data.player.get_lv() < chat_const.SEND_WORLD_MSG_MIN_LV:
            global_data.player.notify_client_message((get_text_by_id(11063).format(lv=chat_const.SEND_WORLD_MSG_MIN_LV),))
            return
        from logic.gcommon.common_const import ui_operation_const as uoc
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return
        check_code, check_result, msg_str = text_utils.check_review_words_chat(msg_str)
        if check_result == text_utils.CHECK_WORDS_NO_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            global_data.player.sa_log_forbidden_msg(channel, msg_str, check_code)
            return
        if check_result == text_utils.CHECK_WORDS_PASS:
            global_data.player.send_msg(channel, msg_str, voice_str, code=check_code)
        elif check_result == text_utils.CHECK_WORDS_ONLY_SELF:
            self._message_data.add_only_self_msg(channel, msg_str, voice_str)
            global_data.player.sa_log_forbidden_msg(channel, msg_str, check_code)

    def get_voice_text_callback(self):
        channel = self._channel_index

        def voice_text_callback(voice_text):
            cur_time = time.time()
            if cur_time - self._last_send_time < 0.5:
                return
            self.send_msg(channel, voice_text)

        return voice_text_callback

    def clean_input_box_msg(self, r_msg):
        msg = self._input_box.get_text()
        if r_msg == msg:
            self._input_box.set_text('')

    def is_chat_open(self):
        return self._is_chat_open

    def chat_open(self, on_shown_cb=None):
        if self._chat_pnl_stage != chat_stage_hide:
            return
        self._chat_pnl_stage = chat_stage_moving
        self.change_channel()
        self.panel.layer_chat.stopAllActions()
        self.panel.layer_chat.setVisible(True)
        self.panel.btn_chat.setVisible(False)
        NewChatPigeon = global_data.ui_mgr.get_ui('NewChatPigeon')
        NewChatPigeon and NewChatPigeon.add_hide_count('MainChat')

        def cb():
            self._chat_pnl_stage = chat_stage_open
            if self._input_box:
                self._input_box.enable_input(True)
            if self._speaker_input_box:
                self._speaker_input_box.enable_input(True)
            if callable(on_shown_cb):
                on_shown_cb()

        act0 = cc.MoveTo.create(0.3, cc.Vec2(self._widget_pos.x, self._widget_pos.y))
        act1 = cc.Sequence.create([act0, cc.DelayTime.create(0.1), cc.CallFunc.create(cb)])
        self.panel.layer_chat.runAction(act1)
        self._is_chat_open = True
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time('MainChat', '')
        self.refresh_red_packet_info()
        global_data.emgr.chat_open.emit()

    def chat_close(self):
        if self._chat_pnl_stage != chat_stage_open:
            return
        self._chat_pnl_stage = chat_stage_moving
        self.panel_recover()
        NewChatPigeon = global_data.ui_mgr.get_ui('NewChatPigeon')
        NewChatPigeon and NewChatPigeon.add_show_count('MainChat')

        def cb():
            self._chat_pnl_stage = chat_stage_hide
            self.panel.layer_chat.setVisible(False)
            self.panel.btn_chat.setVisible(True and self._need_show_btn)
            self._need_show_btn = True
            self._need_block_all_click = False
            self.restore_all_click()
            self._is_msg_lock = False
            self._auto_voice_list = []
            for btn_tab in self._btn_tab.values():
                btn_tab.setVisible(True)

            global_data.emgr.chat_close_end.emit()

        act0 = cc.MoveTo.create(0.3, cc.Vec2(self._widget_pos.x - self._chat_width, self._widget_pos.y))
        act1 = cc.EaseSineIn.create(act0)
        act1 = cc.Sequence.create([act1, cc.CallFunc.create(cb)])
        self.panel.layer_chat.runAction(act1)
        self._is_chat_open = False
        if self._input_box:
            self._input_box.enable_input(False)
        if self._speaker_input_box:
            self._speaker_input_box.enable_input(False)
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time('MainChat', '')

    def on_add_channel_msg(self, index_move, channel, data):
        if channel in chat_const.POP_OUT_CHAT and global_data.player and data.get('sender_info', ''):
            uid = data['sender_info'].get(U_ID, None)
            from logic.gutils.chat_utils import has_extra_msg
            if uid and not has_extra_msg(data):
                lobby_puppet = global_data.player.get_place_puppet(uid)
                if lobby_puppet and lobby_puppet.logic:
                    if data.get('voice', None) and (self._chat_pnl_stage == chat_stage_hide or self._channel_index in chat_const.POP_OUT_CHAT):
                        self.play_auto_voice(data, channel=channel)
                    else:
                        lobby_puppet.logic.send_event('E_SHOW_CHAT_MESSAGE', data)
        if self._chat_pnl_stage == chat_stage_hide:
            return
        else:
            if self._channel_index == channel:
                in_height = self._lv_chat.getInnerContainerSize().height
                out_height = self._lv_chat.getContentSize().height
                if self._is_msg_lock and in_height != out_height:
                    if 'sender_info' in data and 'notify_type' not in data['sender_info'] and self._my_uid == data['sender_info'].get(U_ID, 0):
                        self.change_channel()
                        self.panel.layer_chat.img_bg.btn_top.setVisible(False)
                    else:
                        self._unread_msg_count += 1
                        if self._unread_msg_count <= 99:
                            msg_inf = get_text_by_id(11002, (self._unread_msg_count,))
                        else:
                            msg_inf = get_text_by_id(11003)
                        self.panel.layer_chat.img_bg.btn_top.SetText(msg_inf)
                        self.panel.layer_chat.img_bg.btn_top.setVisible(True)
                else:
                    if data.get('voice', None) and self._channel_index != chat_const.CHAT_TEAM:
                        self.play_auto_voice(data, self._channel_index)
                    self.add_msg(data, is_new=True)
                    if self._is_check_sview == False:
                        self._is_check_sview = True
                        self.SetTimeOut(0.021, self.check_sview)
                    self._lv_chat._container._refreshItemPos()
                    self._lv_chat._refreshItemPos()
                    self._lv_chat.jumpToBottom()
                self._sview_data_index += index_move
            return

    def is_ignore_msg(self, data):
        from logic.gutils.chat_utils import has_extra_msg
        if has_extra_msg(data) and data['extra'].get('type', None) == chat_const.MSG_TYPE_TEAM_RECRUIT:
            uid = data['sender_info'].get(U_ID, None)
            if global_data.player.uid == uid:
                return True
            if self._channel_index != chat_const.CHAT_TEAM:
                return False
            battle_type = data['extra'].get('battle_type', 0)
            if self._cur_match_battle_type_filter != 0 and self._cur_match_battle_type_filter != battle_type:
                return True
        return False

    def add_msg(self, data, is_back_item=True, index=-1, is_new=False):
        try:
            sender_info = data.get('sender_info', '')
            flag = None
            if sender_info:
                from logic.gutils.chat_utils import has_extra_msg
                msg = data.get('msg', None)
                if msg:
                    data['msg'] = check_show_msg(msg)
                if has_extra_msg(data) and data['extra'].get('type', None) in [chat_const.MSG_TYPE_TEAM_INVITE, chat_const.MSG_TYPE_TEAM_RECRUIT]:
                    send_time = data['extra'].get('time', 0)
                    if tutil.get_server_time() - send_time > TEAM_SUMMON_VALID_TIME:
                        return
                if self.is_ignore_msg(data):
                    return
                if not global_data.player:
                    return
                if global_data.player.is_in_team() and data and data.get('extra', {}).get('type', None) == chat_const.MSG_TYPE_TEAM_RECRUIT:
                    return
                if 'notify_type' in sender_info:
                    from logic.gcommon.common_const.notice_const import NOTICE_REWARD, NOTICE_PRIVILEGE, NOTICE_WINNING, NOTICE_RED_PACKET, NOTICE_PVE_CLEAR
                    if sender_info['notify_type'] == NOTICE_REWARD:
                        panel = self.add_lottery_broadcast_msg(data, is_back_item, is_new)
                    elif sender_info['notify_type'] == NOTICE_PRIVILEGE:
                        panel = self.add_privilege_broadcast_msg(data, is_back_item, is_new)
                    elif sender_info['notify_type'] == NOTICE_WINNING:
                        panel = self.add_winning_broadcast_msg(data, is_back_item, is_new)
                    elif sender_info['notify_type'] == NOTICE_PVE_CLEAR:
                        panel = self.add_pve_battle_clearance_broadcast_msg(data, is_back_item, is_new)
                    else:
                        return
                elif 'red_packet_flag' in sender_info:
                    flag = sender_info['red_packet_flag']
                    if flag == RED_PACKET_MESSAGE_NEW_PACKET:
                        panel = self.add_send_red_packet_msg(data, is_back_item, is_new)
                    elif flag == RED_PACKET_MESSAGE_DANMU:
                        panel = self.add_red_packet_dammu_msg(data, is_back_item, is_new)
                    elif flag == RED_PACKET_MESSAGE_CLAIM:
                        panel = self.add_open_red_packet_msg(data, is_back_item, is_new)
                elif data.get('voice', ''):
                    panel = self.add_voice_msg(data, is_back_item)
                else:
                    panel = self.add_text_msg(data, is_back_item)
            else:
                panel = self.add_sys_msg(data, is_back_item)
            if self._need_block_all_click and flag != RED_PACKET_MESSAGE_NEW_PACKET:
                self.get_touch_enabled_children(panel)
                self.set_children_touch_enabled(False)
            return panel
        except Exception as e:
            print (
             'add msg failed', str(e))

        return

    def add_lottery_broadcast_msg(self, data, is_back_item=True, is_new=False):
        from logic.gutils.mecha_skin_utils import is_s_skin_that_can_upgrade
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
        if 'loop_lottery_id' in args:
            lottery_id = args['loop_lottery_id']
        args.pop('_uid')
        if args['playername']:
            args['playername'] = args['playername'].replace('|', '\xef\xbd\x9c')
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
        panel.SetContentSize(panel_size.width, height)
        panel.ChildResizeAndPosition()
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

    def add_pve_battle_clearance_broadcast_msg(self, data, is_back_item=True, is_new=False):
        from logic.gutils.chat_utils import add_pve_battle_clearance_broadcast_msg_imp
        return add_pve_battle_clearance_broadcast_msg_imp(self._lv_chat, data, is_back_item, is_new)

    def on_open_choose_red_packet(self, pid):
        packet_info = self._cur_red_packet_info.get(pid, {})
        if not packet_info:
            return
        if not global_data.player:
            return
        from logic.gcommon.common_const import ui_operation_const as uoc
        content = global_data.player.get_setting_2(uoc.UNDERAGE_MODE_KEY)
        if content:
            global_data.game_mgr.show_tip(get_text_by_id(635260))

            def click_goto():
                from logic.gutils import jump_to_ui_utils
                jump_to_ui_utils.jump_to_underage_mode_btn()

            SecondConfirmDlg2().confirm(content=get_text_by_id(635270), confirm_callback=click_goto)
            return
        red_packet_sender_info = packet_info.get('red_packet_sender_info', {})
        if red_packet_sender_info.get('red_packet_info', {}).get('overdue_time', 0) < tutil.time():
            return
        RedPacketUI(channel=self._channel_index, pid=pid, packet_info=packet_info)

    def add_send_red_packet_msg(self, data, is_back_item=True, is_new=False):
        if self._my_uid == data['sender_info'].get(U_ID, 0):
            conf = self.redpacket_me_temp
            is_other = False
        else:
            is_other = True
            conf = self.redpacket_other_temp
        red_packet = self.make_chat_player_info(data, conf, is_back_item)
        red_packet_info = data['sender_info'].get('red_packet_info')
        init_chat_red_packet(red_packet, red_packet_info, is_other)
        if red_packet_info['pid'] not in self._cur_red_packet_info:
            self._cur_red_packet_info[red_packet_info['pid']] = {'red_packet_sender_info': data['sender_info'],'red_packet_widget': red_packet
               }
        else:
            self._cur_red_packet_info[red_packet_info['pid']].update({'red_packet_sender_info': data['sender_info'],'red_packet_widget': red_packet
               })
        if is_new:
            pass

        @red_packet.temp_head.callback()
        def OnClick(*args):
            self.on_player_simple_inf(data['sender_info'].get(U_ID, 0), '')

        self.on_refresh_red_packet_chat_item(red_packet_info['pid'])
        red_packet.temp_red_packet.nd_touch.BindMethod('OnClick', lambda btn, touch, pid=red_packet_info['pid']: self.on_open_choose_red_packet(pid))
        return red_packet

    def add_red_packet_dammu_msg(self, data, is_back_item=True, is_new=False):
        sender_info = data['sender_info']
        red_packet_info = sender_info.get('red_packet_info', {})
        global_data.emgr.send_red_packet_dammu.emit(sender_info.get(C_NAME, ''), red_packet_info)
        if self._ban_red_packet_dammu == True:
            return None
        else:
            text_idx = red_packet_info.get('text_idx', 0)
            text_type = red_packet_info.get('text_type', 1)
            data['msg'] = get_red_packet_danmu_text(text_idx, text_type)
            return self.add_text_msg(data, is_back_item=is_back_item)

    def add_open_red_packet_msg(self, data, is_back_item=True, is_new=False):
        conf = self.redpacket_open
        red_packet_claim_info = data['sender_info'].get('red_packet_claim_info', {})
        if not red_packet_claim_info:
            return None
        else:
            if is_back_item:
                item = self._lv_chat.AddItem(conf, bRefresh=True)
            else:
                item = self._lv_chat.AddItem(conf, 0, bRefresh=True)
            item.lab_info.SetString(get_text_by_id(634420).format(data['sender_info'][C_NAME]))
            if not global_data.player:
                item.lab_touch.setVisible(False)
            else:
                pid = red_packet_claim_info.get('pid')
                red_packet_info = global_data.player.get_red_packet_info(pid)
                if not red_packet_info:
                    item.lab_touch.setVisible(False)
                else:
                    count = red_packet_info.get('split_count', 10)
                    claim_count = len(red_packet_info.get('avt_info_dict', {}))
                    if count <= claim_count:
                        item.lab_touch.setVisible(True)
                        item.nd_touch.BindMethod('OnClick', lambda btn, touch, pid=pid: self.on_open_choose_red_packet(pid))
                    else:
                        item.lab_touch.setVisible(False)
            return item

    def add_winning_broadcast_msg(self, data, is_back_item=True, is_new=False):
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

    def add_privilege_broadcast_msg(self, data, is_back_item=True, is_new=False):
        from common.utils.ui_path_utils import PRIVILEGE_BAR_BADGE_FRAME, PRIVILEGE_BAR_BADGE_LEVEL
        template_name = 'chat/i_chat_pigeon_item_badge'
        panel = global_data.uisystem.load_template_create(template_name)
        if is_back_item:
            self._lv_chat.AddControl(panel, bRefresh=True)
        else:
            self._lv_chat.AddControl(panel, index=0, bRefresh=True)
        if is_new:
            panel.PlayAnimation('show')
        panel.PlayAnimation('loop')
        init_text = data['msg']
        tid, args = unpack_text_data(init_text)
        lv = args['lv']
        frame_pic = PRIVILEGE_BAR_BADGE_FRAME.get(int(lv))
        level_pic = PRIVILEGE_BAR_BADGE_LEVEL.get(lv)
        panel.temp_badge.bar_level.SetDisplayFrameByPath('', frame_pic)
        panel.temp_badge.img_num_level.SetDisplayFrameByPath('', level_pic)
        uid = args['_uid']
        args.pop('_uid')
        text = get_text_by_id(tid, args)
        textlist = text.split('|')
        msg = textlist[0]
        priv_lv = textlist[1]
        panel.lab_name.SetString(11007)
        panel.lab_kind_name.SetString(priv_lv)

        def touch_callback(_msg, ele, touch, touch_event):
            chat_link.link_touch_callback(_msg, uid)

        msg = chat_link.linkstr_to_richtext(msg)
        lab_width = panel.lab_msg.getContentSize().width
        panel.lab_msg.SetStringWithAdapt(msg, (lab_width, 92))
        if global_data.player.uid != uid:
            panel.lab_msg.SetCallback(touch_callback)
        img_height = panel.img_item.getContentSize().height
        panel_size = panel.getContentSize()
        height = max(img_height + 37, panel_size.height)
        panel.SetContentSize(panel_size.width, height)
        panel.ChildResizeAndPosition()
        panel.lab_msg.SetStringWithAdapt(msg, (lab_width, 92))

        @panel.btn_goto.unique_callback()
        def OnClick(*args):
            from logic.gutils.jump_to_ui_utils import jump_to_charge
            from logic.comsys.charge_ui.ChargeUINew import ACTIVITY_PRIVILEGE_TYPE
            jump_to_charge(ACTIVITY_PRIVILEGE_TYPE)

        return panel

    def add_voice_msg(self, data, is_back_item=True):
        sender_id = data['sender_info'].get(U_ID, 0)
        if self._my_uid == sender_id:
            conf = self.voice_me_temp
            anchor_x = 1.0
            align = 0
            scale = 1
            is_left = False
        else:
            conf = self.voice_other_temp
            anchor_x = 0.0
            align = 0
            scale = -1
            is_left = True
        time, arm_key = data['voice'].split('\n', 1)
        time = float(time)
        format_data = self._template_data[id(conf)]
        chat, msg_pos, size, rt_width, time_msg_offset = self.make_chat_message(data, conf, is_back_item, anchor_x, align, format_data, is_left)

        @chat.btn_voice.callback()
        def OnClick(btn, touch, channel=self._channel_index, sender_id=sender_id):
            self._auto_voice_list = []
            self.play_voice_msg(arm_key, voice_channel=channel, uid=sender_id)

        chat.btn_voice.SetSwallowTouch(False)
        voice_width = VOICE_BAR_WIDTH * 0.4 + (time / 60.0) ** 0.5 * VOICE_BAR_WIDTH * 0.6
        if rt_width < voice_width + RICHTEXT_CONTENT_EDGE * 2:
            rt_width = voice_width + RICHTEXT_CONTENT_EDGE * 2
        chat.btn_voice.SetContentSize(voice_width, chat.btn_voice.getContentSize().height)
        voice_pos = format_data['voice_pos']
        chat.btn_voice.SetPosition(voice_pos['x'], voice_pos['y'])
        chat.btn_voice.lab_time.SetPosition(voice_width / 2, chat.btn_voice.lab_time.getPosition().y)
        s = "%d''" % math.ceil(time)
        chat.btn_voice.lab_time.SetString(s)
        chat.btn_voice.img_icon.SetPosition(voice_width - 20, chat.btn_voice.img_icon.getPosition().y)
        if arm_key in self._unplay_voice and self._my_uid != data['sender_info'].get(U_ID, 0):
            chat.img_redpoint.setVisible(True)
            self._voice_key_to_widget[arm_key] = chat
        else:
            chat.img_redpoint.setVisible(False)
        self.adjust_chat_panel(chat, msg_pos, scale, rt_width, size, time_msg_offset, data=data)
        from logic.gutils.chat_utils import has_extra_msg
        if not has_extra_msg(data):
            report_msg = ''.join([format_data.get('color'), get_server_text(data['msg'])])
        else:
            report_msg = ''

        @chat.temp_head.callback()
        def OnClick(*args):
            self.on_player_simple_inf(data['sender_info'].get(U_ID, 0), report_msg)

        chat.temp_head.SetSwallowTouch(False)
        return chat

    def add_text_msg(self, data, is_back_item=True):
        if self._my_uid == data['sender_info'].get(U_ID, 0):
            if data.get('is_pigoen', False):
                conf = self.speaker_chat_me_temp
            else:
                conf = self.chat_me_temp
            anchor_x = 1.0
            align = 0
            scale = 1
            is_left = False
        else:
            if data.get('is_pigoen', False):
                conf = self.speaker_chat_other_temp
            else:
                conf = self.chat_other_temp
            anchor_x = 0.0
            align = 0
            scale = -1
            is_left = True
        format_data = self._template_data[id(conf)]
        chat, msg_pos, size, rt_width, time_msg_offset = self.make_chat_message(data, conf, is_back_item, anchor_x, align, format_data, is_left)
        self.adjust_chat_panel(chat, msg_pos, scale, rt_width, size, time_msg_offset, data=data)
        from logic.gutils.chat_utils import has_extra_msg
        if not has_extra_msg(data):
            report_msg = ''.join([format_data.get('color'), get_server_text(data['msg'])])
        else:
            report_msg = ''

        @chat.temp_head.callback()
        def OnClick(*args):
            self.on_player_simple_inf(data['sender_info'].get(U_ID, 0), report_msg)

        chat.temp_head.SetSwallowTouch(False)
        return chat

    def make_chat_player_info(self, data, conf, is_back_item):
        if is_back_item:
            chat = self._lv_chat.AddItem(conf, bRefresh=True)
        else:
            chat = self._lv_chat.AddItem(conf, 0, bRefresh=True)
        remark = global_data.player._frds_remark.get(int(data['sender_info'][U_ID]), '')
        name = data['sender_info'][C_NAME]
        if remark:
            name = '%s(%s)' % (name, remark)
        chat.lab_name.SetString(name)
        rank_use_title_dict = data['sender_info'].get('rank_use_title_dict', {})
        title_type = get_rank_use_title_type(rank_use_title_dict)
        rank_info = get_rank_use_title(rank_use_title_dict)
        logic.gutils.template_utils.init_rank_title(chat.temp_title, title_type, rank_info)
        sender_info = data['sender_info']
        uid = sender_info.get(U_ID, 0)
        self._player_info_manager.add_head_item_auto(chat.temp_head, uid, 0, sender_info)
        role_head_utils.set_role_dan(chat.temp_tier, sender_info.get('dan_info'))
        player_data = sender_info.get('privilege', {})
        role_head_utils.init_privilege_name_color_and_badge(chat.lab_name, chat.temp_head, player_data, '#BC')
        return chat

    def make_chat_message(self, data, conf, is_back_item, anchor_x, align, format_data, is_left):
        chat = self.make_chat_player_info(data, conf, is_back_item)
        sender_info = data['sender_info']
        uid = sender_info.get(U_ID, 0)
        is_my_message = self._my_uid == uid
        chat_item_no = sender_info.get('chat_background', 0)
        chat_utils.load_chat_background(chat, chat_item_no, is_my_message)
        time_rt_msg, time_msg_offset = self.add_time_msg(chat, data)
        msg = data.get('msg', '')
        uid = data.get('sender_info', {}).get('uid', 0)
        if global_data.player and global_data.player.uid != uid and chat_utils.anti_spoofing_check(msg):
            self.add_anti_spoofing_msg(self.anti_spoofing, is_back_item)
        msg_pos = format_data['msg_pos']
        from logic.gutils.chat_utils import has_extra_msg
        if not has_extra_msg(data):
            msg = get_server_text(data['msg'])
            try:
                content = CCRichText.Create(msg, 24, cc.Size(RICHTEXT_CONTENT_WIDTH, 0), fontTrans=False)
            except:
                content = CCRichText.Create(' ', 24, cc.Size(RICHTEXT_CONTENT_WIDTH, 0), fontTrans=False)
                post_stack('err richtext %s' % msg)

            content.setAnchorPoint(cc.Vec2(anchor_x, 1.0))
            content.setHorizontalAlign(align)
            content.formatText()
            size = content.getVirtualRendererSize()
            content_width = self.get_max_line_width(content.getLineWidths())
            if not is_left:
                x = msg_pos['x'] + (RICHTEXT_CONTENT_WIDTH - content_width)
                content.setPosition(cc.Vec2(x, msg_pos['y']))
            else:
                content.setPosition(cc.Vec2(msg_pos['x'], msg_pos['y']))
            player_data = sender_info.get('privilege', {})
            privilege_font_color = COLOR_FONT
            priv_settings = player_data.get('priv_settings', {})
            priv_colorful_font = player_data.get('priv_colorful_font', False)
            if priv_colorful_font and priv_settings.get(PRIV_SHOW_COLORFUL_FONT, False):
                content.SetColor(privilege_font_color)
            else:
                content.SetColor('#BC')
            content.SetString(msg)
        else:
            content, size, content_width, hide_bar = self._add_extra_msg(data, is_left)
            if content:
                content.setPosition(cc.Vec2(msg_pos['x'], msg_pos['y']))
            if size is None:
                size = chat.getContentSize()
                content_width = size.width
            if hide_bar:
                chat.temp_bar.setVisible(False)
        if content:
            chat.AddChild('content', content)
        return (
         chat, msg_pos, size, content_width, time_msg_offset)

    def add_sys_msg(self, data, is_back_item=True):
        if is_back_item:
            chat = self._lv_chat.AddItem(self.sys_item_temp, bRefresh=True)
        else:
            chat = self._lv_chat.AddItem(self.sys_item_temp, 0, bRefresh=True)
        time_rt_msg, time_msg_offset = self.add_time_msg(chat, data)
        format_data = self._template_data[id(self.sys_item_temp)]
        if data.get('is_pigoen', False):
            chat.img_sys.lab.SetString(get_text_by_id(11007))
        else:
            chat.img_sys.lab.SetString(get_text_by_id(11020))
        msg_html = '#r%s#n' % get_server_text(data['msg'])
        rt_msg = CCRichText.Create(msg_html, 24, cc.Size(RICHTEXT_CONTENT_WIDTH, 0), fontTrans=False)
        rt_msg.setAnchorPoint(cc.Vec2(0.0, 1.0))
        rt_msg.formatText()
        chat.AddChild('msg', rt_msg)
        size = rt_msg.getVirtualRendererSize()
        rt_width = self.get_max_line_width(rt_msg.getLineWidths())
        msg_pos = format_data['msg_pos']
        rt_msg.setPosition(cc.Vec2(msg_pos['x'], msg_pos['y']))
        self.adjust_chat_panel(chat, msg_pos, 1, rt_width, size, time_msg_offset, data=data)
        return chat

    def add_time_msg(self, chat, data):
        time_msg_offset = 0
        time_rt_msg = None
        if data.get('is_show_time', False) and data.get('time', 0):
            pnl_size = chat.getContentSize()
            time_str = '#SC%s</color>' % common.utilities.get_time_str_chat(data['time'])
            time_rt_msg = CCRichText.Create(time_str, 18, cc.Size(pnl_size.width, 0))
            time_rt_msg.setAnchorPoint(cc.Vec2(0.5, 1.0))
            time_rt_msg.setHorizontalAlign(1)
            time_rt_msg.formatText()
            chat.AddChild(None, time_rt_msg)
            time_msg_offset = time_rt_msg.getVirtualRendererSize().height
            time_rt_msg.SetPosition(pnl_size.width * 0.5, pnl_size.height + time_msg_offset)
        return (
         time_rt_msg, time_msg_offset)

    def add_anti_spoofing_msg(self, conf, is_back_item):
        if is_back_item:
            chat = self._lv_chat.AddItem(conf, bRefresh=True)
        else:
            chat = self._lv_chat.AddItem(conf, 1, bRefresh=True)

    def on_player_simple_inf(self, uid, report_msg):
        if uid == self._my_uid:
            return
        ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
        from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_INTIMACY
        ui.set_extra_btns([BTN_TYPE_INTIMACY])
        ui.refresh_by_uid(uid)
        channel_name = chat_const.CHAT_CHANNEL_NAME.get(self._channel_index, 'unknown')
        ui.set_chat_source(uid, channel_name, report_msg)
        ui.set_position(self._player_simple_inf_pos)

    def adjust_chat_panel(self, chat, msg_pos, scale, rt_width, size, time_msg_offset=0.0, data=None):
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
        bottom_height += time_msg_offset
        if bottom_height < pnl_size.height:
            bottom_height = pnl_size.height
        chat.setContentSize(cc.Size(pnl_size.width, bottom_height))
        offset = bottom_height - time_msg_offset - pnl_size.height
        for child in chat.getChildren():
            pos = child.getPosition()
            child.setPosition(cc.Vec2(pos.x, pos.y + offset))

        return

    def get_max_line_width(self, line_widths):
        max_width = None
        for width in line_widths:
            if not max_width:
                max_width = width
            elif max_width < width:
                max_width = width

        return max_width

    def check_sview(self):
        self._sview_data_index = self._lv_chat.AutoAddAndRemoveItem_chat(self._sview_data_index, self._cur_msg_data, len(self._cur_msg_data), self.add_msg, 400, 400)
        self._is_check_sview = False

    def get_lock_inf(self):
        return (
         self._is_msg_lock, self._channel_index, self._unread_msg_count)

    def on_finalize_panel(self):
        self._btn_tab = {}
        if self.send_red_packet_widget:
            self.send_red_packet_widget.destroy()
            self.send_red_packet_widget = None
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        if self._speaker_input_box:
            self._speaker_input_box.destroy()
            self._speaker_input_box = None
        self.voice_operate.destroy()
        global_data.emgr.chat_add_channel_msg -= self.on_add_channel_msg
        global_data.emgr.chat_add_channel_msg -= self.on_add_msg
        global_data.emgr.chat_history_msg -= self.on_history_msg
        global_data.emgr.message_receive_self_msg -= self.clean_input_box_msg
        global_data.emgr.create_join_success -= self._success_in_clan
        global_data.emgr.create_clan_success -= self._success_in_clan
        global_data.emgr.need_show_room_ui_event -= self.init_left
        global_data.emgr.leave_custom_room -= self.init_left
        global_data.emgr.refresh_item_red_point -= self.update_chat_emote_rp
        global_data.emgr.on_show_room_ui_event -= self.adjust_text_input_box_length
        global_data.emgr.leave_custom_room -= self.reset_text_input_box_length
        self.release_template_format()
        if global_data.ui_lifetime_log_mgr:
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time('MainChat', '')
        return

    def on_voice_empty(self):
        if self._auto_voice_list:
            arm_key, uid, voice_channel = self._auto_voice_list.pop(0)
            self.play_voice_msg(arm_key, voice_channel=voice_channel, uid=uid)

    def on_team_change(self, *args):
        if self._channel_index == chat_const.CHAT_TEAM:
            if not global_data.player.get_team_info():
                self.panel.nd_forbidden.setVisible(True)
                self.panel.nd_input.setVisible(False)
                self.panel.lab_forbidden.SetString(get_text_by_id(2133))
            else:
                self.panel.nd_forbidden.setVisible(False)
                self.panel.nd_input.setVisible(True)
        flag = global_data.player.is_in_team()
        self.panel.btn_chat_quick.setVisible(flag)
        if not flag:
            self._team_quick_chat.set_visible(False)
            self.panel.btn_chat_quick.SetSelect(False)
        else:
            self.touch_channel_btn(UI_TEAM_INDEX)
        self.refresh_base_panel_touch_status()

    def _success_in_clan(self):
        self._lv_chat.setVisible(True)
        self.panel.nd_forbidden.setVisible(False)
        self.panel.nd_input.setVisible(True)
        self.panel.layer_chat.img_bg.nd_empty.setVisible(False)

    def play_voice_msg(self, arm_key, voice_channel=None, uid=None):
        global_data.voice_mgr.play_voice_msg(arm_key)
        widget = self._voice_key_to_widget.get(arm_key, None)
        if widget and widget.isValid():
            widget.img_redpoint.setVisible(False)
        if arm_key in self._unplay_voice:
            self._unplay_voice.remove(arm_key)
        if voice_channel == chat_const.CHAT_TEAM:
            lobby_puppet = global_data.player.get_place_puppet(uid)
            if lobby_puppet and lobby_puppet.logic:
                lobby_puppet.logic.send_event('E_SHOW_CHAT_MESSAGE', {'voice': arm_key})
        return

    def panel_up_move(self, height):
        if self.panel:
            self.panel.layer_chat.SetPosition(0, height)

    def panel_recover(self):
        if self.panel:
            self.panel.layer_chat.SetPosition(0, 0)

    def do_hide_panel(self):
        super(MainChat, self).do_hide_panel()
        if self._input_box:
            self._input_box.hide()
        if self._speaker_input_box:
            self._speaker_input_box.hide()

    def refresh_auto_img_state(self):
        img_choose = self.panel.layer_chat.nd_top.nd_auto_voice.node_voice.img_choose
        if self._is_auto_voice[self._channel_index] == 1:
            img_choose.setVisible(True)
        else:
            img_choose.setVisible(False)

    def refresh_red_packet_ban_dammu(self):
        img_choose = self.panel.temp_red_packet.img_choose
        if self._ban_red_packet_dammu == True:
            img_choose.setVisible(True)
        else:
            img_choose.setVisible(False)

    def ui_vkb_custom_func(self):
        if self._is_chat_open:
            self.chat_close()
            self.refresh_base_panel_touch_status()
            return True
        else:
            return False

    def switch_lobby_scene_capture(self, is_enable):
        if is_enable:
            self.panel.StopAnimation('chat_appear')
            self.panel.PlayAnimation('chat_hide')
            self.ui_vkb_custom_func()
        else:
            self.panel.StopAnimation('chat_hide')
            self.panel.PlayAnimation('chat_appear')

    def refresh_team_quick_chat(self):
        if self._team_quick_chat and self._team_quick_chat.is_visible():
            self._team_quick_chat.set_visible(False)
            self.panel.btn_chat_quick.SetSelect(False)

    def refresh_base_panel_touch_status(self):
        self.panel.SetEnableTouch(self._is_chat_open or self._team_quick_chat.is_visible())

    def get_touch_enabled_children(self, node):
        for child in node.GetChildren():
            if child.IsSupportTouch() and child.GetName() != 'btn_back' and child.GetName() != 'btn_common' and child.GetName() != 'nd_touch':
                self._touch_children_list[child] = child.isTouchEnabled()
            self.get_touch_enabled_children(child)

    def block_all_click(self):
        self._need_block_all_click = True
        self.get_touch_enabled_children(self.panel.layer_chat)
        self.set_children_touch_enabled(False)

    def restore_all_click(self):
        for item, isEnable in filter(None, self._touch_children_list.items()):
            if item.IsSupportTouch() and item.GetName() != None:
                item.SetEnableTouch(isEnable)

        self._touch_children_list = {}
        return

    def set_children_touch_enabled(self, enable):
        for item in filter(None, self._touch_children_list):
            if item.IsSupportTouch() and item.GetName() != None:
                item.SetEnableTouch(enable)

        return

    def set_need_show_btn(self, need_show_btn):
        self._need_show_btn = need_show_btn
        for btn in self._need_show_btn_list:
            btn.setVisible(self._need_show_btn)

    def _add_extra_msg(self, data, is_left):
        msg_func_dict = {chat_const.MSG_TYPE_TEAM_INVITE: self._make_invite_msg,
           chat_const.MSG_TYPE_TEAM_RECRUIT: self._make_team_recruit_msg,
           chat_const.MSG_TYPE_CLAN_CARD: self._make_clan_card_msg,
           chat_const.MSG_TYPE_ROOM_CARD: self._make_room_card_msg,
           chat_const.MSG_TYPE_SKIN_DEFINE: self._make_skin_define_msg,
           chat_const.MSG_TYPE_VIDEO_SHARE: self._make_video_share_msg,
           chat_const.MSG_TYPE_MECHA_SEASON_MEMORY: self._make_mecha_season_memory_msg,
           chat_const.MSG_TYPE_ACHIEVEMENT_SEASON_MEMORY: self._make_achievement_season_memory_msg,
           chat_const.MSG_TYPE_FRIEND_SEASON_MEMORY: self._make_friend_season_memory_msg,
           chat_const.MSG_TYPE_LUCKY_LOTTERY: self._make_lucky_lottery_msg
           }
        extra_msg_type = data['extra'].get('type', None)
        if extra_msg_type in msg_func_dict:
            deal_func = msg_func_dict[extra_msg_type]
            return deal_func(data, is_left)
        else:
            return (
             None, None, None, False)
            return

    def _make_invite_msg(self, data, is_left):
        if is_left:
            temp_conf = self.get_special_temp_conf('invite_message_other')
        else:
            temp_conf = self.get_special_temp_conf('invite_message_me')
        content = global_data.uisystem.create_item(temp_conf)
        extra = data['extra']
        for tab_inde in extra['tab']:
            item = content.list_need.AddTemplateItem(bRefresh=True)
            item.lab_need.SetString(get_text_by_id(chat_const.CHAT_INVITE_TAB_LIST[tab_inde]))

        content.lab_demand.SetString(get_server_text(data['msg']))
        content.btn_join.lab_team_num.SetString('%d/%d' % (extra['num'][0], extra['num'][1]))
        game_mode_text = get_text_by_id(chat_const.CHAT_INVITE_GAME_MODE_LIST[extra['game_mode']]['name'])
        content.lab_mode.SetString(game_mode_text)

        @content.btn_join.callback()
        def OnClick(*args):
            sender_id = data['sender_info'].get(U_ID, 0)
            if global_data.player.is_in_team():
                global_data.player.notify_client_message((get_text_by_id(11034),))
                return
            send_time = data['extra'].get('time', 0)
            if tutil.get_server_time() - send_time > TEAM_SUMMON_VALID_TIME:
                global_data.player.notify_client_message((get_text_by_id(11041),))
                return
            if self._my_uid != sender_id:
                global_data.player.apply_join_team(sender_id)
            else:
                global_data.player.notify_client_message((get_text_by_id(13067),))

        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, False)

    def _make_team_recruit_msg(self, data, is_left):
        from logic.gutils import mode_utils
        if is_left:
            temp_conf = self.get_special_temp_conf('invite_message_other')
        else:
            temp_conf = self.get_special_temp_conf('invite_message_me')
        content = global_data.uisystem.create_item(temp_conf)
        extra = data['extra']
        for tab_inde in extra['tab']:
            item = content.list_need.AddTemplateItem(bRefresh=True)
            item.lab_need.SetString(get_text_by_id(chat_const.CHAT_INVITE_TAB_LIST[tab_inde]))

        content.lab_demand.SetString(get_server_text(data['msg']))
        content.btn_join.lab_team_num.SetString('%d/%d' % (extra['num'][0], extra['num'][1]))
        play_type = extra['play_type']
        if play_type == PLAY_TYPE_PVE or play_type == PLAY_TYPE_PVE_EDIT:
            chapter = extra.get('chapter', 1)
            conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter))
            chapter_str = get_text_by_id(conf.get('title_text'))
            difficulty = extra.get('difficulty', 1)
            difficulty_str = get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty])
            battle_config = confmgr.get('battle_config')
            battle_type = extra['battle_type']
            battle_info = battle_config.get(str(battle_type))
            name_text_id = battle_info.get('cNameTID', -1)
            mode_name_str = get_text_by_id(name_text_id)
            content.lab_mode.SetString(get_text_by_id(860328).format(mode_name_str, chapter_str, difficulty_str))
        else:
            name = mode_utils.get_mode_show_name(play_type)
            content.lab_mode.SetString(name)

        @content.btn_join.callback()
        def OnClick(*args):
            from logic.comsys.lobby.TeamHall.TeamHallList import check_join_team
            sender_id = data['sender_info'].get(U_ID, 0)
            if global_data.player.is_in_team():
                global_data.player.notify_client_message((get_text_by_id(11034),))
                return
            send_time = data['extra'].get('time', 0)
            if tutil.get_server_time() - send_time > TEAM_SUMMON_VALID_TIME:
                global_data.player.notify_client_message((get_text_by_id(11041),))
                return
            if self._my_uid == sender_id:
                global_data.player.notify_client_message((get_text_by_id(13067),))
                return
            extra['leader_uid'] = sender_id
            check_join_team(extra)

        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, False)

    def _make_clan_card_msg(self, data, is_left):
        from logic.gutils.template_utils import init_clan_card_msg
        if is_left:
            temp_conf = self.get_special_temp_conf('chat_crew_other_item')
        else:
            temp_conf = self.get_special_temp_conf('chat_crew_me_item')
        content = global_data.uisystem.create_item(temp_conf)
        extra_data = data['extra']
        init_clan_card_msg(content, extra_data)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, True)

    def _make_video_share_msg(self, data, is_left):
        from logic.gutils.template_utils import init_video_share_msg
        if is_left:
            temp_conf = self.get_special_temp_conf('chat_video_others_item')
        else:
            temp_conf = self.get_special_temp_conf('chat_video_me_item')
        content = global_data.uisystem.create_item(temp_conf)
        extra_data = data['extra']
        init_video_share_msg(content, extra_data)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, True)

    def _make_mecha_season_memory_msg(self, data, is_left):
        if is_left:
            temp_conf = self.get_special_temp_conf('i_chat_bp_memory_other_item')
        else:
            temp_conf = self.get_special_temp_conf('i_chat_bp_memory_me_item')
        content = global_data.uisystem.create_item(temp_conf)
        extra_data = data['extra']
        season = extra_data.get('season')
        mecha_id = extra_data.get('mecha_id')
        clothing_id = extra_data.get('clothing_id')
        mem_data = extra_data.get('data', {})
        title = extra_data.get('title', [])

        def on_click_season_memory(*args):
            from logic.comsys.battle_pass.season_memory.SeasonMechaMemoryUI import SeasonMechaMemoryShareUI
            SeasonMechaMemoryShareUI(None, data_dict=extra_data, uid=data['sender_info'].get(U_ID, None), name=data['sender_info'].get(C_NAME, ''))
            return

        content.temp_bp_memory.btn_show.BindMethod('OnClick', on_click_season_memory)
        name = item_utils.get_mecha_name_by_id(mecha_id)
        content.temp_bp_memory.lab_title.SetString(get_text_by_id(634433, [name]))
        mecha_data = mem_data.get('sst_mecha_stat', {}).get(str(mecha_id), {})
        battle_cnt = mecha_data.get('sst_mecha_game_cnt', 0)
        summary_txt = get_text_by_id(634434, [battle_cnt])
        content.lab_msg.SetString(summary_txt)
        from logic.gutils import mecha_skin_utils
        content.temp_bp_memory.pic.SetDisplayFrameByPath('', mecha_skin_utils.get_mecha_pic_path(clothing_id))
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, True)

    def _make_achievement_season_memory_msg(self, data, is_left):
        if is_left:
            temp_conf = self.get_special_temp_conf('i_chat_bp_memory_other_item')
        else:
            temp_conf = self.get_special_temp_conf('i_chat_bp_memory_me_item')
        content = global_data.uisystem.create_item(temp_conf)
        extra_data = data['extra']
        season = extra_data.get('season')
        role_id = extra_data.get('role_id')
        clothing_id = extra_data.get('clothing_id')
        mem_data = extra_data.get('data', {})
        game_time = extra_data.get('game_time', 0)

        def on_click_season_memory(*args):
            from logic.comsys.battle_pass.season_memory.SeasonAchievementMemoryUI import SeasonAchievementMemoryShareUI
            SeasonAchievementMemoryShareUI(None, data_dict=extra_data, uid=data['sender_info'].get(U_ID, None), name=data['sender_info'].get(C_NAME, ''))
            return

        content.temp_bp_memory.btn_show.BindMethod('OnClick', on_click_season_memory)
        content.temp_bp_memory.lab_title.SetString(get_text_by_id(634435))
        summary_txt = get_text_by_id(634436, ['%.1f' % game_time])
        content.lab_msg.SetString(summary_txt)
        from logic.gutils import mecha_skin_utils
        role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        img_path = role_skin_config.get(str(clothing_id), {}).get('half_img_role')
        content.temp_bp_memory.pic.SetDisplayFrameByPath('', img_path)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, True)

    def _make_friend_season_memory_msg(self, data, is_left):
        if is_left:
            temp_conf = self.get_special_temp_conf('i_chat_bp_memory_other_item')
        else:
            temp_conf = self.get_special_temp_conf('i_chat_bp_memory_me_item')
        content = global_data.uisystem.create_item(temp_conf)
        extra_data = data['extra']
        season = extra_data.get('season')
        mem_data = extra_data.get('data', {})

        def on_click_season_memory(*args):
            from logic.comsys.battle_pass.season_memory.SeasonFriendMemoryUI import SeasonFriendMemoryShareUI
            SeasonFriendMemoryShareUI(None, data_dict=extra_data, uid=data['sender_info'].get(U_ID, None), name=data['sender_info'].get(C_NAME, ''))
            return

        content.temp_bp_memory.btn_show.BindMethod('OnClick', on_click_season_memory)
        content.temp_bp_memory.lab_title.SetString(get_text_by_id(634437))
        frd_cnt_list = [ frd_dict.get('sst_frd_game_cnt', 0) for frd_dict in six.itervalues(mem_data.get('sst_frd_stat', {})) ]
        frd_game_cnt = sum(frd_cnt_list)
        summary_txt = get_text_by_id(634438, [frd_game_cnt])
        content.lab_msg.SetString(summary_txt)
        content.temp_bp_memory.pic.setVisible(False)
        content.temp_bp_memory.img_riko.setVisible(True)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, True)

    def _make_room_card_msg(self, data, is_left):
        from logic.gutils.template_utils import init_room_card_msg
        if is_left:
            temp_conf = self.get_special_temp_conf('chat_room_other_item')
        else:
            temp_conf = self.get_special_temp_conf('chat_room_me_item')
        content = global_data.uisystem.create_item(temp_conf)
        extra_data = data['extra']
        init_room_card_msg(content, extra_data)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, True)

    def _make_skin_define_msg(self, data, is_left):
        from logic.gutils.template_utils import init_skin_define_msg
        if is_left:
            temp_conf = self.get_special_temp_conf('i_chat_define_other_item')
        else:
            temp_conf = self.get_special_temp_conf('i_chat_define_me_item')
        content = global_data.uisystem.create_item(temp_conf)
        extra_data = data['extra']
        init_skin_define_msg(content, extra_data)
        size = content.getContentSize()
        content_width = size.width
        return (
         content, size, content_width, True)

    def _make_lucky_lottery_msg(self, data, is_left):
        if is_left:
            temp_conf = self.get_special_temp_conf('i_chat_pigeon_item_lucky_lottery_others')
        else:
            temp_conf = self.get_special_temp_conf('i_chat_pigeon_item_lucky_lottery_me')
        content = global_data.uisystem.create_item(temp_conf)
        size = content.getContentSize()
        content_width = size.width
        extra_data = data.get('extra', {})
        item_list = extra_data.get('item_list', {})
        luck_score_extra_info = extra_data.get('extra_info', {})
        luck_score = luck_score_extra_info.get('luck_score')
        timestamp = luck_score_extra_info.get('luck_timestamp')
        luck_intervene_weight = luck_score_extra_info.get('luck_intervene_weight')
        luck_exceed_percent = luck_score_extra_info.get('luck_exceed_percent')
        lottery_id = extra_data.get('lottery_id')
        sender_info = data.get('sender_info', '')
        player_data = {'uid': sender_info.get('uid'),
           'name': sender_info.get('char_name'),
           'frame_no': sender_info.get('head_frame'),
           'photo_no': sender_info.get('head_photo')
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
            lab_msg = content.nd.lab_msg.setString(get_text_by_id(634668))
        else:
            lottery_str = get_text_by_id(extra_data.get('text_id'))
            lab_msg = content.nd.lab_msg.setString(get_text_by_id(634669).format(activityname=lottery_str))
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
         content, size, content_width, True)

    def play_auto_voice(self, data, channel=None):
        if data.get('voice', None):
            time, arm_key = data['voice'].split('\n', 1)
            sender_uid = data['sender_info'].get(U_ID, None)
            if channel is None:
                voice_channel = self._channel_index if 1 else channel
                if arm_key not in self._unplay_voice:
                    self._unplay_voice.add(arm_key)
                if self._is_auto_voice[voice_channel]:
                    if arm_key not in self._auto_voice_list:
                        global_data.voice_mgr.is_playing() or self.play_voice_msg(arm_key, voice_channel=voice_channel, uid=sender_uid)
                    else:
                        self._auto_voice_list.append((arm_key, sender_uid, voice_channel))
        return

    def update_auto_voice_data_structure(self):
        if len(self._is_auto_voice) < chat_const.CHAT_CHANNEL_NUM:
            self._is_auto_voice += [0] * (chat_const.CHAT_CHANNEL_NUM - len(self._is_auto_voice))
            self._message_data.set_seting_inf('auto_voice', copy.copy(self._is_auto_voice))

    def show_chat_msg_on_head(self, msg, channel):
        if global_data.lobby_player and channel in chat_const.POP_OUT_CHAT:
            msg_data = {'msg': msg}
            global_data.lobby_player.send_event('E_SHOW_CHAT_MESSAGE', msg_data)

    def mod_input_box_pos(self, pos=None):
        if pos:
            self.panel.btn_chat.SetPosition(*pos)
        else:
            self.panel.btn_chat.ReConfPosition()

    def on_resolution_changed(self):
        self.chat_close()
        self.panel.StopAnimation('chat_appear', finish_ani=True)
        self.panel.StopAnimation('chat_hide')
        self._chat_width = self.panel.layer_chat.getContentSize().width
        self._widget_pos = self.panel.layer_chat.getPosition()
        self._chat_pnl_stage = chat_stage_hide
        self.panel.layer_chat.setPosition(cc.Vec2(self._widget_pos.x - self._chat_width, self._widget_pos.y))
        self.panel.layer_chat.setVisible(False)
        self._is_chat_open = False
        x = self.panel.layer_chat.getContentSize().width + 20
        y = self.panel.getContentSize().height - 20
        self._player_simple_inf_pos = cc.Vec2(x, y)

    def init_touch_event(self):
        self.is_in_touch = False
        self._lv_chat.addTouchEventListener(self._on_normal_touch)

    def _on_normal_touch(self, widget, event):
        import ccui
        if event == ccui.WIDGET_TOUCHEVENTTYPE_BEGAN:
            self.is_in_touch = True
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_ENDED:
            self.is_in_touch = False
        elif event == ccui.WIDGET_TOUCHEVENTTYPE_CANCELED:
            self.is_in_touch = False

    def on_open_pve_main_ui(self):
        self.panel.PlayAnimation('btn_appear_pve')

    def on_close_pve_main_ui(self):
        self.panel.PlayAnimation('chat_appear')

    def underage_mode_changed(self, *args):
        from logic.gcommon.common_const import ui_operation_const as uoc
        is_ban = bool(global_data.player.get_setting_2(uoc.UNDERAGE_MODE_KEY))
        self.panel.btn_red_packet.icon_ban.setVisible(is_ban)