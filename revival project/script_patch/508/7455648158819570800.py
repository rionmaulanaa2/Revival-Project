# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_king/ComKingZoneChecker.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import math3d
from logic.client.const import game_mode_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode

class ComKingZoneChecker(UnitCom):
    BIND_EVENT = {'G_IS_IN_OWN_CAMP': '_get_is_in_own_camp',
       'G_CUR_IN_OCCUPY_ZONE_LIST': 'g_cur_in_occupy_zone_list'
       }

    def __init__(self):
        super(ComKingZoneChecker, self).__init__()
        self._tick_timer = None
        self._is_in_camp = False
        self._cur_in_occupy_zone_list = []
        return

    def on_post_init_complete(self, bdict):
        self.enable_check()

    def destroy(self):
        global_data.game_mgr.unregister_logic_timer(self._tick_timer)
        self._tick_timer = None
        super(ComKingZoneChecker, self).destroy()
        return

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def enable_check(self):
        self.start_tick()

    def start_tick(self):
        from common.utils.timer import CLOCK
        if not self._tick_timer:
            self._tick_timer = global_data.game_mgr.register_logic_timer(self.custom_tick, interval=1, mode=CLOCK)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_KING,))
    def custom_tick(self, *args):
        self.in_camp_tick()
        self.in_occupy_tick()

    def in_camp_tick(self):
        ctarget = self.ev_g_control_target()
        lctarget = ctarget.logic if ctarget else None
        if lctarget:
            pos = lctarget.ev_g_position()
            camp_id = lctarget.ev_g_camp_id()
            if global_data.king_battle_data:
                if global_data.king_battle_data.is_in_camp(pos, camp_id):
                    self.on_enter_camp()
                    return
        self.on_leave_camp()
        return

    def on_enter_camp(self):
        if not self._is_in_camp:
            self._is_in_camp = True
            self.send_event('E_ENTER_KING_CAMP')

    def on_leave_camp(self):
        if self._is_in_camp:
            self._is_in_camp = False
            self.send_event('E_LEAVE_KING_CAMP')

    def _get_is_in_own_camp(self):
        return self._is_in_camp

    def in_occupy_tick(self):
        pos = None
        ctarget = self.ev_g_control_target()
        if ctarget:
            lctarget = ctarget.logic if 1 else None
            if lctarget:
                pos = lctarget.ev_g_position()
            if global_data.game_mode and global_data.game_mode.mode and global_data.game_mode.mode.grid_mgr:
                occupy_zone_list = global_data.game_mode.mode.grid_mgr.get_inside_occupy_zone(pos)
                self.check_enter_zone(self._cur_in_occupy_zone_list, occupy_zone_list)
                self._cur_in_occupy_zone_list = occupy_zone_list
        return

    def check_enter_zone(self, old_occupy_zone, cur_in_occupy_zone_list):
        for occupy_id in cur_in_occupy_zone_list:
            if occupy_id not in old_occupy_zone:
                from logic.gcommon.common_utils.local_text import get_text_by_id
                occupy_cfg = global_data.game_mode.get_cfg_data('king_occupy_data')
                show_text_id = occupy_cfg.get(str(occupy_id), {}).get('show_text_id', '')
                self.send_event('E_SHOW_MESSAGE', get_text_by_id(8102, {'zone_name': get_text_by_id(show_text_id)}))

    def g_cur_in_occupy_zone_list(self):
        return self._cur_in_occupy_zone_list