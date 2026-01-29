# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMonsterStaticCollision.py
from __future__ import absolute_import
from .ComObjCollision import ComObjCollision
import math3d
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComMonsterStaticCollision(ComObjCollision):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_load_complete',
       'E_TRY_AGENT': 'on_try_agent',
       'E_CANCEL_AGENT': 'on_cancel_agent'
       }

    def __init__(self):
        super(ComMonsterStaticCollision, self).__init__()
        from logic.gcommon.common_const.collision_const import GROUP_DEFAULT_VISIBLE
        self._mask = GROUP_DEFAULT_VISIBLE
        self._group = GROUP_DEFAULT_VISIBLE

    def get_collision_info(self):
        cfg_data = self.ev_g_config_data()
        character_size = cfg_data.get('CollisonSize', [2, 2, 2])
        model_scale = cfg_data.get('ModelScale', 1.0)
        width = character_size[0] * NEOX_UNIT_SCALE / 2
        height = character_size[1] * NEOX_UNIT_SCALE / 2
        bounding_box = math3d.vector(width, height, 0)
        mask = self._mask
        group = self._group
        mass = 0
        return {'collision_type': collision.CAPSULE,'bounding_box': bounding_box * model_scale,'mask': mask,'group': group,'mass': mass}

    def _create_col_obj(self):
        if self.sd.ref_is_agent:
            return
        super(ComMonsterStaticCollision, self)._create_col_obj()
        if self._col_obj:
            self._col_obj.car_undrivable = True
        self.on_cancel_agent()

    def on_try_agent(self, *_):
        if self._col_obj:
            model = self.ev_g_model()
            if model and model.valid:
                model.unbind_col_obj(self._col_obj)

    def on_cancel_agent(self, *args, **kargs):
        if self._col_obj:
            model = self.ev_g_model()
            if model and model.valid:
                model.bind_col_obj(self._col_obj, 'biped root')