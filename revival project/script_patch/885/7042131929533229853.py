# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWaterMecha.py
from __future__ import absolute_import
from .ComWater import ComWater
from logic.gcommon.common_const import water_const
from logic.gcommon.common_const.disable_bit_const import DISABLE_MAIN_WEAPON_BY_WATER, DISABLE_SEC_WEAPON_BY_WATER
import math3d

class ComWaterMecha(ComWater):
    BIND_EVENT = ComWater.BIND_EVENT.copy()
    BIND_EVENT.update({'G_IS_DIVING': 'get_diving',
       'E_MODEL_LOADED': '_on_model_loaded'
       })

    def __init__(self):
        super(ComWaterMecha, self).__init__()
        self.diving = False
        self.pos_off = None
        self.off_y = 60
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComWaterMecha, self).init_from_dict(unit_obj, bdict)
        self._init_offset()

    def _on_model_loaded(self, *args):
        self._init_offset()

    def _init_offset(self):
        if self.pos_off:
            return
        model = self.ev_g_model()
        if not model:
            return
        mat = model.get_socket_matrix('water_detect')
        if mat:
            self.pos_off = mat.translation
            self.off_y = self.pos_off.y

    def get_pos(self):
        return self.ev_g_position() + math3d.vector(0, 2, 0)

    def change_status(self, last_status, water_height=None, water_depth=0):
        super(ComWaterMecha, self).change_status(last_status, water_height)
        self.send_event('E_WATER_EVENT', last_status, water_height)
        self.send_event('E_CALL_SYNC_METHOD', 'change_water_status', (last_status, water_height, water_depth), True)

    def on_check_fly_failed(self, pos_y, water_y):
        if pos_y + self.off_y > water_y:
            return True
        else:
            return False

    def on_water_depth_change(self, diff_height):
        if diff_height > self.off_y:
            if self.diving is not True and self.sd.ref_hp:
                self.set_diving(True)
                self.enter_diving()
        elif self.diving is not False:
            self.set_diving(False)
            self.leave_diving()

    def set_diving(self, dive):
        self.diving = dive

    def get_diving(self):
        return self.diving

    def enter_diving(self):
        self.send_event('E_MECHA_ENTER_DIVING')
        self.send_event('E_CALL_SYNC_METHOD', 'mecha_enter_diving', (), True)
        self.send_event('E_DISABLE_BIT_MAIN_WEAPON', DISABLE_MAIN_WEAPON_BY_WATER, True)
        self.send_event('E_DISABLE_BIT_SECOND_WEAPON', DISABLE_SEC_WEAPON_BY_WATER, True)
        self.send_event('TRY_STOP_WEAPON_ATTACK')

    def leave_diving(self):
        self.send_event('E_MECHA_LEAVE_DIVING')
        self.send_event('E_CALL_SYNC_METHOD', 'mecha_leave_diving', (), True)
        self.send_event('E_DISABLE_BIT_MAIN_WEAPON', DISABLE_MAIN_WEAPON_BY_WATER, False)
        self.send_event('E_DISABLE_BIT_SECOND_WEAPON', DISABLE_SEC_WEAPON_BY_WATER, False)