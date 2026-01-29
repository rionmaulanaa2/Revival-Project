# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrackNavigateCollision.py
from __future__ import absolute_import
from .ComWeaponCollisionBase import ComWeaponCollisionBase
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, WATER_GROUP, WATER_MASK, GROUP_CHARACTER_INCLUDE, GROUP_AUTO_AIM, GROUP_GRENADE, GROUP_SHIELD
from math import radians, cos
from common.cfg import confmgr
from mobile.common.EntityManager import EntityManager
from logic.gutils import team_utils
from .ComObjCollision import ignore_lod_collisions

class ComTrackNavigateCollision(ComWeaponCollisionBase):
    BIND_EVENT = ComWeaponCollisionBase.BIND_EVENT.copy()
    BIND_EVENT.update({'E_POSITION': '_on_position_changed',
       'S_DIRECTION': '_on_direction_changed',
       'E_ON_ATTACH_EXPLOSIVE': '_attach_mecha'
       })

    def init_from_dict(self, unit_obj, bdict):
        self.navigate_info = {}
        self.navigate_info.update(bdict)
        self.item_type = self.navigate_info['item_itype']
        super(ComTrackNavigateCollision, self).init_from_dict(unit_obj, bdict)
        self._owner_id = bdict['owner_id']
        self._speed_direction = math3d.vector(*bdict['dir'])
        if not self._speed_direction.is_zero:
            self._speed_direction.normalize()
        from logic.gcommon import time_utility as t_util
        from common.cfg import confmgr
        self._init_time = t_util.time()
        self._last_time = 0
        self._stage = self.track_stage
        self._target = None
        self._conf = confmgr.get('navigate_config', str(bdict['item_itype']))
        self._cos_declination = cos(radians(self._conf['fDeclination']))
        self._speed_value = self._conf['fSpeedInit']
        self._impulse_power = 0
        self._impulse_range = 0
        self._cur_rotate_speed = self._conf['fRotateSpeed']
        self._aim_pos = bdict.get('aim_pos', None)
        if self._aim_pos:
            self._aim_pos = math3d.vector(*self._aim_pos)
        grenade_conf = confmgr.get('grenade_config', str(bdict['item_itype']))
        if grenade_conf:
            self._trigger_type = grenade_conf['iTriggerType']
        self.collision_type_mask = grenade_conf['iCollisionTypeMask']
        cTracks = grenade_conf.get('cTracks')
        self.need_play_lock_sound = bdict.get('sub_idx', 0) == 0
        if bdict.get('fired_socket_index') is not None:
            self.track_name = cTracks[bdict['fired_socket_index']]
            self.need_play_lock_sound = self.need_play_lock_sound and bdict.get('is_first_grenade')
        else:
            sub_idx = bdict.get('sub_idx', 0) if bdict.get('sub_idx', 0) is not None else 0
            self.track_name = cTracks[sub_idx]
        self._col_ids = []
        if bdict.get('trigger_id', None):
            trigger_id = bdict['trigger_id']
            target = EntityManager.getentity(trigger_id)
            if target and target.logic:
                self._col_ids = target.logic.ev_g_human_col_id()
                shield_id = target.logic.share_data.ref_mecha_shield_col_id
                if shield_id:
                    self._col_ids.append(shield_id)
                relative_ids = target.logic.share_data.ref_mecha_relative_cols
                if relative_ids:
                    self._col_ids.extend(relative_ids)
        self._sound_player_id = global_data.sound_mgr.register_game_obj('track_navigate')
        self._fly_sound_id = None
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self._on_position_changed)
        return

    def cache(self):
        self._stop_sound()
        super(ComTrackNavigateCollision, self).cache()
        self._col_ids = []

    def _on_position_changed(self, position):
        if self._col_obj:
            self._col_obj.position = position

    def _on_direction_changed(self, direction):
        if not isinstance(direction, math3d.matrix):
            return
        if self._col_obj:
            self._col_obj.rotation_matrix = direction

    def _create_col_obj(self):
        import collision
        if self._model:
            m = self._model() if 1 else None
            return m or None
        else:
            collision_type = collision.SPHERE
            bounding_box = m.scale * 3
            position = self.navigate_info['position']
            mass = 1
            self._col_obj = collision.col_object(collision_type, bounding_box, 0, 0, mass)
            self.set_group_and_mask(self._col_obj)
            self._col_obj.mask = self._col_obj.mask & ~GROUP_SHIELD
            self._col_obj.position = position
            self._col_obj.rotation_matrix = m.rotation_matrix
            self._col_obj.enable_ccd = True
            self._col_obj.is_explodable = True
            self.sd.ref_col_obj = self._col_obj
            self._last_check_pos = self._col_obj.position
            self.scene.scene_col.add_object(self._col_obj)
            return

    def on_model_load_complete(self, com_unit):
        from common.cfg import confmgr
        super(ComTrackNavigateCollision, self).on_model_load_complete(com_unit)
        if not self._col_obj:
            return
        self.before_track_stage()
        cobj = self._col_obj
        self.need_update = True
        cobj.set_notify_contact(True)
        item_conf = confmgr.get('grenade_res_config', str(self.throw_info['item_itype']))
        if item_conf and item_conf['cFlySound']:
            fly_sound = item_conf['cFlySound']
            if isinstance(fly_sound, str):
                global_data.sound_mgr.set_switch('bullet_fly', fly_sound, self._sound_player_id)
                self._fly_sound_id = global_data.sound_mgr.post_event('Play_bullet_fly2', self._sound_player_id, cobj.position)
            elif isinstance(fly_sound, list):
                if fly_sound[1] == 'nf':
                    self._fly_sound_id = global_data.sound_mgr.post_event(fly_sound[0], self._sound_player_id, cobj.position)

    def init_physical_parameters(self):
        conf = self.navigate_info
        cobj = self._col_obj
        m = self._model()
        cobj.disable_gravity(True)
        speed = self._speed_direction * self._speed_value
        cobj.set_linear_velocity(speed)
        cobj.enable_ccd = True
        bullet_type = conf['item_itype']
        if bullet_type:
            special_sfx_path_list = confmgr.get('break_data', str(bullet_type), 'cBreakBulletHit')
            if special_sfx_path_list:
                cobj.enable_ccd = True
        item_conf = confmgr.get('break_data', str(conf['item_itype']), default={})
        self._impulse_power = item_conf.get('cBreakPower', 0)
        self._impulse_range = item_conf.get('fBreakRange', 0) * NEOX_UNIT_SCALE

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            if len(args) == 3:
                cobj, point, normal = args
            else:
                my_obj, cobj, touch, hit_info = args
                if not touch:
                    return
                point = hit_info.position
                normal = hit_info.normal
            is_ignore, cobj, point, normal = self.collision_check(cobj, point, normal, **kwargs)
            if is_ignore:
                return
            if cobj:
                if cobj.cid in self._col_ids:
                    return
                unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                if unit:
                    if unit.ev_g_is_campmate(self.faction_id):
                        return
                    if team_utils.is_teammate(self._owner_id, unit):
                        return
            if self._model:
                model = self._model() if 1 else None
                return model or None
            self.complete_model_pos_interpolation()
            hit_target = None
            if cobj:
                mecha_unit = global_data.war_mechas.get(cobj.cid)
                if mecha_unit:
                    hit_target = mecha_unit.id
                mecha_unit = global_data.absorb_shields.get(cobj.cid)
                if mecha_unit:
                    hit_target = mecha_unit.id
                mecha_unit = global_data.mecha_shields.get(cobj.cid)
                if mecha_unit:
                    hit_target = mecha_unit.id
                    mecha_unit.send_event('E_HIT_SHIELD_SFX', end=point, itype=self.navigate_info['item_itype'])
                field_unit = global_data.field_shields.get(cobj.cid)
                if field_unit:
                    hit_target = field_unit.id
                    field_unit.send_event('E_HIT_FIELD_SHIELD', end=point)
                target = global_data.war_non_explosion_dis_objs.get(cobj.cid)
                if target:
                    hit_target = target
            if self._col_obj:
                self._col_obj.set_notify_contact(False)
            self.update_explosive_info(cobj, point, model, normal, hit_target, self.navigate_info)
            return

    def before_track_stage(self):
        self.track = global_data.track_cache.create_track(self.track_name)
        self.track_max_time = self.track.duration / 1000.0
        self.track_last_time = 0
        self._col_obj.set_linear_velocity(math3d.vector(0, 0, 0))
        self.start_trans = math3d.matrix()
        self.start_trans.do_rotation(self._col_obj.rotation_matrix)
        self.start_trans.do_translate(self._col_obj.position)
        self.start_trans.do_scale(math3d.vector(1, 1, 1))

    def track_stage(self, model, col, dt):
        self.track_last_time += dt
        if self.track_last_time < self.track_max_time:
            cur_trans = self.track.get_transform(self.track_last_time * 1000)
            new_trans = cur_trans * self.start_trans
            self._col_obj.position = new_trans.translation
            self._col_obj.rotation_matrix = new_trans.rotation
        else:
            self._stage = self.accelerate_stage
            aim_target = self.navigate_info.get('aim_target', None)
            if aim_target:
                from mobile.common.EntityManager import EntityManager
                aim_target = EntityManager.getentity(aim_target)
                if aim_target:
                    self._target = aim_target.logic
                    if self.need_play_lock_sound and not self._conf.get('iNavigateSilently', False):
                        self.send_event('E_AIM_LOCK_TARGET', self._target.id)
            new_dir = None
            if self._target:
                target_pos = self._target.ev_g_aim_position()
                if not target_pos:
                    target_pos = self._target.ev_g_position()
                if target_pos:
                    new_dir = target_pos - self._col_obj.position
                    if not new_dir.is_zero:
                        new_dir.normalize()
            if new_dir is None and self._aim_pos:
                new_dir = self._aim_pos - self._col_obj.position
                if not new_dir.is_zero:
                    new_dir.normalize()
            if new_dir and self._speed_direction.dot(new_dir) > 0:
                self._speed_direction = new_dir
            if not self._speed_direction.is_zero:
                self._speed_direction.normalize()
            self._col_obj.set_linear_velocity(self._speed_direction * self._speed_value)
        return

    def accelerate_stage(self, model, col, dt):
        self.navigate(model, col, dt)
        self._speed_value += self._conf['fAcc'] * dt
        if self._speed_value >= self._conf['fMaxSpeed']:
            self._speed_value = self._conf['fMaxSpeed']
            self._stage = self.navigate
        if not self._speed_direction.is_zero:
            self._speed_direction.normalize()
        self._col_obj.set_linear_velocity(self._speed_direction * self._speed_value)

    def navigate(self, model, col, dt):
        col = self._col_obj
        if not col:
            return
        else:
            if not self._target and not self._aim_pos:
                return
            target_pos = None
            if self._target:
                target_pos = self._target.ev_g_aim_position()
            if target_pos:
                target_pos = target_pos if 1 else self._aim_pos
                return target_pos or None
            direction = target_pos - col.position
            if direction.is_zero:
                return
            direction.normalize()
            dot = direction.dot(self._speed_direction)
            if dot < self._cos_declination:
                return
            if self._cur_rotate_speed < self._conf['fRotateMaxSpeed']:
                self._cur_rotate_speed += self._conf['fRotateAcc'] * dt
                self._cur_rotate_speed = self._conf['fRotateMaxSpeed'] if self._cur_rotate_speed >= self._conf['fRotateMaxSpeed'] else self._cur_rotate_speed
            rotate_angle = radians(self._cur_rotate_speed) * dt
            if cos(rotate_angle) < dot:
                self._speed_direction = direction
            else:
                axis = self._speed_direction.cross(direction)
                if not axis.is_zero:
                    rotation_matrix = math3d.matrix.make_rotation(axis, rotate_angle)
                    self._speed_direction = self._speed_direction * rotation_matrix
                else:
                    self._speed_direction = direction
            new_rot = math3d.matrix.make_orient(self._speed_direction, col.rotation_matrix.up)
            col.rotation_matrix = new_rot
            col.set_linear_velocity(self._speed_direction * self._speed_value)
            return

    def tick(self, dt):
        col_obj = self._col_obj
        if not col_obj:
            self.need_update = False
            return
        else:
            m = self._model() if self._model else None
            if not m or not m.valid:
                self.need_update = False
                return
            cpos = col_obj.position
            if self._need_ray_check:
                self.ray_check(cpos)
            else:
                self._last_check_pos = cpos
            self.intrp_model_pos(dt, try_stop_intrp_in_advance=self._stage != self.track_stage)
            self._stage(m, col_obj, dt)
            if self._fly_sound_id:
                global_data.sound_mgr.set_position(self._sound_player_id, cpos)
            return

    def _attach_mecha(self, *args):
        self.need_update = False
        if self._col_obj:
            self._col_obj.set_notify_contact(False)
            self._col_obj.set_linear_velocity(math3d.vector(0, 0, 0))
            self._col_obj.enable_ccd = True

    def _stop_sound(self):
        if self._fly_sound_id:
            global_data.sound_mgr.stop_playing_id(self._fly_sound_id)
            self._fly_sound_id = None
        if self._sound_player_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_player_id)
            self._sound_player_id = None
        return

    def destroy_col(self):
        if self.sd.ref_col_obj:
            self.sd.ref_col_obj = None
        super(ComTrackNavigateCollision, self).destroy_col()
        return

    def destroy(self):
        self._stop_sound()
        if G_POS_CHANGE_MGR:
            self.unregist_pos_change(self._on_position_changed)
        super(ComTrackNavigateCollision, self).destroy()