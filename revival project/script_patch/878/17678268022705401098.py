# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComCameraEvent.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.cdata import mecha_status_config as m_st_const
from logic.gcommon.cdata import status_config as st_const

class ComCameraEvent(UnitCom):
    BIND_EVENT = {'G_IS_CAN_FREE_CAMERA': '_check_can_free_camera',
       'E_ENABLE_FREE_CAMERA': 'enable_free_camera'
       }

    def __init__(self):
        super(ComCameraEvent, self).__init__()
        self.free_camera_enabled = True

    def destroy(self):
        super(ComCameraEvent, self).destroy()

    def _check_can_free_camera(self):
        if not self.free_camera_enabled:
            return False
        else:
            forbid_state = [
             st_const.ST_SHOOT, st_const.ST_AIM, m_st_const.MC_SHOOT, m_st_const.MC_OTHER_SHOOT,
             m_st_const.MC_SECOND_WEAPON_ATTACK, m_st_const.MC_OTHER_SECOND_WEAPON_ATTACK, m_st_const.MC_ENERGY_BREAK]
            if self.ev_g_is_in_any_state(forbid_state):
                return False
            return True

    def enable_free_camera(self, flag):
        self.free_camera_enabled = flag