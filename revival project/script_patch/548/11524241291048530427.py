# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8021.py
from __future__ import absolute_import
from common.utils.timer import CLOCK
from math3d import matrix_to_rotation
from .ComGenericMechaEffect import ComGenericMechaEffect
SHOCKWAVE_EFFECT_ID = [
 '101', '102', '103', '104']

class ComMechaEffect8021(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded',
       'E_8021_SHOW_SHOCKWAVE': 'show_shockwave'
       })

    def __init__(self):
        super(ComMechaEffect8021, self).__init__()
        self.shockwave_timer_id = None
        self.next_shockwave_idx = 0
        self.shockwave_pos_rot_list = None
        return

    def on_skin_sub_model_loaded(self):
        if self.ev_g_mecha_fashion_id() in (201802152, 201802153, 201802154):
            self.sd.ref_socket_res_agent.play_model_res_anim('idle')

    def show_shockwave(self, pos_rot_list, interval=0.1):
        self.shockwave_pos_rot_list = pos_rot_list
        self.next_shockwave_idx = 0
        self.clear_shockwave_timer()
        self.shockwave_timer_id = global_data.game_mgr.register_logic_timer(self.create_shockwave_sfx, interval=interval, times=len(pos_rot_list), mode=CLOCK)

    def create_shockwave_sfx(self):
        pos, rot = self.shockwave_pos_rot_list[self.next_shockwave_idx]
        pos = (pos.x, pos.y, pos.z)
        rot = matrix_to_rotation(rot)
        rot = (rot.x, rot.y, rot.z, rot.w)
        self.on_trigger_disposable_effect(SHOCKWAVE_EFFECT_ID[self.next_shockwave_idx], pos, rot=rot, duration=0, need_sync=True)
        self.next_shockwave_idx += 1

    def clear_shockwave_timer(self):
        if self.shockwave_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.shockwave_timer_id)
        self.shockwave_timer_id = None
        return

    def destroy(self):
        super(ComMechaEffect8021, self).destroy()
        self.clear_shockwave_timer()