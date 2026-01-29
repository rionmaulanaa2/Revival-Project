# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComGrenadeAppendCollision.py
from __future__ import absolute_import
from .ComObjCollision import ComObjCollision
from common.cfg import confmgr
from logic.gcommon.common_const.collision_const import GROUP_SHOOTUNIT, GROUP_GRENADE
from logic.gcommon.const import NEOX_UNIT_SCALE
from mobile.common.EntityManager import EntityManager
from logic.gutils import team_utils
from logic.gutils import game_mode_utils
import math3d
import collision

class ComGrenadeAppendCollision(ComObjCollision):
    PICK_CONF_PATH = 'grenade_config'

    def __init__(self):
        super(ComGrenadeAppendCollision, self).__init__()
        self.object_conf = None
        self._is_explosive = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComGrenadeAppendCollision, self).init_from_dict(unit_obj, bdict)
        self.item_id = bdict['item_itype']
        str_item_id = str(self.item_id)
        self.object_conf = confmgr.get(self.PICK_CONF_PATH, str_item_id, default={})
        self.faction_id = bdict.get('faction_id', 0)
        self.throw_info = {}
        self.throw_info.update(bdict)
        self._owner_id = bdict['owner_id']
        break_data = confmgr.get('break_data', str_item_id, default={})
        self._impulse_power = float(break_data.get('cBreakPower', 0))
        self._impulse_range = float(break_data.get('fBreakRange', 0)) * NEOX_UNIT_SCALE
        if bdict.get('trigger_id', None):
            trigger_id = bdict['trigger_id']
            target = EntityManager.getentity(trigger_id)
            if target and target.logic:
                self._col_ids = target.logic.ev_g_human_col_id()
        else:
            self._col_ids = []
        return

    def cache(self):
        super(ComGrenadeAppendCollision, self).cache()
        self.object_conf = None
        self._col_ids = []
        self._is_explosive = False
        return

    def on_model_destroy(self):
        if self._col_obj:
            self.scene.scene_col.remove_object(self._col_obj)
            self._col_obj = None
        return

    def _create_col_obj(self):
        if not self.is_enable():
            return
        else:
            if self._model:
                m = self._model() if 1 else None
                return m or None
            collision_type = collision.BOX
            bounding_box = math3d.vector(self.throw_info.get('col_width', 6) * NEOX_UNIT_SCALE, 0.5 * NEOX_UNIT_SCALE, NEOX_UNIT_SCALE)
            rot = m.rotation_matrix
            self._col_obj = collision.col_object(collision_type, bounding_box, GROUP_SHOOTUNIT, GROUP_GRENADE, 1)
            self._col_obj.set_contact_callback(self.on_contact)
            self._col_obj.set_notify_contact(True)
            position = math3d.vector(*self.throw_info['position'])
            self._col_obj.position = position + rot.forward * NEOX_UNIT_SCALE * 1.5
            self._col_obj.rotation_matrix = rot
            self._col_obj.is_explodable = True
            self._col_obj.is_unragdoll = True
            self._col_obj.kinematic = True
            self.scene.scene_col.add_object(self._col_obj)
            self.need_update = True
            return

    def on_contact(self, *args):
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
            trigger_id = self.throw_info['trigger_id']
            if cobj:
                if cobj.cid in self._col_ids:
                    return
                res = global_data.emgr.scene_is_shoot_obj.emit(cobj.cid)
                if not res or not res[0]:
                    return
                res = global_data.emgr.scene_find_unit_event.emit(cobj.cid)
                if not res or not res[0]:
                    return
                unit_obj = res[0]
                if unit_obj.ev_g_is_teammate_door():
                    return
                if unit_obj.ev_g_is_campmate(self.faction_id):
                    return
                if team_utils.ignore_expolosion(self._owner_id, unit_obj.id):
                    return
                if unit_obj.__class__.__name__ == 'LField':
                    trigger = EntityManager.getentity(trigger_id)
                    if trigger and trigger.logic and trigger.logic.ev_g_is_campmate(unit_obj.ev_g_camp_id()):
                        return
            if self._model:
                model = self._model() if 1 else None
                return model or None
            if self._col_obj:
                self._col_obj.set_notify_contact(False)
            player = global_data.player
            if not player and not player.logic:
                return
            if self._is_explosive:
                return
            self._is_explosive = True
            forward = model.rotation_matrix.forward
            upload_data = {'pos': (
                     point.x, point.y, point.z),
               'up': (
                    normal.x, normal.y, normal.z),
               'forward': (
                         forward.x, forward.y, forward.z)
               }
            mecha_unit = global_data.war_mechas.get(cobj.cid)
            if mecha_unit:
                upload_data['target'] = mecha_unit.id
            mecha_unit = global_data.mecha_shields.get(cobj.cid)
            if mecha_unit:
                upload_data['target'] = mecha_unit.id
                mecha_unit.send_event('E_HIT_SHIELD_SFX', end=point, itype=self.item_id)
            target = global_data.war_non_explosion_dis_objs.get(cobj.cid)
            if target:
                upload_data['target'] = target
            if self.ev_g_check_pierce(unit_obj, cobj.cid, point):
                return
            player_id = player.id
            mecha_id = global_data.mecha.id if global_data.mecha else None
            target = upload_data.get('target', None)
            if self.throw_info.get('call_sync_id', None) == global_data.battle_idx:
                need_sync = True
            elif target and (target == player_id or target == mecha_id):
                need_sync = True
            elif trigger_id == player_id or trigger_id == mecha_id:
                need_sync = True
            else:
                need_sync = False
            if need_sync:
                upload_data['col_pos'] = upload_data['pos']
                item_conf = self.object_conf
                if item_conf and item_conf['iDifferentPartDamage']:
                    explode_target_data = global_data.emgr.scene_explode_event.emit(point, game_mode_utils.get_custom_param_by_mode(item_conf, 'fRange') * NEOX_UNIT_SCALE, forward)
                    if explode_target_data:
                        upload_data['extra_info'] = explode_target_data[0]
                if cobj:
                    upload_data['cobj_group'] = cobj.group
                    upload_data['cobj_mask'] = cobj.mask
                    upload_data['impulse_range'] = self._impulse_range
                    upload_data['impulse_power'] = self._impulse_power
                    upload_data['normal'] = (normal.x, normal.y, normal.z)
                    upload_data['model_col_name'] = cobj.model_col_name
                explosive_items = {self.throw_info['uniq_key']: upload_data}
                player.logic.send_event('E_CALL_SYNC_METHOD', 'update_explosive_item_info', (explosive_items,))
            explosive_item = self.throw_info
            explosive_item['position'] = upload_data['pos']
            explosive_item['up'] = upload_data['up']
            explosive_item['forward'] = upload_data['forward']
            from logic.gcommon import time_utility as t_util
            explosive_item['explose_time'] = t_util.time()
            if cobj:
                explosive_item['cobj_group'] = cobj.group
                explosive_item['cobj_mask'] = cobj.mask
                explosive_item['impulse_range'] = self._impulse_range
                explosive_item['impulse_power'] = self._impulse_power
                explosive_item['normal'] = (normal.x, normal.y, normal.z)
                explosive_item['model_col_name'] = cobj.model_col_name
            global_data.game_mgr.post_exec(global_data.emgr.scene_throw_item_explosion_event.emit, {explosive_item['uniq_key']: {'item': explosive_item}})
            return

    def tick(self, delta):
        m = self._model() if self._model else None
        if not m or not m.valid:
            return
        else:
            col_obj = self.sd.ref_col_obj
            if not col_obj or not col_obj.valid:
                return
            self._col_obj.position = col_obj.position + m.rotation_matrix.forward * NEOX_UNIT_SCALE * 1.5
            self._col_obj.rotation_matrix = m.rotation_matrix
            return