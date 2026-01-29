# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/sys_unlock_data.py
_reload_all = True
if G_IS_NA_PROJECT:
    from .na_sys_unlock_data import *
else:
    cfg_data = {'career': {'show_priority': 1,
                  'unlock_lv': 17,
                  'ui_icon_path': 'gui/ui_res_2/main/new_function_tips/img_sysopen_career_icon.png',
                  'ui_txt_pic_path': 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_career.png',
                  'name_text_id': 82057,
                  'jump_to_ui_info': {'func': 'jump_to_career'},'fly_pos_func': {'func': 'lobby_fly','args': ['get_career_icon_cocos_wpos']},'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_shengya.png',
                  'unlock_growth_tips': 82080
                  },
       'clan': {'show_priority': 1,
                'unlock_lv': 3,
                'ui_icon_path': 'gui/ui_res_2/main/new_function_tips/icon_opensys_crew.png',
                'ui_txt_pic_path': 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_crew.png',
                'name_text_id': 82058,
                'jump_to_ui_info': {'func': 'jump_to_clan_main'},'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_jidongtuan.png',
                'unlock_growth_tips': 82079
                },
       'inscription': {'show_priority': 1,
                       'unlock_lv': 15,
                       'ui_icon_path': 'gui/ui_res_2/main/new_function_tips/icon_opensys_techsystem2.png',
                       'ui_txt_pic_path': 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_techsystem.png',
                       'name_text_id': 82059,
                       'jump_to_ui_info': {'func': 'jump_to_inscription','out_anim': True},'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_keji.png',
                       'unlock_growth_tips': 82085
                       },
       'bond': {'show_priority': 1,
                'unlock_lv': 8,
                'ui_icon_path': 'gui/ui_res_2/main/new_function_tips/icon_opensys_bond.png',
                'ui_txt_pic_path': 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_bond.png',
                'name_text_id': 82060,
                'jump_to_ui_info': {'func': 'jump_to_bond'},'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_jiban.png',
                'unlock_growth_tips': 82081
                },
       'custom_room': {'show_priority': 1,
                       'ui_icon_path': '',
                       'ui_txt_pic_path': '',
                       'name_text_id': 80513,
                       'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_zidingyifang.png',
                       'unlock_growth_tips': 82082
                       },
       'battlepass': {'show_priority': 1,
                      'unlock_lv': 6,
                      'ui_icon_path': 'gui/ui_res_2/main/new_function_tips/img_sysopen_pass_icon.png',
                      'ui_txt_pic_path': 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_pass.png',
                      'name_text_id': 82061,
                      'jump_to_ui_info': {'func': 'jump_to_season_pass','out_anim': True},'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_sncard.png',
                      'unlock_growth_tips': 82085
                      },
       'season_task': {'show_priority': 1,
                       'unlock_lv': 6,
                       'ui_icon_path': '',
                       'ui_txt_pic_path': ''
                       },
       'corp_task': {'show_priority': 1,
                     'unlock_lv': 10,
                     'effective_ts': 1608069600,
                     'ui_icon_path': 'gui/ui_res_2/main/new_function_tips/img_sysopen_commission_icon.png',
                     'ui_txt_pic_path': 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_commission.png',
                     'name_text_id': 602034,
                     'jump_to_ui_info': {'func': 'jump_to_task_ui','args': [4]},'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_weituo.png',
                     'unlock_growth_tips': 82083
                     },
       'credit': {'show_priority': 1,
                  'unlock_lv': 11,
                  'ui_icon_path': 'gui/ui_res_2/main/new_function_tips/img_sysopen_credit_icon.png',
                  'ui_txt_pic_path': 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_credit.png',
                  'name_text_id': 900001,
                  'jump_to_ui_info': {'func': 'jump_to_credit','out_anim': True},'fly_pos_func': {'func': 'lobby_fly','args': ['get_avatar_frame_cocos_wpos']},'ui_growth_icon_path': 'gui/ui_res_2/task/growth_task/icon_growthtask_xinyu.png',
                  'unlock_growth_tips': 82084
                  },
       'survey': {'show_priority': 1,
                  'unlock_lv': 2,
                  'ui_icon_path': '',
                  'ui_txt_pic_path': ''
                  }
       }
    SYS_TYPES = frozenset(cfg_data.keys())
try:
    from mobile.distserver.game import GameServerRepo
    hostnum = lambda : GameServerRepo.hostnum
except:
    hostnum = global_data.channel.get_host_num

def get_system_unlock_lv(system_type):
    return cfg_data.get(system_type, {}).get('unlock_lv', 0)


def is_system_disable(system_type):
    if system_type not in cfg_data:
        return False
    data = cfg_data[system_type]
    if 'disable_hostnums' in data and hostnum() in data['disable_hostnums']:
        return True
    if 'enable_hostnums' in data and hostnum() not in data['enable_hostnums']:
        return True
    return False


def check_system_unlock(system_type, avatar):
    if not avatar:
        return False
    else:
        data = cfg_data.get(system_type, None)
        if not data:
            return True
        if is_system_disable(system_type):
            return False
        create_time_limit = data.get('create_time_limit', None)
        if create_time_limit and avatar.get_create_time() >= create_time_limit:
            return False
        effective_ts = data.get('effective_ts', None)
        if effective_ts and avatar.get_create_time() < effective_ts:
            return True
        unlock_lv = data.get('unlock_lv', None)
        if unlock_lv and avatar.get_lv() < unlock_lv:
            return False
        return True