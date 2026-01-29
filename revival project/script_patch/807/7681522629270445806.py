# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEMonsterEventDock.py
from __future__ import absolute_import
from __future__ import print_function
from ..UnitCom import UnitCom
from logic.gcommon.cdata.pve_monster_status_config import desc_2_num

class ComPVEMonsterEventDock(UnitCom):
    BIND_EVENT = {'E_PVE_MONSTER_STATE': 'distribute_state',
       'E_PVE_MONSTER_PARAM_STATE': 'dist_param_state'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEMonsterEventDock, self).init_from_dict(unit_obj, bdict)

    def distribute_state(self, state):
        if global_data.debug_pve_state:
            print('cbp===> PVE Monster Try Active State -', state)
            global_data.game_mgr.show_tip(str(state) + ', cur states: ' + str(self.ev_g_cur_state()))
        if isinstance(state, str):
            state = desc_2_num[state]
        self.send_event('E_ACTIVE_STATE', state)

    def dist_param_state(self, state, *args):
        if global_data.debug_pve_state:
            print('cbp===> PVE Monster Try Active State -%s with params-%s' % (state, args))
            global_data.game_mgr.show_tip(str(state) + ', cur states: ' + str(self.ev_g_cur_state()))
        if isinstance(state, str):
            state = desc_2_num[state]
        self.send_event('E_ACTIVE_PARAM_STATE', state, *args)

    def destroy(self):
        super(ComPVEMonsterEventDock, self).destroy()