# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8028.py
from __future__ import absolute_import
from six.moves import range
from .ComGenericMechaEffect import ComGenericMechaEffect
import logic.gcommon.common_utils.bcast_utils as bcast
FAIRY_ACCUMULATE_STATE_ID = {}
FAIRY_ACCUMULATE_STATE_EFFECT_MAP = {}
for i in range(6):
    FAIRY_ACCUMULATE_STATE_ID[i] = 'fairy_accumulate_%d' % i
    FAIRY_ACCUMULATE_STATE_EFFECT_MAP[i] = str(101 + i)

SWITCH_FAIRY_SHAPE_EFFECT_ID = '107'
SWITCH_RABBIT_SHAPE_EFFECT_ID = '100'
FAIRY_SCREEN_STATE_ID = 'fairy_screen'
FAIRY_SCREEN_EFFECT_ID = '108'
RABBIT_DASH_STATE_ID = 'rabbit_dash'
RABBIT_DASH_EFFECT_ID = '109'
RABBIT_DASH_MOVE_STATE_ID = 'rabbit_dash_move'
RABBIT_DASH_MOVE_EFFECT_ID = '110'
RABBIT_DASH_SCREEN_STATE_ID = 'rabbit_dash_screen'
RABBIT_DASH_SCREEN_EFFECT_ID = '111'

class ComMechaEffect8028(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_PLAY_FAIRY_ACCUMULATE_EFFECT': 'play_fairy_accumulate_effect',
       'E_STOP_FAIRY_ACCUMULATE_EFFECT': 'stop_fairy_accumulate_effect',
       'E_PLAY_SWITCH_FAIRY_SHAPE_EFFECT': 'play_switch_fairy_shape_effect',
       'E_PLAY_SWITCH_RABBIT_SHAPE_EFFECT': 'play_switch_rabbit_shape_effect',
       'E_PLAY_FAIRY_STATE_EFFECT': 'play_fairy_state_effect',
       'E_PLAY_RABBIT_DASH_STATE_EFFECT': 'play_rabbit_dash_state_effect',
       'E_PLAY_RABBIT_DASH_MOVE_EFFECT': 'play_rabbit_dash_move_effect',
       'E_PLAY_RABBIT_DASH_SCREEN_EFFECT': 'play_rabbit_dash_screen_effect'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8028, self).init_from_dict(unit_obj, bdict)
        self.switch_shape_sfx_id = None
        self.switch_shape_sfx = None
        self.update_switch_sfx_event_registered = False
        return

    def destroy(self):
        if self.update_switch_sfx_event_registered:
            if G_POS_CHANGE_MGR:
                self.unregist_pos_change(self.update_switch_sfx_pos)
            else:
                self.unregist_event('E_POSITION', self.update_switch_sfx_pos)
            self.update_switch_sfx_event_registered = True
        super(ComMechaEffect8028, self).destroy()

    def play_fairy_accumulate_effect(self, index):
        self.on_trigger_state_effect(FAIRY_ACCUMULATE_STATE_ID[index], FAIRY_ACCUMULATE_STATE_EFFECT_MAP[index], force=True, need_sync=True)

    def stop_fairy_accumulate_effect(self, index):
        self.on_trigger_state_effect(FAIRY_ACCUMULATE_STATE_ID[index], '', need_sync=True)

    def update_switch_sfx_pos(self, pos):
        self.switch_shape_sfx.position = pos

    def switch_shape_effect_create_callback(self, sfx):
        if not self.is_valid():
            return
        self.switch_shape_sfx = sfx
        sfx.position = self.ev_g_position()
        if G_POS_CHANGE_MGR:
            self.regist_pos_change(self.update_switch_sfx_pos)
        else:
            self.regist_event('E_POSITION', self.update_switch_sfx_pos)
        self.update_switch_sfx_event_registered = True

    def switch_shape_effect_remove_callback(self, sfx):
        if not self.is_valid():
            return
        else:
            self.switch_shape_sfx = None
            if G_POS_CHANGE_MGR:
                self.unregist_pos_change(self.update_switch_sfx_pos)
            else:
                self.unregist_event('E_POSITION', self.update_switch_sfx_pos)
            self.update_switch_sfx_event_registered = False
            return

    def play_switch_fairy_shape_effect(self):
        if self.switch_shape_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.switch_shape_sfx_id)
        self.switch_shape_sfx_id = self.on_trigger_hold_effect(SWITCH_FAIRY_SHAPE_EFFECT_ID, self.switch_shape_effect_create_callback, self.switch_shape_effect_remove_callback)
        if not self.switch_shape_sfx_id:
            self.switch_shape_sfx_id = None
            return
        else:
            self.switch_shape_sfx_id = self.switch_shape_sfx_id[0]
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_SWITCH_FAIRY_SHAPE_EFFECT, ()], True)
            return

    def play_switch_rabbit_shape_effect(self):
        if self.switch_shape_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.switch_shape_sfx_id)
        self.switch_shape_sfx_id = self.on_trigger_hold_effect(SWITCH_RABBIT_SHAPE_EFFECT_ID, self.switch_shape_effect_create_callback, self.switch_shape_effect_remove_callback)
        if not self.switch_shape_sfx_id:
            self.switch_shape_sfx_id = None
            return
        else:
            self.switch_shape_sfx_id = self.switch_shape_sfx_id[0]
            self.unit_obj.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_PLAY_SWITCH_RABBIT_SHAPE_EFFECT, ()], True)
            return

    def play_fairy_state_effect(self, flag):
        effect_id = FAIRY_SCREEN_EFFECT_ID if flag else ''
        self.on_trigger_state_effect(FAIRY_SCREEN_STATE_ID, effect_id, need_sync=True)

    def play_rabbit_dash_state_effect(self, flag):
        effect_id = RABBIT_DASH_EFFECT_ID if flag else ''
        self.on_trigger_state_effect(RABBIT_DASH_STATE_ID, effect_id, need_sync=True)

    def play_rabbit_dash_move_effect(self, flag):
        effect_id = RABBIT_DASH_MOVE_EFFECT_ID if flag else ''
        self.on_trigger_state_effect(RABBIT_DASH_MOVE_STATE_ID, effect_id, need_sync=True)

    def play_rabbit_dash_screen_effect(self, flag):
        effect_id = RABBIT_DASH_SCREEN_EFFECT_ID if flag else ''
        self.on_trigger_state_effect(RABBIT_DASH_SCREEN_STATE_ID, effect_id, need_sync=True)