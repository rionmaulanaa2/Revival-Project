# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPVEShopCore.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const.pve_const import PVE_SHOP_STATE_CLOSED, PVE_SHOP_STATE_OPENED

class ComPVEShopCore(UnitCom):
    BIND_EVENT = {'E_COL_LOADED': 'on_col_loaded',
       'E_SET_SHOP_STATE': 'set_shop_state',
       'G_SHOP_STATE': 'get_shop_state',
       'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone',
       'G_POSITION': '_get_pos',
       'E_TRY_OPEN_PVE_SHOP': 'on_try_open'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComPVEShopCore, self).init_from_dict(unit_obj, bdict)
        self._pos = None
        self.shop_state_dict = bdict.get('shop_state_dict', {})
        self.process_events(True)
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_lplayer_setted
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def on_cam_lplayer_setted(self):
        self.set_shop_state(self.shop_state_dict)

    def on_col_loaded(self, pos):
        self._pos = pos
        if not global_data.cam_lplayer:
            return
        self.set_shop_state(self.shop_state_dict)

    def set_shop_state(self, state_dict):
        if not global_data.cam_lplayer:
            return
        self.shop_state_dict = state_dict
        state = self.shop_state_dict.get(global_data.cam_lplayer.id, PVE_SHOP_STATE_CLOSED)
        if state == PVE_SHOP_STATE_CLOSED:
            self.on_closed()
        elif state == PVE_SHOP_STATE_OPENED:
            self.on_opened()

    def on_closed(self):
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        global_data.emgr.pve_shop_closed_event.emit(self.unit_obj)
        self.send_event('E_ON_PVE_SHOP_CLOSED')

    def on_opened(self):
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        global_data.emgr.pve_shop_opened_event.emit(self.unit_obj, show_tip=True)
        self.send_event('E_ON_PVE_SHOP_OPENED')

    def _check_enter_zone(self, pos):
        if self._pos:
            start = self._pos
            radius = (pos - start).length
            if radius < 12.0 * NEOX_UNIT_SCALE:
                return (True, radius)
        return (
         False, None)

    def _get_pos(self):
        return self._pos

    def get_shop_state(self):
        if not global_data.cam_lplayer:
            return PVE_SHOP_STATE_CLOSED
        return self.shop_state_dict.get(global_data.cam_lplayer.id, PVE_SHOP_STATE_CLOSED)

    def on_try_open(self):
        self.send_event('E_CALL_SYNC_METHOD', 'open_pve_shop', (global_data.cam_lplayer.id,), True, True)

    def destroy(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        global_data.emgr.pve_shop_closed_event.emit(self.unit_obj)
        super(ComPVEShopCore, self).destroy()