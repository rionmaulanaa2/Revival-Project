# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComGenericMechaEffect.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
from functools import cmp_to_key
import exception_hook
try:
    import cython
except:
    exception_hook.post_error('[import ERROR] 1')

from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
from logic.gcommon.item.item_const import MECHA_FASHION_KEY
from logic.gutils.mecha_skin_utils import get_mecha_skin_trigger_res_conf, get_mecha_skin_res_correspond_path, get_mecha_skin_res_readonly_info_by_dynamic_conf, get_accurate_mecha_skin_info_from_fasion_data
from logic.gutils.screen_effect_utils import create_screen_effect_with_auto_refresh, remove_screen_effect_with_auto_refresh, remove_all_screen_effect_with_auto_refresh
from .mecha_effect_optimize_info import IGNORE_EFFECT_WHEN_INVISIBLE_ANIM_INDEX, initialize_engine_trigger_data, USE_LOCAL_CACHE_EFFECT_ID, USE_SCRIPT_TRIGGER_EFFECT_ID, DEBUG_MECHA_EFFECT_LEVEL, MECHA_EFFECT_LEVEL_MODIFY_RECORD, register_mecha_effect_level_debug_event, calculate_mecha_effect_level
from logic.gcommon.common_const.ui_operation_const import QUALITY_MECHA_EFFECT_LEVEL_KEY, QUALITY_OTHER_MECHA_EFFECT_LEVEL_KEY, MECHA_EFFECT_LEVEL_LOW, MECHA_EFFECT_LEVEL_ULTRA
from common.framework import Functor
from common.utils.timer import CLOCK
import logic.gcommon.common_utils.bcast_utils as bcast
import game3d
import math3d
import world
import time
_DEFAULT_NONE_EFFECT_ID = '0'
_INF_TRIGGER_TIME = 999.0
_ANIM = 0
_STATE = 1
_STR_UP_BODY = str(UP_BODY)
_STR_LOW_BODY = str(LOW_BODY)
_EXTERN_1 = 'extern1'
_EXTERN_2 = 'extern2'
_ANIM_EFFECT_TYPE = {_STR_UP_BODY, _STR_LOW_BODY, _EXTERN_1, _EXTERN_2}
_EFFECT_ID = 0
_TIMER_ID = 1
_SFX_ID_LIST = 2
_SCREEN_SFX_PATH_LIST = 3
_LOCAL_CACHE_SFX_LIST = 4
_ANIM_NAME_INDEX = 0
_EVENT_NAME_INDEX = 1
_ANIM_SWITCH_HIDE_INDEX = 2
_ANIM_STOP_HIDE_INDEX = 3
_ANIM_STOP_INHERIT_NO_SPACE_INDEX = 4
_SOCKET_NAME_INDEX = 5
_EFFECT_NAME_INDEX = 6
_FORWARD_TYPE = 'forward'
_BACKWARD_TYPE = 'backward'
_LEFTWARD_TYPE = 'leftward'
_RIGHTWARD_TYPE = 'rightward'
_CENTER_TYPE = 'center'
_EFFECT_INFO_LIST = 0
_DIR_SFX_ID_MAP = 1
_DIR_LOCAL_CACHE_SFX_MAP = 2
_LOCAL_CACHE_EFFECT_CREATE_PRIORITY = game3d.ASYNC_MID
_LOD_LEVEL_EFFECTIVE_TIME = 2.0
_VALID_ANIM_FOR_UPDATE_DST_MIN_ALIVE_TIME = 1.0
FORBIT_LC_BUFF_IDS = frozenset([364, 409, 426, 442, 477, 478, 479, 484, 485, 491, 496, 506, 562, 584])

