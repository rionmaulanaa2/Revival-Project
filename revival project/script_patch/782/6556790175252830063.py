# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMuzzleAppearance.py
from __future__ import absolute_import
import time
import math3d
from common.cfg import confmgr
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_utils.bcast_utils as bcast
INTERVAL_TIME = 0.1

class ComMuzzleAppearance(UnitCom):
    BIND_EVENT = {'E_SHOW_AI_SHOOT': 'play_gun_fire_sfx',
       'E_SHOW_MUZZLE_FIRE_EFFECT': 'play_gun_fire_sfx'
       }

    def __init__(self):
        super(ComMuzzleAppearance, self).__init__()
        self._last_play_time = 0
        self._muzzle_index = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComMuzzleAppearance, self).init_from_dict(unit_obj, bdict)

    def play_gun_fire_sfx(self, *args):
        if time.time() - self._last_play_time < 0.2:
            return
        self._last_play_time = time.time()
        socket_name = 'fx_spark_kaihuo_0%d' % (self._muzzle_index + 1)
        self._muzzle_index = 1 - self._muzzle_index
        socket_matrix = self.ev_g_model_socket_pos(socket_name)
        if not socket_matrix:
            return
        wp_type = self.ev_g_weapon_type()
        if not wp_type:
            log_error('there is no weapon type')
            return
        res_conf = confmgr.get('firearm_res_config', str(wp_type))
        if not res_conf:
            return
        sfx_path = res_conf.get('cSfx')
        model = self.ev_g_model()
        if sfx_path and model and model.valid:

            def create_cb(sfx):
                sfx.scale = math3d.vector(5, 5, 5)

            global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name, on_create_func=create_cb)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_MUZZLE_FIRE_EFFECT, ()], True, False, True)