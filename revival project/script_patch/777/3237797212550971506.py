# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComObserveNonHumanControlTargetGSender.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from .ComObserverGlobalSenderBase import ComObserverGlobalSenderBase
from logic.gcommon import const
import world
import logic.gcommon.common_const.animation_const as animation_const
from logic.gcommon.common_utils.parachute_utils import STAGE_FREE_DROP, STAGE_PARACHUTE_DROP, STAGE_LAND

class ComObserveNonHumanControlTargetGSender(ComObserverGlobalSenderBase):
    BIND_EVENT = {}
    DIRECT_FORWARDING_EVENT = {'E_SYNC_CAM_YAW_NORMAL': 'sync_cam_yaw_with_role',
       'E_SYNC_CAM_PITCH_NORMAL': 'sync_cam_pitch_with_role',
       'E_SHOW_MAIN_BATTLE_MESSAGE': 'show_battle_main_message',
       'E_SHOW_BATTLE_MESSAGE_EVENT': 'battle_show_message_event',
       'E_SHOW_MED_R_BATTLE_MESSAGE': 'show_battle_med_r_message',
       'E_ON_HIT': 'on_be_hit_event',
       'E_FIRE': 'on_non_human_observer_fire_event'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComObserveNonHumanControlTargetGSender, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComObserveNonHumanControlTargetGSender, self).destroy()