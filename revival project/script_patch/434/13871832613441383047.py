# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComFlightForward.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.mecha_const import STATE_HUMANOID, STATE_INJECT
import math3d

class ComFlightForward(UnitCom):
    BIND_EVENT = {'E_ON_POST_JOIN_MECHA': ('on_post_join_mecha', 99)
       }

    def __init__(self):
        super(ComFlightForward, self).__init__(need_update=False)

    def _process_event(self, flag):
        if self.event_registered ^ flag:
            func = self.regist_event if flag else self.unregist_event
            func('E_SET_SERVER_FLIGHT_STATE', self.set_server_flight_state)
            if G_POS_CHANGE_MGR:
                pos_func = self.regist_pos_change if flag else self.unregist_pos_change
                pos_func(self.on_position)
            else:
                func('E_POSITION', self.on_position)
            self.event_registered = flag

    def init_from_dict(self, unit_obj, bdict):
        super(ComFlightForward, self).init_from_dict(unit_obj, bdict)
        self.last_pos = None
        self.last_forward = None
        self.last_time = global_data.game_time
        self.event_registered = False
        self.server_state = bdict.get('flight_state', STATE_HUMANOID)
        return

    def destroy(self):
        self._process_event(False)

    def on_post_join_mecha(self):
        self._process_event(not self.ev_g_is_avatar())

    def set_server_flight_state(self, state):
        if state == STATE_INJECT:
            self.send_event('E_FORBID_ROTATION', True)
        else:
            self.send_event('E_FORBID_ROTATION', False)
        self.server_state = state

    def on_position(self, pos):
        if self.server_state != STATE_INJECT:
            return
        if not self.last_pos:
            self.last_pos = pos
            return
        diff = pos - self.last_pos
        self.last_pos = pos
        if diff.is_zero:
            return
        _time = global_data.game_time
        forward = diff
        scene = self.scene
        if scene:
            if diff.length < 4 and _time - self.last_time <= 0.5:
                return
            mat_cam = scene.active_camera.rotation_matrix
            cam_forward = mat_cam.forward
            forward.normalize()
            if forward.dot(cam_forward) < 0.8:
                tmp = math3d.vector(0, 0, 0)
                tmp.intrp(cam_forward, forward, 0.9)
                forward = tmp
            if self.last_forward:
                forward.intrp(self.last_forward, forward, 0.35)
            self.last_forward = forward
            self.last_time = _time
            self.send_event('E_FORWARD', forward, True)