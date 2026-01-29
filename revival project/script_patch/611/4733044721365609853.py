# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSpotSfxPlayer.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d

class ComSpotSfxPlayer(UnitCom):
    BIND_EVENT = {'E_SPOT_SFX_PLAYER': 'ret_spot_sfx'
       }

    def __init__(self):
        super(ComSpotSfxPlayer, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComSpotSfxPlayer, self).init_from_dict(unit_obj, bdict)
        self.pos = math3d.vector(*bdict.get('position'))
        self.res_path = bdict.get('res_path')
        self.end_res_path = bdict.get('end_res_path')
        res_scale = bdict.get('res_scale', 1.0)
        self.res_scale = math3d.vector(res_scale, res_scale, res_scale)
        self.sfx_id = None
        self.sound_event = bdict.get('sound_event', None)
        return

    def on_init_complete(self):
        self.ret_spot_sfx(True)
        return super(ComSpotSfxPlayer, self).on_init_complete()

    def destroy(self):
        self.clear_sfx()
        self.play_end_sfx()
        super(ComSpotSfxPlayer, self).destroy()

    def ret_spot_sfx(self, ret):
        self.clear_sfx()
        if ret:
            self.sfx_id = global_data.sfx_mgr.create_sfx_in_scene(self.res_path, self.pos, on_create_func=self.on_create)

    def on_create(self, sfx, *args):
        sfx.scale = self.res_scale
        if self.sound_event:
            global_data.sound_mgr.play_event(self.sound_event, self.pos)

    def clear_sfx(self):
        if self.sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sfx_id)
            self.sfx_id = None
        return

    def play_end_sfx(self):
        if self.end_res_path:
            global_data.sfx_mgr.create_sfx_in_scene(self.end_res_path, self.pos, on_create_func=self.on_create_end)

    def on_create_end(self, sfx):
        sfx.scale = self.res_scale