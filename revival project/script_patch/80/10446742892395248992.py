# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_portal/ComSimplePortalCore.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import collision
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComSimplePortalCore(UnitCom):
    BIND_EVENT = {'E_SIMPLE_PORTAL_COL_LOADED': '_on_col_loaded',
       'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone',
       'G_POSITION': '_get_pos'
       }
    DIST = 4 * NEOX_UNIT_SCALE

    def __init__(self):
        super(ComSimplePortalCore, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComSimplePortalCore, self).init_from_dict(unit_obj, bdict)

    def _on_col_loaded(self, pos, size):
        self._pos = pos
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        if global_data.game_mode.is_pve():
            global_data.sound_mgr.post_event_2d_non_opt('Play_ui_pve_pass', None)
        return

    def _get_pos(self):
        return self._pos

    def destroy(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        super(ComSimplePortalCore, self).destroy()

    def _check_enter_zone(self, pos):
        from logic.gcommon.common_const import battle_const
        if self._pos:
            start = self._pos
            radius = (pos - start).length
            if radius < battle_const.TRANSFER_PORTAL_MIN_DISTANCE_CHECK:
                return (True, radius)
        return (
         False, None)