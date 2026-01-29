# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/perform_sdk.py
from __future__ import absolute_import
import six
import render
import game3d
import profiling
from version import get_cur_version_str
from common.platform.device_info import DeviceInfo
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import ui_operation_const
THREE_TRUNK = NEOX_UNIT_SCALE * 64 * 2
TEAM_BATTLE_DIST = THREE_TRUNK * THREE_TRUNK
TEAM_BATTLE_NUM = 4
last_is_team_battle = False

def query_perform_sdk_valid():
    js_dict = {'methodId': 'isPerformanceValid'
       }
    global_data.channel.extend_func_by_dict(js_dict)


def update_game_info(scene_id=0):
    if not global_data.channel or not global_data.channel.perform_sdk_valid:
        return
    device_manufacturer = DeviceInfo().get_device_manufacturer()
    app_version = get_cur_version_str()
    if device_manufacturer == 'vivo':
        js_dict = {'methodId': 'updateGameInfo','1': str(app_version),
           '2': str(scene_id),
           '3': str(profiling.get_render_rate()),
           '5': _get_vivo_quality(),
           '10': '1',
           '11': str(game3d.get_frame_rate()),
           '12': _get_resolution_setting()
           }
        if hasattr(render, 'get_render_thread_id'):
            render_id = render.get_render_thread_id()
            if render_id > 0:
                js_dict['14'] = str(render_id)
        global_data.channel.extend_func_by_dict(js_dict)


def _get_vivo_quality--- This code section failed: ---

  67       0  LOAD_CONST            1  ''
           3  STORE_FAST            0  'quality'

  68       6  LOAD_GLOBAL           0  'global_data'
           9  LOAD_ATTR             1  'player'
          12  POP_JUMP_IF_FALSE    39  'to 39'

  69      15  LOAD_GLOBAL           0  'global_data'
          18  LOAD_ATTR             1  'player'
          21  LOAD_ATTR             2  'get_setting'
          24  LOAD_GLOBAL           3  'ui_operation_const'
          27  LOAD_ATTR             4  'QUALITY_LEVEL_KEY'
          30  CALL_FUNCTION_1       1 
          33  STORE_FAST            0  'quality'
          36  JUMP_FORWARD          0  'to 39'
        39_0  COME_FROM                '36'

  70      39  BUILD_MAP_4           4 

  71      42  LOAD_CONST            2  '2'
          45  LOAD_CONST            1  ''
          48  STORE_MAP        
          49  LOAD_CONST            3  '1'
          52  LOAD_CONST            4  1
          55  STORE_MAP        
          56  LOAD_CONST            5  '0'
          59  LOAD_CONST            6  2
          62  STORE_MAP        
          63  LOAD_CONST            5  '0'
          66  LOAD_CONST            7  3
          69  STORE_MAP        
          70  STORE_FAST            1  'quality_dict'

  73      73  LOAD_FAST             1  'quality_dict'
          76  LOAD_ATTR             5  'get'
          79  LOAD_ATTR             5  'get'
          82  CALL_FUNCTION_2       2 
          85  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 82


def _get_resolution_setting():
    from logic.gcommon.common_const import ui_operation_const
    resolution_code = global_data.player.get_setting(ui_operation_const.QUALITY_RESOLUTION_KEY, default=0)
    resolution_dict = {0: '2',
       1: '1',2: '0',3: '0'}
    return resolution_dict.get(int(resolution_code), '0')


def is_in_team_fight():
    cam = global_data.game_mgr.scene.active_camera
    if global_data.cam_lplayer and cam:
        nums = 0
        war_mechas = global_data.war_mechas
        for mecha in six.itervalues(war_mechas):
            if not mecha:
                continue
            model = mecha.ev_g_model()
            if model:
                target_direction = model.position - cam.position
                if target_direction.is_zero:
                    nums += 1
                elif target_direction.length_sqr <= TEAM_BATTLE_DIST:
                    nums += 1
            if nums >= TEAM_BATTLE_NUM:
                return True

    return False


def battle_begin():
    global last_is_team_battle
    last_is_team_battle = None
    return


def refresh_team_battle_info():
    global last_is_team_battle
    if not global_data.player.is_in_battle():
        return
    is_team_fight = is_in_team_fight()
    if is_team_fight == last_is_team_battle:
        return
    last_is_team_battle = is_team_fight
    scene_id = 8 if is_team_fight else 7
    update_game_info(scene_id)