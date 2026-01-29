# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/Logic8027.py
from __future__ import absolute_import
from six.moves import range
from .BoostLogic import OxRushNew
from common.utils import timer
from .StateBase import StateBase
from logic.gcommon.cdata.mecha_status_config import *
from logic.gcommon.common_const.character_anim_const import *
from logic.gcommon.common_utils import status_utils
import game3d
import world
import math3d
from logic.comsys.control_ui.ShotChecker import ShotChecker
from mobile.common.EntityManager import EntityManager
from .Logic8011 import StandWithGuard
from .JumpLogic import FallPure
from .ShootLogic import Reload
from logic.gcommon.common_const import attr_const
from logic.gcommon import editor
from logic.gutils import scene_utils
from logic.gutils.mecha_utils import do_hit_phantom
from logic.gcommon.common_const.ui_operation_const import SUBWEAPON_FIRE_ON_AUTO_8027, DRAG_DASH_BTN_8027
from logic.gcommon.common_const.idx_const import ExploderID
from logic.gutils.mecha_skin_utils import get_mecha_skin_grenade_weapon_sfx_path
from logic.gcommon.common_const import robot_animation_const
from logic.gcommon.const import NEOX_UNIT_SCALE
UNIT_Y = math3d.vector(0, 1, 0)

class StandWithGuard8027(StandWithGuard):

    def exit(self, enter_states):
        super(StandWithGuard8027, self).exit(enter_states)
        if MC_SECOND_WEAPON_ATTACK in self.ev_g_cur_state():
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)


class Fall8027(FallPure):

    def exit(self, enter_states):
        super(Fall8027, self).exit(enter_states)
        if MC_SECOND_WEAPON_ATTACK in self.ev_g_cur_state():
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)


class Reload8027(Reload):

    def read_data_from_custom_param(self):
        self.stand_shoot_reload_anim = self.custom_param.get('stand_shoot_reload_anim')
        self.stand_reload_anim = self.custom_param.get('stand_reload_anim')
        self.move_shoot_reload_anim = self.custom_param.get('reload_anim')
        self.blend_time = self.custom_param.get('blend_time', 0.2)
        self.move_reload_anim_dir = self.custom_param.get('reload_anim_move_dir', 1)
        self.other_reload_anim_dir = self.custom_param.get('reload_anim_dir', 1)
        super(Reload8027, self).read_data_from_custom_param()

    def enter(self, leave_states):
        if self.is_shoot():
            self.send_event('E_POST_ACTION', 'shoot', UP_BODY, 7, blend_time=0)
            if self.is_move():
                self.reload_anim = self.move_shoot_reload_anim
                self.reload_anim_dir = self.move_reload_anim_dir
            else:
                self.reload_anim = self.stand_shoot_reload_anim
                self.reload_anim_dir = self.other_reload_anim_dir
        else:
            self.reload_anim = self.stand_reload_anim
            self.reload_anim_dir = self.other_reload_anim_dir
        super(Reload8027, self).enter(leave_states)

    def exit(self, enter_states):
        super(Reload, self).exit(enter_states)
        self.send_event('E_SLOW_DOWN', False)
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, None)
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)
        if self.extern_bone_tree or self.sub_bone_tree:
            self.send_event('E_POST_EXTERN_ACTION', None, False, blend_time=self.extern_exit_blend_time)
        self.send_event('E_REPLACE_ACTION_TRIGGER_ANIM', self.use_up_anim_states, None)
        from common.utils.timer import CLOCK

        def _clear_upbody():
            cur_states = self.ev_g_cur_state()
            if self.sd.ref_up_body_anim and 'reload' in self.sd.ref_up_body_anim or self.sd.ref_up_body_anim == 'shoot' and not (MC_RELOAD in cur_states or MC_SHOOT in cur_states):
                self.send_event('E_CLEAR_UP_BODY_ANIM')

        global_data.game_mgr.register_logic_timer(_clear_upbody, interval=0.2, times=1, mode=CLOCK)
        return

    def is_shoot(self):
        return self.ev_g_is_action_down('action1') or self.ev_g_is_action_down('action2') or self.ev_g_is_action_down('action3')

    def is_stand(self):
        return MC_STAND in self.ev_g_cur_state()

    def is_move(self):
        return MC_MOVE in self.ev_g_cur_state()

    def can_play_extern_action(self):
        if self.is_stand():
            return False
        if self.is_move() and self.is_shoot():
            return False
        return True

    def play_anim(self):
        if self.use_up_anim_bone:
            self.send_event('E_REPLACE_UP_BONE_MASK', self.use_up_anim_states, self.use_up_anim_bone)
        if self.bind_action_id:
            self.send_event('E_START_ACTION_CD', self.bind_action_id, self.reload_time)
        if self.reload_anim:
            if self.extern_bone_tree and self.can_play_extern_action():
                self.send_event('E_POST_EXTERN_ACTION', self.reload_anim, True, subtree=self.extern_bone_tree, timeScale=self.timer_rate, blend_time=self.extern_enter_blend_time)
            else:
                self.send_event('E_POST_ACTION', self.reload_anim, UP_BODY, self.reload_anim_dir, timeScale=self.timer_rate, blend_time=self.blend_time)
                if self.sub_bone_tree and self.can_play_extern_action():
                    self.send_event('E_POST_EXTERN_ACTION', self.reload_anim, True, subtree=self.sub_bone_tree, timeScale=self.timer_rate, blend_time=self.extern_enter_blend_time)


