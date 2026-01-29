# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/mode_utils.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id

def get_mode_show_name(play_type):
    mode_show_config = confmgr.get('c_battle_mode_show_config', default={})
    for uid, show_conf in six.iteritems(mode_show_config):
        if play_type == show_conf.get('iPlayType'):
            return get_text_by_id(show_conf['cModeName'])

    return ''


def get_sub_modes_by_play_type(play_type):
    mode_show_config = confmgr.get('c_battle_mode_show_config', default={})
    for uid, show_conf in six.iteritems(mode_show_config):
        if play_type == show_conf.get('iPlayType'):
            return show_conf.get('cIncludeModes', [])

    return []


def get_sub_modes_by_show_type(show_type):
    conf = confmgr.get('c_battle_mode_show_config', str(show_type), default={})
    return conf.get('cIncludeModes', [])


def get_mode_show_conf(play_type, team_num):
    mode_show_config = confmgr.get('c_battle_mode_show_config', default={})
    for uid, show_conf in six.iteritems(mode_show_config):
        if play_type == show_conf.get('iPlayType'):
            supportTeamList = show_conf.get('cSupportTeamList', [])
            if supportTeamList:
                if team_num in supportTeamList:
                    return show_conf
            else:
                return show_conf

    return {}


def get_mode_show_type(play_type, team_num, filter_show=False):
    mode_show_config = confmgr.get('c_battle_mode_show_config', default={})
    for uid, show_conf in six.iteritems(mode_show_config):
        is_show = show_conf.get('iShowInChoose', 0) != 0
        if filter_show and not is_show:
            continue
        if play_type == show_conf.get('iPlayType'):
            supportTeamList = show_conf.get('cSupportTeamList', [])
            if supportTeamList:
                if team_num in supportTeamList:
                    return uid
            else:
                return uid

    return None


def get_mapped_res_path(src_res_path):
    ret_res_path = src_res_path
    is_snow_night = global_data.game_mode.is_snow_night_weather()
    if is_snow_night:
        replace_gim_map = confmgr.get('snow_night_res', 'replace_gim_map', default={})
        key = src_res_path.replace('/', '\\')
        if key in replace_gim_map:
            ret_res_path = replace_gim_map[key].replace('\\', '/')
    return ret_res_path