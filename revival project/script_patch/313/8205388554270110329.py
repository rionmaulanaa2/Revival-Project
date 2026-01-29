# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComUseable.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.battle_const import MARK_REPAIR, MARK_BULLET, MARK_FOOD
from logic.gcommon.common_utils.local_text import get_text_by_id
import math3d

class ComUseable(UnitCom):
    BIND_EVENT = {'E_COLLSION_LOADED': '_on_col_loaded',
       'E_BUILDING_DONE': '_on_build_done',
       'E_UPDATE_USED_PLAYER': '_on_update_used_player',
       'G_CHECK_ENTER_CONSOLOE_ZONE': '_on_check_enter_zone',
       'G_CAN_USE': '_on_get_useable'
       }

    def __init__(self):
        super(ComUseable, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComUseable, self).init_from_dict(unit_obj, bdict)
        self._info = bdict
        self._building_no = bdict.get('building_no', 6011)
        self._used_list = self._info.get('used_players', {})
        from common.cfg import confmgr
        building_conf = confmgr.get('c_building_res', str(self._building_no))
        self._mark_type = building_conf['ExtInfo']['mapmark']
        self._tips = building_conf['ExtInfo']['usetips']

    def destroy(self):
        self._info = None
        self.disable_functional()
        super(ComUseable, self).destroy()
        return

    def _on_col_loaded(self, m, col):
        self._pos = m.position
        self._trigger_size = math3d.vector(m.bounding_box)
        self._trigger_size *= 2.8
        status = self._info.get('status', None)
        from logic.gcommon.common_const import building_const
        if status and status == building_const.BUILDIND_ST_DONE:
            self.enable_functional()
        return

    def _on_build_done(self):
        self.enable_functional()

    def _on_update_used_player(self, player_list):
        self._used_list = player_list
        target = global_data.player.logic
        if target and target.is_valid():
            pos = target.ev_g_position()
            if G_POS_CHANGE_MGR:
                target.notify_pos_change(pos)
            else:
                target.send_event('E_POSITION', pos)
            from common.cfg import confmgr
            building_conf = confmgr.get('c_building_res', str(self._building_no))
            capsule_conf = confmgr.get('c_capsule_info', str(building_conf['CapsuleId']))
            global_data.emgr.capsule_show_msg.emit(capsule_conf['CapId'], get_text_by_id(self._tips))

    def enable_functional(self):
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())

    def disable_functional(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        if not global_data.player:
            return

    def _on_check_enter_zone(self, pos):
        lpos = pos - self._pos
        size = self._trigger_size
        if size.z > lpos.z > -size.z and size.y > abs(lpos.y):
            if size.x > lpos.x > -size.x:
                return (True, lpos.length)
        return (
         False, None)

    def _on_get_useable(self):
        return global_data.player.id not in self._used_list