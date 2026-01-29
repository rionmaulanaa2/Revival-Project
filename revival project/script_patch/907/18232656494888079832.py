# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComExtraTriggerExplodeCollision.py
from __future__ import absolute_import
from .ComObjCollision import ComObjCollision
from logic.gutils.collision_test_utils import CollisionTester
from logic.gcommon import time_utility as t_util
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
import collision
import math3d
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const.attr_const import EXTRA_TRIGGER_COLLISION_FACTOR

class ComExtraTriggerExplodeCollision(ComObjCollision):
    BIND_EVENT = {'E_MODEL_LOADED': ('on_model_load_complete', 99),
       'E_CHARACTER_ATTR': '_change_character_attr'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComExtraTriggerExplodeCollision, self).init_from_dict(unit_obj, bdict)
        self.throw_info = {}
        self.throw_info.update(bdict)
        self.item_id = bdict['item_itype']
        self.owner_id = bdict['owner_id']
        self.is_avatar = global_data.mecha and self.owner_id == global_data.mecha.id or global_data.player and self.owner_id == global_data.player.id
        self.collision_tester = None
        self.start_position = math3d.vector(0, 0, 0)
        self.min_valid_radius = NEOX_UNIT_SCALE
        self.valid_radius_difference = 1
        self.ignore_valid_radius_dist = 0
        return

    def _clear_reference(self):
        if self.collision_tester:
            self.collision_tester.destroy()
            self.collision_tester = None
        self.throw_info = {}
        return

    def cache(self):
        super(ComExtraTriggerExplodeCollision, self).cache()
        self._clear_reference()

    def destroy(self):
        super(ComExtraTriggerExplodeCollision, self).destroy()
        self._clear_reference()

    def explode(self, col, position):
        if not self.is_enable():
            return
        else:
            up = col.rotation_matrix.up
            forward = col.rotation_matrix.forward
            upload_data = {'pos': (
                     position.x, position.y, position.z),
               'up': (
                    up.x, up.y, up.z),
               'forward': (
                         forward.x, forward.y, forward.z),
               'normal': (
                        up.x, up.y, up.z),
               'is_ragdoll_part': False,
               'col_pos': (
                         position.x, position.y, position.z),
               'impulse_range': 0,
               'impulse_power': 0,
               'uploader_id': global_data.player.id
               }
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'update_explosive_item_info', ({self.throw_info['uniq_key']: upload_data},))
            explosive_item = self.throw_info
            explosive_item['position'] = upload_data['pos']
            explosive_item['up'] = upload_data['up']
            explosive_item['forward'] = upload_data['forward']
            explosive_item['explose_time'] = t_util.time()
            explosive_item['hit_target_id'] = upload_data.get('target', None)
            explosive_item['ignore_bomb_sfx'] = upload_data.get('ignore_bomb_sfx', False)
            explosive_item['target'] = upload_data.get('target', None)
            global_data.emgr.scene_throw_item_explosion_event.emit({explosive_item['uniq_key']: {'item': explosive_item}})
            return

    def contact_callback(self, col, position, *args, **kwargs):
        global_data.game_mgr.post_exec(self.explode, col, position)

    def check_valid_func(self, pos, hit_pos):
        fly_dist = (pos - self.start_position).length
        if fly_dist > self.ignore_valid_radius_dist:
            return True
        valid_radius = self.min_valid_radius + fly_dist / self.ignore_valid_radius_dist * self.valid_radius_difference
        return (pos - hit_pos).length <= valid_radius

    def _create_col_obj(self):
        if not self.is_avatar:
            return
        else:
            if not self.is_enable():
                return
            if self._model:
                m = self._model() if 1 else None
                return m or None
            conf = confmgr.get('grenade_config', str(self.item_id), 'cCustomParam', default={})
            col_size_factor = 1
            trigger_id = self.throw_info.get('trigger_id')
            if trigger_id:
                mecha = EntityManager.getentity(trigger_id)
                if mecha and mecha.logic:
                    col_size_factor += mecha.logic.ev_g_add_attr(EXTRA_TRIGGER_COLLISION_FACTOR, self.item_id) or 0
            valid_unit_names = conf.get('valid_unit_names', ('LMecha', 'LMechaRobot'))
            check_valid_func = None
            if 'col_radius' in conf:
                radius = conf['col_radius'] * NEOX_UNIT_SCALE
                col = collision.col_object(collision.SPHERE, math3d.vector(radius, radius, radius), 0, 0, 1)
                m = None
            else:
                check_valid_func = self.check_valid_func
                height = conf.get('col_height', 10.0) * col_size_factor
                depth = conf.get('col_depth', 4.0)
                width = conf.get('col_width', 2.0) * col_size_factor
                self.min_valid_radius = conf.get('min_valid_radius', 3) * NEOX_UNIT_SCALE
                self.valid_radius_difference = max(depth, width, height) * NEOX_UNIT_SCALE - self.min_valid_radius
                self.ignore_valid_radius_dist = conf.get('ignore_valid_radius_dist', 20) * NEOX_UNIT_SCALE
                col = collision.col_object(collision.BOX, math3d.vector(width, height, depth) * 0.5 * NEOX_UNIT_SCALE, 0, 0, 1)
            self.collision_tester = CollisionTester(col, self.owner_id, valid_unit_names=valid_unit_names, ignore_groupmates=True, need_add_to_scene=True, contact_callback=self.contact_callback, check_valid_func=check_valid_func, bind_model=m)
            self.collision_tester.initialize_col_physical_parameters(self.sd.ref_col_obj)
            self.start_position = self.sd.ref_col_obj.position
            return