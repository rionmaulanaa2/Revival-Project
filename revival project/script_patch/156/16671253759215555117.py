# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/mouse/MouseCursorManager.py
from __future__ import absolute_import
import six
import six_ex
from common.framework import Singleton
import game3d
import game
import cc
from logic.comsys.common_ui.MouseLockerUI import MouseLockerUI

class MouseCursorManager(Singleton):
    ALIAS_NAME = 'mouse_mgr'
    GLOBAL_EVENT = {}

    def process_global_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        for event, func_name in six.iteritems(self.GLOBAL_EVENT):
            func = getattr(self, func_name)
            if func and callable(func):
                econf[event] = func

        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init(self):
        self.init_parameter()
        self.init_manager()

    def on_finalize(self):
        if self._is_registed_wheel_event:
            self._inner_unregister_wheel_event()
        self.enable_PC_control(False)
        self.process_global_event(False)
        self.unregist_callback()
        self._mouse_ctrl.disable()
        self._mouse_ctrl.uninstall()
        self._mouse_ctrl.destroy()
        self._mouse_ctrl = None
        return

    def init_parameter(self):
        self.is_win32 = game3d.get_platform() == game3d.PLATFORM_WIN32
        self._cursor_show_count_dict = {}
        self.cursor_enable = True
        self._pc_control_switch = False
        self._cursor_move_enable = False
        self._is_registed_wheel_event = False
        self._wheel_priority_queue = {}
        self._sorted_priority_list = []
        from logic.vscene.parts.mouse.BattleMouse import BattleMouse
        self._mouse_ctrl = BattleMouse()

    def get_mouse_state(self, keycode):
        if self._mouse_ctrl:
            return self._mouse_ctrl.get_key_state(keycode)
        else:
            return False

    def refresh_screen_center(self):
        sz = global_data.ui_mgr.design_screen_size
        self.screen_center = (int(sz.width / 2), int(sz.height / 2))
        self._touch_pos = cc.Vec2(int(sz.width / 2), int(sz.height / 2))

    def is_mouse_enable(self):
        return self._pc_control_switch

    def enable_PC_control(self, switch):
        if self._pc_control_switch == switch:
            return
        self._pc_control_switch = switch
        if switch:
            self.refresh_screen_center()
            if self._mouse_ctrl:
                ctrl = self._mouse_ctrl
                ctrl.install()
                ctrl.enable()
            self.apply_sys_mouse_effect(True)
            self.process_global_event(True)
        else:
            if self._mouse_ctrl:
                ctrl = self._mouse_ctrl
                ctrl.disable()
                ctrl.uninstall()
            self.apply_sys_mouse_effect(False)
            self.process_global_event(False)
            self._cursor_show_count_dict = {}
        if global_data.feature_mgr.is_support_pc_mouse_hover():
            import cc
            cc.Director.getInstance().getEventDispatcher().setMouseHoverEnabled(not switch)

    def apply_sys_mouse_effect(self, enable):
        self.cursor_enable = not enable
        import nxapp
        if nxapp.is_focused():
            self.do_apply_sys_mouse_effect(enable)

    def do_apply_sys_mouse_effect(self, enable):
        if self.is_win32:
            import nxapp
            nxapp.lock_cursor(enable)
            nxapp.show_cursor(not enable)
        elif hasattr(game3d, 'set_cursor_locked'):
            game3d.set_cursor_locked(enable)
        locker_ui = global_data.ui_mgr.get_ui('MouseLockerUI')
        if enable:
            if not locker_ui:
                global_data.ui_mgr.show_ui('MouseLockerUI', 'logic.comsys.common_ui')
            else:
                locker_ui.add_show_count('mouse_lock')
        elif locker_ui:
            locker_ui.add_hide_count('mouse_lock')
        global_data.emgr.mouse_cursor_lock_event.emit(enable)
        if self._mouse_ctrl:
            ctrl = self._mouse_ctrl
            if enable:
                ctrl.enable()
            else:
                ctrl.disable()

    def add_cursor_show_count(self, key):
        if not self._pc_control_switch:
            return
        self._cursor_show_count_dict[key] = 1
        self._check_cursor_show_count_dict()

    def add_cursor_hide_count(self, key):
        if not self._pc_control_switch:
            return
        if key in self._cursor_show_count_dict:
            if self._cursor_show_count_dict[key] >= 0:
                self._cursor_show_count_dict[key] = 0
        self._check_cursor_show_count_dict()

    def _check_cursor_show_count_dict(self):
        for key, val in six.iteritems(self._cursor_show_count_dict):
            if val >= 1:
                self.apply_sys_mouse_effect(False)
                break
        else:
            self.apply_sys_mouse_effect(True)

    def init_manager(self):
        self.regist_callback()

    def regist_callback(self):
        import nxapp
        nxapp.set_focus_callback(self.on_change_focus)
        nxapp.set_cursor_locked_mouse_move_callback(self.on_cursored_locked_mouse_move)

    def unregist_callback(self):
        import nxapp
        nxapp.set_focus_callback(None)
        nxapp.set_cursor_locked_mouse_move_callback(None)
        return

    def on_change_focus(self, is_focus):
        if is_focus:
            if self._pc_control_switch:
                self.do_apply_sys_mouse_effect(not self.cursor_enable)
            else:
                self.do_apply_sys_mouse_effect(False)
        else:
            self.do_apply_sys_mouse_effect(False)
        global_data.emgr.app_change_focus.emit(is_focus)
        self.show_states()

    MOUSE_MOVE_SENSITIVITY_RATIO = 0.5

    def on_cursored_locked_mouse_move(self, delta_x, delta_y):
        delta_x = delta_x * self.MOUSE_MOVE_SENSITIVITY_RATIO
        delta_y = delta_y * self.MOUSE_MOVE_SENSITIVITY_RATIO
        if not self._cursor_move_enable:
            global_data.emgr.touch_pixel_rotate_camera_event.emit(delta_x, -delta_y, [self._touch_pos], self._touch_pos)
        else:
            global_data.emgr.touch_pixel_rotate_other_event.emit(delta_x, -delta_y, [self._touch_pos], self._touch_pos)

    def register_mouse_callback(self, keycode, msg, callback, hot_key_func_name=None):
        if self._mouse_ctrl:
            self._mouse_ctrl.register_mouse_callback(keycode, msg, callback, hot_key_func_name)

    def unregister_mouse_callback(self, keycode, msg, callback):
        if self._mouse_ctrl:
            self._mouse_ctrl.unregister_mouse_callback(keycode, msg, callback)

    def reset_mouse_ctrl(self):
        if self._mouse_ctrl:
            self._mouse_ctrl.reset()

    def set_cursor_move_enable(self, enable):
        self._cursor_move_enable = enable
        if self.is_win32:
            import nxapp
            nxapp.lock_cursor(not enable)
        elif hasattr(game3d, 'set_cursor_locked'):
            game3d.set_cursor_locked(not enable)

    def register_wheel_event(self, priority, key, func):
        self._wheel_priority_queue.setdefault(priority, {})
        self._sorted_priority_list = sorted(six_ex.keys(self._wheel_priority_queue), reverse=True)
        if key not in self._wheel_priority_queue[priority]:
            self._wheel_priority_queue[priority].update({key: func})
        if not self._is_registed_wheel_event:
            self._inner_register_wheel_event()

    def unregister_wheel_event(self, priority, key):
        if priority in self._wheel_priority_queue:
            if key in self._wheel_priority_queue[priority]:
                del self._wheel_priority_queue[priority][key]
                self._sorted_priority_list = sorted(six_ex.keys(self._wheel_priority_queue), reverse=True)
                return
            log_error('unregister_wheel_event failed! func not found!', key)
        else:
            log_error('unregister_wheel_event failed! Priority not found!', priority)

    def _inner_register_wheel_event(self):
        self._is_registed_wheel_event = True
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.register_wheel_event(self.__class__.__name__, self.on_mouse_scroll)

    def _inner_unregister_wheel_event(self):
        self._is_registed_wheel_event = False
        touch_mgr = global_data.touch_mgr_agent
        touch_mgr.unregister_wheel_event(self.__class__.__name__)

    def on_mouse_scroll(self, msg, delta, key_state):
        has_respond = False
        for p in self._sorted_priority_list:
            key_func_dict = self._wheel_priority_queue.get(p, {})
            for func in six_ex.values(key_func_dict):
                if callable(func):
                    ret = func(msg, delta, key_state)
                    if ret:
                        has_respond = True

            if has_respond:
                break

    def show_states(self):
        import nxapp