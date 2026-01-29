# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8032.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
import math3d
import logic.gcommon.common_utils.bcast_utils as bcast
from common.framework import Functor
STATE_TO_SFX = {'sprint': '100',
   'dash': '101',
   'sprint_dash': '102',
   'force_sprint': '104',
   'run_state_mid': '105',
   'run_state_loop': '106',
   'stomp_end': '107',
   'stomp_buff': '108'
   }
STOMP_GROUND_SFX = '103'

class ComMechaEffect8032(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ENBALE_8032_STATE_SFX': 'on_enable_8032_state_sfx',
       'E_PLAY_STOMP_ON_GROUND_SFX': 'on_play_stomp_on_ground_sfx'
       })

    def on_enable_8032_state_sfx(self, state_id, flag):
        sfx_id = STATE_TO_SFX.get(state_id, '100') if flag else ''
        self.on_trigger_state_effect(state_id, sfx_id, force=True, need_sync=False)

    def on_play_stomp_on_ground_sfx(self):
        pos = self.ev_g_position()

        def on_create_cb(sfx):
            sfx.position = pos

        self.on_trigger_disposable_effect(STOMP_GROUND_SFX, [pos.x, pos.y, pos.z], on_create_func=on_create_cb, need_sync=True)