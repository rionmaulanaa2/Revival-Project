# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8018.py
from __future__ import absolute_import
import six
from logic.gcommon import time_utility as tutil
from .StateBase import StateBase
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from common.utils import timer
from logic.comsys.control_ui.ShotChecker import ShotChecker
import logic.gcommon.const as g_const
import logic.gcommon.common_utils.status_utils as status_utils
from logic.gcommon.common_const import collision_const
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
from data import camera_state_const
from logic.gutils.character_ctrl_utils import AirWalkDirectionSetter
import world
import collision
import math3d
import math
from logic.gutils import scene_utils
from logic.gcommon.common_const.web_const import MECHA_MEMORY_LEVEL_8
from logic.gutils.mecha_utils import do_hit_phantom
from logic.gcommon.common_const.ui_operation_const import DRAG_DASH_BTN_8018

class SequenceShoot8018(StateBase):
    BIND_EVENT = {'E_ADD_WIND_RUSH_SKILL': 'on_update_skill',
       'E_FIRE': 'on_fire',
       'TRY_STOP_WEAPON_ATTACK': 'end',
       'G_SEQUENCE_SHOOT_8018_STATE': 'get_sequence_shoot_state'
       }
    ATTACK_END = 0
    STATE_TO_POS = {1: g_const.PART_WEAPON_POS_MAIN2,2: g_const.PART_WEAPON_POS_MAIN2,
       3: g_const.PART_WEAPON_POS_MAIN3
       }
    SUB_ST_PRE = 4
    SUB_ST_HOLD = 5

    def read_data_from_custom_param(self):
        self.skill_id = self.custom_param.get('skill_id', None)
        self.weapon_pos = g_const.PART_WEAPON_POS_MAIN2
        self.blend_dir = self.custom_param.get('blend_dir', 1)
        self.timeScale = self.custom_param.get('timeScale', 1)
        self.pre_time = self.custom_param.get('pre_time', 1)
        self.break_time = self.custom_param.get('break_time', 1)
        self.attack_param = self.custom_param['attack_param']
        self.all_up_body_anim = set()
        for anims in six.itervalues(self.attack_param):
            anim, _ = anims['pre_anim']
            self.all_up_body_anim.add(anim)
            anim, _ = anims['hold_anim']
            self.all_up_body_anim.add(anim)
            anim, _ = anims['anim']
            self.all_up_body_anim.add(anim)

        self.break_states = status_utils.convert_status(self.custom_param.get('break_states', set()))
        skill_conf = confmgr.get('skill_conf', str(self.skill_id))
        ext_info = skill_conf.get('ext_info', {})
        self.trigger_skill_max_duration = ext_info.get('continue_time', 5)
        self.continue_count = ext_info.get('continue_count', 3)
        return

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(SequenceShoot8018, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.try_break = False
        self.re_active_self = False
        self.can_break = False
        self.fired = False
        self.fired_time = 0
        self.acted = False
        self.do_skill = True
        self._trigger_cd_timer_id = None
        self.continue_state = 0
        self.sub_state = self.ATTACK_END
        self.is_try_combo_attack = False
        self.is_cancel_state = False
        self.is_add_white_state = False
        self.click_down = False
        self.register_substate()
        return

    def get_sequence_shoot_state(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            return (self.continue_state, self.continue_count, 0, self.trigger_skill_max_duration)
        if skill_obj._last_cast_time > 0:
            pass_time = tutil.time() - skill_obj._last_cast_time
            leave_time = self.trigger_skill_max_duration - pass_time
            return (
             self.continue_state, self.continue_count, leave_time, self.trigger_skill_max_duration)

    def get_time(self, config, key, default_time=0.2):
        return config.get(key, default_time) / self.timeScale

    def register_substate(self):
        self.reset_sub_states_callback()
        for stage, one_config in six.iteritems(self.attack_param):
            self.register_substate_callback(stage, 0, self.start)
            anim_duration = self.get_time(one_config, 'anim_duration', 1.5)
            self.register_substate_callback(stage, anim_duration, self.end)

        self.register_substate_callback(self.SUB_ST_PRE, 0, self.pre)
        self.register_substate_callback(self.SUB_ST_PRE, self.pre_time, self.pre_end)
        self.register_substate_callback(self.SUB_ST_HOLD, 0, self.hold)

    def destroy(self):
        super(SequenceShoot8018, self).destroy()
        if self._trigger_cd_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._trigger_cd_timer_id)
            self._trigger_cd_timer_id = None
        return

    def action_btn_down(self):
        self.click_down = True
        if self.continue_state >= self.continue_count:
            return False
        else:
            if not self.re_active_self and self.can_break:
                self.can_break = False
                self.disable_self()
                self.re_active_self = True
                return False
            if self.is_active:
                return False
            if not self.sd.ref_is_robot and ShotChecker().check_camera_can_shot():
                return False
            if not self.check_can_active():
                return False
            if not self.check_can_cast_skill():
                return False
            self.weapon_pos = self.STATE_TO_POS.get(self.continue_state + 1)
            if not self.ev_g_is_weapon_can_fire(self.weapon_pos):
                return False
            if not self.ev_g_try_weapon_attack_begin(self.weapon_pos):
                return False
            self.send_event('E_RESET_ROTATION')
            self.active_self()
            if self.ev_g_is_avatar():
                self.is_cancel_state = False
                from logic.comsys.mecha_ui.MechaCancelUI import MechaCancelUI
                MechaCancelUI(None, self.cancel_state)
            super(SequenceShoot8018, self).action_btn_down()
            return True

    def action_btn_up(self):
        self.click_down = False
        if self.sub_state == self.ATTACK_END or self.is_cancel_state:
            super(SequenceShoot8018, self).action_btn_cancel()
            return False
        if not self.is_active:
            return False
        self.try_combo_attack()
        super(SequenceShoot8018, self).action_btn_up()
        return True

    def cancel_state(self):
        self.is_cancel_state = True
        self.end()
        self.send_event('E_ACTION_UP', self.bind_action_id)
        self.reset_aim_ui()
        if not self.do_skill:
            self.continue_state -= 1
            self.do_skill = True

    def reset_aim_ui(self):
        if self.continue_state == 1:
            sub_ui = global_data.ui_mgr.get_ui('Mecha8018SubUI')
            if sub_ui:
                sub_ui.reset_aim_ui()

    def try_combo_attack(self):
        if self.continue_state <= self.continue_count:
            self.combo_attack()

    def on_update_skill(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            return
        self.continue_state = self.continue_count - skill_obj._left_count
        if skill_obj._last_cast_time > 0:
            pass_time = tutil.time() - skill_obj._last_cast_time
            leave_time = self.trigger_skill_max_duration - pass_time
            if leave_time > 0:
                if self._trigger_cd_timer_id:
                    global_data.game_mgr.unregister_logic_timer(self._trigger_cd_timer_id)
                self._trigger_cd_timer_id = global_data.game_mgr.register_logic_timer(self.cost_skill_energy, leave_time, times=1, mode=timer.CLOCK)

    def pre(self, *args):
        clip_name, blend_dir = self.attack_param[self.continue_state]['pre_anim']
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, blend_dir, timeScale=self.timeScale)

    def pre_end(self, *args):
        self.sub_state = self.SUB_ST_HOLD

    def hold(self, *args):
        self.send_event('E_SEQUENCE_SHOOT_8018_HOLD', self.continue_state)
        clip_name, blend_dir = self.attack_param[self.continue_state]['hold_anim']
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, blend_dir, timeScale=self.timeScale, loop=True)
        self.send_event('E_PLAY_CAMERA_TRK', '1055_CHARGE')

    def start(self, *args):
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
        clip_name, blend_dir = self.attack_param[self.continue_state]['anim']
        self.send_event('E_START_SEQUENCESHOOT_8018', self.continue_state, self.continue_count, self.trigger_skill_max_duration, self.trigger_skill_max_duration)
        self.send_event('E_POST_ACTION', clip_name, UP_BODY, blend_dir, timeScale=self.timeScale)
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
        self.continue_state = 0
        self.do_skill = True
        self.sub_state = self.ATTACK_END
        self.send_event('E_END_SKILL', self.skill_id)
        self.disable_self()
        self.reset_aim_ui()
        return

    def combo(self, *args):
        pass

    def combo_attack(self):
        self.sub_state = self.continue_state

    def enter(self, leave_states):
        if self.do_skill:
            self.continue_state += 1
            self.sub_state = self.SUB_ST_PRE
            self.do_skill = False
        self.acted = False
        self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        super(SequenceShoot8018, self).enter(leave_states)
        if not self.click_down:
            self.action_btn_up()

    def exit(self, enter_states):
        super(SequenceShoot8018, self).exit(enter_states)
        self.send_event('E_SEQUENCE_SHOOT_8018_END')
        self.is_add_white_state = False
        self.send_event('E_CANCEL_CAMERA_TRK', '1055_CHARGE')
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
            if not self.fired and not self.is_cancel_state:
                self.cancel_state()
        self.fired = False
        self.fired_time = 0
        self.can_break = False
        if not self.acted:
            weapon_state_info = None
            if self.continue_state in self.STATE_TO_POS:
                weapon_state_info = {'sub_state': self.continue_state}
            self.ev_g_try_weapon_attack_end(self.weapon_pos, True, weapon_state_info)
        self.acted = False
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        if self.sd.ref_up_body_anim in self.all_up_body_anim:
            self.send_event('E_CLEAR_UP_BODY_ANIM')
        if self.re_active_self:
            self.action_btn_down()
        self.re_active_self = False
        if self.continue_state >= self.continue_count:
            self.continue_state = 0
        return

    def trigger_skill(self):
        self.acted = True
        weapon_state_info = None
        if self.continue_state in self.STATE_TO_POS:
            weapon_state_info = {'sub_state': self.continue_state}
        self.ev_g_try_weapon_attack_end(self.weapon_pos, weapon_state_info=weapon_state_info)
        self.send_event('E_DO_SKILL', self.skill_id, self.continue_state, False)
        self.do_skill = True
        if self.ev_g_is_avatar():
            global_data.ui_mgr.close_ui('MechaCancelUI')
        return

    def update(self, dt):
        if self.fired:
            self.fired_time += dt
            self.can_break = self.fired_time >= self.break_time
            if not self.is_add_white_state and self.can_break:
                self.send_event('E_ADD_WHITE_STATE', self.break_states, self.sid)
                self.is_add_white_state = True
        super(SequenceShoot8018, self).update(dt)

    def end(self, *args):
        self.disable_self()

    def on_fire(self, f_cdtime, weapon_pos, *args):
        if not self.is_active:
            return
        if weapon_pos != self.weapon_pos:
            return
        self.fired = True
        self.fired_time = 0

    def refresh_action_param(self, action_param, custom_param):
        super(SequenceShoot8018, self).refresh_action_param(action_param, custom_param)
        if custom_param:
            self.custom_param = custom_param
            self.read_data_from_custom_param()


