# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAIAgentHuman.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d

class ComAIAgentHuman(UnitCom):
    BIND_EVENT = {'E_TRY_AGENT': 'on_try_agent',
       'E_FORCE_AGENT': 'begin_agent',
       'E_TRY_AGENT_ACTION': 'on_try_agent_action',
       'E_CANCEL_AGENT': 'on_cancel_agent',
       'E_ABORT_AGENT': 'on_abort_agent',
       'G_IS_AGENT': 'get_is_agent'
       }

    def __init__(self):
        super(ComAIAgentHuman, self).__init__()
        self.sd.ref_is_agent = False
        self.sd.ref_is_robot = True

    def init_from_dict(self, unit_obj, bdict):
        super(ComAIAgentHuman, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        global_data.emgr.scene_add_agent_robot.emit(self.unit_obj.id)
        super(ComAIAgentHuman, self).destroy()

    def begin_agent(self):
        if self.sd.ref_is_agent:
            return
        else:
            self.sd.ref_is_agent = True
            self.send_event('E_SET_CONTROL_TARGET', None, {'is_agent': 1})
            self.send_event('E_ENABLE_SYNC', True)
            self.send_event('E_SET_STATUS_CHECK_ENABLE', True)
            self.send_event('E_ENABLE_BEHAVIOR', True)
            self.send_event('E_SET_TICK_INVERVAL', 0.1)
            self.send_event('E_BEGIN_AGENT_AI')
            global_data.emgr.scene_add_agent_robot.emit(self.unit_obj.id)
            return

    def on_try_agent(self, pos):
        if self.ev_g_death():
            return
        else:
            model = self.ev_g_model()
            if not model:
                return
            mecha = self.ev_g_ctrl_mecha_obj()
            if mecha:
                return
            if self.sd.ref_is_agent or global_data.player:
                logic = global_data.player.logic if 1 else None
                if logic is None:
                    return
                self.begin_agent()
                logic.send_event('E_CALL_SYNC_METHOD', 'confirm_ai_agent', (self.unit_obj.id,), True)
            return

    def on_try_agent_action(self, evt, args):
        if self.ev_g_death():
            return
        model = self.ev_g_model()
        if not model or not model.visible:
            return
        if not self.sd.ref_is_agent:
            self.begin_agent()
        self.send_event(evt, *args)

    def _on_become_agent(self):
        if self.sd.ref_parachute_stage == parachute_utils.STAGE_PARACHUTE_DROP:
            self.send_event('E_ENABLE_PARACHUTE_COM', True)

    def on_cancel_agent(self):
        self.sd.ref_is_agent = False
        self.send_event('E_ENABLE_SYNC', False)
        self.send_event('E_SET_STATUS_CHECK_ENABLE', False)
        if not self.ev_g_in_mecha():
            self.send_event('E_SET_CONTROL_TARGET', None, {'is_agent': 0})
            self.send_event('E_DISABLE_BEHAVIOR')
        self.send_event('E_END_AGENT_AI')
        global_data.emgr.scene_add_agent_robot.emit(self.unit_obj.id)
        return

    def get_is_agent(self):
        return self.sd.ref_is_agent