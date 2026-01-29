# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_global_sync/ComObserveMechaControlTargetGSender.py
from __future__ import absolute_import
from .ComObserverGlobalSenderBase import ComObserverGlobalSenderBase

class ComObserveMechaControlTargetGSender(ComObserverGlobalSenderBase):
    BIND_EVENT = {}
    DIRECT_FORWARDING_EVENT = {'E_GLOBAL_MECHA_BUFF_ADD': 'battle_add_mecha_buff',
       'E_GLOBAL_MECHA_BUFF_DEL': 'battle_remove_mecha_buff',
       'E_RELOADING': 'on_reload_bullet_event',
       'E_MECHA_BATTLE_MESSAGE': 'show_battle_main_message',
       'E_TRY_SWITCH_TO_CAMERA_STATE': 'switch_target_to_camera_state_event',
       'E_TRY_REPLACE_LAST_CAMERA_STATE': 'replace_last_camera_state_event',
       'E_SET_CAMERA_FOLLOW_SPEED': 'camera_target_follow_speed_event',
       'E_PATTERN_HANDLE': 'mecha_trans_pattern_handle_event'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComObserveMechaControlTargetGSender, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        super(ComObserveMechaControlTargetGSender, self).destroy()