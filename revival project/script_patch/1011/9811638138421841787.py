# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_ai_ctrl/ComRemoteControl.py
from __future__ import absolute_import
import math3d
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const import ai_const

class ComRemoteControl(UnitCom):
    BIND_EVENT = {'E_CTRL_RELOAD': 'reload',
       'E_CTRL_FOOT_POSITION': 'ctrl_foot_position',
       'G_ATTACK_POS': 'get_attack_pos',
       'E_HEALTH_HP_EMPTY': 'on_die'
       }
    SPECIFY_CONTROLLER_LIST = [
     8001, 8002, 8003, 8004, 8005, 8006, 8009, 8011, 8015, 8017, 8021]

    def __init__(self):
        super(ComRemoteControl, self).__init__()
        self._attack_target = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComRemoteControl, self).init_from_dict(unit_obj, bdict)
        npc_id = bdict['npc_id']
        if npc_id in self.SPECIFY_CONTROLLER_LIST:
            ctrl_name = 'ComRemoteControl%s' % npc_id
            com_obj = self.unit_obj.add_com(ctrl_name, 'client.com_ai_ctrl')
            if com_obj:
                com_obj.init_from_dict(self.unit_obj, bdict)

    def destroy(self):
        super(ComRemoteControl, self).destroy()

    def ctrl_foot_position(self, pos):
        self.send_event('E_CTRL_MOVE_STOP')
        pos = math3d.vector(*pos)
        self.send_event('E_FOOT_POSITION', pos)
        self.send_event('E_FORCE_ACTIVE')

    def reload(self, weapon_pos):
        self.send_event('E_CTRL_ACTION_STOP', ai_const.CTRL_ACTION_MAIN)
        self.send_event('E_TRY_RELOAD', weapon_pos)