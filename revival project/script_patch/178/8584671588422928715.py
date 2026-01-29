# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFlyingAttachGrenadeCollsion.py
from __future__ import absolute_import
from .ComGrenadeCollision import ComGrenadeCollision
from logic.gutils.scene_utils import is_break_obj
from logic.gutils.client_unit_tag_utils import preregistered_tags
from logic.gutils import team_utils
from logic.gcommon.common_const import collision_const
from .ComWeaponCollisionBase import COLLISION_MASK_UNIT_IGNORE_COLLISION
import time
from logic.entities.IgniteGrenade import IgniteGrenade
from logic.units.LIgniteGrenade import LIgniteGrenade

class ComFlyingAttachGrenadeCollsion(ComGrenadeCollision):

    def set_group_and_mask(self, obj):
        obj.group = collision_const.GROUP_GRENADE
        obj.mask = collision_const.GROUP_CAN_SHOOT | collision_const.GROUP_SHIELD & ~collision_const.GROUP_MINER
        if self.collision_type_mask & COLLISION_MASK_UNIT_IGNORE_COLLISION:
            obj.ignore_collision = True

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        else:
            if not self._is_collision_enable:
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
            if cobj:
                if cobj.cid in self._col_ids:
                    return
            is_trigger = self.is_trigger(cobj)
            if not is_trigger and not is_break_obj(cobj.model_col_name):
                self._contact_other_col_times += 1
                if not (self._max_contact_other_col_times > 0 and self._contact_other_col_times >= self._max_contact_other_col_times):
                    if self._col_obj.linear_velocity.length > self.COLLIDE_SOUND_SPEED_LIMIT:
                        self.play_collisions_sound(point)
                    return
            if self._model:
                model = self._model() if 1 else None
                if not model:
                    return
                contact_info = {}
                target_id = None
                if cobj:
                    unit = global_data.emgr.scene_find_unit_event.emit(cobj.cid)[0]
                    if unit:
                        hp = unit.share_data.ref_hp
                        if unit.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE and (hp is None or unit.share_data.ref_hp <= 0):
                            return
                        target_id = unit.id
                        if unit.ev_g_is_campmate(self.faction_id) and unit.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE:
                            forward = model.rotation_matrix.forward
                            upload_data = dict({'pos': (
                                     point.x, point.y, point.z),
                               'up': (
                                    normal.x, normal.y, normal.z),
                               'forward': (
                                         forward.x, forward.y, forward.z),
                               'is_ragdoll_part': False,
                               'col_pos': (
                                         point.x, point.y, point.z),
                               'impulse_range': 0,
                               'impulse_power': 0,
                               'bonded_id': target_id
                               })
                            explosive_items = {self.throw_info['uniq_key']: upload_data}
                            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'update_explosive_item_info', (explosive_items,))
                            return
                    if is_trigger:
                        if team_utils.ignore_expolosion(self._owner_id, target_id):
                            return
                    elif unit.ev_g_is_campmate(self.faction_id):
                        return
                    target_type = global_data.emgr.scene_find_unit_type_event.emit(cobj.cid)[0]
                    col_is_pierced = unit.ev_g_is_pierced()
                    if self.is_pierced and (col_is_pierced is None or col_is_pierced is True):
                        self.send_harm_info(unit, cobj.cid, point)
                        self.complete_model_pos_interpolation()
                        return
                    contact_info['target_type'] = target_type
            self.complete_model_pos_interpolation()
            if self._col_obj:
                self.need_update = False
                self._col_obj.set_notify_contact(False)
            self.stop_post_contact_timer()
            explosive_info = (cobj, point, model, normal, target_id, self.throw_info)
            contact_info['explosive_info'] = explosive_info
            self._col_objs.append(contact_info)
            self.post_on_contact()
            self.editor_create_ignite_grenade(point)
            return

    def editor_create_ignite_grenade(self, pos):
        if not global_data.is_local_editor_mode:
            return
        item_type_2_robot_no = {802303: 8023031,802402: 8024031
           }
        throw_item = {'robot_no': item_type_2_robot_no.get(self.item_type, 8023031),
           'position': (
                      pos.x, pos.y, pos.z)
           }
        entity = IgniteGrenade()
        unit = LIgniteGrenade(entity, global_data.battle)
        unit.init_from_dict(throw_item)
        entity.logic = unit
        if global_data.mecha and global_data.mecha.logic:
            global_data.mecha.logic.sd.ref_grenade_unit = unit
            global_data.mecha.logic.sd.ref_grenade_entity = entity