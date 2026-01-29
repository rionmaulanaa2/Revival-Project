# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPhantomCollision.py
from __future__ import absolute_import
from .ComObjCollision import ComObjCollision
from logic.gcommon.common_const.collision_const import GROUP_GRENADE, GROUP_SHOOTUNIT
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
import collision
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
from common.cfg import confmgr

class ComPhantomCollision(ComObjCollision):

    def __init__(self):
        super(ComPhantomCollision, self).__init__()
        self.static_col_height = 0.0
        self._mask = GROUP_GRENADE
        self._group = GROUP_SHOOTUNIT

    def init_from_dict(self, unit_obj, bdict):
        super(ComPhantomCollision, self).init_from_dict(unit_obj, bdict)

    def _create_col_obj(self):
        col_type, bounding_box, mask, group, mass = self.get_collision_info()
        self._col_obj = collision.col_object(col_type, bounding_box, mask, group, mass)
        self.scene.scene_col.add_object(self._col_obj)
        model = self._model()
        model.bind_col_obj(self._col_obj, BONE_BIPED_NAME)
        self._col_obj.position = model.world_position
        self._col_obj.rotation_matrix = model.rotation_matrix
        self._col_obj.set_notify_contact(True)
        self._col_obj.set_contact_callback(self.on_contact)
        self._col_obj.ignore_collision = True
        self._col_obj.car_undrivable = True
        global_data.emgr.scene_add_phantom_obj.emit(self._col_obj.cid, self.unit_obj)

    def get_collision_info(self):
        physic_conf = confmgr.get('mecha_conf', 'PhysicConfig', 'Content')
        mecha_id = self.sd.ref_mecha_id
        physic_conf = physic_conf[str(mecha_id)]
        size = physic_conf['shoot_collison_size']
        col_size = math3d.vector(*size) * (0.5 * NEOX_UNIT_SCALE)
        return (
         collision.BOX, col_size, self._mask, self._group, 0)

    def on_contact(self, *args, **kwargs):
        if not self.is_enable():
            return
        self.send_event('E_PLAY_HIT_SFX')

    def destroy(self):
        if self._col_obj:
            global_data.emgr.scene_remove_phantom_obj.emit(self._col_obj.cid)
        super(ComPhantomCollision, self).destroy()