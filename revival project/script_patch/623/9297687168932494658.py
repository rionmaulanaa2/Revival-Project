# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComParadropBallAppearance.py
from __future__ import absolute_import
import math3d
from .ComBaseModelAppearance import ComBaseModelAppearance
from common.cfg import confmgr
SCALE = 5
RADIUS = 3.16 * SCALE

class ComParadropBallAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({})

    def __init__(self):
        super(ComParadropBallAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComParadropBallAppearance, self).init_from_dict(unit_obj, bdict)

    def cache(self):
        self._destroy_model()
        super(ComParadropBallAppearance, self).cache()

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        direction = bdict.get('dir', [0, 0.785, 1])
        up = bdict.get('up', [0, 1, 0])
        model_path = confmgr.get('script_gim_ref')['beach_volleyball']
        return (
         model_path, None, (pos, direction, up))

    def on_load_model_complete(self, model, userdata):
        pos, direction, up = userdata
        pos = math3d.vector(*pos)
        direction = math3d.vector(*direction)
        up = math3d.vector(*up)
        if up.is_zero:
            up = math3d.vector(0, 1, 0)
        if direction.is_zero:
            direction = math3d.vector(0, 0, 1)
        direction = math3d.vector(1, 0, 0)
        pos += math3d.vector(0, RADIUS, 0)
        model.set_placement(pos, direction, up)
        model.scale = math3d.vector(SCALE, SCALE, SCALE)

    def destroy(self):
        super(ComParadropBallAppearance, self).destroy()