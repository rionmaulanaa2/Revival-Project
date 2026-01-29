# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPuppetSpectated.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager

class ComPuppetSpectated(UnitCom):
    BIND_EVENT = {'E_SPECTATOR_NUM': '_set_spectator_num',
       'G_SPECTATOR_NUM': '_get_spectator_num'
       }

    def __init__(self):
        super(ComPuppetSpectated, self).__init__()
        self._spectator_num = 0

    def init_from_dict(self, unit_obj, bdict):
        super(ComPuppetSpectated, self).init_from_dict(unit_obj, bdict)
        self._spectator_num = bdict.get('spectator_num', 0)

    def _set_spectator_num(self, num):
        self._spectator_num = num

    def _get_spectator_num(self):
        return self._spectator_num