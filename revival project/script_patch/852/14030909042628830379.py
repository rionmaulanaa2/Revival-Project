# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComModeMgr.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.client.const import game_mode_const
MODE_COMS = {'LAvatar': {game_mode_const.GAME_MODE_GULAG_SURVIVAL: ('ComGulag', )
               },
   'LPuppet': {game_mode_const.GAME_MODE_FFA: ('ComReadyBox', ),
               game_mode_const.GAME_MODE_IMPROVISE: ('ComReadyBox', ),
               game_mode_const.GAME_MODE_GULAG_SURVIVAL: ('ComGulag', )
               },
   'LMecha': {game_mode_const.GAME_MODE_GVG: ('ComReadyBox', ),
              game_mode_const.GAME_MODE_ZOMBIE_FFA: ('ComReadyBox', ),
              game_mode_const.GAME_MODE_DUEL: ('ComReadyBox', )
              }
   }

class ComModeMgr(UnitCom):
    BIND_EVENT = {}

    def __init__(self):
        super(ComModeMgr, self).__init__()
        self.init_parameters()

    def init_from_dict(self, unit_obj, bdict):
        super(ComModeMgr, self).init_from_dict(unit_obj, bdict)
        self.init_coms()
        for com in self.mode_coms:
            com.init_from_dict(unit_obj, bdict)

    def init_parameters(self):
        self.mode_coms = []

    def init_coms(self):
        if not self.unit_obj:
            return
        cl_name = self.unit_obj.__class__.__name__
        coms_name = MODE_COMS.get(cl_name, {}).get(global_data.game_mode.get_mode_type(), ())
        for name in coms_name:
            com = self.unit_obj.add_com(name, 'client.com_mode')
            self.mode_coms.append(com)

    def destroy(self):
        self.mode_coms = []
        super(ComModeMgr, self).destroy()