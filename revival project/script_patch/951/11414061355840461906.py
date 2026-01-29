# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComLobbyPlayerSender.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon import const
from common.framework import Functor
from .ComObserverGlobalSenderBase import ComObserverGlobalSenderBase
import math3d
import world
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAND, STAGE_PLANE

class ComLobbyPlayerSender(ComObserverGlobalSenderBase):
    DIRECT_FORWARDING_EVENT = {'E_POSITION': 'on_lobby_player_position_changed'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComLobbyPlayerSender, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComLobbyPlayerSender, self).destroy()