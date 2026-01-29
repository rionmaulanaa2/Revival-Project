# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_fire/ComFireAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
from mobile.common.EntityManager import EntityManager
import world
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
from logic.gcommon.component.client.ComBaseModelAppearance import RES_TYPE_SFX, RES_TYPE_MODEL

class ComFireAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_COLLISION_INFO': '_get_collision_info',
       'E_HIT_BLOOD_SFX': '_on_be_hited'
       })

    def __init__(self):
        super(ComFireAppearance, self).__init__()
        self._sub_sfx_id = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        super(ComFireAppearance, self).destroy()
        self.process_event(False)

    def init_from_dict(self, unit_obj, bdict):
        self.pos = bdict.get('position', [0, 0, 0])
        self.rot = bdict.get('rot', [0, 0, 0, 1])
        super(ComFireAppearance, self).init_from_dict(unit_obj, bdict)

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        model_path = confmgr.get('script_gim_ref')['empty_item_model']
        return (
         model_path, None, (pos, rot, bdict))

    def _get_collision_info(self):
        return {'custom_box': (1.5, 4.5, 1.5),'offset': math3d.vector(0.0, 5, 0.0),'non_explosion_dis': True}

    def on_load_model_complete(self, model, userdata):
        import math3d
        import collision
        import render
        import game3d
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        model.world_position = pos
        self.open_fire_sfx()

    def on_model_destroy(self):
        self._sub_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self._sub_sfx_id)
        self._sub_sfx_id = None
        return

    def _show_fire_sfx(self):
        return True

    def open_fire_sfx(self):
        if self._show_fire_sfx():
            if not self._sub_sfx_id:
                self.create_fire_sfx()
        elif self._sub_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._sub_sfx_id)
            self._sub_sfx_id = None
        return

    def create_fire_sfx(self):

        def create_sfx_cb(sfx):
            sfx.scale = math3d.vector(3.0, 3.0, 3.0)

        self._sub_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self._sub_sfx_id)
        self._sub_sfx_id = global_data.sfx_mgr.create_sfx_in_scene('effect/fx/niudan/xiaofangwanfa/xf_huoyan_01.sfx', math3d.vector(*self.pos), on_create_func=create_sfx_cb)