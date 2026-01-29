# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/FightTeamQuickChat.py
from __future__ import absolute_import
import math
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.client.const.game_mode_const import GAME_MODE_SURVIVALS, GAME_MODE_DEATHS, GAME_MODE_PVES

class FightTeamQuickChat(object):
    CHOOSE_LIST_ROLE_ID = '0'
    DEFAULT_LIST_ROLE_ID = '0'

    @classmethod
    def get_choose_chat_list(cls):
        conf = confmgr.get('team_quick_chat', cls.CHOOSE_LIST_ROLE_ID)
        return cls.get_chat_content_list(conf)

    @classmethod
    def get_chat_content_list(cls, role_conf):
        chat_content = []
        chat_order = None
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type in GAME_MODE_SURVIVALS:
            chat_order = role_conf.get('1_order')
        elif mode_type in GAME_MODE_DEATHS:
            chat_order = role_conf.get('2_order')
        elif mode_type in GAME_MODE_PVES:
            chat_order = role_conf.get('3_order')
        if chat_order is None:
            chat_order = role_conf['order']
        if mode_type not in GAME_MODE_PVES:
            custom_order = global_data.player.get_setting_2(uoc.SHORTCUT_ORDER) if global_data.player else None
            if custom_order:
                chat_order_temp = [ shortcut_id for shortcut_id in custom_order ]
                chat_order_temp.extend([ shortcut_id for shortcut_id in chat_order if shortcut_id not in chat_order_temp ])
                chat_order = chat_order_temp
        for quick_chat_id in chat_order:
            quick_chat_conf = role_conf[str(quick_chat_id)]
            if not cls.is_chat_visible(quick_chat_conf):
                continue
            chat_str = cls.get_chat_str(quick_chat_conf)
            chat_content.append((quick_chat_id, chat_str))

        return chat_content

    @classmethod
    def is_chat_visible(cls, chat_conf):
        show_func_str = chat_conf.get('show_func', None)
        if not show_func_str:
            return True
        else:
            show_func = getattr(cls, show_func_str, None)
            if not show_func:
                log_error('FightTeamQuickChat - show_func not config: ', show_func_str)
                return False
            return show_func()

    @classmethod
    def get_chat_str(cls, chat_conf):
        text_id = chat_conf['text_id']
        process_func_str = chat_conf.get('process_func', '')
        process_func = getattr(cls, process_func_str, None)
        if not process_func:
            return get_text_by_id(text_id)
        else:
            _, text_id_args = process_func(text_id)
            return get_text_by_id(text_id, args=text_id_args)

    @classmethod
    def get_chat_text_id(cls, chat_conf):
        text_id = chat_conf['text_id']
        process_func_str = chat_conf.get('process_func', '')
        process_func = getattr(cls, process_func_str, None)
        if not process_func:
            return (text_id, None)
        else:
            return process_func(text_id)

    @classmethod
    def get_role_chat_str(cls, role_id, chat_id):
        conf = confmgr.get('team_quick_chat', str(role_id))
        if not conf:
            conf = confmgr.get('team_quick_chat', '0')
        quick_chat_conf = conf.get(str(chat_id), None)
        return cls.get_chat_text_id(quick_chat_conf if quick_chat_conf else confmgr.get('team_quick_chat', '0').get(str(chat_id), None))

    @classmethod
    def get_role_chat_trigger_type(cls, role_id, chat_id):
        conf = confmgr.get('team_quick_chat', str(role_id))
        if not conf:
            conf = confmgr.get('team_quick_chat', '0')
        quick_chat_conf = conf[str(chat_id)] if conf.get(str(chat_id)) else confmgr.get('team_quick_chat', '0').get(str(chat_id))
        return quick_chat_conf.get('trigger_type')

    @classmethod
    def mecha_ready(cls):
        if global_data.player and global_data.player.logic:
            _cd_type, _total_cd, left_time = global_data.player.logic.ev_g_get_change_state()
            return left_time <= 0
        else:
            return False

    @classmethod
    def mecha_not_ready(cls):
        return not cls.mecha_ready()

    @classmethod
    def mecha_count_down(cls, text_id):
        if global_data.player and global_data.player.logic:
            _cd_type, _total_cd, left_time = global_data.player.logic.ev_g_get_change_state()
        else:
            left_time = 0
        return (
         text_id, {'second': int(math.ceil(left_time))})