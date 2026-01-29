# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/preload_login_conf_utils.py
from __future__ import absolute_import
from common.cfg import confmgr
PRELOAD_CONF = [
 'lobby_item',
 'task/task_data',
 'common_reward_data',
 'mall_config',
 'mecha_conf',
 'scene_model_inf',
 'item_control/bw_all06/house_info',
 'firearm_config',
 'firearm_res_config',
 'item_control/kongdao/house_info',
 'c_env_config',
 'grenade_config',
 'role_info',
 'item',
 'c_activity_config',
 'grenade_res_config',
 'task/season_task_data',
 'camera_trk_sfx_conf',
 'c_buff_data',
 'break_data',
 'mecha_display',
 'battle_config',
 'scenes',
 'camera_transfer',
 'camera_config',
 'skill_conf',
 'pay_config',
 'house_name_out_in_dic',
 'skin_define_color',
 'map_config',
 'lottery_page_config',
 'c_hot_key_config',
 'firearm_component',
 'death_notice',
 'task/task_const_template',
 'c_building_res',
 'box_res',
 'armor_config',
 'emote',
 'bullet_track',
 'advance_config',
 'monster_data',
 'c_camera_setting',
 'navigate_config',
 'skin_define_decal',
 'c_panel_custom_key_conf',
 'turntable_lottery_custom_conf',
 'c_camera_ani',
 'distort_ui_conf',
 'skin_define_pure_decal',
 'skin_define_path_decal',
 'c_capsule_info',
 'mall_recommend_conf',
 'channel_conf',
 'sst_config',
 'sound_visible_conf',
 'server',
 'charger_data',
 'accumulate_config',
 'ui_lifetime_log_conf',
 'parachute_conf',
 'task/day_task_data',
 'death_notice_detail',
 'scene_sound_conf',
 'mall_tag_conf',
 'aim_helper_conf',
 'miaomiao_model_map',
 'c_hot_key_parameter',
 'lobby_item_rare_degree_count',
 'dress_part_uv',
 'slide_adjust_conf',
 'game_mode/normal/mecha_exp_config',
 'sound_visible_const',
 'c_panel_custom_key_convert',
 'setting',
 'item_backpack_sound_conf',
 'device_quality_conf',
 'version',
 'preload_list',
 'c_mall_new_arrival_conf']
_timer = None
_index = 0
_count = 0

def preload_conf--- This code section failed: ---

  98       0  LOAD_GLOBAL           0  '_timer'
           3  POP_JUMP_IF_FALSE    31  'to 31'

  99       6  LOAD_GLOBAL           1  'global_data'
           9  LOAD_ATTR             2  'game_mgr'
          12  LOAD_ATTR             3  'unregister_logic_timer'
          15  LOAD_GLOBAL           0  '_timer'
          18  CALL_FUNCTION_1       1 
          21  POP_TOP          

 100      22  LOAD_CONST            0  ''
          25  STORE_GLOBAL          0  '_timer'
          28  JUMP_FORWARD          0  'to 31'
        31_0  COME_FROM                '28'

 102      31  LOAD_CONST            1  ''
          34  STORE_GLOBAL          5  '_index'

 103      37  LOAD_GLOBAL           6  'len'
          40  LOAD_GLOBAL           7  'PRELOAD_CONF'
          43  CALL_FUNCTION_1       1 
          46  STORE_GLOBAL          8  '_count'

 105      49  LOAD_CONST               '<code_object _load>'
          52  MAKE_FUNCTION_0       0 
          55  STORE_FAST            0  '_load'

 120      58  LOAD_CONST            1  ''
          61  LOAD_CONST            3  ('LOGIC',)
          64  IMPORT_NAME           9  'common.utils.timer'
          67  IMPORT_FROM          10  'LOGIC'
          70  STORE_FAST            1  'LOGIC'
          73  POP_TOP          

 121      74  LOAD_GLOBAL           1  'global_data'
          77  LOAD_ATTR             2  'game_mgr'
          80  LOAD_ATTR            11  'register_logic_timer'
          83  LOAD_ATTR             4  'None'
          86  LOAD_CONST            5  1
          89  LOAD_CONST            6  'mode'
          92  LOAD_FAST             1  'LOGIC'
          95  CALL_FUNCTION_513   513 
          98  STORE_GLOBAL          0  '_timer'
         101  LOAD_CONST            0  ''
         104  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_513' instruction at offset 95


# global PRELOAD_CONF ## Warning: Unused global# global _timer ## Warning: Unused global# global _count ## Warning: Unused global# global _index ## Warning: Unused global