@editor.state_exporter({('attack_param', 'param'): {'zh_name': '\xe6\x94\xbb\xe5\x87\xbb\xe5\x8f\x82\xe6\x95\xb0','structure': lambda self: self._get_action_param_structure()
                               },
   ('anim_rate', 'param'): {'zh_name': '\xe5\x8a\xa8\xe4\xbd\x9c\xe9\x80\x9f\xe7\x8e\x87'},('is_touch_end_fire', 'param'): {'zh_name': '\xe6\x98\xaf\xe5\x90\xa6\xe6\x9d\xbe\xe6\x89\x8b\xe9\x87\x8a\xe6\x94\xbe\xe6\x8a\x80\xe8\x83\xbd'}})
class ContinuousShoot8027(StateBase):
    MAX_ATTACK_STAGE = 2
    ATTACK_END = 0
    BIND_EVENT = {}

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_sub_fire_on_auto_8027': self.update_sub_fire_on_auto_8027
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(ContinuousShoot8027, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.skill_id = self.custom_param['skill_id']
        self.attack_param = self.custom_param['attack_param']
        self.timer_rate = self.custom_param.get('anim_rate', 1.0)
        self.is_touch_end_fire = global_data.player and not global_data.player.get_setting_2(SUBWEAPON_FIRE_ON_AUTO_8027)
        self.combo_move_status = status_utils.convert_status(self.custom_param.get('break_states', set()))
        self.sub_state = self.ATTACK_END
        self.fire_forward, self.fire_position = (None, None)
        self.continue_fire = False
        self.can_combo_attack = False
        self.process_event(True)
        return None

    def update_sub_fire_on_auto_8027(self, flag):
        self.is_touch_end_fire = not flag

    def _get_action_param_structure(self):
        slash_param_structure = {}
        for i in range(self.MAX_ATTACK_STAGE):
            i += 1
            sub_structure = {}
            sub_structure['fire'] = {'zh_name': '\xe5\xbc\x80\xe7\x81\xab\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe6\x97\xb6\xe5\x88\xbb\xef\xbc\x89','type': 'float'}
            sub_structure['combo_move'] = {'zh_name': '\xe5\x8f\xaf\xe4\xbb\xa5\xe6\x89\x93\xe6\x96\xad\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe6\x97\xb6\xe5\x88\xbb\xef\xbc\x89','type': 'float'}
            sub_structure['combo'] = {'zh_name': '\xe5\x8f\xaf\xe8\xbf\x9e\xe5\x87\xbb\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe6\x97\xb6\xe5\x88\xbb\xef\xbc\x89','type': 'float'}
            slash_param_structure[i] = {'zh_name': '\xe7\xac\xac%d\xe5\x88\x80' % i,'type': 'dict','kwargs': {'structure': sub_structure}}

        return slash_param_structure

    def reset_attack_events(self, stage):
        self.reset_sub_states_callback()
        param = self.attack_param
        self.register_attack_events(stage, param[stage])

    def register_attack_events(self, substate, param):
        fire_ani_s, fire_ani_e, fire, combo_move, combo, end = (
         param['fire_ani_s'], param['fire_ani_e'], param['fire'], param['combo_move'], param['combo'], param['end'])
        pos_factor_name = attr_const.ATTR_SHOOTSPEED_FACTOR_POS_2
        pos_factor = self.ev_g_add_attr(pos_factor_name)
        common_factor = self.ev_g_add_attr(attr_const.ATTR_SHOOTSPEED_FACTOR)
        factor = 1 / (1 + pos_factor + common_factor)
        fire_ani_s *= factor
        fire_ani_e *= factor
        fire *= factor
        self.register_substate_callback(substate, 0, self.reset_param)
        self.register_substate_callback(substate, fire_ani_s / self.timer_rate, self.fire_ani_s)
        self.register_substate_callback(substate, fire_ani_e / self.timer_rate, self.fire_ani_e)
        self.register_substate_callback(substate, fire / self.timer_rate, self.fire)
        self.register_substate_callback(substate, combo_move / self.timer_rate, self.combo_move)
        self.register_substate_callback(substate, end / self.timer_rate, self.end_attack)
        self.register_substate_callback(substate, combo / self.timer_rate, self.combo)

    def setup_fire_direction(self):
        scn = world.get_active_scene()
        camera = scn.active_camera
        self.fire_forward = camera.rotation_matrix.forward
        self.fire_position = camera.position

    def play_animation(self, ani_key):
        param = self.attack_param
        clip, part, blend_dir = param[self.sub_state][ani_key]
        part = LOW_BODY if part == 'lower' else UP_BODY
        self.send_event('E_POST_ACTION', clip, part, blend_dir, timeScale=self.timer_rate)

    def reset_param(self, *args):
        self.can_combo_attack = False
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.play_animation('anim_pre')
        if MC_STAND in self.ev_g_cur_state() or MC_JUMP_3 in self.ev_g_cur_state():
            self.send_event('E_UPBODY_BONE', FULL_BODY_BONE)
        else:
            self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)

    def fire_ani_s(self, *args):
        if MC_STAND in self.ev_g_cur_state():
            self.play_animation('anim')
        else:
            self.play_animation('anim_move')
        self.send_event('E_CONTINUOUSSHOOT8027_ANIM_START', self.sid)

    def fire_ani_e(self, *args):
        self.play_animation('anim_end')

    def fire(self, *args):
        self.setup_fire_direction()
        self.send_event('E_DO_SKILL', self.skill_id, self.sub_state, self.fire_position, self.fire_forward)
        self.send_event('E_CONTINUOUSSHOOT8027_FIRE', self.sid)

    def combo_move(self, *args):
        self.send_event('E_ADD_WHITE_STATE', self.combo_move_status, self.sid)
        for state in self.ev_g_cur_state():
            if state in self.combo_move_status:
                self.disable_self()

    def combo(self, *args):
        self.can_combo_attack = True
        if self.continue_fire and self.ev_g_can_cast_skill(self.skill_id):
            self.combo_attack()

    def end_attack(self):
        self.disable_self()

    def combo_attack(self):
        if not self.can_combo_attack:
            return
        self.sub_state = self.ev_g_attack_stage()
        self.sub_state += 1
        if self.sub_state > self.MAX_ATTACK_STAGE:
            self.sub_state = 1
        self.send_event('E_ATTACK_STAGE', self.sub_state)
        self.reset_attack_events(self.sub_state)
        self.can_combo_attack = False

    def action_btn_down(self):
        if self.is_touch_end_fire:
            self.continue_fire = False
            return True
        if ShotChecker().check_camera_can_shot():
            return False
        if not self.check_can_active():
            return False
        if not self.ev_g_can_cast_skill(self.skill_id):
            return False
        if not self.is_active:
            self.active_self()
        else:
            self.combo_attack()
        self.continue_fire = True
        return True

    def action_btn_up(self):
        if self.is_touch_end_fire:
            if ShotChecker().check_camera_can_shot():
                return False
            if not self.check_can_active():
                return False
            if not self.ev_g_can_cast_skill(self.skill_id):
                return False
            if not self.is_active:
                self.active_self()
            else:
                self.combo_attack()
            return True
        self.continue_fire = False
        return True

    def enter(self, leave_states):
        self.fired_time = 0
        if self.ev_g_on_ground():
            self.send_event('E_CLEAR_SPEED')
        self.can_combo_attack = True
        self.combo_attack()
        super(ContinuousShoot8027, self).enter(leave_states)

    def update(self, dt):
        super(ContinuousShoot8027, self).update(dt)

    def exit(self, enter_states):
        super(ContinuousShoot8027, self).exit(enter_states)
        self.send_event('E_CLEAR_UP_BODY_ANIM')
        self.send_event('E_CLEAR_WHITE_STATE', self.sid)
        self.send_event('E_UPBODY_BONE', DEFAULT_UP_BODY_BONE)

    def destroy(self):
        super(ContinuousShoot8027, self).destroy()
        self.process_event(False)


