# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaInjureClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.const as g_const
from logic.gcommon.common_const import buff_const as bconst
from ...cdata.mecha_status_config import MC_DEAD

class ComMechaInjureClient(UnitCom):
    BIND_EVENT = {'E_REDUCE_MECHA_INJURE': '_reduce_mecha_injure',
       'E_MECHA_INJURE': '_mecha_injure',
       'G_MECHA_INJURE': '_get_mecha_injure',
       'E_DEATH': '_set_death',
       'G_DEATH': '_get_death'
       }

    def __init__(self):
        super(ComMechaInjureClient, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaInjureClient, self).init_from_dict(unit_obj, bdict)
        self._arm_injure = bdict.get('arm_injure', 0)
        self._leg_injure = bdict.get('leg_injure', 0)
        self._dead = bdict.get('hp', 1000) == 0
        if self._dead:
            self._set_death()

    def get_client_dict(self):
        return {}

    def on_init_complete(self):
        pass

    def _reduce_mecha_injure(self, arm_injure, leg_injure):
        self._arm_injure -= arm_injure
        self._leg_injure -= leg_injure

    def _mecha_injure(self, part, injure):
        if part == g_const.HIT_PART_ARM:
            self._arm_injure += injure
        elif part == g_const.HIT_PART_OTHER:
            self._leg_injure += injure

    def _get_mecha_injure(self):
        return (
         self._arm_injure, self._leg_injure)

    def _get_death(self):
        return self._dead

    def _set_death(self):
        self._dead = True
        self.ev_g_status_try_trans(MC_DEAD)