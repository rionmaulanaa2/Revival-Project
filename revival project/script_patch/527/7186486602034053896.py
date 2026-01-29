# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrackCollision.py
from __future__ import absolute_import
from .ComWeaponCollisionBase import ComWeaponCollisionBase
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT, WATER_GROUP, WATER_MASK, GROUP_DYNAMIC_SHOOTUNIT, GROUP_STATIC_SHOOTUNIT, GROUP_GRENADE, GROUP_SHIELD, GROUP_SHOOTUNIT
from common.cfg import confmgr
import logic.gutils.track_reader as track_reader
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.attr_const import ATTR_COL_RADIUS
from logic.gutils import team_utils
from .ComObjCollision import ignore_lod_collisions
import collision

class ComTrackCollision(ComWeaponCollisionBase):
    BIND_EVENT = ComWeaponCollisionBase.BIND_EVENT.copy()
    BIND_EVENT.update({'G_COL_RADIUS_RATE': 'get_col_radius_rate'
       })

    def init_from_dict(self, unit_obj, bdict):
        self._owner_id = bdict['owner_id']
        self.track_info = {}
        self.track_info.update(bdict)
        self.item_type = self.track_info['item_itype']
        conf = self.track_info
        trigger_id = conf['trigger_id']
        target = EntityManager.getentity(trigger_id)
        self._col_ids = target.logic.ev_g_human_col_id()
        shield_id = target.logic.share_data.ref_mecha_shield_col_id
        if shield_id:
            self._col_ids.append(shield_id)
        relative_ids = target.logic.share_data.ref_mecha_relative_cols
        if relative_ids:
            self._col_ids.extend(relative_ids)
        item_conf = confmgr.get('grenade_config', str(self.track_info['item_itype']))
        self.item_conf = item_conf
        self.item_res_conf = confmgr.get('grenade_res_config', str(self.track_info['item_itype']))
        self.collision_type_mask = item_conf['iCollisionTypeMask']
        direction = math3d.vector(*conf['dir'])
        direction.normalize()
        start_pos = math3d.vector(*conf['position'])
        end_pos = math3d.vector(*conf['end'])
        track_data = confmgr.get('bullet_track', str(conf['track']))
        self._track_reader = track_reader.TrackReader()
        self._track_reader.read_track('', direction, start_pos, end_pos, track_data)
        fSpeed = item_conf['fSpeed']
        if 'speed' in conf and conf['speed'] > fSpeed:
            fSpeed = conf['speed']
            if item_conf['fMaxDistance'] < fSpeed:
                fSpeed = item_conf['fMaxDistance']
        self._time_scale = self._track_reader.get_track_time() / (item_conf['fMaxDistance'] / fSpeed)
        self._cur_time = 0.0
        self.ini_linear_speed = direction * fSpeed
        self._gernade_id = global_data.sound_mgr.register_game_obj('gernade')
        self._gernade_player_id = None
        self._impulse_power = 0
        self._impulse_range = 0
        super(ComTrackCollision, self).init_from_dict(unit_obj, bdict)
        return

    def cache(self):
        self._stop_sound()
        super(ComTrackCollision, self).cache()

    def init_physical_parameters(self):
        conf = self.track_info
        cobj = self._col_obj
        cobj.disable_gravity(True)
        self._impulse_power = float(confmgr.get('break_data', str(conf['item_itype']), default={}).get('cBreakPower', 0))
        self._impulse_range = float(confmgr.get('break_data', str(conf['item_itype']), default={}).get('fBreakRange', 0)) * NEOX_UNIT_SCALE

    def _create_col_obj(self):
        import collision
        if self._model:
            m = self._model() if 1 else None
            return m or None
        else:
            item_conf = self.item_conf
            if item_conf:
                radius_add_rate = self.get_col_radius_rate()
                radius = item_conf['fCollisionRadius'] * (1 + radius_add_rate)
                self._radius = float(radius)
                bounding_box = math3d.vector(radius, radius, radius)
            else:
                bounding_box = math3d.vector(6, 6, 6)
            position = self.track_info['position']
            mass = 1
            self._col_obj = collision.col_object(collision.SPHERE, bounding_box, 0, 0, mass)
            self.set_group_and_mask(self._col_obj)
            self._col_obj.position = position
            self._last_check_pos = position
            self._col_obj.rotation_matrix = m.rotation_matrix
            self._col_obj.model_col_name = 'track_bullet'
            self._col_obj.is_explodable = True
            self._col_obj.disable_gravity(True)
            self._col_obj.disable_simulation = False
            self._col_obj.enable_ccd = True
            self.scene.scene_col.add_object(self._col_obj)
            self._col_obj.set_linear_velocity(self.ini_linear_speed)
            return

    def get_col_radius_rate(self):
        track_type = self.track_info['item_itype']
        trigger_id = self.track_info.get('trigger_id', None)
        trigger = self.battle.get_entity(trigger_id)
        radius_add_rate = 0
        if trigger and trigger.logic:
            if trigger.logic.sd.ref_is_mecha:
                radius_add_rate = trigger.logic.ev_g_add_attr(ATTR_COL_RADIUS, track_type)
        return radius_add_rate

    def on_model_load_complete(self, model):
        super(ComTrackCollision, self).on_model_load_complete(model)
        if not self._col_obj:
            return
        self.need_update = True
        cobj = self._col_obj
        cobj.set_notify_contact(True)
        self._last_check_pos = self._col_obj.position
        item_res_conf = self.item_res_conf
        if item_res_conf and item_res_conf['cFlySound']:
            fly_sound = item_res_conf['cFlySound']
            if isinstance(fly_sound, str):
                global_data.sound_mgr.set_switch('bullet_fly', fly_sound, self._gernade_id)
                self._gernade_player_id = global_data.sound_mgr.post_event('Play_bullet_fly2', self._gernade_id, cobj.position)
            elif isinstance(fly_sound, list):
                if fly_sound[1] == 'nf':
                    self._gernade_player_id = global_data.sound_mgr.post_event(fly_sound[0], self._gernade_id, cobj.position)

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            model = self._model() if self._model else None
            if not model or not model.valid:
                return
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
            target = None
            if cobj and cobj.valid:
                if cobj.model_col_name == 'track_bullet':
                    return
                if cobj.mask == WATER_MASK and cobj.group == WATER_GROUP:
                    return
                if cobj.cid in self._col_ids:
                    return
                unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                if unit:
                    if unit.ev_g_is_campmate(self.faction_id):
                        return
                    if team_utils.is_teammate(self._owner_id, unit):
                        return
                    target = unit.id
                    result = self.scene.scene_col.hit_by_ray(self._last_check_pos, cobj.position, 0, 65535, GROUP_SHOOTUNIT, collision.INCLUDE_FILTER, True)
                    if result[0]:
                        for hit_obj in result[1]:
                            check_unit = global_data.emgr.scene_find_unit_event.emit(hit_obj[4].cid)[0]
                            if not check_unit or check_unit.id != target:
                                target = None

            if self._col_obj:
                self._col_obj.set_notify_contact(False)
            self.update_explosive_info(cobj, point, model, normal, target, self.track_info)
            return

    def tick(self, dt):
        self._cur_time += dt
        track_pos, is_end = self._track_reader.get_cur_pos(self._cur_time * self._time_scale)
        if is_end:
            self.on_contact(None, track_pos, math3d.vector(0, 1, 0))
        col_obj = self._col_obj
        if not col_obj or not col_obj.valid:
            return
        else:
            rotation_matrix = None
            if self._last_check_pos and dt:
                vec = track_pos - self._last_check_pos
                col_obj.set_linear_velocity(vec * (1.0 / dt))
                if not vec.is_zero:
                    rotation_matrix = math3d.matrix.make_rotation_between(math3d.vector(0, 0, 1), vec)
            if self._need_ray_check:
                self.ray_check(track_pos)
            else:
                self._last_check_pos = track_pos
            col_obj.position = track_pos
            m = self._model() if self._model else None
            if not m or not m.valid:
                return
            self.intrp_model_pos(dt, rotation_matrix, try_stop_intrp_in_advance=False)
            if self._gernade_player_id:
                global_data.sound_mgr.set_position(self._gernade_id, track_pos)
            return

    def _stop_sound(self):
        if self._gernade_player_id:
            global_data.sound_mgr.stop_playing_id(self._gernade_player_id)
            self._gernade_player_id = None
        global_data.sound_mgr.unregister_game_obj(self._gernade_id)
        return

    def destroy(self):
        self._stop_sound()
        super(ComTrackCollision, self).destroy()