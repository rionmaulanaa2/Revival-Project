# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTowerCollision.py
from __future__ import absolute_import
import time
import math3d
import collision
from . import ComWeaponCollisionBase
from math import pi
from common.cfg import confmgr
from logic.gutils import team_utils
from logic.gutils.scene_utils import is_break_obj
from .ComObjCollision import ignore_lod_collisions
from mobile.common.EntityManager import EntityManager
from logic.units import LMechaRobot, LMecha, LMonster, LMechaTrans, LPuppetRobot, LPuppet, LAvatar
CAN_CONVERT_ANGLE = 30
IGNORE_LIST = (
 LMechaRobot.LMechaRobot,
 LMecha.LMecha,
 LMonster.LMonster,
 LMechaTrans.LMechaTrans,
 LAvatar.LAvatar,
 LPuppet.LPuppet,
 LPuppetRobot.LPuppetRobot)

class ComTowerCollision(ComWeaponCollisionBase.ComWeaponCollisionBase):
    MIN_DELTA_DIST = 0.5
    DELAY_UPDATE_FRAME_COUNT = 30
    DYNAMIC_CHECK_FRAME = 1

    def init_from_dict(self, unit_obj, bdict):
        self.throw_info = {}
        self.item_type = bdict['item_itype']
        self.count_down_frame_cnt = -1
        self._owner_id = bdict['owner_id']
        self._left_time = 1000
        self._trigger_type = None
        self._sink_speed = 0
        self._restitution = 1
        self._gravity = None
        self._distance_for_gravity = 0
        self._interp_time = 0
        self.last_update_time = 0
        self.last_pos = math3d.vector(0, 0, 0)
        trigger_id = bdict.get('trigger_id', None)
        if trigger_id is not None:
            trigger = EntityManager.getentity(trigger_id)
            trigger_logic = trigger.logic
            self._col_ids = trigger_logic.ev_g_human_col_id()
            shield_id = trigger_logic.share_data.ref_mecha_shield_col_id
            if shield_id:
                self._col_ids.append(shield_id)
            relative_ids = trigger_logic.share_data.ref_mecha_relative_cols
            if relative_ids:
                self._col_ids.extend(relative_ids)
        else:
            self._col_ids = []
        self._save_collision_time = time.time()
        self._gernade_id = global_data.sound_mgr.register_game_obj('gernade')
        self._gernade_player_id = None
        super(ComTowerCollision, self).init_from_dict(unit_obj, bdict)
        return

    def cache(self):
        self._stop_sound()
        super(ComTowerCollision, self).cache()

    def init_physical_parameters(self):
        conf = self.throw_info
        item_type_s = str(conf['item_itype'])
        wp_ed_data = {}
        if global_data.wp_ed_data and 'grenade_config' in global_data.wp_ed_data and item_type_s in global_data.wp_ed_data['grenade_config']:
            wp_ed_data = global_data.wp_ed_data['grenade_config'][item_type_s]
        cobj = self._col_obj
        m = self._model()
        item_conf = confmgr.get('grenade_config', item_type_s)
        self._trigger_type = item_conf['iTriggerType']
        self._sink_speed = item_conf['fSinkSpeed']
        direction = math3d.vector(*conf['dir'])
        if direction.is_zero:
            self.need_update = False
            self.throw_info['rise_building'] = False
            self.update_explosive_info(cobj, m.position, m, math3d.vector(0, 1, 0), None, self.throw_info)
            return
        else:
            m.set_placement(m.position, self._col_obj.rotation_matrix.up, direction)
            self._col_obj.rotation_matrix = m.rotation_matrix
            speed_factor = 1 + conf.get('throw_speed_add_rate', 0)
            speed = direction * conf['speed'] * speed_factor
            cobj.mass = conf['mass']
            self._gravity = conf['gravity']
            self._distance_for_gravity = item_conf['DistanceForGravity']
            if 'fSpeed' in wp_ed_data:
                speed = direction * wp_ed_data['fSpeed'] * speed_factor
            if 'fMass' in wp_ed_data:
                cobj.mass = wp_ed_data['fMass']
            if 'fGravity' in wp_ed_data:
                self._gravity = wp_ed_data['fGravity']
            cobj.disable_gravity(True)
            if self._distance_for_gravity == 0:
                cobj.disable_gravity(False)
                cobj.apply_force(math3d.vector(0, -self._gravity, 0))
            cobj.static_friction = item_conf['fStaticFriction']
            cobj.dynamic_friction = item_conf['fDynamicFriction']
            cobj.restitution = item_conf['fRestitution']
            cobj.enable_ccd = True
            self._restitution = item_conf['fRestitution']
            self._col_obj.set_damping(item_conf['fLinearDamp'], item_conf['fLangularDamp'])
            cobj.set_linear_velocity(speed)
            bullet_type = conf['item_itype']
            if bullet_type:
                special_sfx_path_list = confmgr.get('break_data', str(bullet_type), default={}).get('cBreakBulletHit')
                if special_sfx_path_list:
                    cobj.enable_ccd = True
            return

    def _create_col_obj(self):
        if self._model:
            m = self._model() if 1 else None
            return m or None
        else:
            item_type = self.throw_info['item_itype']
            item_conf = confmgr.get('grenade_config', str(item_type))
            bounding_box = math3d.vector(3, 7, 3)
            position = self.throw_info['position']
            self.collision_type_mask = item_conf['iCollisionTypeMask']
            self._col_obj = collision.col_object(collision.CAPSULE, bounding_box, 0, 0, 1)
            self.set_group_and_mask(self._col_obj)
            self._col_obj.position = position
            self._original_pos = self._col_obj.position
            self._col_obj.rotation_matrix = m.rotation_matrix
            self._col_obj.is_explodable = True
            self.scene.scene_col.add_object(self._col_obj)
            global_data.emgr.add_ignore_col_ids_event.emit(self._col_obj.cid)
            return

    def on_model_load_complete(self, com_unit):
        super(ComTowerCollision, self).on_model_load_complete(com_unit)
        if not self._col_obj:
            return
        cobj = self._col_obj
        self.need_update = True
        cobj.set_notify_contact(True)
        self.last_pos = cobj.position
        self.last_check_pos = self.last_pos
        self.last_update_time = time.time()
        item_conf = confmgr.get('grenade_res_config', str(self.throw_info['item_itype']))
        if item_conf and item_conf['cFlySound']:
            fly_sound = item_conf['cFlySound']
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
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                if len(args) == 3:
                    cobj, point, normal = args
                else:
                    my_obj, cobj, touch, hit_info = args
                    if not touch:
                        return
                    point = hit_info.position
                    normal = hit_info.normal
                if cobj:
                    if cobj.cid in self._col_ids:
                        return
                    unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                    if unit:
                        if unit.ev_g_is_campmate(self.faction_id):
                            return
                        if team_utils.is_teammate(self._owner_id, unit):
                            return
                if ignore_lod_collisions(cobj):
                    return
                if normal.pitch * 180 / pi < -CAN_CONVERT_ANGLE:
                    from logic.comsys.battle.Death.DeathBattleUtils import check_in_death_base
                    is_in_death_door = check_in_death_base(point, True)
                    if is_in_death_door:
                        self.throw_info['is_in_death_door'] = is_in_death_door
                    self.update_explosive_info(cobj, point, model, normal, None, self.throw_info)
                    return
                is_break_obj(cobj.model_col_name) or self.play_collisions_sound(point)
            return

    def tick(self, dt):
        self._interp_time += dt
        if self.count_down_frame_cnt == 0:
            self.need_update = False
            return
        else:
            if self.count_down_frame_cnt > 0:
                self.count_down_frame_cnt -= 1
            col_obj = self._col_obj
            if not col_obj or not col_obj.valid:
                self.need_update = False
                return
            if self._gravity and (self._distance_for_gravity == 0 or self._distance_for_gravity <= (col_obj.position - self._original_pos).length):
                col_obj.disable_gravity(False)
                col_obj.apply_force(math3d.vector(0, -self._gravity, 0))
            m = self._model() if self._model else None
            if not m or not m.valid:
                self.need_update = False
                return
            col_pos = col_obj.position
            interp_pos = math3d.vector(0, 0, 0)
            interp_thresh = 1
            u = self._interp_time / interp_thresh if self._interp_time < interp_thresh else 1
            interp_pos.intrp(m.position, col_pos, u)
            m.position = col_pos
            m.rotation_matrix = col_obj.rotation_matrix
            if self.count_down_frame_cnt >= 0:
                return
            now_time = time.time()
            if now_time - self.last_update_time > 2:
                self.last_update_time = now_time
                diff = col_pos - self.last_pos
                self.last_pos = col_pos
                md = max(abs(diff.x), abs(diff.y), abs(diff.z))
                if md < self.MIN_DELTA_DIST:
                    self.count_down_frame_cnt = self.DELAY_UPDATE_FRAME_COUNT
            if self._gernade_player_id:
                global_data.sound_mgr.set_position(self._gernade_id, col_pos)
            return

    def play_collisions_sound(self, position):
        cur_time = time.time()
        if cur_time - self._save_collision_time > 0.1:
            self._save_collision_time = cur_time
            global_data.sound_mgr.set_switch('grenade', 'grenade_ground', self._gernade_id)
            global_data.sound_mgr.post_event('Play_grenade', self._gernade_id, position)

    def _stop_sound(self):
        if self._gernade_player_id:
            global_data.sound_mgr.stop_playing_id(self._gernade_player_id)
            self._gernade_player_id = None
        global_data.sound_mgr.unregister_game_obj(self._gernade_id)
        return

    def destroy_col(self):
        if self._col_obj:
            global_data.emgr.del_ignore_col_ids_event.emit(self._col_obj.cid)
        super(ComTowerCollision, self).destroy_col()

    def destroy(self):
        self._stop_sound()
        super(ComTowerCollision, self).destroy()