class OxRushNew8027(OxRushNew):
    BIND_EVENT = {}
    IS_AUTO_OX_RUSH_COL_CHECK = False
    CAN_CANCEL_RUSH = False

    def init_from_dict(self, unit_obj, bdict, sid, state_info):
        super(OxRushNew8027, self).init_from_dict(unit_obj, bdict, sid, state_info)
        self.need_trigger_btn_up_when_action_forbidden = False
        self.is_hit_play_skill = False
        self.hit_id = set()
        self.check_hit_timer = None
        self.rush_direction = None
        self.in_free_cam = False
        self.hit_phantom = []
        return

    def destroy(self):
        self.clear_check_hit_timer()
        super(OxRushNew8027, self).destroy()

    def init_parameters(self):
        super(OxRushNew8027, self).init_parameters()
        self.rush_direction = None
        self.disposable_speed_offset = 0
        self.hit_valid_num = 0
        return

    def read_data_from_custom_param(self):
        self.is_draw_col = self.custom_param.get('is_draw_col', False)
        self.col_info = self.custom_param.get('col_info', (30, 50))
        self.speed_offset_proportion = self.custom_param.get('speed_offset_proportion', (-0.2,
                                                                                         -0.2))
        super(OxRushNew8027, self).read_data_from_custom_param()

    def action_btn_down(self):
        return StateBase.action_btn_down(self)

    def action_btn_up(self):
        super(OxRushNew8027, self).action_btn_up()
        if not self.check_can_active():
            return False
        if not self.check_can_cast_skill():
            return False
        self.active_self()
        self.sound_custom_start()

    def enter(self, leave_states):
        super(OxRushNew8027, self).enter(leave_states)
        scn = world.get_active_scene()
        self.rush_direction = scn.active_camera.rotation_matrix.forward
        self.rush_direction.normalize()
        self.send_event('E_DO_OXRUSH_8027', True)
        self.hit_phantom = []
        self.start_check_hit()

    def exit(self, enter_states):
        super(OxRushNew8027, self).exit(enter_states)
        self.send_event('E_DO_OXRUSH_8027', False)
        self.stop_check_hit()
        self.rush_direction = None
        return

    def on_begin_rush(self):
        super(OxRushNew8027, self).on_begin_rush()
        self.send_event('E_FORWARD', self.rush_direction, True)
        if self.ev_g_add_attr('enable_8027_dash_throw', False):
            self.on_add_dash_throwable_item()

    def on_begin_miss(self):
        super(OxRushNew8027, self).on_begin_miss()

    def on_add_dash_throwable_item(self):
        dir = self.rush_direction
        position = self.ev_g_position()
        model = self.ev_g_model()
        m_position = model.get_bone_matrix(robot_animation_const.BONE_HEAD_NAME, world.SPACE_TYPE_WORLD).translation
        throw_item_info = {'uniq_key': ExploderID.gen(global_data.battle_idx),
           'position': (
                      position.x, position.y + NEOX_UNIT_SCALE * 5, position.z),
           'm_position': (
                        m_position.x, m_position.y, m_position.z),
           'dir': (
                 dir.x, dir.y, dir.z),
           'item_itype': 802702
           }
        skin_id, shiny_weapon_id = self.ev_g_mecha_skin_and_shiny_weapon_id()
        if get_mecha_skin_grenade_weapon_sfx_path(skin_id, shiny_weapon_id, 802702, 'cRes'):
            throw_item_info['skin_id'] = skin_id
            if shiny_weapon_id:
                throw_item_info['shiny_weapon_id'] = shiny_weapon_id
        self.send_event('E_CALL_SYNC_METHOD', 'skill_add_throwable', (self.skill_id, throw_item_info))

    def update(self, dt):
        StateBase.update(self, dt)
        num = len(self.speed_offset_proportion)
        if self.disposable_speed_offset < self.hit_valid_num and self.hit_valid_num <= num and self.disposable_speed_offset <= num:
            for i in range(self.disposable_speed_offset, self.hit_valid_num):
                prop = self.speed_offset_proportion[i]
                self.cur_speed += self.cur_speed * prop

            self.disposable_speed_offset = self.hit_valid_num
        if self.is_accelerating:
            self.cur_speed += self.acc_speed * dt
            if self.cur_speed > self.max_rush_speed:
                self.cur_speed = self.max_rush_speed
        elif self.is_braking:
            self.cur_speed -= self.brake_speed * dt
            if self.cur_speed < 0:
                self.cur_speed = 0.0
        if self.rush_direction is not None and self.is_moving:
            walk_direction = self.get_walk_direction(self.rush_direction)
            self.air_walk_direction_setter.execute(walk_direction)
        return

    def refresh_air_dash_end_speed(self):
        self.cur_speed = self.air_dash_end_speed
        walk_direction = self.get_walk_direction(self.rush_direction)
        self.send_event('E_VERTICAL_SPEED', 0)
        walk_direction.y = 0
        self.send_event('E_SET_WALK_DIRECTION', walk_direction)
        self.sd.ref_cur_speed = walk_direction.length

    def get_hit_unit_id_list(self):
        height, radius = self.col_info
        hit_unit_id_list = []
        if global_data.player and global_data.player.logic:
            pos = self.ev_g_position() + math3d.vector(0, height, 0)
            if self.is_draw_col:
                global_data.emgr.scene_draw_wireframe_event.emit(pos, math3d.matrix(), 10, length=(radius * 2, radius * 2, radius * 2))
            unit_datas = global_data.emgr.scene_get_hit_all_enemy_unit.emit(self.unit_obj.ev_g_camp_id(), pos, radius)
            if unit_datas and unit_datas[0]:
                for unit in unit_datas[0]:
                    unit_id = unit.id
                    if unit_id not in self.hit_id:
                        if scene_utils.dash_filtrate_hit(self.unit_obj, unit):
                            continue
                        if unit.sd.ref_is_mecha or unit.ev_g_is_human():
                            self.hit_valid_num += 1
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
            self.send_skill_hit(hit_unit_id_list)

    def send_skill_hit(self, info):
        self.send_event('E_CALL_SYNC_METHOD', 'skill_hit_on_target', (self.skill_id, info), False, True)
        self.play_hit_effect(info)

    def play_hit_effect(self, info):
        for eid in info:
            pos = None
            entity = EntityManager.getentity(eid)
            if entity and entity.logic and not entity.logic.ev_g_is_human():
                target_model = entity.logic.ev_g_model()
                if target_model and target_model.valid:
                    pos = target_model.position + math3d.vector(0, target_model.bounding_box.y * target_model.scale.y, 0)
            if not (pos and self.rush_direction):
                return
            mat = math3d.matrix.make_orient(self.rush_direction, UNIT_Y)
            rot = math3d.matrix_to_rotation(mat)
            self.send_event('E_RUSH_HIT_TARGET_SFX', (pos.x, pos.y, pos.z), (rot.x, rot.y, rot.z, rot.w))

        return

    def clear_check_hit_timer(self):
        self.check_hit_timer and global_data.game_mgr.get_logic_timer().unregister(self.check_hit_timer)
        self.check_hit_timer = None
        return

    def stop_check_hit(self):
        self.clear_check_hit_timer()
        self.hit_id = set()