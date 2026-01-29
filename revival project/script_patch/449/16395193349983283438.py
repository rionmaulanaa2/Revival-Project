# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/screen_effect_utils.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.const import SFX_FULL_SCREEN_SIZE
from common.framework import Functor
import math3d
import world
SCREEN_EFFECT_SCALE = None
IS_SCREEN_EFFECT_FLAG = dict()
SCREEN_EFFECT_DATA = dict()
DEFAULT_KEY = 'default'
CUR_TARGET_ID = None

def refresh_screen_effect_scale_value--- This code section failed: ---

  23       0  LOAD_GLOBAL           0  'math3d'
           3  LOAD_ATTR             1  'vector'
           6  LOAD_ATTR             1  'vector'
           9  BINARY_SUBSCR    
          10  LOAD_GLOBAL           2  'SFX_FULL_SCREEN_SIZE'
          13  LOAD_CONST            1  ''
          16  BINARY_SUBSCR    
          17  BINARY_DIVIDE    
          18  BINARY_DIVIDE    
          19  BINARY_DIVIDE    
          20  BINARY_DIVIDE    
          21  BINARY_SUBSCR    
          22  LOAD_GLOBAL           2  'SFX_FULL_SCREEN_SIZE'
          25  LOAD_CONST            2  1
          28  BINARY_SUBSCR    
          29  BINARY_DIVIDE    
          30  LOAD_CONST            3  1.0
          33  CALL_FUNCTION_3       3 
          36  STORE_GLOBAL          3  'SCREEN_EFFECT_SCALE'

Parse error at or near `BINARY_SUBSCR' instruction at offset 9


def _create_screen_effect_callback(sfx, effect_path, on_create_func):
    global SCREEN_EFFECT_SCALE
    global IS_SCREEN_EFFECT_FLAG
    if effect_path in IS_SCREEN_EFFECT_FLAG:
        if IS_SCREEN_EFFECT_FLAG[effect_path]:
            sfx.scale = SCREEN_EFFECT_SCALE
    else:
        flag = True
        for i in range(sfx.get_subfx_count()):
            if sfx.get_sub_type(i) == world.FX_TYPE_CAMERASHAKE:
                flag = False
                break

        if flag:
            sfx.scale = SCREEN_EFFECT_SCALE
        IS_SCREEN_EFFECT_FLAG[effect_path] = flag
    callable(on_create_func) and on_create_func(sfx)


def create_screen_effect_directly--- This code section failed: ---

  51       0  LOAD_FAST             1  'pos'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            8  'is'
           9  POP_JUMP_IF_FALSE    36  'to 36'

  52      12  LOAD_GLOBAL           1  'math3d'
          15  LOAD_ATTR             2  'vector'
          18  LOAD_CONST            1  ''
          21  LOAD_CONST            1  ''
          24  LOAD_CONST            1  ''
          27  CALL_FUNCTION_3       3 
          30  STORE_FAST            1  'pos'
          33  JUMP_FORWARD          0  'to 36'
        36_0  COME_FROM                '33'

  53      36  LOAD_GLOBAL           3  'global_data'
          39  LOAD_ATTR             4  'sfx_mgr'
          42  LOAD_ATTR             5  'create_sfx_in_scene'

  54      45  LOAD_FAST             0  'effect_path'
          48  LOAD_FAST             1  'pos'
          51  LOAD_CONST            2  'on_create_func'
          54  LOAD_GLOBAL           6  'Functor'
          57  LOAD_GLOBAL           7  '_create_screen_effect_callback'
          60  LOAD_CONST            3  'effect_path'
          63  LOAD_CONST            2  'on_create_func'
          66  LOAD_FAST             2  'on_create_func'
          69  CALL_FUNCTION_513   513 
          72  LOAD_CONST            4  'on_remove_func'
          75  LOAD_FAST             3  'on_remove_func'
          78  CALL_FUNCTION_514   514 
          81  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_513' instruction at offset 69


def create_screen_effect_with_auto_refresh(owner_id, effect_path, key=DEFAULT_KEY):
    global CUR_TARGET_ID
    if owner_id is None:
        return
    else:
        if owner_id not in SCREEN_EFFECT_DATA:
            if not SCREEN_EFFECT_DATA:
                global_data.emgr.scene_observed_player_setted_event += refresh_screen_effect
            SCREEN_EFFECT_DATA[owner_id] = dict()
            SCREEN_EFFECT_DATA[owner_id][key] = dict()
        if global_data.cam_lplayer and global_data.cam_lplayer.id == owner_id:
            if effect_path in SCREEN_EFFECT_DATA[owner_id][key]:
                old_sfx_id = SCREEN_EFFECT_DATA[owner_id][key][effect_path]
                if old_sfx_id and global_data.sfx_mgr.get_sfx_by_id(old_sfx_id):
                    return
            sfx_id = create_screen_effect_directly(effect_path)
            CUR_TARGET_ID = owner_id
        else:
            sfx_id = None
        SCREEN_EFFECT_DATA[owner_id][key][effect_path] = sfx_id
        return sfx_id


def remove_screen_effect_with_auto_refresh(owner_id, effect_path, key=DEFAULT_KEY):
    if owner_id not in SCREEN_EFFECT_DATA:
        return
    if key not in SCREEN_EFFECT_DATA[owner_id]:
        return
    if effect_path not in SCREEN_EFFECT_DATA[owner_id][key]:
        return
    sfx_id = SCREEN_EFFECT_DATA[owner_id][key][effect_path]
    if sfx_id:
        global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
    SCREEN_EFFECT_DATA[owner_id][key].pop(effect_path)


def remove_all_screen_effect_with_auto_refresh(owner_id):
    if owner_id not in SCREEN_EFFECT_DATA:
        return
    for effect_map in six.itervalues(SCREEN_EFFECT_DATA[owner_id]):
        for sfx_id in six.itervalues(effect_map):
            if sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

    SCREEN_EFFECT_DATA.pop(owner_id)
    if not SCREEN_EFFECT_DATA:
        global_data.emgr.scene_observed_player_setted_event -= refresh_screen_effect


def remember_screen_effect(owner_id):
    if owner_id is None:
        return
    else:
        for effect_map in six.itervalues(SCREEN_EFFECT_DATA.get(owner_id, {})):
            for effect_path, sfx_id in six.iteritems(effect_map):
                if sfx_id:
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                effect_map[effect_path] = None

        return


def recover_screen_effect(owner_id):
    if owner_id is None:
        return
    else:
        for effect_map in six.itervalues(SCREEN_EFFECT_DATA.get(owner_id, {})):
            for effect_path, sfx_id in six.iteritems(effect_map):
                if sfx_id is None:
                    effect_map[effect_path] = create_screen_effect_directly(effect_path)

        return


def refresh_screen_effect(new_cam_target):
    global CUR_TARGET_ID
    remember_screen_effect(CUR_TARGET_ID)
    if new_cam_target:
        new_target_id = new_cam_target.id
        recover_screen_effect(new_target_id)
        CUR_TARGET_ID = new_target_id