class OxRushNew8018(StateBase):
    BIND_EVENT = {'E_ADD_WIND_RUSH_SKILL': 'on_update_skill',
       'E_ON_POST_JOIN_MECHA': 'on_post_join_mecha',
       'E_ON_LEAVE_MECHA_START': 'on_leave_mecha_start',
       'E_SET_RUSH_DURATION_TIME_SCALE': 'rush_time_scale',
       'G_RUSH_8018_STATE': 'get_rush_state'
       }
    STATE_END = -1
    STATE_PRE = 0
    STATE_RUSH = 1
    STATE_MISS = 2
    IS_AUTO_OX_RUSH_COL_CHECK = False
    IS_AUTO_PLAY_RUSH_ANIM = True
    IS_AUTO_PLAY_MISS_ANIM = True

    def get_rush_info(self):
        dash_param = self.custom_param.get('dash_param', {})
        if self.continue_state in dash_param:
            info = dash_param[self.continue_state]
            self.pre_anim = info.get('pre_anim', 'dash_01')
            self.pre_anim_duration = info.get('pre_anim_duration', 0.2)
            self.rush_anim = info.get('rush_anim', 'dash_02')
            self.max_rush_duration = info.get('max_rush_duration', 0.7) * (self.rush_time_scale + 1)
            self.miss_anim = info.get('miss_anim', 'dash_03')
            self.miss_anim_duration = info.get('miss_anim_duration', 0.5)
            self.max_rush_speed = info.get('max_rush_speed', 60) * NEOX_UNIT_SCALE
            self.start_acc_time = info.get('start_acc_time', 0.1)
            self.acc_speed = self.max_rush_speed / (self.pre_anim_duration - self.start_acc_time)
            self.end_brake_time = info.get('end_brake_time', 0.1)
            self.brake_speed = self.max_rush_speed / self.end_brake_time
            self.start_acc_camera = info.get('start_acc_camera', camera_state_const.MECHA_MODE_FOUR_RUSH)
            self.miss_brake_camera = info.get('miss_brake_camera', camera_state_const.MECHA_MODE_FOUR)
            self.col_info = info.get('col_info', (30, 50))

    def read_data_from_custom_param(self):
        self.tick_interval = self.custom_param.get('tick_interval', 0.1)
        self.skill_id = self.custom_param.get('skill_id', None)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.miss_anim_rate = self.custom_param.get('miss_anim_rate', 1.0)
        self.dash_stepheight = self.custom_param.get('dash_stepheight', 2 * NEOX_UNIT_SCALE)
        self.cam_yaw_sensitivity = self.custom_param.get('cam_yaw_sensitivity', 35) * 0.001
        self.cam_pitch_sensitivity = self.custom_param.get('cam_pitch_sensitivity', 15) * 0.001
        self.air_dash_end_speed = self.custom_param.get('air_dash_end_speed', 0) * NEOX_UNIT_SCALE
        self.boom_dist = self.custom_param.get('boom_dist', 4) * NEOX_UNIT_SCALE
        skill_conf = confmgr.get('skill_conf', str(self.skill_id))
        ext_info = skill_conf.get('ext_info', {})
        self.trigger_skill_max_duration = ext_info.get('continue_time', 5)
        self.continue_count = ext_info.get('continue_count', 2)
        self.range_pitch_angle = self.custom_param.get('range_pitch_angle', [-60, -30])
        self.range_pitch_speed_ratio = self.custom_param.get('range_pitch_speed_ratio', [1.0, 0.3])
        min_angle, max_angle = self.range_pitch_angle
        min_ratio, max_ratio = self.range_pitch_speed_ratio
        self.one_angle_ratio = (max_ratio - min_ratio) / (max_angle - min_angle)
        return

    def _register_sub_state_callbacks(self):
        self.reset_sub_states_callback()
        self.register_substate_callback(self.STATE_PRE, 0.0, self.on_begin_pre)
        self.register_substate_callback(self.STATE_PRE, self.start_acc_time / self.pre_anim_rate, self.on_start_acc)
        self.register_substate_callback(self.STATE_PRE, self.pre_anim_duration / self.pre_anim_rate, self.on_end_pre)
        self.register_substate_callback(self.STATE_RUSH, 0.0, self.on_begin_rush)
        self.register_substate_callback(self.STATE_RUSH, self.max_rush_duration, self.on_end_rush)
        self.register_substate_callback(self.STATE_MISS, 0.0, self.on_begin_miss)
        self.register_substate_callback(self.STATE_MISS, self.end_brake_time / self.miss_anim_rate, self.on_end_miss_brake)
        self.register_substate_callback(self.STATE_MISS, self.miss_anim_duration / self.miss_anim_rate, self.on_end_miss)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(OxRushNew8018, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.read_data_from_custom_param()
        self.air_walk_direction_setter = AirWalkDirectionSetter(self)
        self.need_trigger_btn_up_when_action_forbidden = False
        self.is_accelerating = False
        self.is_braking = False
        self.is_moving = False
        self.cur_speed = 0.0
        self.rush_finished = False
        self.re_active_self = False
        self.continual_on_ground = False
        self.target_hitted = False
        self.water_time_scale = 1.0
        self._old_pos = math3d.vector(0, 0, 0)
        self._dash_dis = 0
        self.is_hit_play_skill = True
        self.post_brake_timer = None
        self.event_registered = False
        self.continue_state = 0
        self._trigger_cd_timer_id = None
        self.do_skill = True
        self.is_first_dash = True
        self.target_hitted = None
        self.rush_time_scale = 0
        self.sub_state = self.STATE_END
        self.hit_id = set()
        self.check_hit_timer = None
        self.hit_phantom = []
        return

    def destroy(self):
        if self.event_registered:
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = False
        if self.air_walk_direction_setter:
            self.air_walk_direction_setter.destroy()
            self.air_walk_direction_setter = None
        self.clear_trigger_cd()
        self.stop_check_hit()
        super(OxRushNew8018, self).destroy()
        return

    def clear_trigger_cd(self):
        if self._trigger_cd_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._trigger_cd_timer_id)
        self._trigger_cd_timer_id = None
        return

    def on_post_join_mecha(self):
        if self.ev_g_is_avatar() and not self.event_registered:
            self.regist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = True

    def on_leave_mecha_start(self):
        if self.ev_g_is_avatar() and self.event_registered:
            self.unregist_event('E_ROTATE', self.on_cam_rotate)
            self.event_registered = False

    def action_btn_up(self):
        if self.continue_state >= self.continue_count:
            return
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        if not self.re_active_self and self.is_first_dash and self.sub_state > self.STATE_PRE:
            self.rush_finished = True
            self.re_active_self = True
            return
        self.active_self()
        self.sound_custom_start()
        super(OxRushNew8018, self).action_btn_up()

    def enter(self, leave_states):
        if self.do_skill:
            self.continue_state += 1
            self.do_skill = False
            self.get_rush_info()
            self.is_first_dash = self.continue_state == 1
            self.IS_AUTO_PLAY_RUSH_ANIM = self.is_first_dash
            self.IS_AUTO_PLAY_MISS_ANIM = self.is_first_dash
            self.IS_AUTO_OX_RUSH_COL_CHECK = self.is_first_dash
            self._register_sub_state_callbacks()
        super(OxRushNew8018, self).enter(leave_states)
        self.init_parameters()
        self.air_walk_direction_setter.reset()
        self.start_rush()
        if self.is_first_dash:
            self.send_event('E_DO_OXRUSH_8018', True)
            self.start_check_hit()

    def get_rush_state(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            return (self.continue_state, self.continue_count, 0, self.trigger_skill_max_duration)
        if skill_obj._last_cast_time > 0:
            pass_time = tutil.time() - skill_obj._last_cast_time
            leave_time = self.trigger_skill_max_duration - pass_time
            return (
             self.continue_state, self.continue_count, leave_time, self.trigger_skill_max_duration)

    def on_update_skill(self):
        skill_obj = self.ev_g_skill(self.skill_id)
        if not skill_obj:
            return
        self.continue_state = self.continue_count - skill_obj._left_count
        if skill_obj._last_cast_time > 0:
            pass_time = tutil.time() - skill_obj._last_cast_time
            leave_time = self.trigger_skill_max_duration - pass_time
            if leave_time > 0:
                self.clear_trigger_cd()
                self._trigger_cd_timer_id = global_data.game_mgr.register_logic_timer(self.cost_skill_energy, leave_time, times=1, mode=timer.CLOCK)

    def cost_skill_energy(self):
        self.clear_trigger_cd()
        self.continue_state = 0
        self.do_skill = True
        self.send_event('E_END_SKILL', self.skill_id)
        self.send_event('E_BEGIN_RECOVER_MP', self.skill_id)
        self.disable_self()
        self.send_event('E_OXRUSH_ENABLE', '2')

    def trigger_rush_skill(self):
        self.send_event('E_DO_SKILL', self.skill_id, self.continue_state, True)
        self.do_skill = True

    def start_rush(self):
        self.send_event('E_START_RUSH_8018', self.continue_state, self.continue_count, self.trigger_skill_max_duration, self.trigger_skill_max_duration)
        self.send_event('E_STEP_HEIGHT', self.dash_stepheight)
        self.send_event('E_IGNORE_RELOAD_ANIM', True)
        self.trigger_rush_skill()
        self.sound_drive.run_start()
        self.send_event('E_GRAVITY', 0)
        self._start_pre()
        self.clear_trigger_cd()
        self._trigger_cd_timer_id = global_data.game_mgr.register_logic_timer(self.cost_skill_energy, self.trigger_skill_max_duration, times=1, mode=timer.CLOCK)

    def _start_pre(self):
        if self.is_first_dash:
            if self.ev_g_on_ground():
                self.sub_state = self.STATE_PRE
            else:
                self.on_start_acc()
                self.on_end_pre()
        else:
            self.sub_state = self.STATE_PRE

    def init_parameters(self):
        self.is_accelerating = False
        self.is_braking = False
        self.is_moving = False
        self.rush_finished = False
        self.continual_on_ground = True
        self.cur_speed = 0.0
        self.target_hitted = False
        self._old_pos = self.ev_g_position()
        self.hit_phantom = []

    def on_begin_pre(self):
        self.send_event('E_CLEAR_SPEED')
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)
        if self.is_first_dash:
            return
        model = self.ev_g_model()
        if model:
            sock_mat = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
            s_position = sock_mat.translation
            direction = model.world_transformation.forward
            direction.normalize()
            e_position = s_position + direction * self.boom_dist
            result = global_data.game_mgr.scene.scene_col.hit_by_ray(s_position, e_position, 0, collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.REGION_SCENE_GROUP, collision_const.GROUP_STATIC_SHOOTUNIT | collision_const.REGION_SCENE_GROUP, collision.INCLUDE_FILTER, False)
            if result[0]:
                e_position = result[1]
            self.send_skill_hit((2, (e_position.x, e_position.y, e_position.z)))

    def on_start_acc(self, *args):
        global_data.player.logic.send_event('E_MECHA_CAMERA', self.start_acc_camera)
        effect = global_data.emgr.show_screen_effect.emit('MeleeRushEffect', {})
        if effect:
            effect = effect[0]
            effect and effect.show()
        if self.IS_AUTO_OX_RUSH_COL_CHECK:
            self.send_event('E_OX_BEGIN_RUSH')
        self.send_event('E_VERTICAL_SPEED', 0)
        self.send_event('E_FORBID_ROTATION', True)
        self.is_accelerating = True
        self.is_moving = True

    def on_end_pre(self):
        self.sub_state = self.STATE_RUSH
        self.is_accelerating = False
        self.cur_speed = self.max_rush_speed

    def on_begin_rush(self):
        self.send_event('E_OXRUSH_ENABLE', self.continue_state)
        self.is_moving = True
        self.cur_speed = self.max_rush_speed
        if self.IS_AUTO_PLAY_RUSH_ANIM:
            self.send_event('E_ANIM_RATE', LOW_BODY, 1.0)
            self.send_event('E_POST_ACTION', self.rush_anim, LOW_BODY, 1, loop=True)
        self._start_cal_dash_dist()

    def on_end_rush(self):
        if self.ev_g_on_ground():
            self.sub_state = self.STATE_MISS
        else:
            self._rush_finished()
        self._finish_cal_dash_dist()
        global_data.emgr.enable_camera_yaw.emit(False)

    def _rush_finished(self):
        self.rush_finished = True
        if self.continue_state >= self.continue_count:
            self.continue_state = 0

    def _start_cal_dash_dist(self):
        self._dash_dis = 0
        self._old_pos = self.ev_g_position()
        self.regist_pos_change(self._on_pos_changed, 0.1)

    def _finish_cal_dash_dist(self):
        self.unregist_pos_change(self._on_pos_changed)
        if self._dash_dis > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'record_mecha_memory', ('8018', MECHA_MEMORY_LEVEL_8, self._dash_dis / NEOX_UNIT_SCALE), False, True)

    def _on_pos_changed(self, pos):
        dist = int((pos - self._old_pos).length)
        self._old_pos = pos
        if dist > 0:
            self._dash_dis += dist

    def on_begin_miss(self):
        if self.IS_AUTO_PLAY_MISS_ANIM:
            self.send_event('E_ANIM_RATE', LOW_BODY, self.miss_anim_rate)
            self.send_event('E_POST_ACTION', self.miss_anim, LOW_BODY, 1)
        self.is_braking = True

    def on_end_miss_brake(self):
        self.is_braking = False
        self.is_moving = False
        self.cur_speed = 0.0
        self.send_event('E_FORBID_ROTATION', False)
        self.send_event('E_RESET_ROTATION')
        self.send_event('E_ACTION_SYNC_STOP')
        self.sound_drive.run_end()
        self.send_event('E_CLEAR_SPEED')
        if self.ev_g_on_ground():
            self.send_event('E_RESET_GRAVITY')
        else:
            self.send_event('E_FALL')
        global_data.player.logic.send_event('E_MECHA_CAMERA', self.miss_brake_camera)

    def on_end_miss(self):
        self.sound_drive.run_end()
        self._rush_finished()

    def update_dash_param(self, scale):
        time_scale = self.water_time_scale / scale
        self.send_event('E_ANIM_RATE', LOW_BODY, scale if scale < 1 else 1)
        self.max_rush_speed /= time_scale
        self.water_time_scale = scale

    def update(self, dt):
        super(OxRushNew8018, self).update(dt)
        if self.is_accelerating:
            self.cur_speed += self.acc_speed * dt
            if self.cur_speed > self.max_rush_speed:
                self.cur_speed = self.max_rush_speed
        elif self.is_braking:
            self.cur_speed -= self.brake_speed * dt
            if self.cur_speed < 0:
                self.cur_speed = 0.0
        if self.is_moving:
            scn = world.get_active_scene()
            speed_scale = self.ev_g_speedup_skill_scale() or 1.0
            self.update_dash_param(speed_scale)
            cam_forward = scn.active_camera.rotation_matrix.forward
            cam_pitch = scn.active_camera.rotation_matrix.pitch
            angle = math.degrees(cam_pitch)
            min_angle, max_angle = self.range_pitch_angle
            min_ratio, max_ratio = self.range_pitch_speed_ratio
            if angle > min_angle and angle < max_angle:
                cur_ratio = (angle - min_angle) * self.one_angle_ratio + min_ratio
            elif angle <= min_angle:
                cur_ratio = min_ratio
            else:
                cur_ratio = max_ratio
            walk_direction = self.get_walk_direction(cam_forward, cur_ratio)
            self.air_walk_direction_setter.execute(walk_direction)
            if not self.ev_g_on_ground():
                self.continual_on_ground = False
            if self.continual_on_ground and cam_forward.y < 0:
                cam_forward.y = 0
                cam_forward.normalize()
            self.send_event('E_FORWARD', cam_forward, True)

    def check_transitions(self):
        if self.rush_finished:
            if not self.ev_g_on_ground():
                self.disable_self()
                return MC_JUMP_2
            rocker_dir = self.sd.ref_rocker_dir
            self.disable_self()
            if rocker_dir and not rocker_dir.is_zero:
                return MC_MOVE
            return MC_STAND

    def get_walk_direction(self, cam_forward, cur_ratio=1.0):
        dir = 1 if self.is_first_dash else -1
        return cam_forward * (dir * self.cur_speed * cur_ratio)

    def exit(self, enter_states):
        super(OxRushNew8018, self).exit(enter_states)
        if self.sub_state == self.STATE_PRE:
            self.send_event('E_OXRUSH_ENABLE', self.continue_state)
        self.send_event('E_IGNORE_RELOAD_ANIM', False)
        global_data.emgr.enable_camera_yaw.emit(True)
        global_data.emgr.destroy_screen_effect.emit('MeleeRushEffect')
        if self.ev_g_on_ground() and MC_SUPER_JUMP not in enter_states:
            self.send_event('E_CLEAR_SPEED')
        elif self.air_dash_end_speed:
            scn = world.get_active_scene()
            cam_forward = scn.active_camera.rotation_matrix.forward
            self.cur_speed = self.air_dash_end_speed
            walk_direction = self.get_walk_direction(cam_forward)
            walk_direction.y = 0
            self.send_event('E_SET_WALK_DIRECTION', walk_direction)
        self.send_event('E_FORBID_ROTATION', False)
        self.send_event('E_RESET_ROTATION')
        if self.IS_AUTO_OX_RUSH_COL_CHECK:
            self.send_event('E_OX_END_RUSH')
        self.send_event('E_RESET_GRAVITY')
        self.send_event('E_RESET_STEP_HEIGHT')
        global_data.player.logic.send_event('E_MECHA_CAMERA', self.miss_brake_camera)
        self.sub_state = self.STATE_END
        if self.re_active_self:
            self.action_btn_up()
        self.re_active_self = False
        if self.is_first_dash:
            self.send_event('E_DO_OXRUSH_8018', False)
            self.stop_check_hit()

    def on_hit_target(self, target):
        pass

    def on_cam_rotate(self, *args):
        if self.is_active and self.is_moving:
            scn = world.get_active_scene()
            speed_scale = self.ev_g_speedup_skill_scale() or 1.0
            self.update_dash_param(speed_scale)
            cam_forward = scn.active_camera.rotation_matrix.forward
            walk_direction = self.get_walk_direction(cam_forward)
            self.air_walk_direction_setter.execute(walk_direction)
            if not self.ev_g_on_ground():
                self.continual_on_ground = False
            if self.continual_on_ground and cam_forward.y < 0:
                cam_forward.y = 0
                cam_forward.normalize()
            self.send_event('E_FORWARD', cam_forward, True)

    def send_skill_hit(self, info):
        self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, info), False, True)

    def rush_time_scale(self, val):
        self.rush_time_scale += val

    def get_hit_unit_id_list(self):
        height, radius = self.col_info
        if global_data.player and global_data.player.logic:
            pos = self.ev_g_position() + math3d.vector(0, height, 0)
            unit_datas = global_data.emgr.scene_get_hit_enemy_unit.emit(self.unit_obj.ev_g_camp_id(), pos, radius)
            hit_unit_id_list = []
            if unit_datas and unit_datas[0]:
                for unit in unit_datas[0]:
                    unit_id = unit.id
                    if unit_id not in self.hit_id:
                        if scene_utils.dash_filtrate_hit(self.unit_obj, unit):
                            continue
                        self.hit_id.add(unit_id)
                        hit_unit_id_list.append(unit_id)

            hit_phantom = global_data.emgr.scene_get_hit_all_phantom_unit.emit(pos, radius)
            if hit_phantom:
                for phantom_list in hit_phantom:
                    for phantom in phantom_list:
                        if phantom not in self.hit_phantom:
                            do_hit_phantom(self, phantom)
                            self.hit_phantom.append(phantom)

                return hit_unit_id_list

    def start_check_hit(self):
        self.clear_check_hit_timer()
        self.check_hit_timer = global_data.game_mgr.get_logic_timer().register(func=self._check_hit, mode=timer.CLOCK, interval=0.1)

    def _check_hit(self):
        hit_unit_id_list = self.get_hit_unit_id_list()
        if hit_unit_id_list:
            self.send_skill_hit((1, hit_unit_id_list))

    def clear_check_hit_timer(self):
        self.check_hit_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_hit_timer)
        self.check_hit_timer = None
        return

    def stop_check_hit(self):
        self.clear_check_hit_timer()
        self.hit_id = set()