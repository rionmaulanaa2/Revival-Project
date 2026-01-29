# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBarrageAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance, RES_TYPE_MODEL, RES_TYPE_SFX
from .ComGrenadeAppearance import ComGrenadeAppearance
from common.cfg import confmgr
import math3d

class ComBarrageAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({})

    def __init__(self):
        super(ComBarrageAppearance, self).__init__()
        self.item_id = None
        self.appearance_type = RES_TYPE_MODEL
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, unit_obj, bdict):
        super(ComBarrageAppearance, self).init_from_dict(unit_obj, bdict)
        self.need_update = False

    def cache(self):
        self.destroy_model()
        super(ComBarrageAppearance, self).cache()
        self.item_id = None
        self.appearance_type = RES_TYPE_MODEL
        return

    def get_model_info(self, unit_obj, bdict):
        self.item_id = bdict['item_itype']
        conf = confmgr.get('grenade_res_config', str(self.item_id), default={})
        model_path = conf.get('cRes', None)
        if model_path.endswith('.sfx'):
            self.load_res_func = self.load_sfx
            self.appearance_type = RES_TYPE_SFX
        m_pos = bdict.get('m_position')
        pos = m_pos if m_pos else bdict.get('position', (0, 0, 0))
        direction = bdict.get('dir', (0, 0, 1))
        up = bdict.get('up', (0, 1, 0))
        return (
         model_path, None, (pos, direction, up))

    def on_load_model_complete(self, model, user_data):
        pos, direction, up = user_data
        pos = math3d.vector(*pos)
        direction = math3d.vector(*direction)
        up = math3d.vector(*up)
        if up.is_zero:
            up = math3d.vector(0, 1, 0)
        if direction.is_zero:
            direction = math3d.vector(0, 0, 1)
        model.set_placement(pos, direction, up)
        scale = confmgr.get('grenade_res_config', str(self.item_id), 'fBulletSfxScale')
        if scale:
            model.scale = math3d.vector(scale, scale, scale)

    def tick(self, dt):
        pass

    def destroy_model(self):
        sfx = self.get_model()
        if sfx and self.appearance_type == RES_TYPE_SFX:
            if sfx.visible:
                import game3d
                from common.framework import Functor
                func = Functor(global_data.sfx_mgr.shutdown_sfx, sfx)
                game3d.delay_exec(40, func)
            else:
                global_data.sfx_mgr.remove_sfx(sfx)

    def destroy(self):
        self.destroy_model()
        super(ComBarrageAppearance, self).destroy()
        self.process_event(False)