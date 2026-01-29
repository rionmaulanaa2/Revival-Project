# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComFogFieldAgent.py
from __future__ import absolute_import
import time
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d

class ComFogFieldAgent(UnitCom):
    BIND_EVENT = {'E_TRY_AGENT': 'on_try_agent',
       'E_TRY_AGENT_ACTION': 'on_try_agent_action',
       'E_CANCEL_AGENT': 'on_cancel_agent',
       'E_ABORT_AGENT': 'on_abort_agent',
       'E_HEALTH_HP_EMPTY': 'on_cancel_agent',
       'G_IS_AGENT': 'get_is_agent'
       }

    def __init__(self):
        super(ComFogFieldAgent, self).__init__()
        self.sd.ref_is_agent = False
        self._need_become_agent = False
        self.need_update = False
        self._agent_pos = None
        self._last_check_time = 0
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComFogFieldAgent, self).init_from_dict(unit_obj, bdict)
        self._bdict = bdict
        global_data.emgr.app_background_event += self.on_cancel_agent

    def destroy(self):
        global_data.emgr.app_background_event -= self.on_cancel_agent
        super(ComFogFieldAgent, self).destroy()

    def begin_agent(self):
        self._need_become_agent = False
        self.need_update = False
        self.sd.ref_is_agent = True
        self.send_event('E_ON_AGENT')

    def on_try_agent(self, pos):
        self._need_become_agent = False
        self.need_update = False
        logic = global_data.player.logic if global_data.player else None
        if self.ev_g_death():
            logic and logic.send_event('E_CALL_SYNC_METHOD', 'confirm_agent', (self.unit_obj.id, False), True)
            return
        else:
            v3d_pos = tp_to_v3d(pos)
            self._agent_pos = v3d_pos
            if not self.sd.ref_is_agent:
                scene = global_data.game_mgr.get_cur_scene()
                if scene:
                    if scene.check_collision_loaded(v3d_pos):
                        self.begin_agent()
                    else:
                        self._need_become_agent = True
                        self.need_update = True
            if logic and not self._need_become_agent:
                logic.send_event('E_CALL_SYNC_METHOD', 'confirm_agent', (self.unit_obj.id, True), True)
            return

    def on_try_agent_action(self, evt, args):
        if self.ev_g_death():
            return
        if not self.sd.ref_is_agent:
            scene = global_data.game_mgr.get_cur_scene()
            if not scene:
                return
            c_pos = self.ev_g_position()
            if not c_pos:
                return
            self._agent_pos = c_pos
            if scene.check_landscape_has_load_detail_collision(c_pos):
                self.begin_agent()
            else:
                self._need_become_agent = True
                self.need_update = True
                return
        self.send_event(evt, *args)

    def on_cancel_agent(self):
        self.sd.ref_is_agent = False

    def get_is_agent(self):
        return self.sd.ref_is_agent

    def tick(self, dt):
        if not self._need_become_agent or not self._agent_pos:
            return
        else:
            if time.time() - self._last_check_time < 0.1:
                return
            self._last_check_time = time.time()
            scene = global_data.game_mgr.get_cur_scene()
            if scene and scene.check_collision_loaded(self._agent_pos, need_refresh=False):
                logic = global_data.player.logic if global_data.player else None
                if logic:
                    logic.send_event('E_CALL_SYNC_METHOD', 'confirm_agent', (self.unit_obj.id, True), True)
                    self.begin_agent()
                self._need_become_agent = False
                self.need_update = False
            return