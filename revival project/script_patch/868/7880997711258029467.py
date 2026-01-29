# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_granbelm/ComGranbelmPortalCore.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import collision
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComGranbelmPortalCore(UnitCom):
    BIND_EVENT = {'E_PORTAL_COL_LOADED': '_on_col_loaded'
       }
    PORTAL_STATE_NONE = 1
    PORTAL_STATE_FALSE = 2
    PORTAL_STATE_TRUE = 3
    DIST = 4 * NEOX_UNIT_SCALE

    def __init__(self):
        super(ComGranbelmPortalCore, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComGranbelmPortalCore, self).init_from_dict(unit_obj, bdict)
        self.listen_target = None
        self.portal_dict = {}
        self.player = global_data.player.logic
        self._is_teleport_ui_show = False
        self._col = None
        return

    def _on_col_loaded(self, col, size):
        self._col = col
        self._pos = col.position
        self._detect_dis = size[0] * NEOX_UNIT_SCALE + 3
        self._process_event(True)

    def _process_event(self, is_bind):
        target = self.player
        if target.ev_g_is_in_spectate() or target.ev_g_death():
            return
        else:
            if is_bind:
                target.regist_event('E_ON_JOIN_MECHA', self.on_ctrl_target_changed, 10)
                target.regist_event('E_ON_LEAVE_MECHA', self.on_ctrl_target_changed, 10)
                target.regist_event('E_ON_JOIN_MECHA_START', self.on_ctrl_target_changed, 10)
                target.regist_event('E_ON_LEAVE_MECHA_START', self.on_ctrl_target_changed, 10)
                ctrl_target = target.ev_g_control_target()
                if ctrl_target and ctrl_target.logic:
                    if G_POS_CHANGE_MGR:
                        ctrl_target.logic.regist_pos_change(self.detect_player, 0.1)
                    else:
                        ctrl_target.logic.regist_event('E_POSITION', self.detect_player)
                    ctrl_target.logic.regist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
                    self.listen_target = ctrl_target.logic
            elif target and target.is_valid():
                target.unregist_event('E_ON_JOIN_MECHA', self.on_ctrl_target_changed)
                target.unregist_event('E_ON_LEAVE_MECHA', self.on_ctrl_target_changed)
                target.unregist_event('E_ON_JOIN_MECHA_START', self.on_ctrl_target_changed)
                target.unregist_event('E_ON_LEAVE_MECHA_START', self.on_ctrl_target_changed)
                if self.listen_target and self.listen_target.is_valid():
                    if G_POS_CHANGE_MGR:
                        self.listen_target.unregist_pos_change(self.detect_player)
                    else:
                        self.listen_target.unregist_event('E_POSITION', self.detect_player)
                    self.listen_target.unregist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
                    self.listen_target = None
            return

    def on_ctrl_target_changed(self, *args):
        ctrl_target = self.player.ev_g_control_target()
        if not ctrl_target or not ctrl_target.logic:
            return
        if self.listen_target and self.listen_target != ctrl_target.logic:
            if G_POS_CHANGE_MGR:
                self.listen_target.unregist_pos_change(self.detect_player)
                ctrl_target.logic.regist_pos_change(self.detect_player, 0.1)
            else:
                self.listen_target.unregist_event('E_POSITION', self.detect_player)
                ctrl_target.logic.regist_event('E_POSITION', self.detect_player)
            self.listen_target.unregist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
            ctrl_target.logic.regist_event('E_ON_TOUCH_GROUND', self.on_touch_ground)
            self.listen_target = ctrl_target.logic

    def detect_player(self, pos):
        detect_result = self.detect_player_pos(pos)
        if detect_result == self.PORTAL_STATE_NONE:
            self.check_hide_teleport_ui()
        elif detect_result == self.PORTAL_STATE_FALSE:
            self.hide_teleport_ui()
        else:
            self.show_teleport_ui()

    def detect_player_pos(self, pos):
        if pos is None:
            return self.PORTAL_STATE_NONE
        else:
            dist = self._pos - pos
            if dist.length > self._detect_dis:
                return self.PORTAL_STATE_NONE
            start = self._pos
            end = math3d.vector(start)
            end.y += 4 * NEOX_UNIT_SCALE
            interact_list = self.scene.scene_col.sweep_intersect(self._col, start, end, -1, -1, collision.INCLUDE_FILTER)
            if not interact_list:
                return self.PORTAL_STATE_FALSE
            target = self.player.ev_g_control_target()
            if not target or not target.logic:
                return self.PORTAL_STATE_FALSE
            col_id = target.logic.ev_g_human_col_id()
            for col_obj in interact_list:
                if col_obj.cid in col_id:
                    return self.PORTAL_STATE_TRUE

            return self.PORTAL_STATE_FALSE

    def on_touch_ground(self, *args):

        def delay_detect():
            if self and self.is_valid():
                if self.listen_target:
                    pos = self.listen_target.ev_g_position()
                    self.detect_player(pos)

        global_data.game_mgr.delay_exec(0.1, delay_detect)

    def show_teleport_ui(self):
        if global_data.gran_sur_battle_mgr.get_tele_tag():
            return
        if self.player == global_data.cam_lplayer:
            eid = self.unit_obj.id
            self.portal_dict = {'eid': eid
               }
            global_data.emgr.update_portal_dict.emit(self.portal_dict)
            dist = self.DIST
            self.player.send_event('E_ENTER_GRANBELM_PORTAL_ZONE', dist)
            self._is_teleport_ui_show = True

    def hide_teleport_ui(self):
        if self.player == global_data.cam_lplayer:
            self.player.send_event('E_LEAVE_GRANBELM_PORTAL_ZONE')
            self._is_teleport_ui_show = False

    def check_hide_teleport_ui(self):
        if self._is_teleport_ui_show:
            self.hide_teleport_ui()

    def destroy(self):
        self._process_event(False)
        if self._col:
            self.scene.scene_col.remove_object(self._col)
            self._col = None
        self.portal_dict = {}
        self.check_hide_teleport_ui()
        super(ComGranbelmPortalCore, self).destroy()
        return