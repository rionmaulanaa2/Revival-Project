# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_logic/ComOpenAimHelper.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from ...UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
import world
import logic.gcommon.common_const.animation_const as animation_const
from common.const import common_const
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.const import ATTACHEMNT_AIM_POS
from common.cfg import confmgr
import math3d
import logic.gcommon.cdata.status_config as status_config
import math
from data.camera_state_const import AIM_MODE
import game3d
TARGET_HIT_BONES = [
 animation_const.BONE_SPINE2_NAME,
 'biped l calf',
 'biped r calf',
 'biped l forearm',
 'biped r forearm']
CHECK_NEED_UPDATE_KEY = 'fScopeRangeSlowOutside'
KEY_SLOW_RANGE_0 = 'f{0}ScopeRangeSlowInside'
KEY_SLOW_RANGE_1 = 'f{0}ScopeRangeSlowOutside'
KEY_SLOW_RANGE_2 = 'f{0}ScopeRangeBullet'
KEY_MIN_MODIFY = 'f{0}RangeSlowMin'
KEY_HIT_BOX_MIN_MODIFY = 'f{0}HitboxRangeSlowMin'
KEY_OPEN_AIM_ADSORB_V = 'f{0}OpenAimAdsorbV'
KEY_OPEN_AIM_ADSORB_MAX_DIST = 'f{0}OpenAimAdsorbMaxDist'
MAX_AIM_DISTANCE = 1000 * NEOX_UNIT_SCALE
MAX_RANGE_NUM = 20
MECHA_AIM_BONE_NAME_LIST = [
 'biped']
HUMAN_AIM_BONE_NAME_LIST = [animation_const.BONE_SPINE2_NAME, animation_const.BONE_SPINE1_NAME]
INF_VALUE = 1000000 * NEOX_UNIT_SCALE

