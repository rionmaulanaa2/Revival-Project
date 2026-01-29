# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_const/setting_const.py
from __future__ import absolute_import
import six
import six_ex
_reload_all = True
from . import ui_operation_const as uoc
SETTING_BASE = 'base'
SETTING_SST = 'sst'
SETTING_OPT = 'opt'
SETTING_VEH = 'vehicle'
SETTING_QUALITY = 'quality'
SETTING_VOICE = 'voice'
SETTING_VIDEO = 'high_video'
SYNC_KEYS = {
 SETTING_BASE, SETTING_OPT, SETTING_VEH, SETTING_VIDEO}
SETTING_KEYS = {SETTING_BASE: {
                uoc.LF_OPE_KEY, uoc.GYROSCOPE_STATE_KEY, uoc.AUTO_OPEN_DOOR, uoc.AIM_HELPER_KEY, uoc.AUTO_PICK_KEY,
                uoc.FREE_SIGHT_KEY, uoc.ROCKER_DASH, uoc.SOUND_VISIBLE_3D_KEY, uoc.INJURE_VISIBLE_3D_KEY,
                uoc.BLOCK_STRANGER_VISIT, uoc.ENABLE_STRANGER_LEFT_MSG, uoc.ENABLE_REWARD_FRIEND_REPORT, uoc.BLOCK_ALL_MSG_KEY,
                uoc.TEAM_ONLY_FRIEND_KEY, uoc.DANMU_SHOW_DEFAULT_HEAD},
   SETTING_SST: {
               uoc.SST_FROCKER_KEY, uoc.SST_SCR_KEY, uoc.SST_AIM_RD_KEY, uoc.SST_AIM_2M_KEY, uoc.SST_AIM_4M_KEY,
               uoc.SST_AIM_6M_KEY, uoc.SST_MECHA_07_KEY, uoc.SST_FS_ROCKER_KEY, uoc.SST_GYROSCOPE_SCR_KEY,
               uoc.SST_GYROSCOPE_RD_KEY, uoc.SST_GYROSCOPE_2M_KEY, uoc.SST_GYROSCOPE_4M_KEY,
               uoc.SST_GYROSCOPE_6M_KEY, uoc.SST_MECHA_ACTION1, uoc.ThreeD_TOUCH_PERCENT_KEY, uoc.SST_AUTO_HELP_KEY},
   SETTING_OPT: {
               uoc.FIREROCKER_OPE_KEY, uoc.ThreeD_TOUCH_TOGGLE_KEY, uoc.NEWBIE_PASS_HIDE_UI},
   SETTING_VEH: {
               uoc.DRIVE_OPE_KEY, uoc.DRIVE_OPE_BUTTON_DIR_KEY},
   SETTING_QUALITY: {
                   uoc.QUALITY_LEVEL_KEY, uoc.PVE_QUALITY_LEVEL_KEY, uoc.QUALITY_HIGH_FRAME_RATE_KEY, uoc.QUALITY_RESOLUTION_KEY, uoc.QUALITY_RESOLUTION_KEY_KONGDAO,
                   uoc.QUALITY_SHADOWMAP_KEY, uoc.QUALITY_HDR_KEY, uoc.QUALITY_MSAA_KEY, uoc.QUALITY_RADIAL_BLUR_KEY},
   SETTING_VIDEO: {
                 uoc.HIGH_LIGHT_KEY, uoc.HIGH_LIGHT_TIMES_KEY}
   }
INSTANT_CACHE_KEYS = (
 uoc.BLOCK_STRANGER_VISIT, uoc.ENABLE_STRANGER_LEFT_MSG, uoc.REVEAL_MECHA_MEMORY_RECORD_KEY, uoc.BLOCK_ALL_MSG_KEY)
KEYS2TAG = {}

def gen_key_to_tag():
    for main_key, key_set in six.iteritems(SETTING_KEYS):
        for key in key_set:
            KEYS2TAG[key] = main_key


gen_key_to_tag()
DESIGN_SCREEN_WIDTH = 'design_screen_width'
RESOLUTION = 'resolution'
BASE_KEYS_POOL_2 = set()
for key_ref in SYNC_KEYS:
    if key_ref in SETTING_KEYS:
        BASE_KEYS_POOL_2 = BASE_KEYS_POOL_2 | SETTING_KEYS[key_ref]

from logic.gcommon.common_const.ui_operation_const import SETTINGS_USE_NEW_2_API_FOR_OLD_CALLSITE
for key in SETTINGS_USE_NEW_2_API_FOR_OLD_CALLSITE:
    BASE_KEYS_POOL_2.add(key)

def get_mecha_id_variant(mecha_id, key):
    return key + '_' + str(mecha_id)


def get_mecha_type_ids():
    if G_IS_SERVER:
        from data import mecha_conf
        return [ int(e) for e in mecha_conf.get_all_mecha_ids() ]
    else:
        from common.cfg import confmgr
        str_keys = six_ex.keys(confmgr.get('mecha_conf', 'MechaConfig', 'Content'))
        return [ int(e) for e in str_keys ]


def gen_mecha_sens_base_keys_pool_2():
    ret = set()
    from logic.gcommon.common_const.ui_operation_const import MECHA_SENS_KEYS
    all_mecha_type_ids = get_mecha_type_ids()
    for key in MECHA_SENS_KEYS:
        for mecha_type_id in all_mecha_type_ids:
            ret.add(get_mecha_id_variant(mecha_type_id, key))

    return ret


MECHA_SENS_BASE_KEYS_POOL_2 = frozenset(gen_mecha_sens_base_keys_pool_2())
BASE_KEYS_POOL_2 = BASE_KEYS_POOL_2 | MECHA_SENS_BASE_KEYS_POOL_2
BASE_KEYS_POOL_2 = BASE_KEYS_POOL_2 | SETTING_KEYS[SETTING_VEH]
BASE_KEYS_POOL_2 = BASE_KEYS_POOL_2 | SETTING_KEYS[SETTING_QUALITY]
BASE_KEYS_POOL_2 = BASE_KEYS_POOL_2 | SETTING_KEYS[SETTING_SST]
BASE_KEYS_POOL_2 = frozenset(BASE_KEYS_POOL_2)

def is_setting_key_valid_2(raw_key):
    if raw_key in BASE_KEYS_POOL_2:
        return True
    for base_key in BASE_KEYS_POOL_2:
        if get_pc_platform_variant(base_key) == raw_key:
            return True

    return False


def get_pc_platform_variant(key):
    return 'pc/' + key