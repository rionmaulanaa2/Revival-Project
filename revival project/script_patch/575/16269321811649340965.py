# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_pet/ComPetFollow.py
import math
import six
from math import sin
import math3d
from common.cfg import confmgr
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.component.UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
from logic.gcommon.cdata.pet_status_config import PT_IDLE, PT_MOVE, PT_HIDE, PT_SHOW
from logic.gcommon.common_const.collision_const import MECHA_IDLE_BIPED_BONE_LOCAL_POS_Y
SWITCH_TARGET_TIME = 1
from common.utils.timer import RELEASE

class ComPetFollow(UnitCom):
    BIND_EVENT = {'E_PET_MODEL_LOADED': 'on_pet_model_loaded',
       'E_SET_PET_YAW_OFFSET': 'on_set_yaw_offset',
       'E_SET_PET_DEFAULT_YAW_OFFSET': 'set_default_yaw_offset',
       'G_PET_ANIM_DIR': 'get_anim_dir_param'
       }

    @property
    def owner_logic(self):
        if self._owner_logic:
            return self._owner_logic
        else:
            if self._owner_id:
                owner = EntityManager.getentity(self._owner_id)
                if owner:
                    self._owner_logic = owner.logic
                    return self._owner_logic
            return None

    def __init__(self, *args, **kwargs):
        super(ComPetFollow, self).__init__(*args, **kwargs)
        self.model = None
        self.on_mecha = False
        self.timer_id = None
        self.last_pos = None
        self.owner_last_pos = None
        self.enter_yaw_offset_intrp_duration = 0.2
        self.leave_yaw_offset_intrp_duration = 0.2
        self.cur_anim_duration = 0
        self.cur_anim_played_duration = 0
        self.follow_target = None
        self.switch_target_timer = 0
        self.last_owner_foward = None
        self.ver_offset = 0
        self.ver_float_timer = 0
        self.waiting_owner = True
        self.last_move_vec = math3d.vector(0, 0, 0)
        self.cur_move_rot = 0
        self.follow_target_status_offset = [
         0, 0, 0]
        self.anim_dir_param = [
         0, 0]
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPetFollow, self).init_from_dict(unit_obj, bdict)
        self.skin_id = str(bdict['pet_id'])
        self.level = bdict.get('level', 1)
        self.skin_conf = confmgr.get('c_pet_info', self.skin_id)
        self.follow_conf = self.skin_conf['follow_conf']
        self._owner_logic = bdict.get('owner_logic', None)
        self._owner_id = bdict.get('owner_id', None)
        if not self._owner_logic:
            owner = EntityManager.getentity(self._owner_id)
            if owner:
                self._owner_logic = owner.logic
        self.waiting_owner = not bool(self._owner_logic)
        self.has_pre_move_anim = None
        self.yaw_offset = self.default_yaw_offset = self.follow_conf.get('yaw_offset', 0)
        return

    def on_follow_target_changed(self, follow_target):
        econf = {}
        if self.follow_target:
            for event, (func, prio) in six.iteritems(econf):
                self.follow_target.unregist_event(event, func)

        self.follow_target = follow_target
        if not follow_target:
            return
        else:
            for event, (func, prio) in six.iteritems(econf):
                self.follow_target.regist_event(event, func, prio)

            self.follow_target_status_com = self.follow_target.get_com('ComStatusMechaClient' if self.on_mecha else 'ComStatusHuman')
            self.follow_target_status_offset = [0, 0, 0]
            if self.on_mecha:
                mecha_id = self.follow_target.ev_g_mecha_id()
                shoot_collison_size = confmgr.get('mecha_conf', 'PhysicConfig', 'Content', str(mecha_id), 'shoot_collison_size', default=None)
                if shoot_collison_size:
                    biped_bone_pos_y = MECHA_IDLE_BIPED_BONE_LOCAL_POS_Y[mecha_id]
                    if type(biped_bone_pos_y) in (list, tuple):
                        biped_bone_pos_y = biped_bone_pos_y[0]
                    self.follow_target_status_offset = [shoot_collison_size[0] * NEOX_UNIT_SCALE / 2.0 * (1 if self.cur_follow_conf['follow_offset'][0] >= 0 else -1),
                     shoot_collison_size[1] * NEOX_UNIT_SCALE / 2.0 + biped_bone_pos_y, 0]
            return

    def on_pet_model_loaded(self, model, user_data, *arg):
        self.model = model
        self.regist_timer()

    def regist_timer(self, *args):
        if self.timer_id:
            global_data.game_mgr.get_post_logic_timer().unregister(self.timer_id)
        self.timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self.post_tick, interval=1, times=-1, timedelta=True)

    def destroy(self):
        if self.timer_id:
            global_data.game_mgr.get_post_logic_timer().unregister(self.timer_id)
        self.timer_id = None
        super(ComPetFollow, self).destroy()
        return

    def post_tick(self, delta):
        if not self._is_valid:
            return RELEASE
        else:
            if not self.owner_logic:
                return
            if self.waiting_owner:
                self.send_event('E_OWNER_INITED')
                self.waiting_owner = False
            if not self.model or not self.model.valid:
                return
            new_follow_target = self.owner_logic.sd.ref_ctrl_target
            self.on_mecha = new_follow_target.__class__.__name__ == 'Mecha'
            if self.on_mecha:
                new_follow_target = new_follow_target.logic
            else:
                new_follow_target = self.owner_logic
            if new_follow_target != self.follow_target:
                self.send_event('E_FOLLOW_TARGET_CHANGED', new_follow_target, self.on_mecha)
                self.send_event('E_HIDE_MODEL')
                self.switch_target_timer = SWITCH_TARGET_TIME
                self.follow_target = new_follow_target
                self.get_follow_conf()
                self.on_follow_target_changed(new_follow_target)
                return
            reset_pos = False
            if self.switch_target_timer > 0:
                self.switch_target_timer -= delta
                if self.switch_target_timer > 0:
                    return
                self.send_event('E_REFRESH_MODEL_SCALE')
                self.send_event('E_SHOW_MODEL')
                reset_pos = True
            if not self.model.visible or not self.follow_target:
                return
            follow_conf = self.cur_follow_conf
            owner_model = self.follow_target.ev_g_model()
            if not owner_model or not owner_model.valid:
                return
            owner_pos = owner_model.world_position
            if not owner_pos:
                return
            if self.owner_last_pos is None:
                self.owner_last_pos = owner_pos
            owner_move = owner_pos - self.owner_last_pos
            self.owner_last_pos = owner_pos
            if delta > 0:
                owner_speed = owner_move.length / delta if 1 else 0
                owner_forward = owner_model.world_rotation_matrix.forward
                if self.follow_target.sd.ref_is_ball_mode:
                    owner_forward = owner_move.is_zero or owner_move
                elif self.last_owner_foward and not self.last_owner_foward.is_zero:
                    owner_forward = self.last_owner_foward
                else:
                    owner_forward = math3d.vector(0, 0, 1)
                owner_forward.normalize()
            self.last_owner_foward = owner_forward
            owner_forward_hori = math3d.vector(owner_forward)
            owner_forward_hori.y = 0
            if owner_forward_hori.is_zero:
                owner_forward_hori = math3d.vector(0, 0, 1)
            if self.last_pos is None:
                self.last_pos = self.model.world_position
            follow_offset = follow_conf['follow_offset']
            follow_offset = [ follow_offset[i] + self.follow_target_status_offset[i] for i in range(len(follow_offset)) ]
            up = math3d.vector(0, 1, 0)
            owner_matrix = math3d.matrix.make_orient(owner_forward_hori, up)
            owner_right = owner_matrix.right
            follow_pos = owner_pos + owner_forward_hori * follow_offset[2] + owner_right * follow_offset[0]
            follow_pos.y += follow_offset[1]
            if reset_pos:
                self.last_pos = follow_pos
            cur_pos = math3d.vector(self.last_pos)
            offset_follow_pos = math3d.vector(follow_pos)
            if owner_speed > 0:
                follow_offset_len = min(follow_conf['max_follow_dist'], owner_speed * follow_conf['follow_dist_mul'])
                follow_offset_dir = owner_forward if owner_move.is_zero else owner_move
                follow_offset_dir.normalize()
                offset_follow_pos -= follow_offset_dir * follow_offset_len
            move_vec = offset_follow_pos - cur_pos
            move_dist = move_vec.length
            if move_dist < follow_conf.get('min_follow_dist', 0.5):
                move_dist = 0
            if move_dist > 0:
                move_dist = min(follow_conf['local_pos_change_speed'] * delta, move_dist)
                move_vec.normalize()
                cur_pos += move_vec * move_dist
            follow_pos_dir = follow_pos - cur_pos
            follow_pos_dist = follow_pos_dir.length
            if follow_pos_dist > follow_conf['max_follow_dist'] > 0:
                follow_pos_dir.normalize()
                cur_pos = follow_pos - follow_pos_dir * follow_conf['max_follow_dist']
            if self.has_pre_move_anim is None:
                anim_name, _, _ = self.ev_g_anim_info('pre_move_anim')
                self.has_pre_move_anim = bool(anim_name)
            move_vec = math3d.vector(owner_move)
            move_vec.y = 0
            moving = not move_vec.is_zero
            if moving:
                move_vec.normalize()
                self.last_move_vec = move_vec
            is_multi_dir_anim = bool(self.sd.ref_anim_dir and self.sd.ref_anim_dir > 1)
            if self.has_pre_move_anim or is_multi_dir_anim:
                self.anim_dir_param = [
                 0, 0]
                if moving:
                    self.anim_dir_param[0] = -move_vec.dot(owner_forward)
                    self.anim_dir_param[1] = -move_vec.dot(owner_right)
                if is_multi_dir_anim:
                    self.send_event('E_CHANGE_ANIM_MOVE_DIR', *self.anim_dir_param)
            if self.yaw_offset:
                self.cur_anim_played_duration += delta
                if self.cur_anim_played_duration >= self.cur_anim_duration > 0:
                    cur_yaw_offset = 0
                    self.yaw_offset = 0
                elif self.cur_anim_played_duration < self.enter_yaw_offset_intrp_duration:
                    cur_yaw_offset = self.yaw_offset * self.cur_anim_played_duration / self.enter_yaw_offset_intrp_duration
                elif self.cur_anim_duration < 0 or self.cur_anim_played_duration < self.cur_anim_duration - self.leave_yaw_offset_intrp_duration:
                    cur_yaw_offset = self.yaw_offset
                else:
                    cur_yaw_offset = self.yaw_offset * (self.cur_anim_duration - self.cur_anim_played_duration) / self.leave_yaw_offset_intrp_duration
                if cur_yaw_offset:
                    owner_matrix.do_rotation(math3d.matrix.make_rotation_y(cur_yaw_offset))
            target_move_rot = follow_conf.get('move_rot', 0.6) if moving else 0
            rot_change_spd = follow_conf.get('rot_change_spd', 3)
            if self.cur_move_rot != target_move_rot:
                if self.cur_move_rot > target_move_rot:
                    self.cur_move_rot = max(self.cur_move_rot - delta * rot_change_spd, target_move_rot)
                elif self.cur_move_rot < target_move_rot:
                    self.cur_move_rot = min(self.cur_move_rot + delta * rot_change_spd, target_move_rot)
            rot_forward = move_vec if moving else self.last_move_vec
            if self.cur_move_rot > 0 and not rot_forward.is_zero:
                owner_matrix.do_rotation(math3d.matrix.make_rotation(up.cross(rot_forward), self.cur_move_rot))
            self.model.rotation_matrix = owner_matrix
            cur_moving = PT_MOVE in self.ev_g_cur_state()
            if cur_moving ^ moving:
                self.send_event('E_ACTIVE_STATE', PT_MOVE if moving else PT_IDLE)
            self.last_pos = math3d.vector(cur_pos)
            should_float = True
            if not should_float or self.ver_float_timer == 0 and self.ver_offset != 0:
                self.ver_float_timer = 0
                if self.ver_offset > 0:
                    self.ver_offset -= min(follow_conf['local_pos_change_speed'] * delta, self.ver_offset)
                elif self.ver_offset < 0:
                    self.ver_offset += min(follow_conf['local_pos_change_speed'] * delta, -self.ver_offset)
            else:
                self.ver_float_timer += delta
                self.ver_offset = (sin(self.ver_float_timer * follow_conf.get('ver_offset_freq', 1)) * 2 - 1) * follow_conf.get('max_ver_offset', 1)
            cur_pos.y += self.ver_offset
            self.model.position = cur_pos
            return

    def get_follow_conf(self):
        follow_conf = self.follow_conf
        target_shape_id = 'mecha' if self.on_mecha else 'human'
        self.cur_follow_conf = follow_conf[target_shape_id]

    def init_event(self):
        super(ComPetFollow, self).init_event()
        self.bind_global_event(True)

    def destroy_event(self):
        super(ComPetFollow, self).destroy_event()
        self.bind_global_event(False)

    def bind_global_event(self, is_bind):
        e_conf = {'avatar_reconnect_destroy_event': self.regist_timer
           }
        if is_bind:
            global_data.emgr.bind_events(e_conf)
        else:
            global_data.emgr.unbind_events(e_conf)

    def set_default_yaw_offset(self, default_yaw_offset):
        self.default_yaw_offset = default_yaw_offset

    def on_set_yaw_offset(self, yaw_offset, enter_intrp_duration=0.2, leave_intrp_duration=0.2, anim_duration=1.0):
        if yaw_offset is None:
            yaw_offset = self.default_yaw_offset
            enter_intrp_duration = -1
            leave_intrp_duration = -1
            anim_duration = -1
        self.yaw_offset = math.radians(yaw_offset)
        self.enter_yaw_offset_intrp_duration = enter_intrp_duration
        self.leave_yaw_offset_intrp_duration = leave_intrp_duration
        self.cur_anim_duration = anim_duration
        self.cur_anim_played_duration = 0
        return

    def get_anim_dir_param(self):
        return self.anim_dir_param