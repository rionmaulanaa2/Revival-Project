# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEBoxAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
import math3d
from logic.gcommon.common_const.pve_const import PVE_BOX_STATE_CLOSE, PVE_BOX_STATE_OPEN, PVE_BOX_STATE_OPENED, PVE_BOX_TYPE_ENERGY, PVE_BOX_TYPE_BREAK

class ComPVEBoxAppearance(UnitCom):
    BIND_EVENT = {'E_ON_PVE_BOX_CLOSE': 'on_closed',
       'E_ON_PVE_BOX_OPEN': 'on_open',
       'E_ON_PVE_BOX_OPENED': 'on_opened',
       'G_PVE_BOX_TYPE': 'get_box_type',
       'G_MODEL': 'get_model'
       }
    T_D = {10006001: PVE_BOX_TYPE_ENERGY,
       10006002: PVE_BOX_TYPE_BREAK
       }
    UP = math3d.vector(0, 1, 0)

    def __init__(self):
        super(ComPVEBoxAppearance, self).__init__()
        self.model = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEBoxAppearance, self).init_from_dict(unit_obj, bdict)
        self.item_id = bdict.get('box_type')
        self.box_type = self.T_D[self.item_id]
        self.res_conf = confmgr.get('box_res', str(self.item_id))
        self.pos = math3d.vector(*bdict.get('position'))
        self.dir = bdict.get('dir', None)
        self.model = None
        return

    def on_init_complete(self):
        self.init_model()

    def init_model(self):
        path = self.res_conf.get('res')
        scale = self.res_conf.get('model_scale', 1.0)
        col_info = self.res_conf.get('col_info')

        def cb(model):
            model.position = self.pos
            model.scale = math3d.vector(scale, scale, scale)
            self.model = model
            if self.dir:
                forward = math3d.vector(*self.dir)
                if not forward.is_zero:
                    forward.normalize()
                    mat = math3d.matrix.make_orient(forward, self.UP)
                    model.rotation_matrix = mat
            self.send_event('E_MODEL_LOADED', self.pos, scale, col_info)

        global_data.model_mgr.create_model_in_scene(path, on_create_func=cb)

    def init_sfx(self):
        pass

    def init_sound(self):
        pass

    def on_closed(self):
        if self.model:
            self.model.play_animation('idle')

    def on_open(self):
        if self.model:
            self.model.play_animation('idle')

    def on_opened(self):
        if self.model:
            self.model.play_animation('open')
            global_data.sound_mgr.play_sound_2d('Play_props', ('props_option', 'open_airdrop'))

    def get_box_type(self):
        return self.box_type

    def get_item_id(self):
        return self.item_id

    def get_model(self):
        return self.model

    def tick(self, dt):
        super(ComPVEBoxAppearance, self).tick(dt)

    def destroy(self):
        self.model and global_data.model_mgr.remove_model(self.model)
        self.model = None
        super(ComPVEBoxAppearance, self).destroy()
        return