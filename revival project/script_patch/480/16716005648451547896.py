# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEShopAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
import math3d
from logic.gcommon.common_const.pve_const import PVE_SHOP_STATE_CLOSED, PVE_SHOP_STATE_OPENED

class ComPVEShopAppearance(UnitCom):
    BIND_EVENT = {'E_ON_PVE_SHOP_CLOSED': 'on_closed',
       'E_ON_PVE_SHOP_OPENED': 'on_opened',
       'G_MODEL': 'get_model'
       }
    UP = math3d.vector(0, 1, 0)
    SFX_RES = 'effect/fx/scenes/common/pve/pve_shangcheng.sfx'
    SFX_SOCKET = 'fx_root'

    def __init__(self):
        super(ComPVEShopAppearance, self).__init__()
        self.model = None
        self.sfx_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEShopAppearance, self).init_from_dict(unit_obj, bdict)
        self.item_id = bdict.get('npc_id')
        self.res_conf = confmgr.get('box_res', str(self.item_id))
        self.pos = math3d.vector(*bdict.get('position'))
        self.dir = bdict.get('dir', None)
        self.model = None
        self.sfx_id = None
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
            self.init_sfx()

        global_data.model_mgr.create_model_in_scene(path, on_create_func=cb)

    def init_sfx(self):
        if self.sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
        if self.model:
            global_data.sfx_mgr.create_sfx_on_model(self.SFX_RES, self.model, self.SFX_SOCKET)

    def init_sound(self):
        pass

    def on_closed(self):
        pass

    def on_opened(self):
        global_data.sound_mgr.play_sound_2d('Play_props', ('props_option', 'open_airdrop'))

    def get_model(self):
        return self.model

    def tick(self, dt):
        super(ComPVEShopAppearance, self).tick(dt)

    def destroy(self):
        self.model and global_data.model_mgr.remove_model(self.model)
        self.model = None
        self.sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
        self.sfx_id = None
        super(ComPVEShopAppearance, self).destroy()
        return