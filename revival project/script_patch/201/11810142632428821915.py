# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/system_unlock_utils.py
from __future__ import absolute_import
SYSTEM_CAREER = 'career'
SYSTEM_CLAN = 'clan'
SYSTEM_BOND = 'bond'
SYSTEM_INSCRIPTION = 'inscription'
SYSTEM_CUSTOM_ROOM = 'custom_room'
SYSTEM_BATTLE_PASS = 'battlepass'
SYSTEM_ASSESS_TASK = 'assess_task'
SYSTEM_SEASON_TASK = 'season_task'
SYSTEM_CORP_TASK = 'corp_task'
SYSTEM_CREDIT = 'credit'
SYS_2_UI_DICT = {'ClanMainUI': {'sys': SYSTEM_CLAN
                  },
   'ClanJoinMainUI': {'sys': SYSTEM_CLAN
                      },
   'SeasonPassLevelUp': {'sys': SYSTEM_BATTLE_PASS,
                         'no_tips': True
                         },
   'BpAdvisementUI': {'sys': SYSTEM_BATTLE_PASS
                      }
   }

def get_sys_unlock_level(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    unlock_lv = su_data.cfg_data.get(sys_type, {}).get('unlock_lv', None)
    return (
     unlock_lv is not None, unlock_lv)


def get_sys_unlock_effective_ts(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    et_ts = su_data.cfg_data.get(sys_type, {}).get('effective_ts', None)
    return (
     et_ts is not None, et_ts)


def _get_is_sys_disabled(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    return su_data.cfg_data.get(sys_type, {}).get('is_disable', False)


def has_sys_unlock_mechanics(sys_type):
    sub_player = global_data.player
    if not sub_player:
        return False
    else:
        has_et, et_ts = get_sys_unlock_effective_ts(sys_type)
        if has_et and sub_player.get_create_time() <= et_ts:
            return False
        return True


def is_sys_unlocked(sys_type):
    from logic.gcommon.cdata.sys_unlock_data import check_system_unlock
    return check_system_unlock(sys_type, global_data.player)


def get_sys_unlock_ui_pics(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    icon_path = su_data.cfg_data.get(sys_type, {}).get('ui_icon_path', '')
    text_pic_path = su_data.cfg_data.get(sys_type, {}).get('ui_txt_pic_path', '')
    return (
     icon_path, text_pic_path)


def get_sys_unlock_growth_icon(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    icon_path = su_data.cfg_data.get(sys_type, {}).get('ui_growth_icon_path', '')
    return icon_path


def get_sys_unlock_growth_tip(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    return su_data.cfg_data.get(sys_type, {}).get('unlock_growth_tips', 0)


def get_sys_name_text_id(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    return su_data.cfg_data.get(sys_type, {}).get('name_text_id', -1)


def get_sys_jump_info(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    return su_data.cfg_data.get(sys_type, {}).get('jump_to_ui_info', {})


def get_sys_unlock_fly_func_info(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    return su_data.cfg_data.get(sys_type, {}).get('fly_pos_func', None)


def get_ui_unlock(ui_class_name):
    if ui_class_name not in SYS_2_UI_DICT:
        return True
    info = SYS_2_UI_DICT[ui_class_name]
    sys_type = info['sys']
    has_unlock = is_sys_unlocked(sys_type)
    return has_unlock


def can_open_ui(ui_class_name):
    has_unlock = get_ui_unlock(ui_class_name)
    if not has_unlock:
        info = SYS_2_UI_DICT[ui_class_name]
        sys_type = info['sys']
        if not info.get('no_tips', False):
            show_sys_unlock_tips(sys_type)
    return has_unlock


def is_sys_no_prompt(sys_type):
    from logic.gcommon.cdata import sys_unlock_data as su_data
    return not bool(su_data.cfg_data.get(sys_type, {}).get('ui_icon_path', ''))


def show_sys_unlock_tips(sys_type):
    sub_player = global_data.player
    if not sub_player:
        return
    has, unlock_lv = get_sys_unlock_level(sys_type)
    unlocked = not has or sub_player.get_lv() >= unlock_lv
    if not unlocked:
        global_data.game_mgr.show_tip(get_text_by_id(603007).format(unlock_lv))
        return