class ComOpenAimHelper(UnitCom):
    DYNAMIC_EVENT = {'E_SUCCESS_AIM': 'on_success_aim',
       'E_QUIT_AIM': 'on_quit_aim',
       'G_SIGHTING_TARGET_POS': '_get_sighting_target_pos',
       'E_GUN_ATTACK': 'on_gun_attack',
       'E_TOUCH_SLIDE': 'on_touch_slide',
       'G_ADSORB_DIFF_TARGET_YAW': 'get_adsorb_diff_target_yaw',
       'G_AIM_LOOK_AT_POS': 'get_aim_look_at_pos',
       'E_ACTION_SWITCHING': 'on_switch_weapon',
       'E_ON_ACTION_ON_VEHICLE': '_on_enter_mecha',
       'E_ON_ACTION_ENTER_MECHA': '_on_enter_mecha',
       'E_ON_JOIN_MECHA': '_on_enter_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_ON_ACTION_LEAVE_VEHICLE': '_on_leave_mecha',
       'E_ON_ENABLE_AIM_HELPER': 'on_enable_aim_helper'
       }

    def __init__(self):
        super(ComOpenAimHelper, self).__init__()
        self.target_id = None
        self.tick_interval = 1
        self.tick_count = 0
        self.sd.ref_modify_ratio = 1.0
        self.slow_dist_sqr_inside = 0
        self.slow_dist_sqr_outside = 0
        self.aim_dist_sqr = 0
        self.need_handle_dist_sqr = 0
        self.find_target_dist_sqr = 0
        self._min_sensor_modify = 0
        self._adsorb_v = 0
        self._adsorb_max_dist = 0
        self._adsorb_target_id = None
        self._adsorb_target_pos = None
        self._adsorb_time = 0
        self._adsorb_by_fire = False
        self._camera_offset_yaw = 0
        self.init_config()
        self.is_in_aim = False
        self.aim_helper_allowed = True
        self.aim_helper_enabled = True
        self.event_registered = False
        self.want_to_tick = True
        return

    def _process_event(self, flag):
        if self.event_registered ^ flag:
            process_func = self.regist_event if flag else self.unregist_event
            for event_name, func_name in self.DYNAMIC_EVENT.items():
                process_func(event_name, getattr(self, func_name))

            if G_POS_CHANGE_MGR:
                if flag:
                    self.regist_pos_change(self._on_pos_changed)
                else:
                    self.unregist_pos_change(self._on_pos_changed)
            else:
                process_func('E_POSITION', self._on_pos_changed)
            emgr = global_data.emgr
            econf = {'player_enable_aim_helper': self.on_enable_aim_helper,
               'player_user_setting_changed_event': self.on_user_setting_changed
               }
            if flag:
                emgr.bind_events(econf)
            else:
                emgr.unbind_events(econf)
            self.event_registered = flag

    def _refresh_tick_state(self):
        need_update = self.aim_helper_enabled and self.want_to_tick and self.check_cur_weapon_need_update()
        if self.need_update ^ need_update:
            self.need_update = need_update
            self.update_aim_config()
            if not need_update:
                self.target_id = None
                self.sd.ref_modify_ratio = 1.0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComOpenAimHelper, self).init_from_dict(unit_obj, bdict)
        self.aim_helper_allowed = not (global_data.is_pc_mode or global_data.deviceinfo.is_emulator())
        self.aim_helper_enabled = global_data.player.get_setting(uoc.AIM_HELPER_KEY_1)
        self.event_registered = False
        if self.aim_helper_allowed:
            self._process_event(True)

    def on_user_setting_changed(self, *args, **kwargs):
        self.aim_helper_enabled = global_data.player.get_setting(uoc.AIM_HELPER_KEY_1)
        self._refresh_tick_state()

    def on_post_init_complete(self, bdict):
        self._refresh_tick_state()

    def destroy(self):
        self._process_event(False)
        super(ComOpenAimHelper, self).destroy()

    def get_ref_bones(self, target):
        if not target:
            return MECHA_AIM_BONE_NAME_LIST
        else:
            if target.ev_g_is_human():
                return HUMAN_AIM_BONE_NAME_LIST
            return MECHA_AIM_BONE_NAME_LIST

    def _on_enter_mecha(self, *args, **kwargs):
        self.on_enable_aim_helper(False)

    def _on_leave_mecha(self, *args):
        self.on_enable_aim_helper(True)

    def on_enable_aim_helper(self, flag):
        if self.want_to_tick ^ flag:
            self.want_to_tick = flag
            self._refresh_tick_state()
        self._adsorb_target_pos = None
        return

    def _get_open_aim_target_id(self):
        return self.target_id

    def on_touch_slide(self):
        if not self._adsorb_by_fire:
            return
        else:
            self._adsorb_by_fire = False
            self._adsorb_target_id = None
            self._adsorb_target_pos = None
            return

    def on_switch_weapon(self, *args):
        self._refresh_tick_state()

    def on_gun_attack(self, *args, **kwargs):
        self.debug_gun_attack()

    def debug_gun_attack(self, *args):
        self._adsorb_target_pos = None
        if not global_data.player:
            return
        else:
            camera = self.get_camera()
            if not camera:
                return
            weapon_config = self.get_weapon_config()
            if not weapon_config:
                return
            aim_attach_id = weapon_config.get('iType')
            adsorb_args_conf = confmgr.get('fire_adsorb_args', default={}).get(str(aim_attach_id), {})
            if not adsorb_args_conf:
                return
            target = self.get_target()
            if not target:
                return
            target_type = self.get_target_type()
            key = 'f{}FireTime'.format(target_type)
            fire_time = adsorb_args_conf.get(key, 0)
            if not fire_time:
                return
            adsorb_v = adsorb_args_conf.get('f{}AdsorbV'.format(target_type), 0)
            if not adsorb_v:
                return
            dist_key = 'f{}Dist'.format(target_type)
            max_dist = adsorb_args_conf.get(dist_key, 0) * NEOX_UNIT_SCALE
            if not max_dist:
                return
            dist_scale = self.get_attack_dist_adjust_scale(target)
            if not dist_scale:
                return
            dist = self.get_target_dist(target, use_pos_dist=False)
            max_dist = (max_dist * dist_scale) ** 2
            if dist > max_dist:
                return
            position = camera.world_position
            direction = camera.world_transformation.forward
            is_hit_target = self.is_can_hit_target(target, position, direction * MAX_AIM_DISTANCE)
            if is_hit_target:
                return
            self._adsorb_target_id = self.target_id
            self._adsorb_v = adsorb_v
            self._adsorb_max_dist = max_dist
            self._adsorb_time = fire_time
            self._adsorb_by_fire = True
            self.check_adsorb_target()
            self.send_event('E_GUN_ATTACK_ADSORB')
            return

    def _get_sighting_target_pos(self, start_pos, direction, ignore_aim_dist=False):
        if not self.target_id:
            return None
        else:
            target_puppet = self.get_target()
            if not target_puppet:
                return None
            target_pos = target_puppet.ev_g_position()
            if not target_pos:
                return None
            if not self.is_can_hit_target(target_puppet, start_pos, direction * MAX_AIM_DISTANCE):
                target_model = target_puppet.ev_g_model()
                hit_pos = self.get_neareast_can_hit_pos(target_puppet, ignore_aim_dist=ignore_aim_dist)
                return hit_pos
            return None

    def get_neareast_can_hit_pos(self, target_puppet, ignore_aim_dist):
        model = target_puppet.ev_g_model()
        camera = self.get_camera()
        if not model:
            return
        else:
            camera_pos = camera.world_position
            camera_forward = camera.world_transformation.forward
            model_pos = None
            bone_list = self.get_ref_bones(target_puppet)
            for one_bone_name in bone_list:
                matrix = model.get_bone_matrix(one_bone_name, world.SPACE_TYPE_WORLD)
                if matrix:
                    model_pos = matrix.translation
                    break

            if not model_pos:
                return
            dist = self._cal_dist_sqr_point_to_line(model_pos, camera_pos, camera_forward)
            is_dist_exceed = dist > self.aim_dist_sqr
            if not ignore_aim_dist and is_dist_exceed:
                return
            if not target_puppet.ev_g_is_human():
                if ignore_aim_dist:
                    return (model_pos, is_dist_exceed)
                else:
                    return model_pos

            bone_2_socket = {'biped l forearm': 'l_forearm','biped r forearm': 'r_forearm'
               }
            target_pos = None
            max_sqr_dis = dist
            last_bone_name = ''
            for index in range(1, len(TARGET_HIT_BONES)):
                bone_name = TARGET_HIT_BONES[index]
                bone_mat = model.get_bone_matrix(bone_name, world.SPACE_TYPE_WORLD)
                if not bone_mat:
                    log_error('cannot find bone [%s] in model [%s]!!!!!!!', bone_name, model.filename)
                    continue
                bone_pos = bone_mat.translation
                one_dist = self._cal_dist_sqr_point_to_line(bone_pos, camera_pos, camera_forward)
                if one_dist <= max_sqr_dis:
                    last_bone_name = bone_name
                    socket_name = bone_2_socket.get(bone_name, '')
                    if socket_name:
                        if model.has_socket(socket_name):
                            mat = model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)
                            target_pos = mat.translation
                        else:
                            target_pos = bone_pos
                            log_error('lack socket: ', socket_name, ', on model: ', model.filename)
                    else:
                        target_pos = bone_pos
                    max_sqr_dis = one_dist

            if ignore_aim_dist:
                return (target_pos, is_dist_exceed)
            return target_pos
            return

    def is_can_hit_target(self, target_puppet, start_pos, pdir):
        subresult = target_puppet.ev_g_model_hit_ray(start_pos, pdir)
        return bool(subresult)

    def _on_aim(self, *args):
        self._adsorb_target_pos = None
        if not global_data.player:
            return
        else:
            if not self.target_id:
                old_target_id = self.target_id
                self._update_target()
                if old_target_id != self.target_id and self.target_id and self.aim_helper_enabled:
                    self.update_aim_config()
                else:
                    self.update_min_sensor_modify()
            self.update_aim_config()
            if not self.target_id:
                return
            weapon_config = self.get_weapon_config()
            if not weapon_config:
                return
            self._adsorb_target_id = self.target_id
            target_type = self.get_target_type()
            key = KEY_OPEN_AIM_ADSORB_V.format(target_type)
            self._adsorb_v = float(weapon_config.get(key, 0))
            self._adsorb_by_fire = False
            if not self._adsorb_v:
                return
            target = self.get_adsorb_target()
            self._adsorb_max_dist = self.get_open_aim_adsorb_max_dist(target) ** 2
            if not self._adsorb_max_dist:
                return
            if target:
                self.check_adsorb_target()
            return

    def get_open_aim_adsorb_max_dist(self, target):
        if not target:
            return 0
        self_pos = self.ev_g_position()
        if not self_pos:
            return 0
        aim_config = self.get_aim_config()
        if not aim_config:
            return 0
        dist_key_prefix = 'cHumanDist'
        if target.share_data.ref_is_mecha:
            dist_key_prefix = 'cMechaDist'
        target_type = self.get_target_type()
        adsorb_max_dist_key_prefix = KEY_OPEN_AIM_ADSORB_MAX_DIST.format(target_type)
        dist = self.get_target_dist(target, use_pos_dist=True)
        dist = dist ** 0.5
        for index in range(1, MAX_RANGE_NUM):
            dist_key = dist_key_prefix + str(index)
            adsorb_max_dist_key = adsorb_max_dist_key_prefix + str(index)
            one_dist_range = aim_config.get(dist_key, [])
            if not one_dist_range:
                break
            one_min_dist = one_dist_range[0] * NEOX_UNIT_SCALE
            one_max_dist = one_dist_range[1] * NEOX_UNIT_SCALE
            if dist < one_min_dist or dist > one_max_dist:
                continue
            return aim_config.get(adsorb_max_dist_key, 0) * NEOX_UNIT_SCALE

        return 0

    def update_camera_yaw(self, dt, *args):
        if self._adsorb_target_pos:
            self._update_adsorb_target_info(dt)

    def on_success_aim(self):
        self.is_in_aim = True
        self._refresh_tick_state()

    def on_quit_aim(self):
        self.is_in_aim = False
        self._refresh_tick_state()
        self._adsorb_target_pos = None
        return

    def get_weapon_config(self):
        if self.is_in_aim:
            return self.ev_g_attachment_attr(ATTACHEMNT_AIM_POS)
        else:
            obj_weapon = self.sd.ref_wp_bar_cur_weapon
            if not obj_weapon:
                return None
            return confmgr.get('firearm_config', str(obj_weapon.get_item_id()))
            return None

    def get_aim_config(self):
        aim_attach_id = 0
        if self.is_in_aim:
            weapon_config = self.ev_g_attachment_attr(ATTACHEMNT_AIM_POS)
            aim_config = None
            if weapon_config:
                aim_attach_id = weapon_config.get('iType')
        else:
            obj_weapon = self.sd.ref_wp_bar_cur_weapon
            if not obj_weapon:
                return
            aim_attach_id = obj_weapon.get_item_id()
        return confmgr.get('firearm_aim_args', str(aim_attach_id))

    def check_cur_weapon_need_update(self):
        weapon_config = self.get_weapon_config()
        return bool(weapon_config and weapon_config.get(CHECK_NEED_UPDATE_KEY, 0))

    def update_aim_config(self):
        enable_helper = self.need_update
        if enable_helper:
            weapon_config = self.get_weapon_config()
            if not weapon_config:
                return
            self.update_conf(weapon_config)
        else:
            self.reset_conf()

    def reset_conf(self):
        self._min_sensor_modify = 0
        self.slow_dist_sqr_inside = 0
        self.slow_dist_sqr_outside = 0
        self.aim_dist_sqr = 0
        self.need_handle_dist_sqr = 0
        self.find_target_dist_sqr = 0

    def update_min_sensor_modify(self):
        result = self.get_dist_aim_conf()
        target_type = self.get_target_type()
        if not result:
            return
        aim_config, index = result
        if not aim_config or not index:
            return
        camera = self.get_camera()
        if not camera:
            return
        target_puppet = self.get_target()
        key = KEY_MIN_MODIFY.format(target_type) + str(index)
        target_type = self.get_target_type()
        if target_puppet:
            position = camera.world_position
            direction = camera.world_transformation.forward
            if self.is_can_hit_target(target_puppet, position, direction * 1000):
                key = KEY_HIT_BOX_MIN_MODIFY.format(target_type) + str(index)
        min_sensor_modify_key = key.format(target_type)
        self._min_sensor_modify = float(aim_config.get(min_sensor_modify_key, 0))
        if self._min_sensor_modify <= 0:
            self._min_sensor_modify = 1

    def get_target_type(self):
        target_type = 'Human'
        if self.target_id:
            target_puppet = self.get_target()
            if target_puppet and target_puppet.share_data.ref_is_mecha:
                target_type = 'Mecha'
        return target_type

    def get_dist_aim_conf(self):
        target = self.get_target()
        if not target:
            return
        self_pos = self.ev_g_position()
        if not self_pos:
            return
        aim_config = self.get_aim_config()
        if not aim_config:
            return
        aim_attach_id = aim_config.get('iType')
        if not aim_config:
            return
        dist_key_prefix = 'cHumanDist'
        if target.share_data.ref_is_mecha:
            dist_key_prefix = 'cMechaDist'
        dist = self.get_target_dist(target, use_pos_dist=True)
        dist = dist ** 0.5
        for index in range(1, MAX_RANGE_NUM):
            dist_key = dist_key_prefix + str(index)
            one_dist_range = aim_config.get(dist_key, [])
            if not one_dist_range:
                break
            one_min_dist = one_dist_range[0] * NEOX_UNIT_SCALE
            one_max_dist = one_dist_range[1] * NEOX_UNIT_SCALE
            if dist < one_min_dist or dist > one_max_dist:
                continue
            return (aim_config, index)

    def update_conf(self, weapon_config):
        self.update_min_sensor_modify()
        result = self.get_dist_aim_conf()
        aim_config = None
        index = None
        target_type = self.get_target_type()
        if result:
            aim_config, index = result
        find_target_dist_sqr_outside_key = KEY_SLOW_RANGE_1.format('')
        self.find_target_dist_sqr = (float(weapon_config.get(find_target_dist_sqr_outside_key, 0)) * NEOX_UNIT_SCALE) ** 2
        if self.sd.ref_in_aim or self.sd.ref_is_mecha:
            slow_dist_sqr_outside_key = KEY_SLOW_RANGE_1.format('')
            self.slow_dist_sqr_outside = (float(weapon_config.get(slow_dist_sqr_outside_key, 0)) * NEOX_UNIT_SCALE) ** 2
            self.aim_dist_sqr = (float(weapon_config.get(KEY_SLOW_RANGE_2.format(''), 0)) * NEOX_UNIT_SCALE) ** 2
        elif aim_config:
            slow_dist_sqr_outside_key = KEY_SLOW_RANGE_1.format(target_type) + str(index)
            self.slow_dist_sqr_outside = (float(aim_config.get(slow_dist_sqr_outside_key, 0)) * NEOX_UNIT_SCALE) ** 2
            aim_dist_sqr_key = KEY_SLOW_RANGE_2.format(target_type) + str(index)
            self.aim_dist_sqr = (float(aim_config.get(aim_dist_sqr_key, 0)) * NEOX_UNIT_SCALE) ** 2
        self.need_handle_dist_sqr = max(self.slow_dist_sqr_outside, self.aim_dist_sqr)
        if aim_config:
            slow_dist_sqr_inside_key = KEY_SLOW_RANGE_0.format(target_type) + str(index)
            self.slow_dist_sqr_inside = (float(aim_config.get(slow_dist_sqr_inside_key, 0)) * NEOX_UNIT_SCALE) ** 2
        else:
            self.slow_dist_sqr_inside = 0
        return

    def init_config(self):
        aim_conf = confmgr.get('aim_helper_conf')
        self.update_conf(aim_conf)

    def _on_pos_changed(self, *args):
        if self.need_update:
            self.update_aim_config()

    def _try_find_target(self, *args):
        old_target_id = self.target_id
        self._update_target()
        if old_target_id != self.target_id and self.target_id:
            self.update_aim_config()
        else:
            self.update_min_sensor_modify()

    def _cal_dist_sqr_point_to_line(self, model_pos, camera_pos, camera_forward):
        tmp_vector = model_pos - camera_pos
        d = tmp_vector.dot(camera_forward) / camera_forward.length
        dist = tmp_vector.length ** 2 - d ** 2
        if dist < 0:
            dist = 0
        return dist

    def is_target_model_valid(self, target, camera_pos, camera):
        model = target.ev_g_model()
        if not model:
            return (False, None, None)
        else:
            if not model.is_visible_in_this_frame():
                return (False, None, None)
            character_pos = self.get_aim_pos_from_model(target)
            if not character_pos:
                return (False, None, None)
            character_direction = character_pos - camera_pos
            if character_direction.is_zero:
                return (False, None, None)
            screen_pos = camera.world_to_screen(character_pos)
            pos_diff = (common_const.WINDOW_WIDTH * 0.5 - screen_pos[0]) * (common_const.WINDOW_WIDTH * 0.5 - screen_pos[0]) + (common_const.WINDOW_HEIGHT * 0.5 - screen_pos[1]) * (common_const.WINDOW_HEIGHT * 0.5 - screen_pos[1])
            return (
             True, character_pos, pos_diff)

    def _update_target(self):
        self.target_id = self._find_one_type_target(global_data.war_noteam_puppets)
        if self.target_id is None:
            self.target_id = self._find_one_type_target(global_data.war_noteam_mechas)
        if self.target_id is None:
            self.sd.ref_modify_ratio = 1.0
        return

    def _find_one_type_target(self, puppets_dict):
        camera = self.get_camera()
        camera_pos = camera.world_position
        target_id = None
        model_pos = None
        min_diff = None
        for puppet_key, lpuppet in six.iteritems(puppets_dict):
            if not lpuppet:
                continue
            if self.ev_g_is_groupmate(lpuppet.id):
                continue
            if lpuppet.ev_g_death():
                continue
            is_valid, character_pos, pos_diff = self.is_target_model_valid(lpuppet, camera_pos, camera)
            if not is_valid:
                continue
            if min_diff is None or pos_diff < min_diff:
                min_diff = pos_diff
                target_id = puppet_key
                model_pos = character_pos

        if model_pos is None:
            return
        else:
            dist_sqr = self._cal_dist_sqr_point_to_line(model_pos, camera_pos, camera.world_transformation.forward)
            if dist_sqr > self.find_target_dist_sqr:
                target_id = None
            return target_id

    def get_target(self):
        target = global_data.war_noteam_puppets.get(self.target_id, None)
        if not target:
            target = global_data.war_noteam_mechas.get(self.target_id, None)
        return target

    def get_adsorb_target(self):
        if not self._adsorb_target_id:
            return
        else:
            target = global_data.war_noteam_puppets.get(self._adsorb_target_id, None)
            if not target:
                target = global_data.war_noteam_mechas.get(self._adsorb_target_id, None)
            return target

    def get_attack_dist_adjust_scale(self, target):
        if not target:
            return 1
        else:
            self_pos = self.ev_g_position()
            if not self_pos:
                return 1
            weapon_config = self.get_weapon_config()
            if not weapon_config:
                return 1
            aim_attach_id = weapon_config.get('iType')
            adsorb_args_conf = confmgr.get('fire_adsorb_args', default={}).get(str(aim_attach_id), {})
            if not adsorb_args_conf:
                return 1
            dist_key_prefix = 'cHumanDist'
            dist_scale_key_prefix = 'cHumanDistScale'
            if target.share_data.ref_is_mecha:
                dist_key_prefix = 'cMechaDist'
                dist_scale_key_prefix = 'cMechaDistScale'
            dist = self.get_target_dist(target, use_pos_dist=True)
            dist = dist ** 0.5
            dist_scale = 1
            last_dist_index = None
            for index in range(1, MAX_RANGE_NUM):
                dist_key = dist_key_prefix + str(index)
                dist_scale_key = dist_scale_key_prefix + str(index)
                one_dist_range = adsorb_args_conf.get(dist_key, [])
                if not one_dist_range:
                    break
                one_min_dist = one_dist_range[0] * NEOX_UNIT_SCALE
                one_max_dist = one_dist_range[1] * NEOX_UNIT_SCALE
                last_dist_index = index
                if dist < one_min_dist or dist > one_max_dist:
                    continue
                one_dist_scale_range = adsorb_args_conf.get(dist_scale_key, [])
                if not one_dist_scale_range:
                    break
                dist_scale = (dist - one_min_dist) / (one_max_dist - one_min_dist) * (one_dist_scale_range[1] - one_dist_scale_range[0]) + one_dist_scale_range[0]
                return dist_scale

            if last_dist_index is not None:
                dist_key = dist_key_prefix + str(last_dist_index)
                one_dist_range = adsorb_args_conf.get(dist_key, [])
                one_max_dist = one_dist_range[1] * NEOX_UNIT_SCALE
                if dist > one_max_dist:
                    return 0
            return dist_scale

    def get_speed_adjust_scale(self, target):
        if not target:
            return 1
        target_pos = target.ev_g_position()
        if not target_pos:
            return 1
        self_pos = self.ev_g_position()
        if not self_pos:
            return 1
        aim_config = self.get_aim_config()
        if not aim_config:
            return 1
        is_mecha = target.share_data.ref_is_mecha
        speed_key_prefix = 'cHumanSpeed'
        speed_scale_key_prefix = 'cHumanSpeedScale'
        if is_mecha:
            speed_key_prefix = 'cMechaSpeed'
            speed_scale_key_prefix = 'cMechaSpeedScale'
        self_move_dir = self.ev_g_get_walk_direction() or math3d.vector(0, 0, 0)
        target_move_dir = target.ev_g_get_walk_direction() or math3d.vector(0, 0, 0)
        diff_move_dir = self_move_dir - target_move_dir
        target_speed = diff_move_dir.length
        speed_scale = 1
        for index in range(1, MAX_RANGE_NUM):
            speed_key = speed_key_prefix + str(index)
            speed_scale_key = speed_scale_key_prefix + str(index)
            one_speed_range = aim_config.get(speed_key, [])
            if not one_speed_range:
                break
            if target_speed < one_speed_range[0] or target_speed > one_speed_range[1]:
                continue
            one_speed_scale_range = aim_config.get(speed_scale_key, [])
            if not one_speed_scale_range:
                break
            speed_scale = (target_speed - one_speed_range[0]) / (one_speed_range[1] - one_speed_range[0]) * (one_speed_scale_range[1] - one_speed_scale_range[0]) + one_speed_scale_range[0]
            break

        return speed_scale

    def get_target_dist(self, target, use_pos_dist=True):
        if use_pos_dist:
            target_model_pos = target.ev_g_position()
            if not target_model_pos:
                return 0
            self_pos = self.ev_g_position()
            if not self_pos:
                return 0
            diff_offset = self_pos - target_model_pos
            return diff_offset.length_sqr
        else:
            camera = self.get_camera()
            target_model_pos = self.get_aim_pos_from_model(target)
            if not target_model_pos:
                return INF_VALUE
            camera_pos = camera.world_position
            dist_sqr = self._cal_dist_sqr_point_to_line(target_model_pos, camera_pos, camera.world_transformation.forward)
            return dist_sqr

    def check_adsorb_target(self):
        self._adsorb_target_pos = None
        scn = world.get_active_scene()
        if not scn:
            return
        else:
            camera = self.get_camera()
            if not camera:
                return
            target = self.get_adsorb_target()
            if not target or not target.ev_g_model():
                self._adsorb_target_id = None
                target = None
            camera_position = camera.world_position
            camera_direction = camera.world_transformation.forward
            if camera_direction.is_zero:
                return
            if target:
                start_pos = camera_position + camera_direction * 2.5
                is_hit_target = False
                if self.is_in_aim:
                    result = self._get_sighting_target_pos(start_pos, camera_direction, ignore_aim_dist=True)
                    if result:
                        new_target_pos, is_dist_exceed = result
                        self._adsorb_target_pos = new_target_pos
                        if not is_dist_exceed:
                            is_hit_target = True
                else:
                    is_hit_target = self.is_can_hit_target(target, camera_position, camera_direction * MAX_AIM_DISTANCE)
                    self._adsorb_target_pos = target.ev_g_position()
                if is_hit_target:
                    self._adsorb_target_pos = None
                    return
                dist_sqr = self.get_target_dist(target, use_pos_dist=False)
                if dist_sqr > self._adsorb_max_dist:
                    self._adsorb_target_id = None
                    self._adsorb_target_pos = None
                    return
            if self._adsorb_target_pos:
                aim_dir = self._adsorb_target_pos - camera_position
                if aim_dir.is_zero:
                    self._adsorb_target_pos = None
                    return
            return

    def get_aim_look_at_pos(self):
        self._on_aim()
        adsorb_target_pos = self._adsorb_target_pos
        self._adsorb_target_pos = None
        return adsorb_target_pos

    def get_adsorb_target_yaw(self):
        scn = world.get_active_scene()
        if not scn:
            self._adsorb_target_pos = None
            return
        else:
            if not self._adsorb_target_pos:
                return
            camera = self.get_camera()
            if not camera:
                self._adsorb_target_pos = None
                return
            camera_direction = camera.world_transformation.forward
            if camera_direction.is_zero:
                return
            camera_position = camera.world_position
            aim_dir = self._adsorb_target_pos - camera_position
            if aim_dir.is_zero:
                self._adsorb_target_pos = None
                return
            aim_dir.normalize()
            target_yaw = aim_dir.yaw
            return target_yaw

    def get_adsorb_diff_target_yaw(self):
        if not self._adsorb_target_pos:
            return 0
        camera = self.get_camera()
        if not camera:
            return 0
        pi = math.pi
        pi2 = pi * 2
        target_yaw = self.get_adsorb_target_yaw()
        cur_yaw = camera.world_rotation_matrix.yaw
        diff_target_yaw = target_yaw - cur_yaw
        if diff_target_yaw > pi:
            diff_target_yaw -= pi2
        elif diff_target_yaw < -pi:
            diff_target_yaw += pi2
        return diff_target_yaw

    def _update_adsorb_target_info(self, dt):
        scn = world.get_active_scene()
        if not scn:
            self._adsorb_target_pos = None
            return
        else:
            target_yaw = self.get_adsorb_target_yaw()
            cur_yaw = self.ev_g_yaw() or 0
            pi = math.pi
            pi2 = pi * 2
            diff_target_yaw = target_yaw - cur_yaw
            if diff_target_yaw > pi:
                diff_target_yaw -= pi2
            else:
                if diff_target_yaw < -pi:
                    diff_target_yaw += pi2
                if not target_yaw or abs(diff_target_yaw) <= 0.001:
                    self._adsorb_target_pos = None
                    return
            delta_yaw = self._adsorb_v * dt
            target = self.get_adsorb_target()
            sign = diff_target_yaw / abs(diff_target_yaw)
            if delta_yaw >= abs(diff_target_yaw):
                delta_yaw = abs(diff_target_yaw)
                self._adsorb_target_pos = None
            delta_yaw *= sign
            ctrl = scn.get_com('PartCtrl')
            if ctrl:
                ctrl.rotate_camera(delta_yaw, 0, False, ignore_aim_ratio=True)
            old_time = self._adsorb_time
            self._adsorb_time -= dt
            if old_time > 0 and self._adsorb_time <= 0:
                self._adsorb_time = 0
                self._adsorb_target_pos = None
            return

    def _update_target_info(self):
        scn = world.get_active_scene()
        if not scn:
            return
        else:
            target = self.get_target()
            if not target or not target.ev_g_model():
                self.target_id = None
                self.sd.ref_modify_ratio = 1.0
                return
            target_pos = target.ev_g_position()
            speed_scale = self.get_speed_adjust_scale(target)
            adujst_scale = speed_scale
            slow_dist_sqr_inside = self.slow_dist_sqr_inside * adujst_scale
            slow_dist_sqr_outside = self.slow_dist_sqr_outside * adujst_scale
            need_handle_dist_sqr = self.need_handle_dist_sqr * adujst_scale
            min_sensor_modify = self._min_sensor_modify * adujst_scale
            dist_sqr = self.get_target_dist(target, use_pos_dist=False)
            if dist_sqr > self.find_target_dist_sqr:
                self.target_id = None
                self.sd.ref_modify_ratio = 1.0
            elif slow_dist_sqr_inside < dist_sqr < slow_dist_sqr_outside:
                max_sensor_modify = 1
                scale = (dist_sqr - slow_dist_sqr_inside) / (slow_dist_sqr_outside - slow_dist_sqr_inside)
                sensor_modify_value = min_sensor_modify
                self.sd.ref_modify_ratio = sensor_modify_value + scale * (max_sensor_modify - sensor_modify_value)
            elif dist_sqr <= slow_dist_sqr_inside:
                self.sd.ref_modify_ratio = min_sensor_modify
            return

    def get_aim_pos_from_model(self, target):
        model = target.ev_g_model()
        if not model:
            return
        bone_list = self.get_ref_bones(target)
        for one_bone_name in bone_list:
            matrix = model.get_bone_matrix(one_bone_name, world.SPACE_TYPE_WORLD)
            if matrix:
                return matrix.translation

    def get_camera(self):
        return world.get_active_scene().active_camera

    def tick(self, dt):
        if self.tick_count < self.tick_interval:
            self.tick_count += 1
        else:
            self._try_find_target()
            self.tick_count = 0
        if self.target_id:
            self._update_target_info()
        if self._adsorb_target_pos:
            self._update_adsorb_target_info(dt)