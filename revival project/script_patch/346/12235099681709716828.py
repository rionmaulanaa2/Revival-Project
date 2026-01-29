# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LBillboard.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component
import math3d
import game3d
from common.cfg import confmgr
import world
import math
_HASH_TEX0 = game3d.calc_string_hash('Tex0')

@component(client=[])
class LBillboard(Unit):

    def init_from_dict(self, bdict):
        super(LBillboard, self).init_from_dict(bdict)
        self._billborad = None
        self.create_billborad(bdict)
        return

    def create_billborad(self, bdict):
        scn = global_data.game_mgr.scene
        if not scn or not scn.valid:
            return
        else:
            uid = bdict.get('uid', None)
            tex = bdict.get('texture', None)
            pos = bdict.get('position', None)
            bconf = confmgr.get('tv_conf', 'billboard', 'Content', default={})
            bb_info = bconf.get(str(uid), '')
            if bb_info:
                pos = math3d.vector(*pos)
                mpath = bb_info.get('model', '')
                rot = bb_info.get('rot', [0, 0, 0])
                scale = bb_info.get('scale', [1, 1, 1])
                rot = [ x / 180.0 * math.pi for x in rot ]
                self._billborad = world.model(mpath, scn)
                self._billborad.world_position = pos
                rot = math3d.euler_to_matrix(math3d.vector(*rot))
                self._billborad.world_rotation_matrix = rot
                self._billborad.scale = math3d.vector(*scale)
                self._billborad.all_materials.set_texture(_HASH_TEX0, 'Tex0', tex)
            return

    def destroy(self):
        if self._billborad and self._billborad.valid:
            self._billborad.destroy()
        self._billborad = None
        super(LBillboard, self).destroy()
        return