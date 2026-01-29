# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/AimScopeAdjust/AimScopeAdjustUIWidget.py
from __future__ import absolute_import
from common.utils.time_utils import get_time
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.local_text import get_text_by_id

class AimScopeAdjustUIWidget(object):

    def on_init_panel(self, panel, parent_panel, aim_scope_id, scope_times, scope_times_floor, scope_times_ceil, btn_adjust, prog_adjust, nd_btn_turn, extras):
        self.panel = panel
        self.panel.setVisible(True)
        self.parent_panel = parent_panel
        self._drag_node = btn_adjust
        self._prog_adjust_node = prog_adjust
        self._turn_adjust_node = nd_btn_turn
        if extras is None:
            extras = {}
        self._prog_adjust_floor = extras.get('prog_adjust_floor', 0)
        self._prog_adjust_ceil = extras.get('prog_adjust_ceil', self._prog_adjust_floor)
        self._turn_adjust_floor = extras.get('turn_adjust_floor', 0)
        self._turn_adjust_ceil = extras.get('turn_adjust_ceil', self._turn_adjust_floor)
        self._aim_scope_id = aim_scope_id
        if scope_times_floor > scope_times_ceil:
            scope_times_ceil = scope_times_floor
        if scope_times > scope_times_ceil or scope_times < scope_times_floor:
            scope_times = scope_times_floor
        self._cur_scope_times = scope_times
        self._scope_times_floor = scope_times_floor
        self._scope_times_ceil = scope_times_ceil
        self._max_times_node = getattr(self.parent_panel, 'lab_adjust_1', None)
        if self._max_times_node:
            show_times = int(self._scope_times_ceil) if int(self._scope_times_ceil) == self._scope_times_ceil else self._scope_times_ceil
            self._max_times_node.SetString(get_text_by_id(81225).format(show_times))
        self._min_times_node = getattr(self.parent_panel, 'lab_adjust_2', None)
        if self._min_times_node:
            show_times = int(self._scope_times_floor) if int(self._scope_times_floor) == self._scope_times_floor else self._scope_times_floor
            self._min_times_node.SetString(get_text_by_id(81225).format(show_times))
        if self._scope_times_ceil == self._scope_times_floor:
            self._cur_percentage = 1.0
        else:
            self._cur_percentage = (float(self._cur_scope_times) - self._scope_times_floor) / (self._scope_times_ceil - self._scope_times_floor)
        self._adjust_end_time = None
        self._check_adjust_timer = None
        self._init_ui_events()
        self.process_events(True)
        self._refresh_view(False)
        return

    def on_finalize_panel(self):
        self.process_events(False)
        if self._check_adjust_timer is not None:
            global_data.game_mgr.unregister_logic_timer(self._check_adjust_timer)
            self._check_adjust_timer = None
        return

    def setVisible(self, visible):
        self.panel.setVisible(visible)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_cur_aim_scope_times_event': self._on_refresh_cur_aim_scope_times
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _can_drag(self):
        if global_data.cam_lplayer and global_data.player and global_data.player.logic:
            if global_data.cam_lplayer.id == global_data.player.logic.id:
                return True
        return False

    def _init_ui_events(self):
        self.can_drag = self._can_drag()

        @self._drag_node.unique_callback()
        def OnBegin(btn, touch):
            if self.can_drag:
                self.parent_panel.PlayAnimation('show_adjust')
            return self.can_drag

        ratio = 237.0 / 1.0
        self.percentage_ratio = ratio

        @self._drag_node.unique_callback()
        def OnDrag(btn, touch):
            delta = touch.getDelta()
            self._update_percentage(delta.y)

        @self._drag_node.unique_callback()
        def OnEnd(btn, touch):
            self._adjust_end_time = get_time()

        def adjust_checker():
            if self._adjust_end_time is not None and get_time() - self._adjust_end_time >= 3:
                self.parent_panel.StopAnimation('show_adjust')
                self.parent_panel.PlayAnimation('disappear_adjust')
                self._adjust_end_time = None
            return

        self._check_adjust_timer = global_data.game_mgr.register_logic_timer(adjust_checker, times=-1, interval=1, mode=CLOCK)

    def on_hot_key_mouse_scroll(self, delta):
        self._update_percentage(delta * 0.4)

    def _update_percentage(self, delta):
        percentage_step = delta / self.percentage_ratio
        self._cur_percentage = self._cur_percentage + percentage_step
        if self._cur_percentage > 1.0:
            self._cur_percentage = 1.0
        elif self._cur_percentage < 0.0:
            self._cur_percentage = 0.0
        self._refresh_view(True)

    def _refresh_view(self, change_logic):
        prog_val = self._prog_adjust_floor + self._cur_percentage * (self._prog_adjust_ceil - self._prog_adjust_floor)
        self._prog_adjust_node.SetPercentage(prog_val)
        rot_val = self._turn_adjust_floor + self._cur_percentage * (self._turn_adjust_ceil - self._turn_adjust_floor)
        self._turn_adjust_node.setRotation(rot_val)
        if change_logic:
            val = self._scope_times_floor + self._cur_percentage * (self._scope_times_ceil - self._scope_times_floor)
            self._set_scope_times(val)

    def _set_scope_times(self, scope_times, scope_id=None):
        global_data.emgr.switch_aim_magnification_event.emit(scope_times)

    def _on_refresh_cur_aim_scope_times(self, aim_scope_id, times):
        if self._aim_scope_id != aim_scope_id:
            return
        if self._can_drag():
            return
        self._cur_scope_times = times
        if self._scope_times_ceil == self._scope_times_floor:
            self._cur_percentage = 1.0
        else:
            self._cur_percentage = (float(self._cur_scope_times) - self._scope_times_floor) / (self._scope_times_ceil - self._scope_times_floor)
        self._refresh_view(False)