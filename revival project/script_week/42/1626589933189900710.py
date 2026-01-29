# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/WhirlwindLogic.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import math
import math3d
import world
from .StateBase import StateBase
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.const import NEOX_UNIT_SCALE, SOUND_TYPE_MECHA_FIRE
from logic.gcommon.common_utils import status_utils
from logic.gcommon.common_const import collision_const
from common.cfg import confmgr
import collision
from logic.gutils.scene_utils import is_break_obj
from mobile.common.EntityManager import EntityManager
import common.utils.timer as timer
from logic.gcommon import time_utility as tutil
from ..cdata import state_physic_arg
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gutils import scene_utils
from logic.gcommon import editor
from logic.gutils.slash_utils import NEED_CHECK_VALID_TAG_VALUE
from logic.gutils.client_unit_tag_utils import register_unit_tag
from logic.gutils.mecha_utils import do_hit_phantom
END_CUT_BACK1_EVENT = 'MC_CUT_BACK2_combo'
ATTACK_BONE = 'biped_bone18'
NEED_STOP_WHEN_CONTACT_TAG_VALUE = register_unit_tag(('LDeathDoor', 'LMecha', 'LMechaTrans',
                                                      'LMechaRobot', 'LMonster'))

def __editor_attack_structure(self):
    structure = {}
    for i in range(1, 4):
        sub_structure = dict()
        sub_structure['zh_name'] = '\xe7\xac\xac%d\xe5\x88\x80\xe5\x8f\x82\xe6\x95\xb0' % i
        params = dict()
        params['anim'] = {'zh_name': '\xe5\x8a\xa8\xe7\x94\xbb\xe5\x8f\x82\xe6\x95\xb0',
           'type': 'list','kwargs': {'structure': [{'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe5\x90\x8d'}, {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x83\xa8\xe4\xbd\x8d'}, {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x96\xb9\xe5\x90\x91'}]}}
        params['hit_start'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe7\xa7\xbb\xe5\x8a\xa8/\xe6\x94\xbb\xe5\x87\xbb\xe5\x88\xa4\xe5\xae\x9a\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','type': 'float'}
        params['large_col'] = {'zh_name': '\xe8\xbf\x98\xe5\x8e\x9f\xe6\x94\xbb\xe5\x87\xbb\xe5\x88\xa4\xe5\xae\x9a\xe5\x8c\x85\xe5\x9b\xb4\xe7\x9b\x92\xe7\xbc\xa9\xe6\x94\xbe\xe5\x80\xbc\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','type': 'float'}
        params['brake'] = {'zh_name': '\xe5\xbc\x80\xe5\xa7\x8b\xe5\x87\x8f\xe9\x80\x9f\xe7\xa7\xbb\xe5\x8a\xa8\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','type': 'float'}
        params['hit_end'] = {'zh_name': '\xe5\x81\x9c\xe6\xad\xa2\xe6\x94\xbb\xe5\x87\xbb\xe5\x88\xa4\xe5\xae\x9a\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','type': 'float'}
        params['combo'] = {'zh_name': '\xe8\xbf\x9e\xe5\x87\xbb/\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9','type': 'float'}
        params['anim_duration'] = {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x97\xb6\xe9\x95\xbf','type': 'float'}
        sub_structure['type'] = 'dict'
        sub_structure['kwargs'] = {'structure': params}
        structure[i] = sub_structure

    return structure


@editor.state_exporter({('timeScale', 'param'): {'zh_name': '\xe5\x8a\xa0\xe9\x80\x9f\xe9\x80\x9f\xe7\x8e\x87'},('move_dist', 'meter'): {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe8\xb7\x9d\xe7\xa6\xbb'},('brake_move_dist', 'meter'): {'zh_name': '\xe5\x87\x8f\xe9\x80\x9f\xe7\xa7\xbb\xe5\x8a\xa8\xe8\xb7\x9d\xe7\xa6\xbb'},('dash_stepheight', 'meter'): {'zh_name': '\xe6\x8a\xac\xe8\x84\x9a\xe9\xab\x98\xe5\xba\xa6'},('blend_to_move_time', 'param'): {'zh_name': '\xe7\xa7\xbb\xe5\x8a\xa8\xe8\xbf\x87\xe6\xb8\xa1\xe6\x97\xb6\xe9\x97\xb4'},('hit_range', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x88\xa4\xe5\xae\x9a\xe8\x8c\x83\xe5\x9b\xb4',
                            'param_type': 'list','structure': [{'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe5\xae\xbd\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\xab\x98\xe5\xba\xa6','type': 'float'}, {'zh_name': '\xe6\x8c\xa5\xe7\xa0\x8d\xe9\x95\xbf\xe5\xba\xa6\xef\xbc\x88\xe7\xba\xb5\xe6\xb7\xb1\xef\xbc\x89','type': 'float'}],'post_setter': lambda self: self.init_hit_range_parameters()
                            },
   ('hit_forward_offset', 'meter'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x88\xa4\xe5\xae\x9a\xe5\x8c\x85\xe5\x9b\xb4\xe7\x9b\x92\xe5\x89\x8d\xe5\x90\x91\xe5\x81\x8f\xe7\xa7\xbb'},('right_offset', 'meter'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x88\xa4\xe5\xae\x9a\xe5\x8c\x85\xe5\x9b\xb4\xe7\x9b\x92\xe5\x8f\xb3\xe5\x90\x91\xe5\x81\x8f\xe7\xa7\xbb'},('small_hit_range_scale', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x88\xa4\xe5\xae\x9a\xe5\x8c\x85\xe5\x9b\xb4\xe7\x9b\x92\xe7\xbc\xa9\xe6\x94\xbe\xe5\x80\xbc\xef\xbc\x88\xe5\xb0\x8f\xef\xbc\x89'},('attack_param', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8f\x82\xe6\x95\xb0',
                               'structure': lambda self: __editor_attack_structure(self),
                               'post_setter': lambda self: self.register_callbacks()
                               },
   ('pve_hit_range_scale', 'param'): {'zh_name': 'pve\xe6\x8c\xa5\xe7\xa0\x8d\xe5\x88\xa4\xe5\xae\x9a\xe5\xa4\xa7\xe5\xb0\x8f\xe7\xbc\xa9\xe6\x94\xbe','post_setter': lambda self: self.init_hit_range_parameters()
                                      }
   })
class NormalWhirlwind(StateBase):
    SUB_STATE_ID = 1
    ATTACK_END = 0
    STATE_ATTACK_1 = 1
    STATE_ATTACK_2 = 2
    STATE_ATTACK_3 = 3
    BIND_EVENT = {'E_CHARACTER_ATTR': 'change_character_attr',
       'E_ADD_WIND_RUSH_SKILL': 'on_update_skill',
       'E_WIND_RUSH_SKILL_MP_FULL': 'on_update_skill',
       'G_WHIRLWIND_STATE': 'get_whirlwind_state',
       'E_DEBUG_COL': 'debug_col',
       'E_CHANGE_STAGE_COUNT': 'on_change_stage_count'
       }

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(NormalWhirlwind, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.init_parameters()
        self.register_callbacks()
        self.create_hit_collision()

    def destroy(self):
        super(NormalWhirlwind, self).destroy()
        if self.hit_col:
            global_data.game_mgr.scene.scene_col.remove_object(self.hit_col)
            self.hit_col = None
        if self.valid_col:
            global_data.game_mgr.scene.scene_col.remove_object(self.valid_col)
            self.valid_col = None
        if self._trigger_cd_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._trigger_cd_timer_id)
            self._trigger_cd_timer_id = None
        return

    def change_character_attr(self, name, *arg):
        if name == 'animator_info':
            if self.is_active:
                print('test--NormalWhirlwind.animator_info--sub_state =', self.sub_state, '--sub_sid_timer =', self.sub_sid_timer, '--sub_states_triggers =', self.sub_states_triggers, '--_trigger_cd_timer_id =', self._trigger_cd_timer_id)
        elif name == 'test_hit':
            self.create_test_hit_collision()

    def debug_col(self, is_show_col, scale=None):
        print(('test--debug_col--hit_col =', self.hit_col, '--is_show_col =', is_show_col, '--scale =', scale, '--hit_col.position =', self.hit_col.position))
        if not self.hit_col:
            return
        if is_show_col:
            global_data.game_mgr.scene.scene_col.add_object(self.hit_col)
            if scale:
                scene_utils.set_col_scale(self.hit_col, scale)
        else:
            global_data.game_mgr.scene.scene_col.remove_object(self.hit_col)

    def action_btn_down(self):
        super(NormalWhirlwind, self).action_btn_down()
        if not self.check_can_active():
            return True
        if self.ev_g_is_diving():
            return True
        if not self.ev_g_can_cast_skill(self.skill_id):
            return True
        if not self.is_active:
            self.active_self()
        if self.sub_state < self.max_stage and not self._wait_start:
            self.combo_attack()
        return True

    def init_hit_range_parameters(self):
        if self.is_pve:
            self.hit_range = [
             self.hit_range_conf[0] * self.pve_hit_range_scale, self.hit_range_conf[0] * self.pve_hit_range_scale, self.hit_range_conf[0] * self.pve_hit_range_scale]
        self.hit_width = self.hit_range[0] * NEOX_UNIT_SCALE
        self.hit_height = self.hit_range[1] * NEOX_UNIT_SCALE
        self.hit_depth = self.hit_range[2] * NEOX_UNIT_SCALE
        self.reset_hit_collision()

    def init_parameters(self):
        self.is_pve = global_data.game_mode.is_pve()
        self.tick_interval = self.custom_param.get('tick_interval', 0.1)
        self.skill_id = self.custom_param['skill_id']
        self.attack_param = self.custom_param['attack_param']
        self.combo_status = status_utils.convert_status(self.custom_param.get('break_states', set()))
        self.sub_state = self.ATTACK_END
        self.move_dist = self.custom_param.get('move_dist', 1) * NEOX_UNIT_SCALE
        self.brake_move_dist = self.custom_param.get('brake_move_dist', 1) * NEOX_UNIT_SCALE
        self.timeScale = self.custom_param.get('timeScale', 1)
        self.blend_to_move_time = self.custom_param.get('blend_to_move_time', 0.2)
        self.dash_stepheight = self.custom_param.get('dash_stepheight', 2 * NEOX_UNIT_SCALE)
        skill_conf = confmgr.get('skill_conf', str(self.skill_id))
        ext_info = skill_conf.get('ext_info', {})
        self.trigger_skill_max_duration = ext_info.get('continue_time', 5)
        self.max_stage = ext_info.get('continue_count', 3)
        self.brake_begin = 0
        self.brake_speed = 0
        self._is_moving = False
        self.hit_col = None
        self.valid_col = None
        self.break_obj_list = []
        self.alreay_hit_objs = set()
        self.hit_need_stop_obj = False
        self.hit_range = self.custom_param.get('hit_range', [8, 8, 6])
        self.hit_range_conf = self.hit_range
        self.pve_hit_range_scale = confmgr.get('mecha_init_data', default={}).get('8002', {}).get('pve_diff_param', {}).get('pve_hit_range_scale', 1.0)
        self.init_hit_range_parameters()
        self.small_hit_range_scale = self.custom_param.get('small_hit_range_scale', 0.5)
        self.hit_forward_offset = self.custom_param.get('hit_forward_offset', 0.5) * NEOX_UNIT_SCALE
        self.right_offset = self.custom_param.get('right_offset', 1) * NEOX_UNIT_SCALE
        self.offset_y = math3d.vector(0, self.hit_height, 0)
        self.hit_forward = math3d.vector(0, 0, 1)
        self.hit_right = math3d.vector(1, 0, 0)
        self.is_start_hit = False
        self._trigger_cd_timer_id = None
        self._wait_start = False
        self.skill_break_power = []
        break_data_config = confmgr.get('break_data', str(self.skill_id))
        if break_data_config:
            break_power = break_data_config.get('cBreakPower', None)
            self.skill_break_power = {self.skill_id: break_power}
        self.is_pve = global_data.game_mode.is_pve()
        self.hit_phantom = []
        self.sword_skill_id = 8002511
        self.enable_extra_sword = False
        self.enable_param_changed_by_buff()
        return

    def get_time(self, config, key, default_time=0.2):
        return config.get(key, default_time) / self.timeScale

    def on_update_skill(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            print('[error] test--on_update_skill--skill_id =', self.skill_id)
            import traceback
            traceback.print_stack()
            return
        self.sub_state = self.max_stage - skill_obj._left_count
        if skill_obj._last_cast_time > 0:
            pass_time = tutil.time() - skill_obj._last_cast_time
            leave_time = self.trigger_skill_max_duration - pass_time
            if leave_time > 0:
                self._trigger_cd_timer_id = global_data.game_mgr.register_logic_timer(self.cost_skill_energy, leave_time, times=1, mode=timer.CLOCK)

    def on_change_stage_count(self, count):
        self.max_stage = count

    def create_hit_collision(self):
        size = math3d.vector(self.hit_width / 2.0, self.hit_height, self.hit_depth / 2.0)
        self.hit_col = collision.col_object(collision.BOX, size, 0, 0, 0)
        self.hit_col.mask = collision_const.GROUP_SHOOTUNIT
        self.hit_col.group = collision_const.GROUP_SHOOTUNIT
        size = math3d.vector(NEOX_UNIT_SCALE * 0.3, NEOX_UNIT_SCALE * 0.4, NEOX_UNIT_SCALE / 10)
        self.valid_col = collision.col_object(collision.BOX, size, 0, 0, 0)
        self.valid_col.mask = collision_const.GROUP_CHARACTER_INCLUDE
        self.valid_col.group = collision_const.GROUP_CHARACTER_INCLUDE

    def reset_hit_collision(self):
        if self.hit_col:
            global_data.game_mgr.scene.scene_col.remove_object(self.hit_col)
            self.hit_col = None
        self.create_hit_collision()
        return

    def create_test_hit_collision--- This code section failed: ---

 282       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_FALSE    43  'to 43'

 283      15  LOAD_GLOBAL           2  'global_data'
          18  LOAD_ATTR             3  'game_mgr'
          21  LOAD_ATTR             4  'scene'
          24  LOAD_ATTR             5  'scene_col'
          27  LOAD_ATTR             6  'remove_object'
          30  LOAD_FAST             0  'self'
          33  LOAD_ATTR             7  'test_hit_col'
          36  CALL_FUNCTION_1       1 
          39  POP_TOP          
          40  JUMP_FORWARD          0  'to 43'
        43_0  COME_FROM                '40'

 285      43  LOAD_GLOBAL           8  'math3d'
          46  LOAD_ATTR             9  'vector'
          49  LOAD_FAST             0  'self'
          52  LOAD_ATTR            10  'hit_width'
          55  LOAD_CONST            2  2.0
          58  BINARY_DIVIDE    
          59  LOAD_FAST             0  'self'
          62  LOAD_ATTR            11  'hit_height'
          65  LOAD_FAST             0  'self'
          68  LOAD_ATTR            12  'hit_depth'
          71  LOAD_CONST            2  2.0
          74  BINARY_DIVIDE    
          75  CALL_FUNCTION_3       3 
          78  STORE_FAST            1  'size'

 286      81  LOAD_GLOBAL          13  'collision'
          84  LOAD_ATTR            14  'col_object'
          87  LOAD_GLOBAL          13  'collision'
          90  LOAD_ATTR            15  'BOX'
          93  LOAD_FAST             1  'size'
          96  LOAD_CONST            3  ''
          99  LOAD_CONST            3  ''
         102  LOAD_CONST            3  ''
         105  CALL_FUNCTION_5       5 
         108  LOAD_FAST             0  'self'
         111  STORE_ATTR            7  'test_hit_col'

 287     114  LOAD_GLOBAL          16  'collision_const'
         117  LOAD_ATTR            17  'GROUP_SHOOTUNIT'
         120  LOAD_FAST             0  'self'
         123  LOAD_ATTR             7  'test_hit_col'
         126  STORE_ATTR           18  'mask'

 288     129  LOAD_GLOBAL          16  'collision_const'
         132  LOAD_ATTR            17  'GROUP_SHOOTUNIT'
         135  LOAD_FAST             0  'self'
         138  LOAD_ATTR             7  'test_hit_col'
         141  STORE_ATTR           19  'group'

 289     144  LOAD_GLOBAL           2  'global_data'
         147  LOAD_ATTR             3  'game_mgr'
         150  LOAD_ATTR             4  'scene'
         153  LOAD_ATTR             5  'scene_col'
         156  LOAD_ATTR            20  'add_object'
         159  LOAD_FAST             0  'self'
         162  LOAD_ATTR             7  'test_hit_col'
         165  CALL_FUNCTION_1       1 
         168  POP_TOP          

 290     169  LOAD_FAST             0  'self'
         172  LOAD_ATTR            21  'ev_g_model_rotation'
         175  CALL_FUNCTION_0       0 
         178  LOAD_FAST             0  'self'
         181  LOAD_ATTR             7  'test_hit_col'
         184  STORE_ATTR           22  'rotation_matrix'

 291     187  LOAD_FAST             0  'self'
         190  LOAD_ATTR            23  'ev_g_position'
         193  CALL_FUNCTION_0       0 
         196  LOAD_FAST             0  'self'
         199  LOAD_ATTR            24  'offset_y'
         202  BINARY_ADD       
         203  LOAD_FAST             0  'self'
         206  LOAD_ATTR             7  'test_hit_col'
         209  STORE_ATTR           25  'position'
         212  LOAD_CONST            0  ''
         215  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def register_callbacks(self):
        self.reset_sub_states_callback()
        for stage, one_config in six.iteritems(self.attack_param):
            start_time = 0
            self.register_substate_callback(stage, start_time, self.start)
            combo_time = self.get_time(one_config, 'combo', 1)
            self.register_substate_callback(stage, combo_time, self.combo)
            hit_start_time = self.get_time(one_config, 'hit_start', 1.5)
            self.register_substate_callback(stage, hit_start_time, self.hit_start)
            large_col_time = self.get_time(one_config, 'large_col', 1.5)
            self.register_substate_callback(stage, large_col_time, self.large_col)
            hit_end_time = self.get_time(one_config, 'hit_end', 1.5)
            self.register_substate_callback(stage, hit_end_time, self.hit_end)
            anim_duration = self.get_time(one_config, 'anim_duration', 1.5)
            self.register_substate_callback(stage, anim_duration, self.end)

    def start(self, *args):
        self._wait_start = False
        clip_name, part, blend_dir = self.attack_param[self.sub_state]['anim']
        self.send_event('E_START_WHIRLWIND', self.sub_state, self.max_stage, self.trigger_skill_max_duration, self.trigger_skill_max_duration)
        self.send_event('E_POST_ACTION', clip_name, LOW_BODY, blend_dir, timeScale=self.timeScale)
        self.trigger_skill()
        self.send_event('E_UPDATE_STATUS_TIME', self.sid)
        if self._trigger_cd_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._trigger_cd_timer_id)
            self._trigger_cd_timer_id = None
        self._trigger_cd_timer_id = global_data.game_mgr.register_logic_timer(self.cost_skill_energy, self.trigger_skill_max_duration, times=1, mode=timer.CLOCK)
        return

    def cost_skill_energy(self):
        if self._trigger_cd_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._trigger_cd_timer_id)
            self._trigger_cd_timer_id = None
        self.sub_state = self.ATTACK_END
        self.send_event('E_END_SKILL', self.skill_id)
        return

    def trigger_skill(self):
        max_duration = self.trigger_skill_max_duration
        if self.sub_state >= self.max_stage:
            max_duration = 0
        self.send_event('E_DO_SKILL', self.skill_id, self.sub_state, False)

    def end(self, *args):
        self.send_event('E_ANIM_RATE', LOW_BODY, 1)
        self.send_event('E_ACTIVE_STATE', MC_STAND)
        if self.sub_state >= self.max_stage:
            self.sub_state = self.ATTACK_END

    def start_move(self, *args):
        walk_direction = self.ev_g_model_forward()
        attack_param = self.attack_param[self.sub_state]
        self.brake_begin = self.get_time(attack_param, 'brake', 0.2)
        move_duration = self.brake_begin - self.get_time(attack_param, 'hit_start', 0.2)
        speed = self.move_dist / move_duration
        brake_duration = self.get_time(attack_param, 'combo', 1) - self.brake_begin
        self.brake_speed = (self.brake_move_dist - speed * brake_duration) * 2 / brake_duration ** 2
        self.brake_speed = abs(self.brake_speed)
        cur_pos = self.ev_g_position()
        total_dist = self.brake_move_dist + self.move_dist
        target_pos = cur_pos + walk_direction * total_dist
        diff_pos = target_pos - cur_pos
        walk_direction = walk_direction * speed
        self.start_move_pos = cur_pos
        self.sd.ref_cur_speed = speed
        self.send_event('E_SET_WALK_DIRECTION', walk_direction, reach_target_callback=self.reach_target_callback, reach_target_pos=target_pos)
        self._is_moving = True
        self.send_event('E_VERTICAL_SPEED', 0)

    def reach_target_callback(self):
        cur_pos = self.ev_g_position()
        diff_pos = cur_pos - self.start_move_pos
        self.stop_or_continue_move()

    def stop_or_continue_move(self):
        move_dir, move_state = self.ev_g_input_move_dir()
        if not move_dir or move_dir.is_zero:
            self.send_event('E_CLEAR_SPEED')

    def brake_tick(self, dt):
        if self.sub_sid_timer < self.brake_begin:
            return
        speed = self.sd.ref_cur_speed
        if speed <= 0:
            return
        walk_direction = self.ev_g_model_forward()
        if walk_direction.is_zero:
            return
        decr_speed = self.brake_speed * dt
        speed -= decr_speed
        speed = max(speed, 0)
        self.sd.ref_cur_speed = speed
        walk_direction = walk_direction * speed
        self.send_event('E_SET_WALK_DIRECTION', walk_direction)

    def cal_hit_right_dir(self):
        camera = global_data.game_mgr.scene.active_camera
        if not camera:
            return
        world_rotation_matrix = camera.world_rotation_matrix
        forward = world_rotation_matrix.forward
        up = math3d.vector(0, 1, 0)
        right = math3d.vector(0, 0, 0)
        if not forward.is_zero:
            forward.normalize()
            right = up.cross(forward)
        if not right.is_zero:
            right.normalize()
        self.hit_right = right * self.right_offset

    def hit_start(self, *args):
        self.start_move()
        self.cal_hit_right_dir()
        self.is_start_hit = True
        pos = self.ev_g_position() + self.offset_y
        self.hit_forward = self.ev_g_model_forward()
        self.hit_col.position = pos + self.hit_right + self.hit_forward * self.hit_forward_offset
        self.hit_col.rotation_matrix = self.ev_g_model_rotation()
        global_data.game_mgr.scene.scene_col.add_object(self.hit_col)
        scene_utils.set_col_scale(self.hit_col, self.small_hit_range_scale)
        self.alreay_hit_objs = set()
        self.hit_phantom = []
        self.hit_need_stop_obj = False

    def large_col(self, *args):
        scene_utils.set_col_scale(self.hit_col, 1)

    def hit_end(self, *args):
        self.is_start_hit = False
        global_data.game_mgr.scene.scene_col.remove_object(self.hit_col)
        if self.enable_extra_sword and self.is_pve:
            if self.ev_g_is_agent():
                fire_forward = self.ev_g_forward()
                fire_position = self.ev_g_position()
            else:
                scn = world.get_active_scene()
                camera = scn.active_camera
                fire_forward = camera.rotation_matrix.forward
                fire_position = camera.position
            self.send_event('E_DO_SKILL', self.sword_skill_id, 1, fire_position, fire_forward)

    def combo(self, *args):
        self.send_event('E_ADD_WHITE_STATE', self.combo_status, self.sid)
        if MC_MOVE in self.combo_status:
            move_dir = self.sd.ref_rocker_dir
            if move_dir and not move_dir.is_zero:
                self.send_event('E_SET_SMOOTH_DURATION', LOW_BODY_SELECT, self.blend_to_move_time)
                self.send_event('E_ACTIVE_STATE', MC_MOVE)

    def combo_attack(self):
        need_cover_old_states = self.ev_g_can_cover_states(self.sid)
        if need_cover_old_states:
            if self.sid in need_cover_old_states:
                need_cover_old_states.remove(self.sid)
            self.send_event('E_DISABLE_STATE', need_cover_old_states)
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.sub_state += 1
        self._wait_start = True
        sound_idx = 3 if self.sub_state > 3 else self.sub_state
        sound_name = ['m_8002_weapon1_atk%d' % sound_idx, 'nf']
        self.send_event('E_EXECUTE_MECHA_ACTION_SOUND', 1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_EXECUTE_MECHA_ACTION_SOUND, (1, sound_name, 0, 0, 1, SOUND_TYPE_MECHA_FIRE)], True)

    def enter(self, leave_states):
        super(NormalWhirlwind, self).enter(leave_states)
        self._wait_start = False
        self.send_event('E_STEP_HEIGHT', self.dash_stepheight)

    def exit(self, enter_states):
        super(NormalWhirlwind, self).exit(enter_states)
        self.send_event('E_RESET_STEP_HEIGHT')
        self.send_event('E_ANIM_RATE', LOW_BODY, 1)
        self._is_moving = False
        self.reset_step_height()
        self.send_event('E_RESET_GRAVITY')
        global_data.game_mgr.scene.scene_col.remove_object(self.hit_col)
        if self.ev_g_on_ground():
            self.stop_or_continue_move()
        if self.ev_g_immobilized():
            self.send_event('E_POST_ACTION', 'shake', LOW_BODY, 1)
        if self.sub_state >= self.max_stage:
            self.sub_state = self.ATTACK_END

    def reset_step_height(self):
        pass

    def _process_break_power(self, tgt_model_name, pos):
        impulse_power = self.skill_break_power.get(self.skill_id, None)
        if not impulse_power:
            return
        else:
            scn = world.get_active_scene()
            if not scn:
                return
            tgt_model = scn.get_model(tgt_model_name)
            if not tgt_model:
                return
            normal = tgt_model.world_position - pos
            normal.normalize()
            break_item_info = {'model_col_name': tgt_model.name,'point': pos,
               'normal': normal,
               'power': impulse_power,
               'break_type': collision_const.BREAK_TRIGGER_TYPE_WEAPON
               }
            self.break_obj_list.append(break_item_info)
            return

    def update(self, dt):
        super(NormalWhirlwind, self).update(dt)
        self.check_hit_enemy_tick(dt)
        self.brake_tick(dt)
        if self.sub_state == self.ATTACK_END:
            self.disable_self()

    def check_valid(self, eid):
        target = EntityManager.getentity(eid)
        if target and target.logic and target.logic.MASK & NEED_CHECK_VALID_TAG_VALUE == 0:
            return True
        if target and target.logic:
            pos = target.logic.ev_g_position()
            if not pos:
                return True
            start_pos = math3d.vector(pos.x, pos.y, pos.z)
            pos = self.ev_g_position()
            if not pos:
                return True
            end_pos = math3d.vector(pos.x, pos.y, pos.z)
            direct = end_pos - start_pos
            direct.y = 0
            if direct.is_zero:
                return True
            direct.normalize()
            forward = self.ev_g_forward()
            if not forward or direct.dot(forward) > 0.0:
                return False
            if target.__class__.__name__ == 'Puppet':
                offset = state_physic_arg.stand_collision_width * NEOX_UNIT_SCALE
                offset_y = state_physic_arg.stand_collision_height * NEOX_UNIT_SCALE / 2
            else:
                physic_info = target.logic.ev_g_mecha_config('PhysicConfig')
                if not physic_info:
                    return True
                offset = physic_info['character_size'][0] * NEOX_UNIT_SCALE / 2
                offset_y = physic_info['character_size'][1] * NEOX_UNIT_SCALE / 2
            start_pos = start_pos + direct * offset * 1.8
            start_pos.y += offset_y + NEOX_UNIT_SCALE
            physic_info = self.ev_g_mecha_config('PhysicConfig')
            end_pos.y += physic_info['character_size'][1] * NEOX_UNIT_SCALE / 2
            self.valid_col.position = start_pos
            self.valid_col.rotation_matrix = math3d.matrix.make_orient(direct, math3d.vector(0, 1, 0))
            GROUP_COLLISION = collision_const.GROUP_CHARACTER_INCLUDE & ~(collision_const.GROUP_CHARACTER_INCLUDE & collision_const.WATER_GROUP)
            result = global_data.game_mgr.scene.scene_col.sweep_test(self.valid_col, start_pos, end_pos, GROUP_COLLISION, GROUP_COLLISION, 0, collision.INCLUDE_FILTER)
            if result:
                return not result[0]
        return True

    def get_whirlwind_state(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            return (self.sub_state, self.max_stage, 0, self.trigger_skill_max_duration)
        if skill_obj._last_cast_time > 0:
            pass_time = tutil.time() - skill_obj._last_cast_time
            leave_time = self.trigger_skill_max_duration - pass_time
            return (
             self.sub_state, self.max_stage, leave_time, self.trigger_skill_max_duration)

    def play_hit_effect(self, eid):
        model = self.ev_g_model()
        if not model:
            return
        else:
            start = model.get_bone_matrix(ATTACK_BONE, world.SPACE_TYPE_WORLD).translation
            pos, rot = None, math3d.matrix()
            entity = EntityManager.getentity(eid)
            if entity and entity.logic:
                target_model = entity.logic.ev_g_model()
                if target_model and target_model.valid:
                    end = target_model.position + math3d.vector(0, target_model.bounding_box.y, 0)
                    direct = end - start
                    direct.normalize()
                    direct *= NEOX_UNIT_SCALE * 50
                    if entity.logic.sd.ref_model_hit_by_ray_func:
                        res = entity.logic.sd.ref_model_hit_by_ray_func(start, direct)
                    else:
                        res = target_model.hit_by_ray2(start, direct)
                    if res and res[0]:
                        pos = start + direct * res[1]
            if not pos:
                return rot
            sfx_path = 'effect/fx/robot/robot_qishi/qishi_daoguang_hit.sfx'
            self.send_event('E_SHOW_SKILL_HIT_SFX', sfx_path, (pos.x, pos.y, pos.z))
            return rot

    def check_hit_enemy_tick(self, dt):
        if not self.is_start_hit:
            return
        else:
            if not global_data.player or not global_data.player.logic:
                return
            main_player = global_data.player.logic
            self.break_obj_list = []
            pos = self.ev_g_position() + self.offset_y
            self.hit_col.position = pos + self.hit_right + self.hit_forward * self.hit_forward_offset
            ret = global_data.game_mgr.scene.scene_col.static_test(self.hit_col, 65535, collision_const.GROUP_SHOOTUNIT, collision.INCLUDE_FILTER) or []
            hit_obj = []
            hit_static = []
            hit_effect_rot = []
            hit_phantom = []
            hit_cid = self.ev_g_human_base_col_id()
            relative_ids = self.sd.ref_mecha_relative_cols
            self_cids = [self.hit_col.cid, hit_cid]
            if relative_ids:
                self_cids.extend(relative_ids)
            for col in ret:
                if col.cid not in self_cids:
                    model_col_name = getattr(col, 'model_col_name', '')
                    if is_break_obj(model_col_name):
                        self._process_break_power(model_col_name, self.hit_col.position)
                    if global_data.emgr.scene_is_shoot_obj.emit(col.cid):
                        res = global_data.emgr.scene_find_unit_event.emit(col.cid)
                        if res and res[0] and res[0].__class__.__name__ == 'LHouse':
                            self.is_start_hit = False
                            return
                        if res and res[0] and res[0].__class__.__name__ == 'LField':
                            eid = res[0].id
                            field = EntityManager.getentity(eid)
                            if field and field.logic and self.ev_g_is_campmate(field.logic.ev_g_camp_id()):
                                continue
                            if eid not in self.alreay_hit_objs and self.check_valid(eid):
                                self.is_start_hit = False
                                hit_obj.append(eid)
                                rot = self.play_hit_effect(eid)
                                hit_effect_rot.append(rot)
                                self.alreay_hit_objs.add(eid)
                                break
                        if res and res[0] and col.cid in global_data.phantoms:
                            if res[0] not in self.hit_phantom:
                                self.hit_phantom.append(res[0])
                                do_hit_phantom(self, res[0])
                            continue
                        if res and res[0] and res[0].ev_g_is_campmate(self.ev_g_camp_id()):
                            continue
                        if res and res[0] and res[0] != global_data.player.logic:
                            eid = res[0].id
                            ent = EntityManager.getentity(eid)
                            if not ent:
                                continue
                            if eid not in self.alreay_hit_objs and self.check_valid(eid):
                                if res[0].MASK & NEED_STOP_WHEN_CONTACT_TAG_VALUE and not self.is_pve:
                                    self.hit_need_stop_obj = True
                                    if res[0].__class__.__name__ == 'LDeathDoor':
                                        self.hit_need_stop_obj = not res[0].ev_g_is_weak_door()
                                if res[0].__class__.__name__ == 'LHPBreakable':
                                    if res[0].share_data.ref_hp is None or res[0].share_data.ref_hp <= 0:
                                        continue
                                if res[0].__class__.__name__ == 'LMecha':
                                    mecha_creator = res[0].ev_g_creator()
                                    if not mecha_creator:
                                        continue
                                    is_teammate = main_player.ev_g_is_groupmate(mecha_creator.id, False)
                                    if is_teammate:
                                        continue
                                hit_obj.append(eid)
                                rot = self.play_hit_effect(eid)
                                hit_effect_rot.append(rot)
                                self.alreay_hit_objs.add(eid)
                    else:
                        hit_static.append(col)

            start = self.hit_col.position
            if len(hit_obj) > 0:
                if self.hit_need_stop_obj:
                    self.send_event('E_CLEAR_SPEED')
                    self._is_moving = False
                pos = self.ev_g_position()
                self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, [hit_obj, hit_effect_rot, (pos.x, pos.y, pos.z)]), False, True)
                for eid in hit_obj:
                    target = EntityManager.getentity(eid)
                    if target and target.logic:
                        target.logic.send_event('E_HIT_SHIELD_SFX', end=start)

            if self.break_obj_list:
                global_data.emgr.scene_add_break_objs.emit(self.break_obj_list, True)
            return