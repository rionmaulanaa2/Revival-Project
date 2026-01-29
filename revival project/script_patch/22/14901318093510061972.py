# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/granbelm_utils.py
from __future__ import absolute_import
from logic.gcommon.common_const.battle_const import GRANBELM_PORTAL_TYPE_POISON, GRANBELM_PORTAL_TYPE_PARADROP, GRANBELM_PORTAL_FIRST_TELEPORT, GRANBELM_PORTAL_SECOND_TELEPORT, GRANBELM_PORTAL_TELE_ROLE_HUMAN, GRANBELM_PORTAL_TELE_ROLE_MECHA
from logic.client.const.camera_const import AIM_MODE
from logic.units.LMecha import LMecha
from common.cfg import confmgr
GRANBELM_SCREEN_SFX_PATH = {GRANBELM_PORTAL_TYPE_POISON: 'effect/fx/scenes/common/manyue/chuansong_skcs_red.sfx',
   GRANBELM_PORTAL_TYPE_PARADROP: 'effect/fx/scenes/common/manyue/chuansong_skcs_blue.sfx'
   }
GRANBELM_TELE_SFX_PATH = {GRANBELM_PORTAL_TYPE_POISON: {GRANBELM_PORTAL_TELE_ROLE_HUMAN: 'effect/fx/scenes/common/manyue/chuansong_fz_red_human',
                                 GRANBELM_PORTAL_TELE_ROLE_MECHA: 'effect/fx/scenes/common/manyue/chuansong_fz_red_mecha'
                                 },
   GRANBELM_PORTAL_TYPE_PARADROP: {GRANBELM_PORTAL_TELE_ROLE_HUMAN: 'effect/fx/scenes/common/manyue/chuansong_fz_blue_human',
                                   GRANBELM_PORTAL_TELE_ROLE_MECHA: 'effect/fx/scenes/common/manyue/chuansong_fz_blue_mecha'
                                   }
   }
GRANBELM_TELE_SOUND_MAP = {GRANBELM_PORTAL_TYPE_POISON: ('portal1_process', 'portal1_completed'),
   GRANBELM_PORTAL_TYPE_PARADROP: ('portal2_process', 'portal2_completed')
   }
RUNE_PIC_PATH = {False: 'gui/ui_res_2/battle/moon/icon_gear_lock.png',
   True: 'gui/ui_res_2/battle/moon/icon_gear_unlock.png'
   }
RUNE_ABILITY_DISPLAY_DICT = {0: {'name': 19620,
       'path': 'gui/ui_res_2/battle/moon/icon_talent_1.png',
       'desc': 19621,
       'id': 459
       },
   1: {'name': 19622,
       'path': 'gui/ui_res_2/battle/moon/icon_talent_2.png',
       'desc': 17511,
       'id': 460
       },
   2: {'name': 19624,
       'path': 'gui/ui_res_2/battle/moon/icon_talent_3.png',
       'desc': 19625,
       'id': 461
       },
   3: {'name': 19626,
       'path': 'gui/ui_res_2/battle/moon/icon_talent_4.png',
       'desc': 19627,
       'id': 462
       },
   4: {'name': 19628,
       'path': 'gui/ui_res_2/battle/moon/icon_talent_5.png',
       'desc': 19629,
       'id': 463
       }
   }
RUNE_ABILITY_DICT = {459: {'desc': 19621,
         'path': 'gui/ui_res_2/battle/moon/icon_talent_1.png'
         },
   460: {'desc': 17511,
         'path': 'gui/ui_res_2/battle/moon/icon_talent_2.png'
         },
   461: {'desc': 19625,
         'path': 'gui/ui_res_2/battle/moon/icon_talent_3.png'
         },
   462: {'desc': 19627,
         'path': 'gui/ui_res_2/battle/moon/icon_talent_4.png'
         },
   463: {'desc': 19629,
         'path': 'gui/ui_res_2/battle/moon/icon_talent_5.png'
         }
   }

def get_tele_screen_sfx_path(portal_type):
    if portal_type in GRANBELM_SCREEN_SFX_PATH:
        return GRANBELM_SCREEN_SFX_PATH.get(portal_type)


def get_tele_sfx_path(portal_type, tele_role, tele_stage):
    path = GRANBELM_TELE_SFX_PATH.get(portal_type).get(tele_role)
    if tele_stage == GRANBELM_PORTAL_FIRST_TELEPORT:
        return path + '_1.sfx'
    return path + '_2.sfx'


def get_tele_sound_map(portal_type, tag):
    map_list = GRANBELM_TELE_SOUND_MAP.get(portal_type)
    return map_list[tag]


def get_region_model_path(region_level):
    region_model_dict = confmgr.get('script_gim_ref')['granbelm_region_range']
    key = str(region_level)
    if key in region_model_dict:
        return region_model_dict[key]


def get_rune_pic_path(is_finish):
    return RUNE_PIC_PATH.get(is_finish)


def get_rune_ability_display_dict_all():
    return RUNE_ABILITY_DISPLAY_DICT


def get_rune_ability_display_dict(index):
    return RUNE_ABILITY_DISPLAY_DICT.get(index, None)


def get_rune_ability_dict(rune_id):
    return RUNE_ABILITY_DICT.get(rune_id)


def check_switch_model_visible():
    if global_data.game_mgr.scene.get_com('PartCamera').get_cur_camera_state_type() in (AIM_MODE,):
        return False
    target = global_data.cam_lplayer.ev_g_control_target()
    if target and target.logic and type(target.logic) == LMecha:
        return False
    return True