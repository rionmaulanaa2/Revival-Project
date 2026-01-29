# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComPVESlopeBouncer.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d

class ComPVESlopeBouncer(UnitCom):
    BIND_EVENT = {}
    SFX_PATH = 'effect/fx/building/tishi_45.sfx'
    SFX_SCALE = 3.0

    def __init__(self):
        super(ComPVESlopeBouncer, self).__init__()
        self.dynamic_jump_arg = None
        self.fixed_jump_dir = None
        self.sfx_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVESlopeBouncer, self).init_from_dict(unit_obj, bdict)
        self.dynamic_jump_arg = bdict.get('dynamic_jump_arg', None)
        if self.dynamic_jump_arg:
            self.fixed_jump_dir = self.dynamic_jump_arg['fixed_jump_dir']
        if self.fixed_jump_dir:
            global_data.game_mgr.next_exec(self.reset_model_dir)
        return

    def reset_model_dir(self, *args):
        model = self.ev_g_model()
        if model and model.valid:
            dire = math3d.vector(*self.fixed_jump_dir)
            dire.normalize()
            mat = math3d.matrix.make_orient(dire, math3d.vector(0, 1, 0))
            model.rotation_matrix = mat
            self.init_sfx(mat)

    def init_sfx(self, mat):
        self.clear_sfx()
        model = self.ev_g_model()
        if model and model.valid:

            def cb(sfx):
                sfx.scale = math3d.vector(self.SFX_SCALE, self.SFX_SCALE, self.SFX_SCALE)
                sfx.rotation_matrix = mat

            pos = model.world_position
            self.sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.SFX_PATH, pos, on_create_func=cb)

    def clear_sfx(self):
        if self.sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
            self.sfx_id = None
        return

    def destroy(self):
        self.clear_sfx()
        super(ComPVESlopeBouncer, self).destroy()