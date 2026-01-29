# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComShockWaveAppearance.py
from __future__ import absolute_import
from common.cfg import confmgr
from ..UnitCom import UnitCom
import math3d

class ComShockWaveAppearance(UnitCom):
    BIND_EVENT = {}

    def init_from_dict(self, unit_obj, bdict):
        super(ComShockWaveAppearance, self).init_from_dict(unit_obj, bdict)
        self.init_params(bdict)
        self.process_event(True)

    def on_post_init_complete(self, bdict):
        self.init_sfx()

    def init_params(self, bdict):
        self.item_id = bdict.get('item_id')
        self.conf = confmgr.get('grenade_res_config', str(self.item_id))
        self.params = global_data.pve_shockwave_dict or self.conf.get('cCustomParam') if 1 else global_data.pve_shockwave_dict
        self.ori_pos = math3d.vector(*bdict.get('position'))

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_sfx(self):
        pos = self.ori_pos
        sfx_path = self.params['sfx']
        dur = self.params['dur']
        scale = self.params['scale']
        rate = self.params['rate']
        sfx_offset = self.params['sfx_offset']

        def cb(sfx):
            sfx.scale = math3d.vector(scale, scale, scale)
            sfx.frame_rate = rate
            self.send_event('E_SFX_INIT')

        global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos + math3d.vector(0, sfx_offset, 0), duration=dur / rate, on_create_func=cb)

    def destroy(self):
        self.process_event(False)
        super(ComShockWaveAppearance, self).destroy()