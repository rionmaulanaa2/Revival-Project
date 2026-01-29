# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAIAgent.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils import get_on_mecha_utils
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d

class ComAIAgent(UnitCom):
    BIND_EVENT = {'E_TRY_AGENT': 'on_try_agent',
       'E_FORCE_AGENT': 'begin_agent',
       'E_TRY_AGENT_ACTION': 'on_try_agent_action',
       'E_CANCEL_AGENT': 'on_cancel_agent',
       'E_ABORT_AGENT': 'on_abort_agent',
       'G_IS_AGENT': 'get_is_agent'
       }

    def __init__(self):
        super(ComAIAgent, self).__init__()
        self.sd.ref_is_agent = False
        self.sd.ref_is_robot = True

    def init_from_dict(self, unit_obj, bdict):
        super(ComAIAgent, self).init_from_dict(unit_obj, bdict)
        self._bdict = bdict
        self.setup_component('AI_Receiver')
        global_data.emgr.app_background_event += self.on_cancel_agent

    def destroy(self):
        global_data.emgr.app_background_event -= self.on_cancel_agent
        super(ComAIAgent, self).destroy()

    def begin_agent(self):
        if self.sd.ref_is_agent:
            return
        self.sd.ref_is_agent = True
        self.del_component('AI_Receiver')
        self.setup_component('AI_Agent')
        self.send_event('E_ENABLE_SYNC', True)
        self.send_event('E_ENABLE_MOVE_SYNC_SENDER', True)
        self.send_event('E_ACTIVE_DRIVER')
        self.send_event('E_CLEAR_BEHAVIOR')
        self.send_event('E_ENABLE_BEHAVIOR', True)
        self.send_event('E_SET_TICK_INVERVAL', 0.1)
        self.send_event('E_BEGIN_AGENT_AI')

    def on_try_agent(self, pos):
        if self.ev_g_agony() or self.ev_g_death():
            return
        else:
            model = self.ev_g_model()
            if not model:
                return
            if self.sd.ref_is_agent or global_data.player:
                logic = global_data.player.logic if 1 else None
                if logic is None:
                    return
                self.begin_agent()
                logic.send_event('E_CALL_SYNC_METHOD', 'confirm_ai_agent', (self.unit_obj.id,), True)
            return

    def on_try_agent_action(self, evt, args):
        if self.ev_g_agony() or self.ev_g_death():
            return
        model = self.ev_g_model()
        if not model or not model.visible:
            return
        if not self.sd.ref_is_agent:
            self.begin_agent()
        self.send_event(evt, *args)

    def on_cancel_agent(self):
        self.sd.ref_is_agent = False
        self.del_component('AI_Agent')
        self.setup_component('AI_Receiver')
        self.send_event('E_ENABLE_SYNC', False)
        self.send_event('E_ENABLE_MOVE_SYNC_SENDER', False)
        self.send_event('E_DISABLE_BEHAVIOR')
        self.send_event('E_END_AGENT_AI')

    def get_is_agent(self):
        return self.sd.ref_is_agent

    def setup_component(self, com_type):
        obj = self.unit_obj
        com_list = get_on_mecha_utils.get_mecha_component(com_type, True)
        self._install_com(obj, com_list)

    def del_component(self, com_type):
        obj = self.unit_obj
        com_list = get_on_mecha_utils.get_mecha_component(com_type)
        self._uninstall_com(obj, com_list)

    def _install_com(self, owner, com_list):
        complete_list = []
        bdict = self._bdict.copy()
        cur_pos = self.ev_g_position()
        if cur_pos:
            bdict['position'] = (
             cur_pos.x, cur_pos.y, cur_pos.z)
        for com_info in com_list:
            com_name = com_info['component']
            cpath = 'client'
            if com_name.find('.') > 0:
                com_prefix, com_name = com_name.rsplit('.', 1)
                cpath = 'client.{}'.format(com_prefix)
            com = owner.get_com(com_name)
            if not com:
                getter = com_info.get('bdict_getter', None)
                bdict.update(getter(owner) if getter else {})
                com = owner.add_com(com_name, cpath)
                com.init_from_dict(owner, bdict)
                init_func = com_info.get('init_func', None)
                if init_func:
                    init_func(owner, com)
                complete_list.append(com)

        for com in complete_list:
            com.on_init_complete()

        return

    def _uninstall_com(self, owner, com_list):
        for com_info in com_list:
            com_name = com_info['component']
            if com_name.find('.') > 0:
                _, com_name = com_name.rsplit('.', 1)
            owner.del_com(com_name)