class ComGenericMechaEffect(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_CHANGE_ANIM_MOVE_DIR': 'on_change_anim_move_dir',
       'E_TRIGGER_STATE_EFFECT': 'on_trigger_state_effect',
       'E_TRIGGER_DISPOSABLE_EFFECT': 'on_trigger_disposable_effect',
       'E_ON_DRIVER_CHANGE': 'on_driver_change',
       'G_MECHA_READONLY_EFFECT_INFO': 'get_readonly_effect_info',
       'E_MECHA_LOD_LEVEL_CHANGED': 'update_mecha_effect_level_for_lod',
       'E_BEGIN_REFRESH_WHOLE_MODEL': 'on_begin_refresh_whole_model',
       'E_SWITCH_MODEL': 'on_switch_model',
       'E_ENABLE_EDITOR_MODE': 'enable_editor_mode',
       'E_DISABLE_EDITOR_MODE': 'disable_editor_mode',
       'E_REFRESH_OPTIMIZATION_OPTION': 'refresh_optimization_option',
       'E_ADD_SCRIPT_ANIM_EFFECT': 'add_script_anim_effect',
       'E_MODIFY_EFFECT_IGNORE': 'modify_effect_ignore',
       'E_MODIFY_EFFECT_INFO': 'modify_effect_info',
       'E_REFRESH_ACTIVE_STATE_EFFECT': 'refresh_active_active_state_effect',
       'E_RESET_SCRIPT_ANIM_EFFECT': 'reset_script_anim_effect',
       'G_ALL_EFFECT_INFO_DATA': 'get_all_effect_info_data',
       'G_EFFECT_INFO_DATA_BY_ID': 'get_effect_info_data_by_id',
       'G_ALL_EFFECT_IDS': 'get_all_effect_ids',
       'E_HANDLE_ADD_BUFF': '_handle_buff',
       'E_HANDLE_DEL_BUFF': '_remove_buff'
       }

    def __init__(self, need_update=False):
        super(ComGenericMechaEffect, self).__init__(need_update)
        self._mecha_id = 8001
        self._skin_id = ''
        self._shiny_weapon_id = ''
        self._model = None
        self._cur_anim_info = {}
        self._effect_map = {}
        self._trigger_end_effect_start_index = {}
        self._state_effect_cache = {}
        self._anim_dir_types = set()
        self._center_anim_dir_equal_type = _CENTER_TYPE
        self._anim_dir_types.add(self._center_anim_dir_equal_type)
        self._dir_effect_map = {}
        self._local_cache_effect_map = {}
        self._ignore_effect_when_invisible_anim_index = set()
        self._anim_effect_id_map = {}
        self._effect_id_anim_name_map = {}
        self._script_anim_effect_conf = {}
        self._engine_anim_effect_conf = {}
        self._support_set_engine_trigger = False
        self._local_cache_enabled = True
        self._dynamic_effect_conf = {}
        self._readonly_effect_conf = {}
        self._cur_mecha_effect_level = MECHA_EFFECT_LEVEL_ULTRA
        self._setting_mecha_effect_level = MECHA_EFFECT_LEVEL_ULTRA
        self._cur_engine_mecha_effect_level = -1
        self._lod_level = 0
        self._filtered_effect_info = {}
        self._filtered_engine_effect_info = {}
        self._need_update_engine_trigger_anim_name_set = set()
        self._set_dynamic_static_triggers_parameters = ()
        self._valid_for_update_dst_start_time_info = {}
        self._mecha_effect_level_timer = -1
        self._is_avatar = False
        self._driver_id = None
        self._start_trigger_effect_by_type_func = None
        self._create_effect_func = None
        self.on_trigger_disposable_effect = None
        self.on_trigger_hold_effect = None
        self.notify_trigger_effect_id_func = None
        self.destroy_callback_for_editor = None
        self.passenger_leave_event_registered = False
        self.is_cam_campmate = True
        self._force_disable_self_only = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        self._start_trigger_effect_by_type_func = self._start_trigger_effect_by_type
        self._create_effect_func = self._create_effect
        self.on_trigger_disposable_effect = self._on_trigger_disposable_effect
        self.on_trigger_hold_effect = self._on_trigger_hold_effect
        super(ComGenericMechaEffect, self).init_from_dict(unit_obj, bdict)
        self._mecha_id = bdict['mecha_id']
        skin_id, shiny_weapon_id = get_accurate_mecha_skin_info_from_fasion_data(self._mecha_id, bdict.get(MECHA_FASHION_KEY, {}))
        self._skin_id = str(skin_id)
        if shiny_weapon_id is None:
            self._shiny_weapon_id = 'common'
        else:
            self._shiny_weapon_id = str(shiny_weapon_id)
        self._model = None
        self._cur_anim_info = {UP_BODY: (None, 0.0),
           LOW_BODY: (None, 0.0),
           _EXTERN_1: (None, 0.0),
           _EXTERN_2: (None, 0.0)
           }
        self._valid_for_update_dst_start_time_info = {UP_BODY: 0.0,
           LOW_BODY: 0.0,
           _EXTERN_1: 0.0,
           _EXTERN_2: 0.0
           }
        self._effect_map = {_ANIM: {_STR_UP_BODY: {_EFFECT_ID: _DEFAULT_NONE_EFFECT_ID,
                                  _TIMER_ID: None,
                                  _SFX_ID_LIST: [],_SCREEN_SFX_PATH_LIST: [],_LOCAL_CACHE_SFX_LIST: []},
                   _STR_LOW_BODY: {_EFFECT_ID: _DEFAULT_NONE_EFFECT_ID,
                                   _TIMER_ID: None,
                                   _SFX_ID_LIST: [],_SCREEN_SFX_PATH_LIST: [],_LOCAL_CACHE_SFX_LIST: []},
                   _EXTERN_1: {_EFFECT_ID: _DEFAULT_NONE_EFFECT_ID,
                               _TIMER_ID: None,
                               _SFX_ID_LIST: [],_SCREEN_SFX_PATH_LIST: [],_LOCAL_CACHE_SFX_LIST: []},
                   _EXTERN_2: {_EFFECT_ID: _DEFAULT_NONE_EFFECT_ID,
                               _TIMER_ID: None,
                               _SFX_ID_LIST: [],_SCREEN_SFX_PATH_LIST: [],_LOCAL_CACHE_SFX_LIST: []}
                   },
           _STATE: {}}
        self._trigger_end_effect_start_index = {}
        self._state_effect_cache = {}
        self._anim_dir_types = set()
        self._anim_dir_types.add(self._center_anim_dir_equal_type)
        self._dir_effect_map = {}
        self._local_cache_effect_map = {}
        self._ignore_effect_when_invisible_anim_index = IGNORE_EFFECT_WHEN_INVISIBLE_ANIM_INDEX.get(self._mecha_id, set())
        self._init_effect_info()
        self._support_set_engine_trigger = global_data.feature_mgr.is_support_set_dynamic_static_triggers_1_0() and not global_data.test_script_effect_trigger
        self._local_cache_enabled = not global_data.mecha_effect_local_cache_disabled
        if self._support_set_engine_trigger:
            initialize_engine_trigger_data()
        self._cur_mecha_effect_level = global_data.player.get_setting_2(QUALITY_MECHA_EFFECT_LEVEL_KEY)
        self._setting_mecha_effect_level = self._cur_mecha_effect_level
        global_data.emgr.set_mecha_effect_level += self.update_mecha_effect_level_for_setting
        if DEBUG_MECHA_EFFECT_LEVEL:
            register_mecha_effect_level_debug_event()
            global_data.emgr.set_specific_mecha_effect_level += self.modify_mecha_effect_level
        self._create_effect_func = self._create_effect
        global_data.emgr.scene_observed_player_setted_event += self.update_is_cam_campmate
        return

    def update_is_cam_campmate(self, *args):
        if not global_data.cam_lplayer:
            return
        self.is_cam_campmate = self._is_avatar or global_data.cam_lplayer.ev_g_is_campmate(self.unit_obj.ev_g_camp_id())

    @staticmethod
    def get_effect_conf_copy(conf):
        conf_copy = dict()
        for effect_id, part_effect_details in six.iteritems(conf):
            conf_copy[effect_id] = dict()
            for part, part_effect_list in six.iteritems(part_effect_details):
                conf_copy[effect_id][part] = list()
                for part_effect in part_effect_list:
                    new_part_effect = dict()
                    new_part_effect.update(part_effect)
                    conf_copy[effect_id][part].append(new_part_effect)

        return conf_copy

    def _init_effect_info(self):
        conf = get_mecha_skin_trigger_res_conf(self._mecha_id, self._skin_id)
        if conf:
            self._anim_effect_id_map = dict()
            self._anim_effect_id_map.update(conf.get('anim_id', {}))
            self._effect_id_anim_name_map = {}
            for anim_name, effect_id in six.iteritems(self._anim_effect_id_map):
                if effect_id not in self._effect_id_anim_name_map:
                    self._effect_id_anim_name_map[effect_id] = []
                self._effect_id_anim_name_map[effect_id].append(anim_name)

            self._script_anim_effect_conf = self.get_effect_conf_copy(conf.get('anim_effect', {}))
            self._engine_anim_effect_conf = {}
            self._dynamic_effect_conf = self.get_effect_conf_copy(conf.get('dynamic_effect', {}))
            self._readonly_effect_conf = get_mecha_skin_res_readonly_info_by_dynamic_conf(self._dynamic_effect_conf, self._skin_id, self._shiny_weapon_id, True)
            self._filtered_effect_info = {}
            self._filtered_engine_effect_info = {}

    def _refresh_is_avatar(self):
        self._is_avatar = bool(self._driver_id and global_data.player and self._driver_id == global_data.player.id)
        setting_mecha_effect_level = global_data.player.get_setting_2(QUALITY_MECHA_EFFECT_LEVEL_KEY if self._is_avatar else QUALITY_OTHER_MECHA_EFFECT_LEVEL_KEY)
        self.update_mecha_effect_level_for_setting(setting_mecha_effect_level, self._is_avatar)
        self.update_is_cam_campmate()

    def on_post_init_complete(self, bdict):
        self._driver_id = self.sd.ref_driver_id
        self._refresh_is_avatar()

    def _unregister_mecha_effect_level_timer(self):
        if self._mecha_effect_level_timer != -1:
            global_data.game_mgr.unregister_logic_timer(self._mecha_effect_level_timer)
            self._mecha_effect_level_timer = -1

    def _clear_local_cache_effect(self):
        for cache_sfx_info in six.itervalues(self._local_cache_effect_map):
            for sfx_info_list in six.itervalues(cache_sfx_info):
                if not sfx_info_list:
                    continue
                for sfx_info in sfx_info_list:
                    if sfx_info[1] and sfx_info[1].valid:
                        sfx_info[1].unregister_shutdown_event()
                    sfx_info[0] = False
                    sfx_info[1] = None

        self._local_cache_effect_map.clear()
        return

    def destroy(self):
        self._start_trigger_effect_by_type_func = None
        self._create_effect_func = None
        self.on_trigger_disposable_effect = None
        self.on_trigger_hold_effect = None
        self.notify_trigger_effect_id_func = None
        if self.destroy_callback_for_editor:
            self.destroy_callback_for_editor()
            self.destroy_callback_for_editor = None
        self._model = None
        stop_effect_timer = self._stop_effect_timer
        for effect_part, effect_info in six.iteritems(self._effect_map[_ANIM]):
            stop_effect_timer(_ANIM, effect_part, _TIMER_ID)

        for state_id, effect_info in six.iteritems(self._effect_map[_STATE]):
            stop_effect_timer(_STATE, state_id, _TIMER_ID)

        self._clear_local_cache_effect()
        self._ignore_effect_when_invisible_anim_index = set()
        remove_all_screen_effect_with_auto_refresh(self._driver_id)
        self._need_update_engine_trigger_anim_name_set.clear()
        self._set_dynamic_static_triggers_parameters = ()
        self._unregister_mecha_effect_level_timer()
        global_data.emgr.set_mecha_effect_level -= self.update_mecha_effect_level_for_setting
        if DEBUG_MECHA_EFFECT_LEVEL:
            global_data.emgr.set_specific_mecha_effect_level -= self.modify_mecha_effect_level
        self._create_effect_func = None
        if self.passenger_leave_event_registered:
            self.unregist_event('E_NOTIFY_PASSENGER_LEAVE', self.on_notify_passenger_leave)
            self.passenger_leave_event_registered = False
        global_data.emgr.scene_observed_player_setted_event -= self.update_is_cam_campmate
        super(ComGenericMechaEffect, self).destroy()
        return

    def _reset_skin_id_and_shiny_weapon_id(self):
        skin_id, shiny_weapon_id = self.ev_g_mecha_skin_and_shiny_weapon_id()
        self._skin_id = str(skin_id)
        if shiny_weapon_id is None:
            self._shiny_weapon_id = 'common'
        else:
            self._shiny_weapon_id = str(shiny_weapon_id)
        return

    def on_model_loaded(self, model):
        self._model = model
        self._reset_skin_id_and_shiny_weapon_id()
        self._lod_level = self.ev_g_lod_level()
        self._cur_mecha_effect_level = calculate_mecha_effect_level(self._setting_mecha_effect_level, self._lod_level)
        if self.sd.ref_is_refreshing_whole_model:
            self._init_effect_info()
        self._remove_unused_effect_info()
        self._fix_anim_effect_info()
        self._fix_dynamic_effect_info()
        if DEBUG_MECHA_EFFECT_LEVEL and self._mecha_id in MECHA_EFFECT_LEVEL_MODIFY_RECORD:
            for effect_id, effect_level_data in six.iteritems(MECHA_EFFECT_LEVEL_MODIFY_RECORD[self._mecha_id]):
                for index, level in six.iteritems(effect_level_data):
                    self.modify_mecha_effect_level(self._mecha_id, effect_id, index + 1, level, silently=True)

            self._refresh_cur_mecha_effect_level()
        if not self.sd.ref_is_refreshing_whole_model:
            self.regist_event('E_TRIGGER_ANIM_EFFECT', self.on_trigger_anim_effect)
        for state_id, args in six.iteritems(self._state_effect_cache):
            self.on_trigger_state_effect(state_id, *args)

        self._state_effect_cache.clear()
        self._update_model_dynamic_static_triggers(skip_check=True)
        self.send_event('E_RESTORE_ANIM_TRIGGER_EFFECT')

    def _remove_unused_effect_info(self):
        keep_self_only = global_data.enable_mecha_lightmap and self._is_avatar
        self._do_remove_unused_effect_info(self._script_anim_effect_conf, keep_self_only)
        self._do_remove_unused_effect_info(self._engine_anim_effect_conf, keep_self_only)
        self._do_remove_unused_effect_info(self._dynamic_effect_conf, keep_self_only)
        self._do_remove_unused_effect_info2(self._readonly_effect_conf, keep_self_only)
        self._do_remove_unused_effect_info(self._filtered_effect_info, keep_self_only)
        self._do_remove_unused_effect_info(self._filtered_engine_effect_info, keep_self_only)

    def _do_remove_unused_effect_info(self, effect_dict, keep_self_only=False):
        if keep_self_only:
            return
        for effect_id, effect_group in six.iteritems(effect_dict):
            for state_id, effect_list in six.iteritems(effect_group):
                to_del = []
                for i, item in enumerate(effect_list):
                    if item.get('self_only'):
                        to_del.append(i)

                if to_del:
                    for i in reversed(to_del):
                        del effect_list[i]

    def _do_remove_unused_effect_info2(self, effect_group, keep_self_only=False):
        if keep_self_only:
            return
        for state_id, effect_list in six.iteritems(effect_group):
            to_del = []
            for i, item in enumerate(effect_list):
                if item.get('self_only'):
                    to_del.append(i)

            if to_del:
                for i in reversed(to_del):
                    del effect_list[i]

    def _fix_anim_effect_info(self):
        fix_func = self._fix_effect_list
        own_use_script_trigger_effect_id = USE_SCRIPT_TRIGGER_EFFECT_ID.get(self._mecha_id, set())
        empty_effect_id_list = []
        for effect_id, effect_info in six.iteritems(self._script_anim_effect_conf):
            use_engine_trigger = self._support_set_engine_trigger and effect_id not in own_use_script_trigger_effect_id
            valid_effect_part_count = 0
            for part, part_effect_list in six.iteritems(effect_info):
                if not part_effect_list:
                    continue
                if fix_func(effect_id, part, part_effect_list, use_engine_trigger):
                    valid_effect_part_count += 1

            if valid_effect_part_count == 0:
                empty_effect_id_list.append(effect_id)

        for effect_id in empty_effect_id_list:
            del self._script_anim_effect_conf[effect_id]
            anim_name_list = self._effect_id_anim_name_map[effect_id]
            for anim_name in anim_name_list:
                del self._anim_effect_id_map[anim_name]

            del self._filtered_effect_info[effect_id]

    def _fix_specific_anim_effect_info(self, anim_name):
        if not self._model or anim_name not in self._anim_effect_id_map:
            return
        effect_id = self._anim_effect_id_map[anim_name]
        part_effect_details = self._script_anim_effect_conf[effect_id]
        fix_func = self._fix_effect_list
        for part, part_effect_list in six.iteritems(part_effect_details):
            fix_func(effect_id, part, part_effect_list, False)

    def _fix_dynamic_effect_info(self):
        for effect_id in six.iterkeys(self._dynamic_effect_conf):
            self._fix_specific_dynamic_effect_info(effect_id)

    def _fix_specific_dynamic_effect_info(self, effect_id):
        effect_details = self._dynamic_effect_conf[effect_id]
        for effect_type, effect_list in six.iteritems(effect_details):
            self._fix_effect_list(effect_id, effect_type, effect_list, False)

    @staticmethod
    def _get_anim_event_time(model, anim_name, anim_event_name):
        if model.has_anim(anim_name) and model.has_anim_event(anim_name, anim_event_name):
            return model.get_anim_event_time(anim_name, anim_event_name) / 1000.0
        anim_name += '_f'
        if model.has_anim(anim_name) and model.has_anim_event(anim_name, anim_event_name):
            return model.get_anim_event_time(anim_name, anim_event_name) / 1000.0
        return -1

    @staticmethod
    def _my_cmp--- This code section failed: ---

 495       0  LOAD_GLOBAL           0  'six_ex'
           3  LOAD_ATTR             1  'compare'
           6  LOAD_ATTR             1  'compare'
           9  BINARY_SUBSCR    
          10  LOAD_FAST             1  'b'
          13  LOAD_CONST            1  'final_trigger_time'
          16  BINARY_SUBSCR    
          17  CALL_FUNCTION_2       2 
          20  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `BINARY_SUBSCR' instruction at offset 9

    def _get_specific_effect_path_from_list(self, effect_id, effect_path_list):
        return effect_path_list[0]

    def _init_local_cache_effect_map_keys(self, socket_list, effect_path):
        for socket in socket_list:
            if socket not in self._local_cache_effect_map:
                self._local_cache_effect_map[socket] = {}
            if type(effect_path) is list:
                for _effect_path in effect_path:
                    self._local_cache_effect_map[socket][_effect_path] = []

            elif effect_path not in self._local_cache_effect_map[socket]:
                self._local_cache_effect_map[socket][effect_path] = []

    @staticmethod
    def _check_is_engine_trigger--- This code section failed: ---

 515       0  LOAD_FAST             0  'effect_data'
           3  LOAD_ATTR             0  'get'
           6  LOAD_CONST            1  'socket_list'
           9  BUILD_LIST_0          0 
          12  CALL_FUNCTION_2       2 
          15  STORE_FAST            1  'socket_list'

 516      18  LOAD_FAST             1  'socket_list'
          21  UNARY_NOT        
          22  POP_JUMP_IF_TRUE     43  'to 43'
          25  LOAD_GLOBAL           1  'type'
          28  LOAD_FAST             1  'socket_list'
          31  CALL_FUNCTION_1       1 
          34  LOAD_GLOBAL           2  'dict'
          37  COMPARE_OP            2  '=='
        40_0  COME_FROM                '22'
          40  POP_JUMP_IF_FALSE    47  'to 47'

 517      43  LOAD_GLOBAL           3  'False'
          46  RETURN_END_IF    
        47_0  COME_FROM                '40'

 518      47  LOAD_CONST            2  'duration'
          50  LOAD_FAST             0  'effect_data'
          53  COMPARE_OP            6  'in'
          56  POP_JUMP_IF_TRUE     71  'to 71'
          59  LOAD_CONST            3  'create_interval'
          62  LOAD_FAST             0  'effect_data'
          65  COMPARE_OP            6  'in'
        68_0  COME_FROM                '56'
          68  POP_JUMP_IF_FALSE    75  'to 75'

 519      71  LOAD_GLOBAL           3  'False'
          74  RETURN_END_IF    
        75_0  COME_FROM                '68'

 520      75  LOAD_CONST            4  'trigger_time'
          78  LOAD_FAST             0  'effect_data'
          81  COMPARE_OP            6  'in'
          84  POP_JUMP_IF_FALSE   120  'to 120'
          87  LOAD_CONST            5  'anim_event_name'
          90  LOAD_FAST             0  'effect_data'
          93  COMPARE_OP            7  'not-in'
        96_0  COME_FROM                '84'
          96  POP_JUMP_IF_FALSE   120  'to 120'

 521      99  POP_JUMP_IF_FALSE     4  'to 4'
         102  BINARY_SUBSCR    
         103  LOAD_CONST            6  ''
         106  COMPARE_OP            2  '=='
         109  POP_JUMP_IF_FALSE   116  'to 116'

 522     112  LOAD_GLOBAL           4  'True'
         115  RETURN_END_IF    
       116_0  COME_FROM                '109'

 523     116  LOAD_GLOBAL           3  'False'
         119  RETURN_END_IF    
       120_0  COME_FROM                '99'
       120_1  COME_FROM                '96'

 524     120  LOAD_GLOBAL           4  'True'
         123  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 99

    def _fix_effect_list--- This code section failed: ---

 528       0  LOAD_CONST            1  ''
           3  STORE_FAST            5  'trigger_end_count'

 529       6  LOAD_CONST            1  ''
           9  BUILD_LIST_0          0 
          12  ROT_TWO          
          13  STORE_FAST            6  'invalid_effect_count'
          16  STORE_FAST            7  'invalid_effect_index_list'

 530      19  LOAD_FAST             4  'use_engine_trigger'
          22  POP_JUMP_IF_FALSE    34  'to 34'

 531      25  LOAD_GLOBAL           0  'False'
          28  STORE_FAST            8  'use_local_cache'
          31  JUMP_FORWARD         39  'to 73'

 533      34  LOAD_FAST             0  'self'
          37  LOAD_ATTR             1  '_local_cache_enabled'
          40  JUMP_IF_FALSE_OR_POP    70  'to 70'
          43  LOAD_FAST             1  'effect_id'
          46  LOAD_GLOBAL           2  'USE_LOCAL_CACHE_EFFECT_ID'
          49  LOAD_ATTR             3  'get'
          52  LOAD_FAST             0  'self'
          55  LOAD_ATTR             4  '_mecha_id'

 534      58  LOAD_GLOBAL           5  'set'
          61  CALL_FUNCTION_0       0 
          64  CALL_FUNCTION_2       2 
          67  COMPARE_OP            6  'in'
        70_0  COME_FROM                '40'
          70  STORE_FAST            8  'use_local_cache'
        73_0  COME_FROM                '31'

 535      73  SETUP_LOOP          629  'to 705'
          76  LOAD_GLOBAL           6  'enumerate'
          79  LOAD_FAST             3  'effect_list'
          82  CALL_FUNCTION_1       1 
          85  GET_ITER         
          86  FOR_ITER            615  'to 704'
          89  UNPACK_SEQUENCE_2     2 
          92  STORE_FAST            9  'index'
          95  STORE_FAST           10  'effect'

 536      98  LOAD_GLOBAL           7  'get_mecha_skin_res_correspond_path'
         101  LOAD_FAST            10  'effect'
         104  LOAD_FAST             0  'self'
         107  LOAD_ATTR             8  '_skin_id'
         110  LOAD_FAST             0  'self'
         113  LOAD_ATTR             9  '_shiny_weapon_id'
         116  CALL_FUNCTION_3       3 
         119  STORE_FAST           11  'final_correspond_path'

 537     122  LOAD_FAST            11  'final_correspond_path'
         125  POP_JUMP_IF_TRUE    157  'to 157'

 538     128  LOAD_FAST             7  'invalid_effect_index_list'
         131  LOAD_ATTR            10  'append'
         134  LOAD_FAST             9  'index'
         137  CALL_FUNCTION_1       1 
         140  POP_TOP          

 539     141  LOAD_FAST             6  'invalid_effect_count'
         144  LOAD_CONST            2  1
         147  INPLACE_ADD      
         148  STORE_FAST            6  'invalid_effect_count'

 540     151  CONTINUE             86  'to 86'
         154  JUMP_FORWARD         90  'to 247'

 541     157  LOAD_GLOBAL          11  'type'
         160  LOAD_FAST            11  'final_correspond_path'
         163  CALL_FUNCTION_1       1 
         166  LOAD_GLOBAL          12  'list'
         169  COMPARE_OP            2  '=='
         172  POP_JUMP_IF_FALSE   247  'to 247'

 544     175  LOAD_GLOBAL          13  'getattr'
         178  LOAD_GLOBAL           3  'get'
         181  CALL_FUNCTION_2       2 
         184  STORE_FAST           12  'self_func'

 545     187  LOAD_FAST            12  'self_func'
         190  LOAD_GLOBAL          13  'getattr'
         193  LOAD_GLOBAL          14  'super'
         196  LOAD_FAST             0  'self'
         199  LOAD_ATTR            15  '__class__'
         202  LOAD_FAST             0  'self'
         205  CALL_FUNCTION_2       2 
         208  LOAD_CONST            3  '_get_specific_effect_path_from_list'
         211  LOAD_FAST            12  'self_func'
         214  CALL_FUNCTION_3       3 
         217  COMPARE_OP            3  '!='
         220  POP_JUMP_IF_FALSE   247  'to 247'

 546     223  LOAD_FAST             0  'self'
         226  LOAD_ATTR            16  '_get_specific_effect_path_from_list'
         229  LOAD_FAST             1  'effect_id'
         232  LOAD_FAST            11  'final_correspond_path'
         235  CALL_FUNCTION_2       2 
         238  STORE_FAST           11  'final_correspond_path'
         241  JUMP_ABSOLUTE       247  'to 247'
         244  JUMP_FORWARD          0  'to 247'
       247_0  COME_FROM                '244'
       247_1  COME_FROM                '154'

 547     247  LOAD_FAST            11  'final_correspond_path'
         250  LOAD_FAST            10  'effect'
         253  LOAD_CONST            4  'final_correspond_path'
         256  STORE_SUBSCR     

 548     257  LOAD_FAST             9  'index'
         260  LOAD_FAST            10  'effect'
         263  LOAD_CONST            5  'index'
         266  STORE_SUBSCR     

 549     267  LOAD_FAST            10  'effect'
         270  LOAD_ATTR             3  'get'
         273  LOAD_CONST            6  'trigger_time'
         276  LOAD_CONST            7  ''
         279  CALL_FUNCTION_2       2 
         282  STORE_FAST           13  'trigger_time'

 550     285  LOAD_FAST            10  'effect'
         288  LOAD_ATTR             3  'get'
         291  LOAD_CONST            8  'anim_event_name'
         294  LOAD_CONST            9  ''
         297  CALL_FUNCTION_2       2 
         300  STORE_FAST           14  'anim_event_name'

 551     303  LOAD_FAST            14  'anim_event_name'
         306  POP_JUMP_IF_FALSE   484  'to 484'

 552     309  SETUP_LOOP          172  'to 484'
         312  LOAD_FAST             0  'self'
         315  LOAD_ATTR            17  '_effect_id_anim_name_map'
         318  LOAD_ATTR             3  'get'
         321  LOAD_FAST             1  'effect_id'
         324  BUILD_LIST_0          0 
         327  CALL_FUNCTION_2       2 
         330  GET_ITER         
         331  FOR_ITER            146  'to 480'
         334  STORE_FAST           15  'anim_name'

 553     337  LOAD_FAST             0  'self'
         340  LOAD_ATTR            18  '_get_anim_event_time'
         343  LOAD_FAST             0  'self'
         346  LOAD_ATTR            19  '_model'
         349  LOAD_FAST            15  'anim_name'
         352  LOAD_FAST            14  'anim_event_name'
         355  CALL_FUNCTION_3       3 
         358  STORE_FAST           16  'anim_event_time'

 554     361  LOAD_FAST            16  'anim_event_time'
         364  LOAD_CONST           10  -1
         367  COMPARE_OP            3  '!='
         370  POP_JUMP_IF_FALSE   383  'to 383'

 555     373  LOAD_FAST            16  'anim_event_time'
         376  STORE_FAST           13  'trigger_time'

 556     379  BREAK_LOOP       
         380  JUMP_BACK           331  'to 331'

 557     383  LOAD_FAST             0  'self'
         386  LOAD_ATTR            20  'sd'
         389  LOAD_ATTR            21  'ref_second_model_dir'
         392  POP_JUMP_IF_FALSE   331  'to 331'

 559     395  LOAD_FAST             0  'self'
         398  LOAD_ATTR            20  'sd'
         401  LOAD_ATTR            22  'ref_using_second_model'
         404  POP_JUMP_IF_FALSE   419  'to 419'
         407  LOAD_FAST             0  'self'
         410  LOAD_ATTR            23  'ev_g_mecha_original_model'
         413  CALL_FUNCTION_0       0 
         416  JUMP_FORWARD          9  'to 428'
         419  LOAD_FAST             0  'self'
         422  LOAD_ATTR            24  'ev_g_mecha_second_model'
         425  CALL_FUNCTION_0       0 
       428_0  COME_FROM                '416'
         428  STORE_FAST           17  'other_model'

 560     431  LOAD_FAST             0  'self'
         434  LOAD_ATTR            18  '_get_anim_event_time'
         437  LOAD_FAST            17  'other_model'
         440  LOAD_FAST            15  'anim_name'
         443  LOAD_FAST            14  'anim_event_name'
         446  CALL_FUNCTION_3       3 
         449  STORE_FAST           16  'anim_event_time'

 561     452  LOAD_FAST            16  'anim_event_time'
         455  LOAD_CONST           10  -1
         458  COMPARE_OP            3  '!='
         461  POP_JUMP_IF_FALSE   477  'to 477'

 562     464  LOAD_FAST            16  'anim_event_time'
         467  STORE_FAST           13  'trigger_time'

 563     470  BREAK_LOOP       
         471  JUMP_ABSOLUTE       477  'to 477'
         474  JUMP_BACK           331  'to 331'
         477  JUMP_BACK           331  'to 331'
         480  POP_BLOCK        
       481_0  COME_FROM                '309'
         481  JUMP_FORWARD          0  'to 484'
       484_0  COME_FROM                '309'

 564     484  LOAD_FAST            10  'effect'
         487  LOAD_ATTR             3  'get'
         490  LOAD_CONST           11  'trigger_end'
         493  LOAD_GLOBAL           0  'False'
         496  CALL_FUNCTION_2       2 
         499  POP_JUMP_IF_FALSE   521  'to 521'

 565     502  LOAD_FAST             5  'trigger_end_count'
         505  LOAD_CONST            2  1
         508  INPLACE_ADD      
         509  STORE_FAST            5  'trigger_end_count'

 566     512  LOAD_GLOBAL          25  '_INF_TRIGGER_TIME'
         515  STORE_FAST           13  'trigger_time'
         518  JUMP_FORWARD          0  'to 521'
       521_0  COME_FROM                '518'

 567     521  LOAD_FAST            13  'trigger_time'
         524  LOAD_FAST            10  'effect'
         527  LOAD_CONST           12  'final_trigger_time'
         530  STORE_SUBSCR     

 568     531  LOAD_FAST             8  'use_local_cache'
         534  LOAD_FAST            10  'effect'
         537  LOAD_CONST           13  'use_local_cache'
         540  STORE_SUBSCR     

 569     541  LOAD_FAST             8  'use_local_cache'
         544  POP_JUMP_IF_FALSE   647  'to 647'

 570     547  LOAD_FAST            10  'effect'
         550  LOAD_ATTR             3  'get'
         553  LOAD_CONST           14  'socket_list'
         556  BUILD_LIST_0          0 
         559  CALL_FUNCTION_2       2 
         562  STORE_FAST           18  'socket_list'

 571     565  LOAD_GLOBAL          11  'type'
         568  LOAD_FAST            18  'socket_list'
         571  CALL_FUNCTION_1       1 
         574  LOAD_GLOBAL          26  'dict'
         577  COMPARE_OP            2  '=='
         580  POP_JUMP_IF_FALSE   628  'to 628'

 572     583  SETUP_LOOP           58  'to 644'
         586  LOAD_GLOBAL          27  'six'
         589  LOAD_ATTR            28  'itervalues'
         592  LOAD_FAST            18  'socket_list'
         595  CALL_FUNCTION_1       1 
         598  GET_ITER         
         599  FOR_ITER             22  'to 624'
         602  STORE_FAST           19  '_socket_list'

 573     605  LOAD_FAST             0  'self'
         608  LOAD_ATTR            29  '_init_local_cache_effect_map_keys'
         611  LOAD_FAST            19  '_socket_list'
         614  LOAD_FAST            11  'final_correspond_path'
         617  CALL_FUNCTION_2       2 
         620  POP_TOP          
         621  JUMP_BACK           599  'to 599'
         624  POP_BLOCK        
       625_0  COME_FROM                '583'
         625  JUMP_ABSOLUTE       647  'to 647'

 575     628  LOAD_FAST             0  'self'
         631  LOAD_ATTR            29  '_init_local_cache_effect_map_keys'
         634  LOAD_FAST            18  'socket_list'
         637  LOAD_FAST            11  'final_correspond_path'
         640  CALL_FUNCTION_2       2 
         643  POP_TOP          
         644  JUMP_FORWARD          0  'to 647'
       647_0  COME_FROM                '644'

 576     647  LOAD_CONST           15  'socket_list_len'
         650  LOAD_FAST            10  'effect'
         653  COMPARE_OP            6  'in'
         656  POP_JUMP_IF_FALSE    86  'to 86'

 577     659  BUILD_LIST_0          0 
         662  LOAD_GLOBAL          30  'range'
         665  LOAD_FAST            10  'effect'
         668  LOAD_CONST           15  'socket_list_len'
         671  BINARY_SUBSCR    
         672  CALL_FUNCTION_1       1 
         675  GET_ITER         
         676  FOR_ITER             12  'to 691'
         679  STORE_FAST           20  'x'
         682  LOAD_CONST            7  ''
         685  LIST_APPEND           2  ''
         688  JUMP_BACK           676  'to 676'
         691  LOAD_FAST            10  'effect'
         694  LOAD_CONST           16  'last_create_timestamp'
         697  STORE_SUBSCR     
         698  JUMP_BACK            86  'to 86'
         701  JUMP_BACK            86  'to 86'
         704  POP_BLOCK        
       705_0  COME_FROM                '73'

 578     705  SETUP_LOOP           43  'to 751'
         708  LOAD_FAST             6  'invalid_effect_count'
         711  LOAD_CONST            1  ''
         714  COMPARE_OP            4  '>'
         717  POP_JUMP_IF_FALSE   750  'to 750'

 579     720  LOAD_FAST             6  'invalid_effect_count'
         723  LOAD_CONST            2  1
         726  INPLACE_SUBTRACT 
         727  STORE_FAST            6  'invalid_effect_count'

 580     730  LOAD_FAST             3  'effect_list'
         733  LOAD_ATTR            31  'pop'
         736  LOAD_FAST             7  'invalid_effect_index_list'
         739  LOAD_FAST             6  'invalid_effect_count'
         742  BINARY_SUBSCR    
         743  CALL_FUNCTION_1       1 
         746  POP_TOP          
         747  JUMP_BACK           708  'to 708'
         750  POP_BLOCK        
       751_0  COME_FROM                '705'

 581     751  LOAD_FAST             3  'effect_list'
         754  LOAD_ATTR            32  'sort'
         757  LOAD_CONST           17  'key'
         760  LOAD_GLOBAL          33  'cmp_to_key'
         763  LOAD_FAST             0  'self'
         766  LOAD_ATTR            34  '_my_cmp'
         769  CALL_FUNCTION_1       1 
         772  CALL_FUNCTION_256   256 
         775  POP_TOP          

 583     776  LOAD_FAST             4  'use_engine_trigger'
         779  POP_JUMP_IF_FALSE  1190  'to 1190'

 585     782  LOAD_FAST             1  'effect_id'
         785  LOAD_FAST             0  'self'
         788  LOAD_ATTR            35  '_engine_anim_effect_conf'
         791  COMPARE_OP            7  'not-in'
         794  POP_JUMP_IF_FALSE   813  'to 813'

 586     797  BUILD_MAP_0           0 
         800  LOAD_FAST             0  'self'
         803  LOAD_ATTR            35  '_engine_anim_effect_conf'
         806  LOAD_FAST             1  'effect_id'
         809  STORE_SUBSCR     
         810  JUMP_FORWARD          0  'to 813'
       813_0  COME_FROM                '810'

 587     813  LOAD_FAST             2  'effect_type'
         816  LOAD_FAST             0  'self'
         819  LOAD_ATTR            35  '_engine_anim_effect_conf'
         822  LOAD_FAST             1  'effect_id'
         825  BINARY_SUBSCR    
         826  COMPARE_OP            7  'not-in'
         829  POP_JUMP_IF_FALSE   852  'to 852'

 588     832  BUILD_LIST_0          0 
         835  LOAD_FAST             0  'self'
         838  LOAD_ATTR            35  '_engine_anim_effect_conf'
         841  LOAD_FAST             1  'effect_id'
         844  BINARY_SUBSCR    
         845  LOAD_FAST             2  'effect_type'
         848  STORE_SUBSCR     
         849  JUMP_FORWARD          0  'to 852'
       852_0  COME_FROM                '849'

 589     852  LOAD_FAST             0  'self'
         855  LOAD_ATTR            35  '_engine_anim_effect_conf'
         858  LOAD_FAST             1  'effect_id'
         861  BINARY_SUBSCR    
         862  LOAD_FAST             2  'effect_type'
         865  BINARY_SUBSCR    
         866  STORE_FAST           21  'engine_trigger_effect_list'

 590     869  LOAD_GLOBAL          36  'len'
         872  LOAD_FAST             3  'effect_list'
         875  CALL_FUNCTION_1       1 
         878  LOAD_FAST             5  'trigger_end_count'
         881  BINARY_SUBTRACT  
         882  LOAD_CONST            2  1
         885  BINARY_SUBTRACT  
         886  STORE_FAST           22  'normal_trigger_index'

 591     889  SETUP_LOOP           70  'to 962'
         892  LOAD_FAST            22  'normal_trigger_index'
         895  LOAD_CONST           10  -1
         898  COMPARE_OP            4  '>'
         901  POP_JUMP_IF_FALSE   961  'to 961'

 592     904  LOAD_FAST             0  'self'
         907  LOAD_ATTR            37  '_check_is_engine_trigger'
         910  LOAD_FAST             3  'effect_list'
         913  LOAD_FAST            22  'normal_trigger_index'
         916  BINARY_SUBSCR    
         917  CALL_FUNCTION_1       1 
         920  POP_JUMP_IF_FALSE   948  'to 948'

 593     923  LOAD_FAST            21  'engine_trigger_effect_list'
         926  LOAD_ATTR            10  'append'
         929  LOAD_FAST             3  'effect_list'
         932  LOAD_ATTR            31  'pop'
         935  LOAD_FAST            22  'normal_trigger_index'
         938  CALL_FUNCTION_1       1 
         941  CALL_FUNCTION_1       1 
         944  POP_TOP          
         945  JUMP_FORWARD          0  'to 948'
       948_0  COME_FROM                '945'

 594     948  LOAD_FAST            22  'normal_trigger_index'
         951  LOAD_CONST            2  1
         954  INPLACE_SUBTRACT 
         955  STORE_FAST           22  'normal_trigger_index'
         958  JUMP_BACK           892  'to 892'
         961  POP_BLOCK        
       962_0  COME_FROM                '889'

 595     962  LOAD_FAST            21  'engine_trigger_effect_list'
         965  LOAD_ATTR            38  'reverse'
         968  CALL_FUNCTION_0       0 
         971  POP_TOP          

 597     972  LOAD_FAST             1  'effect_id'
         975  LOAD_FAST             0  'self'
         978  LOAD_ATTR            39  '_filtered_engine_effect_info'
         981  COMPARE_OP            7  'not-in'
         984  POP_JUMP_IF_FALSE  1003  'to 1003'

 598     987  BUILD_MAP_0           0 
         990  LOAD_FAST             0  'self'
         993  LOAD_ATTR            39  '_filtered_engine_effect_info'
         996  LOAD_FAST             1  'effect_id'
         999  STORE_SUBSCR     
        1000  JUMP_FORWARD          0  'to 1003'
      1003_0  COME_FROM                '1000'

 599    1003  LOAD_FAST             2  'effect_type'
        1006  LOAD_FAST             0  'self'
        1009  LOAD_ATTR            39  '_filtered_engine_effect_info'
        1012  LOAD_FAST             1  'effect_id'
        1015  BINARY_SUBSCR    
        1016  COMPARE_OP            7  'not-in'
        1019  POP_JUMP_IF_FALSE  1190  'to 1190'

 600    1022  BUILD_LIST_0          0 
        1025  LOAD_FAST             0  'self'
        1028  LOAD_ATTR            39  '_filtered_engine_effect_info'
        1031  LOAD_FAST             1  'effect_id'
        1034  BINARY_SUBSCR    
        1035  LOAD_FAST             2  'effect_type'
        1038  STORE_SUBSCR     

 602    1039  LOAD_FAST             0  'self'
        1042  LOAD_ATTR            39  '_filtered_engine_effect_info'
        1045  LOAD_FAST             1  'effect_id'
        1048  BINARY_SUBSCR    
        1049  LOAD_FAST             2  'effect_type'
        1052  BINARY_SUBSCR    
        1053  STORE_FAST           23  'filtered_list'

 603    1056  SETUP_LOOP           61  'to 1120'
        1059  LOAD_GLOBAL           6  'enumerate'
        1062  LOAD_FAST            21  'engine_trigger_effect_list'
        1065  CALL_FUNCTION_1       1 
        1068  GET_ITER         
        1069  FOR_ITER             47  'to 1119'
        1072  UNPACK_SEQUENCE_2     2 
        1075  STORE_FAST            9  'index'
        1078  STORE_FAST           10  'effect'

 604    1081  LOAD_FAST            10  'effect'
        1084  LOAD_CONST           18  'level'
        1087  BINARY_SUBSCR    
        1088  LOAD_FAST             0  'self'
        1091  LOAD_ATTR            40  '_cur_mecha_effect_level'
        1094  COMPARE_OP            4  '>'
        1097  POP_JUMP_IF_FALSE  1069  'to 1069'

 605    1100  LOAD_FAST            23  'filtered_list'
        1103  LOAD_ATTR            10  'append'
        1106  LOAD_FAST             9  'index'
        1109  CALL_FUNCTION_1       1 
        1112  POP_TOP          
        1113  JUMP_BACK          1069  'to 1069'
        1116  JUMP_BACK          1069  'to 1069'
        1119  POP_BLOCK        
      1120_0  COME_FROM                '1056'

 606    1120  LOAD_GLOBAL          36  'len'
        1123  LOAD_FAST            23  'filtered_list'
        1126  CALL_FUNCTION_1       1 
        1129  STORE_FAST           24  'filtered_count'

 607    1132  SETUP_LOOP           52  'to 1187'
        1135  LOAD_FAST            24  'filtered_count'
        1138  LOAD_CONST            1  ''
        1141  COMPARE_OP            4  '>'
        1144  POP_JUMP_IF_FALSE  1183  'to 1183'

 608    1147  LOAD_FAST            24  'filtered_count'
        1150  LOAD_CONST            2  1
        1153  INPLACE_SUBTRACT 
        1154  STORE_FAST           24  'filtered_count'

 609    1157  LOAD_FAST            21  'engine_trigger_effect_list'
        1160  LOAD_ATTR            31  'pop'
        1163  LOAD_FAST            23  'filtered_list'
        1166  LOAD_FAST            24  'filtered_count'
        1169  BINARY_SUBSCR    
        1170  CALL_FUNCTION_1       1 
        1173  LOAD_FAST            23  'filtered_list'
        1176  LOAD_FAST            24  'filtered_count'
        1179  STORE_SUBSCR     
        1180  JUMP_BACK          1135  'to 1135'
        1183  POP_BLOCK        
      1184_0  COME_FROM                '1132'
        1184  JUMP_ABSOLUTE      1190  'to 1190'
        1187  JUMP_FORWARD          0  'to 1190'
      1190_0  COME_FROM                '1187'

 612    1190  LOAD_FAST             1  'effect_id'
        1193  LOAD_FAST             0  'self'
        1196  LOAD_ATTR            41  '_filtered_effect_info'
        1199  COMPARE_OP            7  'not-in'
        1202  POP_JUMP_IF_FALSE  1221  'to 1221'

 613    1205  BUILD_MAP_0           0 
        1208  LOAD_FAST             0  'self'
        1211  LOAD_ATTR            41  '_filtered_effect_info'
        1214  LOAD_FAST             1  'effect_id'
        1217  STORE_SUBSCR     
        1218  JUMP_FORWARD          0  'to 1221'
      1221_0  COME_FROM                '1218'

 614    1221  LOAD_FAST             2  'effect_type'
        1224  LOAD_FAST             0  'self'
        1227  LOAD_ATTR            41  '_filtered_effect_info'
        1230  LOAD_FAST             1  'effect_id'
        1233  BINARY_SUBSCR    
        1234  COMPARE_OP            7  'not-in'
        1237  POP_JUMP_IF_FALSE  1436  'to 1436'

 615    1240  BUILD_LIST_0          0 
        1243  LOAD_FAST             0  'self'
        1246  LOAD_ATTR            41  '_filtered_effect_info'
        1249  LOAD_FAST             1  'effect_id'
        1252  BINARY_SUBSCR    
        1253  LOAD_FAST             2  'effect_type'
        1256  STORE_SUBSCR     

 616    1257  LOAD_FAST             0  'self'
        1260  LOAD_ATTR            41  '_filtered_effect_info'
        1263  LOAD_FAST             1  'effect_id'
        1266  BINARY_SUBSCR    
        1267  LOAD_FAST             2  'effect_type'
        1270  BINARY_SUBSCR    
        1271  STORE_FAST           23  'filtered_list'

 617    1274  SETUP_LOOP           92  'to 1369'
        1277  LOAD_GLOBAL           6  'enumerate'
        1280  LOAD_FAST             3  'effect_list'
        1283  CALL_FUNCTION_1       1 
        1286  GET_ITER         
        1287  FOR_ITER             78  'to 1368'
        1290  UNPACK_SEQUENCE_2     2 
        1293  STORE_FAST            9  'index'
        1296  STORE_FAST           10  'effect'

 618    1299  LOAD_FAST            10  'effect'
        1302  LOAD_CONST           18  'level'
        1305  BINARY_SUBSCR    
        1306  LOAD_FAST             0  'self'
        1309  LOAD_ATTR            40  '_cur_mecha_effect_level'
        1312  COMPARE_OP            4  '>'
        1315  POP_JUMP_IF_FALSE  1287  'to 1287'

 619    1318  LOAD_FAST            23  'filtered_list'
        1321  LOAD_ATTR            10  'append'
        1324  LOAD_FAST             9  'index'
        1327  CALL_FUNCTION_1       1 
        1330  POP_TOP          

 620    1331  LOAD_FAST            10  'effect'
        1334  LOAD_ATTR             3  'get'
        1337  LOAD_CONST           11  'trigger_end'
        1340  LOAD_GLOBAL           0  'False'
        1343  CALL_FUNCTION_2       2 
        1346  POP_JUMP_IF_FALSE  1365  'to 1365'

 621    1349  LOAD_FAST             5  'trigger_end_count'
        1352  LOAD_CONST            2  1
        1355  INPLACE_SUBTRACT 
        1356  STORE_FAST            5  'trigger_end_count'
        1359  JUMP_ABSOLUTE      1365  'to 1365'
        1362  JUMP_BACK          1287  'to 1287'
        1365  JUMP_BACK          1287  'to 1287'
        1368  POP_BLOCK        
      1369_0  COME_FROM                '1274'

 622    1369  LOAD_GLOBAL          36  'len'
        1372  LOAD_FAST            23  'filtered_list'
        1375  CALL_FUNCTION_1       1 
        1378  STORE_FAST           24  'filtered_count'

 623    1381  SETUP_LOOP           52  'to 1436'
        1384  LOAD_FAST            24  'filtered_count'
        1387  LOAD_CONST            1  ''
        1390  COMPARE_OP            4  '>'
        1393  POP_JUMP_IF_FALSE  1432  'to 1432'

 624    1396  LOAD_FAST            24  'filtered_count'
        1399  LOAD_CONST            2  1
        1402  INPLACE_SUBTRACT 
        1403  STORE_FAST           24  'filtered_count'

 625    1406  LOAD_FAST             3  'effect_list'
        1409  LOAD_ATTR            31  'pop'
        1412  LOAD_FAST            23  'filtered_list'
        1415  LOAD_FAST            24  'filtered_count'
        1418  BINARY_SUBSCR    
        1419  CALL_FUNCTION_1       1 
        1422  LOAD_FAST            23  'filtered_list'
        1425  LOAD_FAST            24  'filtered_count'
        1428  STORE_SUBSCR     
        1429  JUMP_BACK          1384  'to 1384'
        1432  POP_BLOCK        
      1433_0  COME_FROM                '1381'
        1433  JUMP_FORWARD          0  'to 1436'
      1436_0  COME_FROM                '1381'

 627    1436  LOAD_FAST             3  'effect_list'
        1439  POP_JUMP_IF_TRUE   1459  'to 1459'
        1442  LOAD_FAST             0  'self'
        1445  LOAD_ATTR            41  '_filtered_effect_info'
        1448  LOAD_FAST             1  'effect_id'
        1451  BINARY_SUBSCR    
        1452  LOAD_FAST             2  'effect_type'
        1455  BINARY_SUBSCR    
      1456_0  COME_FROM                '1439'
        1456  POP_JUMP_IF_FALSE  1521  'to 1521'

 628    1459  LOAD_FAST             1  'effect_id'
        1462  LOAD_FAST             0  'self'
        1465  LOAD_ATTR            42  '_trigger_end_effect_start_index'
        1468  COMPARE_OP            7  'not-in'
        1471  POP_JUMP_IF_FALSE  1490  'to 1490'

 629    1474  BUILD_MAP_0           0 
        1477  LOAD_FAST             0  'self'
        1480  LOAD_ATTR            42  '_trigger_end_effect_start_index'
        1483  LOAD_FAST             1  'effect_id'
        1486  STORE_SUBSCR     
        1487  JUMP_FORWARD          0  'to 1490'
      1490_0  COME_FROM                '1487'

 630    1490  LOAD_GLOBAL          36  'len'
        1493  LOAD_FAST             3  'effect_list'
        1496  CALL_FUNCTION_1       1 
        1499  LOAD_FAST             5  'trigger_end_count'
        1502  BINARY_SUBTRACT  
        1503  LOAD_FAST             0  'self'
        1506  LOAD_ATTR            42  '_trigger_end_effect_start_index'
        1509  LOAD_FAST             1  'effect_id'
        1512  BINARY_SUBSCR    
        1513  LOAD_FAST             2  'effect_type'
        1516  STORE_SUBSCR     

 632    1517  LOAD_GLOBAL          43  'True'
        1520  RETURN_END_IF    
      1521_0  COME_FROM                '1456'

 634    1521  LOAD_GLOBAL           0  'False'
        1524  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 181

    def _check_update_model_dynamic_static_triggers(self):
        if not self._set_dynamic_static_triggers_parameters:
            return
        if self._cur_mecha_effect_level == self._cur_engine_mecha_effect_level:
            if global_data.debug_mecha_effect_system:
                print('return for level same in check')
            self._set_dynamic_static_triggers_parameters = ()
            return
        invalid, latest_valid_time = False, -1
        for part, (cur_anim_name, anim_start_time) in six.iteritems(self._cur_anim_info):
            if cur_anim_name in self._need_update_engine_trigger_anim_name_set:
                self._valid_for_update_dst_start_time_info[part] = -1
                invalid = True
            else:
                if self._valid_for_update_dst_start_time_info[part] == -1:
                    self._valid_for_update_dst_start_time_info[part] = anim_start_time
                latest_valid_time = max(latest_valid_time, self._valid_for_update_dst_start_time_info[part])

        if invalid:
            if global_data.debug_mecha_effect_system:
                print('------------return for invalid anim')
            return
        if global_data.game_time - latest_valid_time < _VALID_ANIM_FOR_UPDATE_DST_MIN_ALIVE_TIME:
            if global_data.debug_mecha_effect_system:
                print('------------return for lack of time')
            return
        if global_data.debug_mecha_effect_system:
            print('===========================update', self._cur_anim_info)
        self._need_update_engine_trigger_anim_name_set.clear()
        self._model.set_dynamic_static_triggers(*self._set_dynamic_static_triggers_parameters)
        self._cur_engine_mecha_effect_level = self._cur_mecha_effect_level
        self._set_dynamic_static_triggers_parameters = ()

    def _update_model_dynamic_static_triggers(self, skip_check=False, ignore_level_check=False):
        if not self._support_set_engine_trigger or not self._model or not self._model.valid:
            return
        if not ignore_level_check and self._cur_mecha_effect_level == self._cur_engine_mecha_effect_level:
            if global_data.debug_mecha_effect_system:
                print('===========================return for same level before calculate')
            return
        anim, event, switch, stop, inherit, socket, effect = ([], [], [], [], [], [], [])
        self._need_update_engine_trigger_anim_name_set.clear()
        for effect_id, effect_info in six.iteritems(self._engine_anim_effect_conf):
            for effect_list in six.itervalues(effect_info):
                for anim_name in self._effect_id_anim_name_map[effect_id]:
                    self._need_update_engine_trigger_anim_name_set.add(anim_name)
                    for engine_trigger_effect in effect_list:
                        if 'anim_event_name' not in engine_trigger_effect:
                            anim_event_name = 'start'
                        else:
                            anim_event_name = engine_trigger_effect['anim_event_name']
                            if not self._model.has_anim_event(anim_name, anim_event_name):
                                anim_event_name = 'start'
                        effect_path = engine_trigger_effect['final_correspond_path']
                        for socket_name in engine_trigger_effect['socket_list']:
                            switch_stop_hide = not engine_trigger_effect.get('keep_alive', False)
                            anim.append(anim_name)
                            event.append(anim_event_name)
                            switch.append(switch_stop_hide)
                            stop.append(switch_stop_hide)
                            inherit.append(False)
                            socket.append(socket_name)
                            effect.append(effect_path.replace('/', '\\'))

        if skip_check:
            self._model.set_dynamic_static_triggers(anim, event, switch, stop, inherit, socket, effect)
            self._cur_engine_mecha_effect_level = self._cur_mecha_effect_level
        else:
            self._set_dynamic_static_triggers_parameters = (
             anim, event, switch, stop, inherit, socket, effect)
            self._check_update_model_dynamic_static_triggers()

    @staticmethod
    def _set_effect_rot(sfx, rot):
        rot = math3d.rotation(*rot)
        sfx.world_rotation_matrix = math3d.rotation_to_matrix(rot)

    def _on_after_create_sfx(self, sfx, user_data, task):
        if sfx is None:
            return
        else:
            if not self.is_valid():
                sfx.destroy()
                return
            socket, effect_path, index = user_data
            local_cache_effect_list = self._local_cache_effect_map[socket][effect_path]
            if not self._model or not self._model.valid:
                sfx.destroy()
                local_cache_effect_list.pop(index)
                return
            local_cache_effect_list[index][1] = sfx
            self._model.bind(socket, sfx, world.BIND_TYPE_DEFAULT)
            if not local_cache_effect_list[index][0]:
                sfx.shutdown()
                sfx.visible = False
            if not sfx.has_shutdown_event():

                def shutdown_cb(*args):
                    local_cache_effect_list[index][0] = False
                    if local_cache_effect_list[index][1]:
                        local_cache_effect_list[index][1].visible = False

                sfx.register_shutdown_event(shutdown_cb)
            return

    def _create_local_cache_effect(self, socket, effect_path, local_cache_sfx_list, keep_alive=False):
        local_cache_effect_list = self._local_cache_effect_map[socket][effect_path]
        for index, (active, cache_sfx) in enumerate(local_cache_effect_list):
            if not active and cache_sfx and cache_sfx.get_state() == world.FX_STATE_SHUTDOWN:
                local_cache_effect_list[index][0] = True
                cache_sfx.visible = True
                cache_sfx.restart()
                break
        else:
            index = len(local_cache_effect_list)
            local_cache_effect_list.append([True, None])
            world.create_sfx_async(effect_path, self._on_after_create_sfx, (socket, effect_path, index), _LOCAL_CACHE_EFFECT_CREATE_PRIORITY)

        local_cache_sfx_list.append((socket, effect_path, index, keep_alive))
        return

    def _create_dir_effect(self, effect_info, map_mid_key, socket_map, effect_path):
        if map_mid_key not in self._dir_effect_map:
            self._add_new_dir_effect_type(map_mid_key)
        self._dir_effect_map[map_mid_key][_EFFECT_INFO_LIST].append(effect_info)
        use_local_cache = effect_info['use_local_cache']
        for dir_type in self._anim_dir_types:
            for socket in socket_map.get(dir_type, []):
                if use_local_cache:
                    self._create_local_cache_effect(socket, effect_path, self._dir_effect_map[map_mid_key][_DIR_LOCAL_CACHE_SFX_MAP][dir_type])
                else:
                    sfx_id = global_data.sfx_mgr.create_sfx_on_model(effect_path, self._model, socket)
                    self._dir_effect_map[map_mid_key][_DIR_SFX_ID_MAP][dir_type].append(sfx_id)

    def _create_common_effect(self, effect_info, sfx_id_list, local_cache_sfx_list, socket_list, effect_path, rot):
        duration = effect_info.get('duration', 0.0)
        keep_alive = effect_info.get('keep_alive', False)
        create_interval = effect_info.get('create_interval', None)
        use_local_cache = effect_info['use_local_cache']
        for i, socket in enumerate(socket_list):
            if create_interval:
                last_create_timestamp = effect_info['last_create_timestamp'][i]
                cur_timestamp = time.time()
                if cur_timestamp - last_create_timestamp <= create_interval:
                    continue
                effect_info['last_create_timestamp'][i] = cur_timestamp
            if use_local_cache:
                self._create_local_cache_effect(socket, effect_path, local_cache_sfx_list, keep_alive)
            else:
                ex_data = {'need_diff_process': effect_info.get('camp_diff', 0) and not self.is_cam_campmate}
                if rot is None:
                    sfx_id = global_data.sfx_mgr.create_sfx_on_model(effect_path, self._model, socket, duration=duration, ex_data=ex_data)
                else:
                    sfx_id = global_data.sfx_mgr.create_sfx_on_model(effect_path, self._model, socket, duration=duration, on_create_func=Functor(self._set_effect_rot, rot=rot), ex_data=ex_data)
                not keep_alive and sfx_id_list.append(sfx_id)

        return

    def _create_effect(self, effect_info, sfx_id_list, local_cache_sfx_list, map_mid_key, socket_index, rot, screen_sfx_path_list):
        effect_path = effect_info['final_correspond_path']
        socket_list = effect_info.get('socket_list', [])
        if socket_list:
            if socket_index == -1:
                if type(socket_list) == dict:
                    self._create_dir_effect(effect_info, map_mid_key, socket_list, effect_path)
                else:
                    self._create_common_effect(effect_info, sfx_id_list, local_cache_sfx_list, socket_list, effect_path, rot)
            elif socket_index < effect_info['socket_list_len']:
                if type(effect_path) is list:
                    effect_path = effect_path[socket_index]
                duration = effect_info.get('duration', 0.0)
                keep_alive = effect_info.get('keep_alive', False)
                create_interval = effect_info.get('create_interval', None)
                if create_interval:
                    last_create_timestamp = effect_info['last_create_timestamp'][socket_index]
                    cur_timestamp = time.time()
                    if cur_timestamp - last_create_timestamp <= create_interval:
                        return
                    effect_info['last_create_timestamp'][socket_index] = cur_timestamp
                if effect_info['use_local_cache']:
                    self._create_local_cache_effect(socket_list[socket_index], effect_path, local_cache_sfx_list, keep_alive)
                else:
                    socket = socket_list[socket_index]
                    ex_data = {'need_diff_process': effect_info.get('camp_diff', 0) and not self.is_cam_campmate}
                    sfx_id = global_data.sfx_mgr.create_sfx_on_model(effect_path, self._model, socket, duration=duration, ex_data=ex_data)
                    not keep_alive and sfx_id_list.append(sfx_id)
            else:
                import exception_hook
                err_msg = 'ComGenericMechaEffect -- socket_index too large -- list index out of range\n'
                err_msg += 'socket_index: {}, mecha_id: {}, effect_info: {}\n'.format(socket_index, self._mecha_id, str(effect_info))
                err_msg += 'is_avatar: {}, mecha_state: {}\n'.format(str(self.ev_g_is_avatar()), str(self.ev_g_cur_state()))
                exception_hook.post_error(err_msg)
        else:
            screen_sfx_path_list.append(effect_path)
            create_screen_effect_with_auto_refresh(self._driver_id, effect_path)
        return

    def _remove_effect(self, map_key, map_mid_key):
        sfx_id_list_type, screen_sfx_path_list_type = _SFX_ID_LIST, _SCREEN_SFX_PATH_LIST
        effect_details = self._effect_map[map_key][map_mid_key]
        sfx_id_list = effect_details[sfx_id_list_type]
        for sfx_id in sfx_id_list:
            global_data.sfx_mgr.shutdown_sfx_by_id(sfx_id)

        del sfx_id_list[:]
        local_cache_sfx_list = effect_details[_LOCAL_CACHE_SFX_LIST]
        for socket, sfx_path, index, keep_alive in local_cache_sfx_list:
            if keep_alive:
                continue
            active, sfx = self._local_cache_effect_map[socket][sfx_path][index]
            if active:
                self._local_cache_effect_map[socket][sfx_path][index][0] = False
                sfx and sfx.shutdown()

        del local_cache_sfx_list[:]
        if map_mid_key in self._dir_effect_map:
            for dir_type in self._anim_dir_types:
                for sfx_id in self._dir_effect_map[map_mid_key][_DIR_SFX_ID_MAP][dir_type]:
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

                for socket, sfx_path, index, keep_alive in self._dir_effect_map[map_mid_key][_DIR_LOCAL_CACHE_SFX_MAP][dir_type]:
                    if keep_alive:
                        continue
                    active, sfx = self._local_cache_effect_map[socket][sfx_path][index]
                    if active:
                        self._local_cache_effect_map[socket][sfx_path][index][0] = False
                        sfx and sfx.shutdown()

                del self._dir_effect_map[map_mid_key][_DIR_LOCAL_CACHE_SFX_MAP][dir_type][:]

            self._dir_effect_map.pop(map_mid_key)
        driver_id = self._driver_id
        sfx_path_list = effect_details[screen_sfx_path_list_type]
        for path in sfx_path_list:
            remove_screen_effect_with_auto_refresh(driver_id, path)

        del sfx_path_list[:]

    def _stop_effect_timer(self, map_key, map_mid_key, timer_id_type):
        if self._effect_map[map_key][map_mid_key][timer_id_type]:
            global_data.game_mgr.unregister_logic_timer(self._effect_map[map_key][map_mid_key][timer_id_type])
            self._effect_map[map_key][map_mid_key][timer_id_type] = None
        return

    def _trigger_end_effect(self, effect_id, effect_type):
        if effect_id != _DEFAULT_NONE_EFFECT_ID:
            if effect_type not in self._trigger_end_effect_start_index[effect_id]:
                return
            index = self._trigger_end_effect_start_index[effect_id][effect_type]
            part_effect_list = self._script_anim_effect_conf[effect_id][effect_type]
            pass_self_only = not self._force_disable_self_only
            for effect_info_index in range(index, len(part_effect_list)):
                effect_item = part_effect_list[effect_info_index]
                if pass_self_only or not effect_item.get('self_only'):
                    self._create_effect_func(part_effect_list[effect_info_index], self._effect_map[_ANIM][effect_type][_SFX_ID_LIST], self._effect_map[_ANIM][effect_type][_LOCAL_CACHE_SFX_LIST], effect_type, -1, None, self._effect_map[_ANIM][effect_type][_SCREEN_SFX_PATH_LIST])

        return

    def _trigger_single_effect(self, map_key, effect_info_list, effect_info_index, index_gap, effect_type, map_mid_key, socket_index=-1, rot=None, pass_self_only=True):
        timer_id_type, sfx_id_list_type, screen_sfx_path_list_type = _TIMER_ID, _SFX_ID_LIST, _SCREEN_SFX_PATH_LIST
        effect_info = effect_info_list[effect_info_index]
        effect_map_details = self._effect_map[map_key][map_mid_key]
        if pass_self_only or not effect_info.get('self_only'):
            self._create_effect_func(effect_info, effect_map_details[sfx_id_list_type], effect_map_details[_LOCAL_CACHE_SFX_LIST], map_mid_key, socket_index, rot, effect_map_details[screen_sfx_path_list_type])
        effect_map_details[timer_id_type] = None
        next_effect_info_index = effect_info_index + 1
        if next_effect_info_index < index_gap:
            next_effect_info = effect_info_list[next_effect_info_index]
            trigger_interval = next_effect_info['final_trigger_time'] - effect_info['final_trigger_time']
            if map_key == _ANIM:
                if effect_type in (_STR_UP_BODY, _STR_LOW_BODY):
                    anim_rate = self.sd.ref_anim_rate.get(int(effect_type), 1.0)
                    if anim_rate > 0:
                        trigger_interval /= anim_rate
            if trigger_interval <= 0.03:
                self._trigger_single_effect(map_key, effect_info_list, next_effect_info_index, index_gap, effect_type, map_mid_key, socket_index, rot, pass_self_only)
            else:
                effect_map_details[timer_id_type] = global_data.game_mgr.register_logic_timer(self._trigger_single_effect, interval=trigger_interval, args=(
                 map_key, effect_info_list, next_effect_info_index, index_gap, effect_type, map_mid_key,
                 socket_index, rot, pass_self_only), times=1, mode=CLOCK)
        return

    def _start_trigger_effect_by_type(self, effect_id, effect_info_list, effect_type, map_mid_key, socket_index=-1, rot=None):
        if self._trigger_end_effect_start_index[effect_id].get(effect_type, 0) != 0:
            timer_id_type, sfx_id_list_type = _TIMER_ID, _SFX_ID_LIST
            effect_info = effect_info_list[0]
            trigger_time = effect_info['final_trigger_time']
            map_key = _STATE
            if effect_type in _ANIM_EFFECT_TYPE:
                if effect_type in (_STR_UP_BODY, _STR_LOW_BODY):
                    anim_rate = self.sd.ref_anim_rate.get(int(effect_type), 1.0)
                    if anim_rate > 0:
                        trigger_time /= anim_rate
                map_key = _ANIM
            index_gap = self._trigger_end_effect_start_index[effect_id][effect_type]
            if trigger_time <= 0.0:
                self._trigger_single_effect(map_key, effect_info_list, 0, index_gap, effect_type, map_mid_key, socket_index, rot, not self._force_disable_self_only)
            else:
                self._effect_map[map_key][map_mid_key][timer_id_type] = global_data.game_mgr.register_logic_timer(self._trigger_single_effect, interval=trigger_time, args=(
                 map_key, effect_info_list, 0, index_gap, effect_type, map_mid_key, socket_index, rot,
                 not self._force_disable_self_only), times=1, mode=CLOCK)

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        effect_id = self._anim_effect_id_map.get(anim_name, _DEFAULT_NONE_EFFECT_ID)
        effect_type = str(part)
        cur_effect_id = self._effect_map[_ANIM][effect_type][_EFFECT_ID]
        self._cur_anim_info[part] = (anim_name, global_data.game_time)
        if effect_id != cur_effect_id or force_trigger_effect:
            self._effect_map[_ANIM][effect_type][_EFFECT_ID] = effect_id
            self._remove_effect(_ANIM, effect_type)
            self._trigger_end_effect(cur_effect_id, effect_type)
            self._stop_effect_timer(_ANIM, effect_type, _TIMER_ID)
            if effect_id not in self._ignore_effect_when_invisible_anim_index or self._model.is_visible_in_this_frame():
                if effect_id != _DEFAULT_NONE_EFFECT_ID:
                    effect_info_list = self._script_anim_effect_conf[effect_id][str(part)]
                    self._start_trigger_effect_by_type_func(effect_id, effect_info_list, effect_type, effect_type, socket_index)
        self._check_update_model_dynamic_static_triggers()

    def make_center_anim_dir_equals_to_forward(self):
        self._center_anim_dir_equal_type = _FORWARD_TYPE
        if _CENTER_TYPE in self._anim_dir_types:
            self._anim_dir_types = {
             _FORWARD_TYPE}

    def reset_center_anim_dir_equals_type(self):
        self._center_anim_dir_equal_type = _CENTER_TYPE

    def _add_new_dir_effect_type(self, map_mid_key):
        self._dir_effect_map[map_mid_key] = {_EFFECT_INFO_LIST: [],_DIR_SFX_ID_MAP: {_CENTER_TYPE: [],_FORWARD_TYPE: [],_BACKWARD_TYPE: [],_LEFTWARD_TYPE: [],_RIGHTWARD_TYPE: []},_DIR_LOCAL_CACHE_SFX_MAP: {_CENTER_TYPE: [],_FORWARD_TYPE: [],_BACKWARD_TYPE: [],_LEFTWARD_TYPE: [],_RIGHTWARD_TYPE: []}}

    def on_change_anim_move_dir(self, dir_x, dir_y, force=False):
        if abs(dir_x) <= 0.01:
            dir_x = 0.0
        if abs(dir_y) <= 0.01:
            dir_y = 0.0
        dir_types = set()
        if dir_x == 0.0 and dir_y == 0.0:
            dir_types.add(self._center_anim_dir_equal_type)
        else:
            if dir_x < 0.0:
                dir_types.add(_LEFTWARD_TYPE)
            else:
                if dir_x > 0.0:
                    dir_types.add(_RIGHTWARD_TYPE)
                if dir_y < 0.0:
                    dir_types.add(_BACKWARD_TYPE)
                else:
                    dir_types.add(_FORWARD_TYPE)
            if dir_types == self._anim_dir_types:
                return
        remove_dir_types = self._anim_dir_types - dir_types
        new_dir_types = dir_types - self._anim_dir_types
        for dir_effect_info in six.itervalues(self._dir_effect_map):
            effect_info_list = dir_effect_info[_EFFECT_INFO_LIST]
            dir_sfx_id_map = dir_effect_info[_DIR_SFX_ID_MAP]
            dir_local_cache_sfx_map = dir_effect_info[_DIR_LOCAL_CACHE_SFX_MAP]
            for dir_type in remove_dir_types:
                sfx_id_list = dir_sfx_id_map[dir_type]
                for sfx_id in sfx_id_list:
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

                del sfx_id_list[:]
                local_cache_sfx_list = dir_local_cache_sfx_map[dir_type]
                for socket, sfx_path, index, keep_alive in dir_local_cache_sfx_map[dir_type]:
                    if keep_alive:
                        continue
                    active, sfx = self._local_cache_effect_map[socket][sfx_path][index]
                    if active:
                        self._local_cache_effect_map[socket][sfx_path][index][0] = False
                        sfx and sfx.shutdown()

                del local_cache_sfx_list[:]

            for dir_type in new_dir_types:
                sfx_id_list = dir_sfx_id_map[dir_type]
                for effect_info in effect_info_list:
                    effect_path = effect_info['final_correspond_path']
                    socket_list = effect_info['socket_list'].get(dir_type, [])
                    for socket in socket_list:
                        sfx_id = global_data.sfx_mgr.create_sfx_on_model(effect_path, self._model, socket)
                        sfx_id_list.append(sfx_id)

        self._anim_dir_types = dir_types

    def _add_new_state_id(self, state_id):
        self._effect_map[_STATE][state_id] = {_EFFECT_ID: _DEFAULT_NONE_EFFECT_ID,
           _TIMER_ID: None,
           _SFX_ID_LIST: [],_LOCAL_CACHE_SFX_LIST: [],_SCREEN_SFX_PATH_LIST: []}
        self._dir_effect_map[state_id] = {_EFFECT_INFO_LIST: [],_DIR_SFX_ID_MAP: {_CENTER_TYPE: [],_FORWARD_TYPE: [],_BACKWARD_TYPE: [],_LEFTWARD_TYPE: [],_RIGHTWARD_TYPE: []},_DIR_LOCAL_CACHE_SFX_MAP: {_CENTER_TYPE: [],_FORWARD_TYPE: [],_BACKWARD_TYPE: [],_LEFTWARD_TYPE: [],_RIGHTWARD_TYPE: []}}
        return

    def on_trigger_state_effect(self, state_id, effect_id, force=False, socket_index=-1, rot=None, need_sync=False):
        if not self._model:
            self._state_effect_cache[state_id] = (
             effect_id, force, socket_index, rot, need_sync)
            return
        if effect_id == '':
            effect_id = _DEFAULT_NONE_EFFECT_ID
        if effect_id != _DEFAULT_NONE_EFFECT_ID and not self._dynamic_effect_conf[effect_id]['state']:
            return
        if state_id not in self._effect_map[_STATE]:
            self._add_new_state_id(state_id)
        if self._effect_map[_STATE][state_id][_EFFECT_ID] != effect_id or force:
            self._remove_effect(_STATE, state_id)
            self._stop_effect_timer(_STATE, state_id, _TIMER_ID)
            if effect_id != _DEFAULT_NONE_EFFECT_ID:
                if effect_id not in self._ignore_effect_when_invisible_anim_index or self._model.is_visible_in_this_frame():
                    effect_info_list = self._dynamic_effect_conf[effect_id]['state']
                    self._start_trigger_effect_by_type_func(effect_id, effect_info_list, 'state', state_id, socket_index=socket_index, rot=rot)
            self._effect_map[_STATE][state_id][_EFFECT_ID] = effect_id
        need_sync and self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_TRIGGER_STATE_EFFECT, (state_id, effect_id, force, socket_index, rot)], True)

    def _on_trigger_disposable_effect(self, effect_id, pos, rot=None, duration=0.5, on_create_func=None, need_sync=False):
        effect_info_list = self._dynamic_effect_conf.get(effect_id, {}).get('disposable', [])
        for effect_info in effect_info_list:
            path = effect_info.get('final_correspond_path', None)
            if path is None:
                return
            ex_data = {'need_diff_process': effect_info.get('camp_diff', 0) and not self.is_cam_campmate}
            if rot is None:
                global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*pos), duration=duration, on_create_func=on_create_func, ex_data=ex_data)
            else:
                global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*pos), duration=duration, on_create_func=Functor(self._set_effect_rot, rot=rot), ex_data=ex_data)

        need_sync and self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_TRIGGER_DISPOSABLE_EFFECT, (effect_id, pos, rot, duration)], True)
        return

    def _on_trigger_hold_effect(self, effect_id, create_cb=None, remove_cb=None, duration=0):
        effect_info_list = self._dynamic_effect_conf.get(effect_id, {}).get('hold', [])
        sfx_id_list = []
        for effect_info in effect_info_list:
            path = effect_info.get('final_correspond_path', None)
            if path is None:
                return sfx_id_list
            if path.endswith('.gim'):
                self.ev_g_load_model(path, create_cb)
            else:
                sfx_id_list.append(global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(0, 0, 0), duration=duration, on_create_func=create_cb, on_remove_func=remove_cb))

        return sfx_id_list

    def on_driver_change(self, new_driver_id):
        if new_driver_id:
            self._driver_id = new_driver_id
            self._refresh_is_avatar()

    def get_readonly_effect_info(self):
        return self._readonly_effect_conf

    def clear_triggered_anim_effect(self):
        for effect_type in six.iterkeys(self._effect_map[_ANIM]):
            self._remove_effect(_ANIM, effect_type)

    @staticmethod
    def level_up_cmp_func(a, b):
        return a > b

    @staticmethod
    def level_down_cmp_func(a, b):
        return a <= b

    def _reorganize_two_sorted_effect_list(self, effect_list_a, effect_list_b, cmp_func):
        changed = False
        if not effect_list_b:
            return changed
        new_effect_list_a, new_effect_list_b, head, tail = ([], [], 0, len(effect_list_a))
        for effect_b in effect_list_b:
            if cmp_func(effect_b['level'], self._cur_mecha_effect_level):
                new_effect_list_b.append(effect_b)
                continue
            trigger_time = effect_b['final_trigger_time']
            while head < tail:
                if effect_list_a[head]['final_trigger_time'] < trigger_time:
                    new_effect_list_a.append(effect_list_a[head])
                    head += 1
                else:
                    break

            new_effect_list_a.append(effect_b)
            changed = True

        if changed:
            while head < tail:
                new_effect_list_a.append(effect_list_a[head])
                head += 1

            del effect_list_a[:]
            del effect_list_b[:]
            effect_list_a.extend(new_effect_list_a)
            effect_list_b.extend(new_effect_list_b)
        return changed

    def _update_trigger_end_effect_start_index(self, effect_id, effect_type, effect_list):
        tail = len(effect_list)
        while tail > 0:
            if effect_list[tail - 1].get('trigger_end', False):
                tail -= 1
            else:
                break

        if effect_id not in self._trigger_end_effect_start_index:
            self._trigger_end_effect_start_index[effect_id] = {}
        self._trigger_end_effect_start_index[effect_id][effect_type] = tail

    def _on_mecha_effect_level_changed(self, new_level, is_avatar=True):
        if self._is_avatar ^ is_avatar:
            return
        else:
            if new_level == self._cur_mecha_effect_level:
                if global_data.debug_mecha_effect_system:
                    print('----------mecha effect level stay same({})'.format(new_level))
                return
            if global_data.debug_mecha_effect_system:
                print('------------mecha effect level changed(from {} to {})'.format(self._cur_mecha_effect_level, new_level))
            cur_level = self._cur_mecha_effect_level
            self._cur_mecha_effect_level = new_level
            if self._model is None:
                return
            if new_level > cur_level:
                for effect_id, effect_info in six.iteritems(self._filtered_effect_info):
                    for effect_type, filtered_effect_list in six.iteritems(effect_info):
                        if effect_type in _ANIM_EFFECT_TYPE:
                            effect_list = self._script_anim_effect_conf[effect_id][effect_type]
                            self._reorganize_two_sorted_effect_list(effect_list, filtered_effect_list, self.level_up_cmp_func)
                        else:
                            effect_list = self._dynamic_effect_conf[effect_id][effect_type]
                            self._reorganize_two_sorted_effect_list(effect_list, filtered_effect_list, self.level_up_cmp_func)
                        self._update_trigger_end_effect_start_index(effect_id, effect_type, effect_list)

                for effect_id, effect_info in six.iteritems(self._filtered_engine_effect_info):
                    for effect_type, filtered_effect_list in six.iteritems(effect_info):
                        if effect_type in _ANIM_EFFECT_TYPE:
                            effect_list = self._engine_anim_effect_conf[effect_id][effect_type]
                            self._reorganize_two_sorted_effect_list(effect_list, filtered_effect_list, self.level_up_cmp_func)
                        else:
                            log_error('Error')

            else:
                for effect_id, effect_info in six.iteritems(self._script_anim_effect_conf):
                    for effect_type, effect_list in six.iteritems(effect_info):
                        if not effect_list:
                            continue
                        filtered_effect_list = self._filtered_effect_info[effect_id][effect_type]
                        changed = self._reorganize_two_sorted_effect_list(filtered_effect_list, effect_list, self.level_down_cmp_func)
                        if changed:
                            self._update_trigger_end_effect_start_index(effect_id, effect_type, effect_list)
                            if effect_id == self._effect_map[_ANIM][effect_type][_EFFECT_ID]:
                                self._stop_effect_timer(_ANIM, effect_type, _TIMER_ID)

            for effect_id, effect_info in six.iteritems(self._engine_anim_effect_conf):
                for effect_type, effect_list in six.iteritems(effect_info):
                    if not effect_list:
                        continue
                    filtered_effect_list = self._filtered_engine_effect_info[effect_id][effect_type]
                    self._reorganize_two_sorted_effect_list(filtered_effect_list, effect_list, self.level_down_cmp_func)

            changed_state_effect_id_set = set()
            for effect_id, effect_info in six.iteritems(self._dynamic_effect_conf):
                for effect_type, effect_list in six.iteritems(effect_info):
                    filtered_effect_list = self._filtered_effect_info[effect_id][effect_type]
                    changed = self._reorganize_two_sorted_effect_list(filtered_effect_list, effect_list, self.level_down_cmp_func)
                    if changed:
                        self._update_trigger_end_effect_start_index(effect_id, effect_type, effect_list)
                        if effect_type == 'state':
                            changed_state_effect_id_set.add(effect_id)

            for state_id, effect_info in six.iteritems(self._effect_map[_STATE]):
                if effect_info[_EFFECT_ID] in changed_state_effect_id_set:
                    self._stop_effect_timer(_STATE, state_id, _TIMER_ID)

            self._update_model_dynamic_static_triggers()
            return

    def update_mecha_effect_level_for_setting(self, setting_level, is_avatar=True):
        self._setting_mecha_effect_level = setting_level
        new_level = calculate_mecha_effect_level(setting_level, self._lod_level, not is_avatar)
        self._on_mecha_effect_level_changed(new_level, is_avatar)

    def update_mecha_effect_level_for_lod(self, lod_level):
        self._lod_level = lod_level
        if global_data.debug_mecha_effect_system:
            print('-------------lod level changed(cur_level--{})'.format(lod_level))
        self._set_dynamic_static_triggers_parameters = ()
        self._unregister_mecha_effect_level_timer()
        self._mecha_effect_level_timer = global_data.game_mgr.register_logic_timer(self.check_mecha_effect_level_changed, interval=_LOD_LEVEL_EFFECTIVE_TIME, times=1, mode=CLOCK)

    def check_mecha_effect_level_changed(self):
        if global_data.debug_mecha_effect_system:
            print('-----------------lod level has kept same for 2.0s')
        new_level = calculate_mecha_effect_level(self._setting_mecha_effect_level, self._lod_level, not self._is_avatar)
        self._on_mecha_effect_level_changed(new_level, self._is_avatar)
        self._mecha_effect_level_timer = -1

    def _refresh_cur_mecha_effect_level(self):
        cur_level = self._cur_mecha_effect_level
        new_level = MECHA_EFFECT_LEVEL_LOW if cur_level != MECHA_EFFECT_LEVEL_LOW else cur_level + 1
        self._on_mecha_effect_level_changed(new_level, self._is_avatar)
        self._on_mecha_effect_level_changed(cur_level, self._is_avatar)

    def modify_mecha_effect_level(self, mecha_id, effect_id, index, level, silently=False):
        if int(mecha_id) != self._mecha_id:
            return
        effect_id = str(effect_id)
        index -= 1
        effect_info_list = []
        if effect_id in self._script_anim_effect_conf:
            effect_info_list.append(self._script_anim_effect_conf[effect_id])
        elif effect_id in self._dynamic_effect_conf:
            effect_info_list.append(self._dynamic_effect_conf[effect_id])
        if effect_id in self._engine_anim_effect_conf:
            effect_info_list.append(self._engine_anim_effect_conf[effect_id])
        if effect_id in self._filtered_effect_info:
            effect_info_list.append(self._filtered_effect_info[effect_id])
        if effect_id in self._filtered_engine_effect_info:
            effect_info_list.append(self._filtered_engine_effect_info[effect_id])
        for effect_info in effect_info_list:
            for effect_list in six.itervalues(effect_info):
                for effect in effect_list:
                    if effect['index'] == index:
                        effect['level'] = level
                        if not silently:
                            self._refresh_cur_mecha_effect_level()
                            global_data.game_mgr.show_tip('\xe4\xbf\xae\xe6\x94\xb9\xe6\x88\x90\xe5\x8a\x9f!')
                        return

    def on_begin_refresh_whole_model(self):
        for cache_sfx_info in six.itervalues(self._local_cache_effect_map):
            for sfx_path in six.iterkeys(cache_sfx_info):
                cache_sfx_info[sfx_path] = []

    def on_switch_model(self, model):
        stop_effect_timer = self._stop_effect_timer
        for effect_part, effect_info in six.iteritems(self._effect_map[_ANIM]):
            stop_effect_timer(_ANIM, effect_part, _TIMER_ID)

        for state_id, effect_info in six.iteritems(self._effect_map[_STATE]):
            stop_effect_timer(_STATE, state_id, _TIMER_ID)

        self._model = model

    def _create_effect_in_editor(self, effect_info, sfx_id_list, local_cache_sfx_list, map_mid_key, socket_index, rot, screen_sfx_path_list):
        if effect_info.get('ignore'):
            return
        self._create_effect(effect_info, sfx_id_list, local_cache_sfx_list, map_mid_key, socket_index, rot, screen_sfx_path_list)

    def _start_trigger_effect_by_type_in_editor(self, effect_id, effect_info_list, effect_type, map_mid_key, socket_index=-1, rot=None):
        self.notify_trigger_effect_id_func(effect_id)
        self._start_trigger_effect_by_type(effect_id, effect_info_list, effect_type, map_mid_key, socket_index, rot)

    def _on_trigger_disposable_effect_in_editor(self, effect_id, pos, rot=None, duration=0.5, on_create_func=None, need_sync=False):
        self.notify_trigger_effect_id_func(effect_id)
        effect_info_list = self._dynamic_effect_conf.get(effect_id, {}).get('disposable', [])
        for effect_info in effect_info_list:
            if effect_info.get('ignore'):
                continue
            path = effect_info.get('final_correspond_path', None)
            if path is None:
                return
            if rot is None:
                global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*pos), duration=duration, on_create_func=on_create_func)
            else:
                global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(*pos), duration=duration, on_create_func=Functor(self._set_effect_rot, rot=rot))

        need_sync and self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [
         bcast.E_TRIGGER_DISPOSABLE_EFFECT, (effect_id, pos, rot, duration)], True)
        return

    def _on_trigger_hold_effect_in_editor(self, effect_id, create_cb=None, remove_cb=None, duration=0):
        self.notify_trigger_effect_id_func(effect_id)
        effect_info_list = self._dynamic_effect_conf.get(effect_id, {}).get('hold', [])
        sfx_id_list = []
        for effect_info in effect_info_list:
            if effect_info.get('ignore'):
                continue
            path = effect_info.get('final_correspond_path', None)
            if path is None:
                return sfx_id_list
            if path.endswith('.gim'):
                self.ev_g_load_model(path, create_cb)
            else:
                sfx_id_list.append(global_data.sfx_mgr.create_sfx_in_scene(path, math3d.vector(0, 0, 0), duration=duration, on_create_func=create_cb, on_remove_func=remove_cb))

        return sfx_id_list

    def enable_editor_mode(self, notify_func, destroy_callback):
        self._create_effect_func = self._create_effect_in_editor
        self._start_trigger_effect_by_type_func = self._start_trigger_effect_by_type_in_editor
        self.on_trigger_disposable_effect = self._on_trigger_disposable_effect_in_editor
        self.on_trigger_hold_effect = self._on_trigger_hold_effect_in_editor
        self.destroy_event()
        self.init_event()
        self.notify_trigger_effect_id_func = notify_func
        self.destroy_callback_for_editor = destroy_callback
        if not self.passenger_leave_event_registered:
            self.regist_event('E_NOTIFY_PASSENGER_LEAVE', self.on_notify_passenger_leave, 99)
            self.passenger_leave_event_registered = True
        self.refresh_optimization_option()
        self._refresh_is_avatar()

    def disable_editor_mode(self):
        self._create_effect_func = self._create_effect
        self._start_trigger_effect_by_type_func = self._start_trigger_effect_by_type
        self.on_trigger_disposable_effect = self._on_trigger_disposable_effect
        self.on_trigger_hold_effect = self._on_trigger_hold_effect
        self.destroy_event()
        self.init_event()
        self.notify_trigger_effect_id_func = None
        self.destroy_callback_for_editor = None
        if self.passenger_leave_event_registered:
            self.unregist_event('E_NOTIFY_PASSENGER_LEAVE', self.on_notify_passenger_leave)
            self.passenger_leave_event_registered = False
        return

    def refresh_optimization_option(self):
        new_support_engine_trigger = global_data.feature_mgr.is_support_set_dynamic_static_triggers_1_0() and not global_data.test_script_effect_trigger
        new_local_cache_enabled = not global_data.mecha_effect_local_cache_disabled
        if self._support_set_engine_trigger ^ new_support_engine_trigger or self._local_cache_enabled ^ new_local_cache_enabled:
            self._support_set_engine_trigger = new_support_engine_trigger
            self._local_cache_enabled = new_local_cache_enabled
            self._init_effect_info()
            if self._model:
                self._fix_anim_effect_info()
                self._fix_dynamic_effect_info()
                if not new_support_engine_trigger:
                    if self._model:
                        self._model.set_dynamic_static_triggers([], [], [], [], [], [], [])
                if not new_local_cache_enabled:
                    self._clear_local_cache_effect()

    def on_notify_passenger_leave(self, *args, **kwargs):
        if self.destroy_callback_for_editor:
            self.destroy_callback_for_editor()
            self.destroy_callback_for_editor = None
        return

    def _force_add_new_effect_id_for_anim(self, anim_name, anim_name_without_suffix=''):
        effect_id = '10000'
        while effect_id in self._script_anim_effect_conf:
            effect_id = str(int(effect_id) + 1)

        self._anim_effect_id_map[anim_name] = effect_id
        self._effect_id_anim_name_map[effect_id] = [anim_name]
        if anim_name_without_suffix:
            self._anim_effect_id_map[anim_name_without_suffix] = effect_id
            self._effect_id_anim_name_map[effect_id].append(anim_name_without_suffix)
        self._script_anim_effect_conf[effect_id] = {_STR_UP_BODY: [],_STR_LOW_BODY: [],_EXTERN_1: [],_EXTERN_2: []}
        return effect_id

    def _get_anim_effect_id(self, anim_name):
        effect_id = self._anim_effect_id_map.get(anim_name, None)
        is_new = False
        if effect_id is None:
            the_last_split_char_index = anim_name.rfind('_')
            if the_last_split_char_index != -1:
                dir_suffix = anim_name[the_last_split_char_index + 1:]
                if dir_suffix in ('f', 'fl', 'fr', 'b', 'bl', 'br', 'l', 'r'):
                    anim_name_without_suffix = anim_name[:the_last_split_char_index]
                    if anim_name_without_suffix in self._anim_effect_id_map:
                        effect_id = self._anim_effect_id_map[anim_name_without_suffix]
                        self._anim_effect_id_map[anim_name] = effect_id
                        self._effect_id_anim_name_map[effect_id].append(anim_name)
                    else:
                        effect_id = self._force_add_new_effect_id_for_anim(anim_name, anim_name_without_suffix)
                        is_new = True
                else:
                    effect_id = self._force_add_new_effect_id_for_anim(anim_name)
                    is_new = True
            else:
                effect_id = self._force_add_new_effect_id_for_anim(anim_name)
                is_new = True
        return (
         effect_id, is_new)

    def _check_is_duplicated_effect(self, part_effect_data, anim_name, anim_event_name, socket_list, res_path):
        for cur_effect_data in part_effect_data:
            if cur_effect_data['normal_res_path'] != res_path:
                continue
            if cur_effect_data.get('socket_list', []) != socket_list:
                continue
            if 'anim_event_name' in cur_effect_data:
                if cur_effect_data['anim_event_name'] == anim_event_name:
                    return True
            elif cur_effect_data['final_trigger_time'] == self._get_anim_event_time(self._model, anim_name, anim_event_name):
                return True

        return False

    def add_script_anim_effect(self, anim_effect_data, force=False):
        if not self._model:
            return False
        for anim_name, event_effect_data in six.iteritems(anim_effect_data):
            effect_id, is_new = self._get_anim_effect_id(anim_name)
            script_effect_data = self._script_anim_effect_conf[effect_id]
            for part_effect_data in six.itervalues(script_effect_data):
                if not part_effect_data and not is_new:
                    continue
                for anim_event_name, effect_path_to_socket_list_map in six.iteritems(event_effect_data):
                    for effect_path, socket_list in six.iteritems(effect_path_to_socket_list_map):
                        if self._check_is_duplicated_effect(part_effect_data, anim_name, anim_event_name, socket_list, effect_path):
                            continue
                        effect_data = {'normal_res_path': effect_path,'anim_event_name': anim_event_name,'level': 0,'is_extra': True
                           }
                        if socket_list[0]:
                            effect_data.update({'socket_list': socket_list,
                               'socket_list_len': len(socket_list)
                               })
                        part_effect_data.append(effect_data)

                if not is_new:
                    break

        self._fix_anim_effect_info()
        return True

    def modify_effect_ignore(self, effect_id, part, index, ignore):
        effect_info_list = []
        if effect_id in self._script_anim_effect_conf and part in self._script_anim_effect_conf[effect_id]:
            effect_info_list = self._script_anim_effect_conf[effect_id][part]
        elif effect_id in self._dynamic_effect_conf and part in self._dynamic_effect_conf[effect_id]:
            effect_info_list = self._dynamic_effect_conf[effect_id][part]
        for effect_info in effect_info_list:
            if effect_info['index'] == index:
                effect_info['ignore'] = ignore
                break

    def modify_effect_info(self, effect_id, part, index, modify_info):
        need_fix_anim_effect = False
        effect_info_list = []
        if effect_id in self._script_anim_effect_conf and part in self._script_anim_effect_conf[effect_id]:
            effect_info_list = self._script_anim_effect_conf[effect_id][part]
        elif effect_id in self._dynamic_effect_conf and part in self._dynamic_effect_conf[effect_id]:
            effect_info_list = self._dynamic_effect_conf[effect_id][part]
        elif effect_id in self._engine_anim_effect_conf and part in self._engine_anim_effect_conf[effect_id]:
            effect_info_list = self._engine_anim_effect_conf[effect_id][part]
            need_fix_anim_effect = True
        for effect_index, effect_info in enumerate(effect_info_list):
            if effect_info.get('index', effect_index) == index:
                effect_info.update(modify_info)
                break

        need_fix_anim_effect and self._update_model_dynamic_static_triggers(skip_check=True, ignore_level_check=True)

    def refresh_active_active_state_effect(self, effect_id):
        for state_id, state_effect_data in six.iteritems(self._effect_map[_STATE]):
            if state_effect_data[_EFFECT_ID] == effect_id:
                self.on_trigger_state_effect(state_id, effect_id, force=True)

    def reset_script_anim_effect(self):
        conf = get_mecha_skin_trigger_res_conf(self._mecha_id, self._skin_id)
        for effect_id in self._script_anim_effect_conf:
            if int(effect_id) >= 10000:
                anim_name_list = self._effect_id_anim_name_map.pop(effect_id)
                for anim_name in anim_name_list:
                    self._anim_effect_id_map.pop(anim_name)

        self._script_anim_effect_conf = self.get_effect_conf_copy(conf.get('anim_effect', {}))
        self._fix_anim_effect_info()

    def get_effect_info_data_by_id(self, effect_id):
        if effect_id in self._script_anim_effect_conf:
            return (self._script_anim_effect_conf[effect_id], self._effect_id_anim_name_map.get(effect_id, []))
        if effect_id in self._dynamic_effect_conf:
            return (self._dynamic_effect_conf[effect_id], [])
        if effect_id in self._readonly_effect_conf:
            return (self._readonly_effect_conf[effect_id], [])

    def get_all_effect_info_data(self):
        import copy
        ret = copy.deepcopy(self._script_anim_effect_conf)
        ret.update(copy.deepcopy(self._dynamic_effect_conf))
        return ret

    def get_all_effect_ids(self):
        ret = six_ex.keys(self._script_anim_effect_conf)
        ret.extend(six_ex.keys(self._dynamic_effect_conf))
        ret.extend(six_ex.keys(self._readonly_effect_conf))
        return ret

    def _handle_buff(self, hdl_name, data, left_time, overlying):
        if data['BuffId'] in FORBIT_LC_BUFF_IDS:
            self.inc_disable_self_only_counter()

    def _remove_buff(self, hdl_name, buff_key, buff_id, buff_idx):
        if buff_id in FORBIT_LC_BUFF_IDS:
            self.dec_disable_self_only_counter()

    def inc_disable_self_only_counter(self):
        self._force_disable_self_only += 1
        return self._force_disable_self_only

    def dec_disable_self_only_counter(self):
        self._force_disable_self_only -= 1
        if self._force_disable_self_only < 0:
            self._force_disable_self_only = 0
        return self._force_disable_self_only