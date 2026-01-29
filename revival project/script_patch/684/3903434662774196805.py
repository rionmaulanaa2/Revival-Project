# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoKill.py
from __future__ import absolute_import
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_TYPE_MESSAGE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import battle_const
import cc
from logic.client.const import game_mode_const

class BattleInfoKill(BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle/fight_kill_tips'
    UI_TYPE = UI_TYPE_MESSAGE

    def init_parameters(self):
        super(BattleInfoKill, self).init_parameters()

    def process_one_message(self, message, finish_cb):
        msg_dict = message[0]
        is_knock_down = msg_dict.get('is_knock_down', False)
        is_kill = msg_dict.get('is_kill', False)
        is_kill_mecha = msg_dict.get('is_kill_mecha', False)
        is_being_knock_down = msg_dict.get('is_being_knock_down', False)
        is_being_kill = msg_dict.get('is_being_kill', False)
        is_self = msg_dict.get('is_self', False)
        is_assist = msg_dict.get('is_assist', False)
        is_critic = msg_dict.get('is_critic', False)
        msg = msg_dict.get('msg', '')
        type_msg = msg_dict.get('type_msg', '')
        kill_num = msg_dict.get('kill_num', 0)
        points = msg_dict.get('points', 0)
        is_mecha_being_kill = msg_dict.get('is_mecha_being_kill', False)
        kill_mecha_num = None
        kill_mecha_points = None
        if is_kill_mecha:
            kill_mecha_num = kill_num
            kill_mecha_points = points
        kill_player_num = None
        kill_player_points = None
        if is_kill:
            kill_player_num = kill_num
            kill_player_points = points
        icon_path = ''
        if kill_player_num:
            icon_path = 'gui/ui_res_2/battle_banshu/notice/icon_msg_kill.png'
            is_self and self.play_kill_player_voice(kill_num)
        elif kill_mecha_num:
            icon_path = 'gui/ui_res_2/battle/notice/icon_msg_mech_kill_blue.png'
            is_self and self.play_kill_mecha_voice()
        elif is_knock_down or is_being_knock_down:
            icon_path = 'gui/ui_res_2/battle/notice/icon_msg_down.png'
        elif is_being_kill:
            icon_path = 'gui/ui_res_2/battle_banshu/notice/icon_msg_kill.png'
        elif is_mecha_being_kill:
            icon_path = 'gui/ui_res_2/battle/notice/icon_msg_mech_kill.png'
        if is_assist:
            icon_path = 'gui/ui_res_2/battle/notice/icon_msg_mech_kda.png'
        bar_path = self.get_message_bar_path(is_knock_down, is_being_knock_down, is_kill, is_being_kill, is_kill_mecha, is_self)
        message = {'i_type': battle_const.MED_KILL_INFO,
           'content_txt': msg,
           'icon_path': icon_path,
           'bar_path': bar_path
           }
        if global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_HUNTING:
            message['panel_self_attr_dict'] = {'func_name': 'setScale','args': (1.0, )}
        self.main_process_one_message((message,), finish_cb)
        return

    def get_message_bar_path(self, is_knock_down, is_being_knock_down, is_kill, is_being_kill, is_kill_mecha, is_self):
        DEFAULT_BAR_PATH = 'gui/ui_res_2/battle/notice/bar_kill_me.png'
        if is_being_knock_down or is_being_kill:
            return 'gui/ui_res_2/battle/notice/bar_kill_me.png'
        if is_knock_down or is_kill or is_kill_mecha:
            if is_self:
                return 'gui/ui_res_2/battle/notice/bar_kill_blue.png'
            else:
                return 'gui/ui_res_2/battle/notice/bar_teammate_kill.png'

        return DEFAULT_BAR_PATH

    def play_kill_player_voice(self, kill_num):
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'achievement_level3'))
        if kill_num >= 5:
            global_data.emgr.play_virtual_anchor_voice.emit('vo5_1')
        else:
            global_data.emgr.play_virtual_anchor_voice.emit('vo5_2')

    def play_kill_mecha_voice(self):
        global_data.emgr.play_virtual_anchor_voice.emit('vo4_2')
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'achievement_level2'))