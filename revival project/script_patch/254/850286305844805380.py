# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/ctrl/PCCtrlManager.py
from __future__ import absolute_import
import six_ex
import six
from common.framework import Singleton
import game3d
import game
from common.cfg import confmgr
from common.utils.timer import CLOCK
import time
import game
import logic.vscene.parts.ctrl.GamePyHook as game_hook
from logic.client.const import pc_const
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.manager_agents.manager_decorators import sync_exec
from logic.gutils.pc_utils import check_can_enable_pc_mode

class PCCtrlManager(Singleton):
    ALIAS_NAME = 'pc_ctrl_mgr'
    PRESS_NEED_TIME = 0.5
    DOUBLE_CLICK_INTERVAL = 0.3

    def _can_enable_valid(self):
        if self._support_enable_ctrl is None:
            self._support_enable_ctrl = check_can_enable_pc_mode()
        return self._support_enable_ctrl

    def init(self):
        import game3d
        self._support_enable_ctrl = None
        self.is_mumu = global_data.is_mumu
        if not self._can_enable_valid():
            err_msg = '[PCCtrlManager] should not be constructed on platforms other than win32!!!'
            log_error(err_msg)
            if global_data.is_inner_server:
                global_data.game_mgr.show_tip(err_msg)
        self._pc_control_switch = False
        self._keyboard_control_switch = False
        self.keyboardMouseOperations = None
        if not self.keyboardMouseOperations:
            from logic.vscene.parts.ctrl.KeyboardMouseOperations import KeyboardMouseOperations
            self.keyboardMouseOperations = KeyboardMouseOperations()
        self._keyboard_ctrl = None
        self._is_registered_keyboard_mouse_key = False
        self._general_key_func_maps = {}
        self._key_press_timer_dict = {}
        self._key_click_time_dict = {}
        self._on_progress_hot_key_func = set()
        self._on_progress_hot_key_func_cancel_map = {}
        self._has_down_hot_key_func = set()
        self._registed_combined_keys = {}
        self.regist_callback()
        self._init_win_width, self._init_win_height, _, _, _ = game3d.get_window_size()
        hot_key_par = confmgr.get('c_hot_key_parameter')
        self._press_func_uninterrupt_map = {}
        for k, v in six.iteritems(hot_key_par.get('press_func_uninterrupt_map', {})):
            self._press_func_uninterrupt_map[k] = set(v)

        self._pc_control_switch_enabled = True
        self._req_fullscreen_from_setting_ui = False
        self.switch_imm_switch(False)
        self._pc_hotkey_hint_display_option = pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_DEFAULT
        self._pc_hotkey_hint_switch = pc_const.PC_HOTKEY_SWITCH_DEFAULT
        self.sync_some_members_with_user_setting()
        self._hotkey_block_dict = {}
        if global_data.channel and global_data.channel.is_musdk():
            game_hook.set_hot_key_code_map({game3d.AVK_BACK: game.VK_ESCAPE})
        self.update_google_play_input_mapping()
        global_data.emgr.app_change_focus += self._on_app_change_focus
        global_data.emgr.avatar_finish_create_event_global += self._on_avatar_finish_create
        return

    def on_finalize(self):
        self.unregist_callback()
        if self.keyboardMouseOperations:
            self.keyboardMouseOperations.destroy()
            self.keyboardMouseOperations = None
        if self._keyboard_ctrl:
            self._keyboard_ctrl.destroy()
            self._keyboard_ctrl = None
        if global_data.mouse_mgr:
            global_data.mouse_mgr.finalize()
        self._is_registered_keyboard_mouse_key = False
        self._on_progress_hot_key_func_cancel_map = {}
        self._hotkey_block_dict.clear()
        global_data.emgr.app_change_focus -= self._on_app_change_focus
        global_data.emgr.avatar_finish_create_event_global -= self._on_avatar_finish_create
        return

    def _on_app_change_focus(self, is_focus):
        if not self._can_enable_valid():
            return
        if not is_focus:
            if self.is_fullscreen():
                if global_data.is_pc_mode:
                    import nxapp
                    if hasattr(nxapp, 'get_async_key_state'):
                        if not game.get_key_state(game.VK_TAB) and nxapp.get_async_key_state(game.VK_LALT) and nxapp.get_async_key_state(game.VK_TAB):
                            if hasattr(nxapp, 'minimize_window'):
                                nxapp.minimize_window()
        if not is_focus:
            game_hook.release_all_keys()
            if global_data.human_fire_keyboard_mgr:
                global_data.human_fire_keyboard_mgr.reset()

    def _on_avatar_finish_create(self):
        self.sync_some_members_with_user_setting()
        self.hot_key_conf_refresh()

    def is_pc_control_enable(self):
        return self._pc_control_switch

    def enable_keyboard_control(self, switch):
        if not self._can_enable_valid():
            return
        if switch:
            self._keyboard_control_switch = True
            self.register_keyboard_mouse_binding()
            self._keyboard_ctrl.install()
            self._keyboard_ctrl.enable()
        else:
            self._keyboard_control_switch = False
            if self._keyboard_ctrl:
                self._keyboard_ctrl.disable()
                self._keyboard_ctrl.uninstall()

    def register_keyboard_mouse_binding(self):
        if self._is_registered_keyboard_mouse_key:
            return
        if not self.keyboardMouseOperations:
            from logic.vscene.parts.ctrl.KeyboardMouseOperations import KeyboardMouseOperations
            self.keyboardMouseOperations = KeyboardMouseOperations()
        if not global_data.mouse_mgr:
            from logic.vscene.parts.mouse.MouseCursorManager import MouseCursorManager
            MouseCursorManager()
        if not self._keyboard_ctrl:
            from logic.vscene.parts.keyboard.KeyboardCtrl import KeyboardCtrl
            self._keyboard_ctrl = KeyboardCtrl()
        if not self._is_registered_keyboard_mouse_key:
            self.process_keyboard_center_binding(True)
            self._is_registered_keyboard_mouse_key = True

    def enable_PC_control(self, switch):
        if not global_data.player:
            return
        if not self._can_enable_valid():
            return
        if self._pc_control_switch == switch:
            return
        if not self._pc_control_switch_enabled:
            return
        self._pc_control_switch = switch
        global_data.is_pc_control_enable = self._pc_control_switch
        if switch:
            self.register_keyboard_mouse_binding()
            if not self._keyboard_control_switch:
                self.enable_keyboard_control(True)
            if global_data.mouse_mgr:
                global_data.mouse_mgr.enable_PC_control(switch)
            self.set_pc_hidden_ui_list_block_state(True)
            global_data.emgr.hot_key_swtich_on_event.emit()
        else:
            if global_data.mouse_mgr:
                global_data.mouse_mgr.enable_PC_control(switch)
            global_data.emgr.hot_key_swtich_off_event.emit()
            self.set_pc_hidden_ui_list_block_state(False)
        if global_data.human_fire_keyboard_mgr:
            if hasattr(global_data.human_fire_keyboard_mgr, 'stop_shot'):
                global_data.human_fire_keyboard_mgr.stop_shot()
        if not switch:
            if global_data.mecha and global_data.mecha.logic:
                mecha = global_data.mecha.logic
                mecha.send_event('E_ALL_ACTION_UP')

    def switch_imm_switch(self, enable):
        if not self._can_enable_valid():
            return
        import nxapp
        nxapp.enable_imm(enable)

    def pop_window_up(self):
        if not self._can_enable_valid():
            return
        import nxapp
        if hasattr(nxapp, 'restore_window'):
            nxapp.restore_window()
        if hasattr(nxapp, 'set_window_foreground'):
            nxapp.set_window_foreground(True)

    def is_fullscreen(self):
        if not self._can_enable_valid():
            return False
        import nxapp
        return nxapp.is_fullscreen()

    def request_fullscreen(self, is_open, req_from_setting_ui=False, persistent=False):
        ok = self.request_fullscreen_core(is_open, req_from_setting_ui=req_from_setting_ui)
        if ok:
            if persistent:
                archive_data = global_data.achi_mgr.get_general_archive_data()
                archive_data.set_field(uoc.PC_FULL_SCREEN_KEY, is_open)
        return ok

    @sync_exec
    def _do_async_request_fullscreen(self, is_open):
        import nxapp
        nxapp.request_fullscreen(is_open)

    def request_fullscreen_core(self, is_open, req_from_setting_ui=False):
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            return False
        desktop_sz_w, desktop_sz_h = game3d.get_desktop_size()
        if desktop_sz_w == self._init_win_width and desktop_sz_h == self._init_win_height:
            return False
        import nxapp
        if is_open != nxapp.is_fullscreen():
            if not is_open:
                from logic.gutils.pc_resolution_utils import read_pc_resolution_pref
                pref_res_val = read_pc_resolution_pref()
            if not is_open and pref_res_val[0] != 0 and pref_res_val[1] != 0:
                return self.request_change_resolution(pref_res_val[0], pref_res_val[1], req_from_setting_ui=req_from_setting_ui)
            else:
                self._req_fullscreen_from_setting_ui = req_from_setting_ui
                self._do_async_request_fullscreen(is_open)
                return True

        return False

    def request_change_resolution(self, w, h, req_from_setting_ui=False):
        if not self._can_enable_valid():
            return False
        width, height, depth, window_type, multisample = game3d.get_window_size()
        if width == w and height == h:
            return False
        if global_data.debug_perf_switch_global:
            w = global_data.get_debug_perf_val('resolution_width', w)
            h = global_data.get_debug_perf_val('resolution_height', h)
        is_fullscreen = self.is_fullscreen()
        flag = True
        if hasattr(game3d, 'set_window_size_force'):
            flag = game3d.set_window_size_force(w, h + 3, depth, window_type, multisample)
            flag = game3d.set_window_size_force(w, h, depth, window_type, multisample)
        else:
            flag = game3d.set_window_size(w, h, depth, window_type, multisample)
        if flag:
            if is_fullscreen:
                self._req_fullscreen_from_setting_ui = req_from_setting_ui
            else:
                self._on_resolution_changed_only(req_from_setting_ui)
            return True
        return False

    def _on_resolution_changed_only(self, req_from_setting_ui=False):
        if req_from_setting_ui:
            global_data.reshow_settings_after_reload = True
        self.on_set_window_size()
        global_data.ui_mgr.on_window_size_changed()
        global_data.emgr.resolution_changed.emit()
        global_data.emgr.resolution_changed_end.emit()

    def regist_callback(self):
        if not self._can_enable_valid():
            return
        import nxapp
        nxapp.set_fullscreen_callback(self.on_finish_fullscreen_setting)

    def unregist_callback(self):
        if not self._can_enable_valid():
            return
        else:
            import nxapp
            nxapp.set_fullscreen_callback(None)
            return

    def check_is_part_of_combined_key(self, keycode):
        for key in self._registed_combined_keys.get(keycode, []):
            if game.get_key_state(key):
                return True

        return False

    def register_cancel_func(self, hot_key_func_name, callback):
        self._on_progress_hot_key_func_cancel_map[hot_key_func_name] = callback

    def unregister_cancel_func(self, hot_key_func_name):
        if hot_key_func_name in self._on_progress_hot_key_func_cancel_map:
            del self._on_progress_hot_key_func_cancel_map[hot_key_func_name]

    def block_hotkey(self, hotkey_name, source):
        if hotkey_name is None:
            return
        else:
            if hotkey_name not in self._hotkey_block_dict:
                self._hotkey_block_dict[hotkey_name] = set()
            self._hotkey_block_dict[hotkey_name].add(source)
            return

    def unblock_hotkey(self, hotkey_name, source):
        if hotkey_name not in self._hotkey_block_dict:
            return
        if source in self._hotkey_block_dict[hotkey_name]:
            self._hotkey_block_dict[hotkey_name].remove(source)

    def is_hotkey_blocked(self, hotkey_name):
        if hotkey_name not in self._hotkey_block_dict:
            return False
        return bool(self._hotkey_block_dict[hotkey_name])

    def hotkey_block_wrapper(self, hotkey_name):

        def gen_decorator(func):

            def wrapped(*args, **kwargs):
                if self.is_hotkey_blocked(hotkey_name):
                    if global_data.is_inner_server:
                        pass
                    return False
                return func(*args, **kwargs)

            return wrapped

        return gen_decorator

    def prepare_key_callback(self, hot_key_func_name, str_msg, callback):
        hot_key, msg_func_dict = self.prepare_key_callback_core(hot_key_func_name, str_msg, callback)
        if hot_key is not None and msg_func_dict is not None:
            for msg in six_ex.keys(msg_func_dict):
                func = msg_func_dict[msg]
                msg_func_dict[msg] = self.hotkey_block_wrapper(hot_key_func_name)(func)

        return (
         hot_key, msg_func_dict)

    def prepare_key_callback_core(self, hot_key_func_name, str_msg, callback):
        from logic.gutils.hot_key_utils import is_keyboard_hot_key, hot_key_fix, is_combined_hot_key, is_hot_key_unset_raw_by_code, hot_key_func_to_hot_key, get_hot_key_extra_arg
        hot_key_raw = hot_key_func_to_hot_key(hot_key_func_name)
        if is_hot_key_unset_raw_by_code(hot_key_raw):
            return (None, None)
        else:
            hot_key = hot_key_fix(hot_key_raw)
            if isinstance(hot_key, (list, tuple)) and not hot_key:
                try:
                    import exception_hook
                    from logic.gutils.hot_key_utils import get_hotkey_binding
                    hot_key_spec = get_hotkey_binding(hot_key_func_name)
                    err_msg = 'register hotkey error, hot_key_spec: {}, hot_key_func_name: {}, hot_key_raw:{}, hot_key:{}, player:{}'.format(hot_key_spec, hot_key_func_name, hot_key_raw, hot_key, global_data.player)
                    exception_hook.post_error(err_msg)
                except:
                    pass

                return (None, None)
            is_keyboard = is_keyboard_hot_key(hot_key)
            is_combined_key = is_combined_hot_key(hot_key)
            if is_combined_key:
                last_key = hot_key[-1]
                previous_keys = hot_key[:len(hot_key) - 1]

                def check_combined_key_state(previous_keys=previous_keys):
                    for key in previous_keys:
                        if not game.get_key_state(key):
                            return False

                    return True

                combined_keys = self._registed_combined_keys.setdefault(last_key, set())
                combined_keys.update(previous_keys)
            else:
                last_key = None

                def check_combined_key_state():
                    return True

            def clear_progress_fun(trigger_name):
                if self._on_progress_hot_key_func:
                    to_be_removed = []
                    for func_name in self._on_progress_hot_key_func:
                        if trigger_name in self._press_func_uninterrupt_map.get(func_name, []):
                            continue
                        self._cancel_on_progress_callback(func_name)
                        to_be_removed.append(func_name)

                    for f in to_be_removed:
                        self._on_progress_hot_key_func.remove(f)

            def add_into_progress_func():
                if hot_key_func_name in self._on_progress_hot_key_func_cancel_map:
                    self._on_progress_hot_key_func.add(hot_key_func_name)

            def remove_from_progress_func():
                if hot_key_func_name in self._on_progress_hot_key_func:
                    self._on_progress_hot_key_func.remove(hot_key_func_name)

            if not is_keyboard and is_combined_key:
                log_error('prepare_key_callback ERROR! mouse should not be in combined key', hot_key_func_name, str_msg)
                return (
                 None, {})
            down_key_msg = game.MSG_KEY_DOWN if is_keyboard else game.MSG_MOUSE_DOWN
            up_key_msg = game.MSG_KEY_UP if is_keyboard else game.MSG_MOUSE_UP
            if str_msg == 'PRESS':

                def press_func(msg, keycode):

                    def press_callback():
                        callback(msg, keycode)

                    add_into_progress_func()
                    press_time = get_hot_key_extra_arg(hot_key_func_name, 'press_invoke_time', default=self.PRESS_NEED_TIME)
                    t_id = global_data.game_mgr.register_logic_timer(press_callback, interval=press_time, times=1, mode=CLOCK)
                    if t_id:
                        self._key_press_timer_dict[hot_key_func_name] = t_id

                def up(msg, keycode):
                    if hot_key_func_name not in self._on_progress_hot_key_func_cancel_map:
                        return
                    else:

                        def up_press_callback():
                            callback(msg, keycode)

                        t_id = self._key_press_timer_dict.get(hot_key_func_name)
                        if t_id is not None:
                            global_data.game_mgr.unregister_logic_timer(t_id)
                            self._key_press_timer_dict[hot_key_func_name] = None
                        up_press_callback()
                        remove_from_progress_func()
                        return

                return (
                 hot_key, {down_key_msg: press_func,up_key_msg: up})
            if str_msg == 'DOUBLE_CLICK':

                def double_click_func(msg, keycode):
                    cur_time = time.time()
                    last_click_time = self._key_click_time_dict.get(hot_key_func_name)
                    if last_click_time:
                        self._key_click_time_dict[hot_key_func_name] = 0
                        if cur_time - last_click_time < self.DOUBLE_CLICK_INTERVAL:
                            callback(msg, keycode)
                    self._key_click_time_dict[hot_key_func_name] = cur_time

                return (
                 hot_key, {up_key_msg: double_click_func})
            is_down = str_msg in ('DOWN', 'DOWN_UP')
            is_up = str_msg in ('UP', 'DOWN_UP')

            def down_func(msg, keycode):
                if is_combined_key:
                    if not check_combined_key_state():
                        return
                elif self.check_is_part_of_combined_key(keycode):
                    return
                clear_progress_fun(hot_key_func_name)
                add_into_progress_func()
                self._has_down_hot_key_func.add(hot_key_func_name)
                if is_down:
                    return callback(msg, keycode)

            def up_func(msg, keycode):
                if hot_key_func_name in self._has_down_hot_key_func:
                    self._has_down_hot_key_func.remove(hot_key_func_name)
                    if hot_key_func_name in self._on_progress_hot_key_func_cancel_map:
                        if hot_key_func_name not in self._on_progress_hot_key_func:
                            return
                    remove_from_progress_func()
                    if is_up:
                        return callback(msg, keycode)

            if is_combined_key:
                return (last_key, {down_key_msg: down_func,up_key_msg: up_func})
            return (
             hot_key, {down_key_msg: down_func,up_key_msg: up_func})
            return

    def _cancel_on_progress_callback(self, hot_key_func_name):
        cancel_func = self._on_progress_hot_key_func_cancel_map.get(hot_key_func_name, None)
        t_id = self._key_press_timer_dict.get(hot_key_func_name)
        if t_id is not None:
            global_data.game_mgr.unregister_logic_timer(t_id)
            self._key_press_timer_dict[hot_key_func_name] = None
        if cancel_func:
            cancel_func()
        return

    def register_keyboard_callback(self, keycode, msg, callback, hot_key_func_name=None):
        if self._keyboard_ctrl:
            self._keyboard_ctrl.register_keyboard_callback(keycode, msg, callback, hot_key_func_name)

    def unregister_keyboard_callback(self, keycode, msg, callback):
        if self._keyboard_ctrl:
            self._keyboard_ctrl.unregister_keyboard_callback(keycode, msg, callback)

    def register_key_callback(self, keycode, msg, callback, hot_key_func_name):
        from logic.gutils.hot_key_utils import is_keyboard_hot_key
        is_keyboard = is_keyboard_hot_key(keycode)
        if is_keyboard:
            self.register_keyboard_callback(keycode, msg, callback, hot_key_func_name)
        else:
            if not global_data.mouse_mgr:
                return
            register_mouse_callback = global_data.mouse_mgr.register_mouse_callback
            register_mouse_callback(keycode, msg, callback, hot_key_func_name)

    def unregister_key_callback(self, keycode, msg, callback):
        from logic.gutils.hot_key_utils import is_keyboard_hot_key
        is_keyboard = is_keyboard_hot_key(keycode)
        if is_keyboard:
            self.unregister_keyboard_callback(keycode, msg, callback)
        else:
            if not global_data.mouse_mgr:
                return
            unregister_mouse_callback = global_data.mouse_mgr.unregister_mouse_callback
            unregister_mouse_callback(keycode, msg, callback)

    def process_keyboard_center_binding(self, is_bind):
        hot_key_conf = confmgr.get('c_hot_key_config')
        for hot_key_func_name, conf in six.iteritems(hot_key_conf):
            cHotKeyImp = conf.get('cHotKeyImp')
            if cHotKeyImp not in ('ui_imp', 'custom_imp'):
                if cHotKeyImp in ('general_imp', 'general_imp_ex'):
                    self.process_general_key_binding(hot_key_func_name, conf, is_bind)
                else:
                    self.process_key_binding(hot_key_func_name, is_bind)

    def process_custom_key_binding(self, hot_key_func_name, func, is_bind):
        hot_key_conf = confmgr.get('c_hot_key_config')
        conf = hot_key_conf.get(hot_key_func_name)
        if is_bind:
            self.process_general_key_binding(hot_key_func_name, conf, is_bind, func)
        else:
            self.process_general_key_binding(hot_key_func_name, conf, False)

    def process_general_key_binding(self, hot_key_func_name, conf, is_bind=True, custom_func=None):
        str_message = conf.get('cHotkeyMessage', 'DOWN')
        if is_bind:
            _keyboardMouseOperations = self.keyboardMouseOperations
            if not custom_func:
                process_func = _keyboardMouseOperations.parse_general_imp_func(conf)

                def func(msg, keycode):
                    return process_func(keycode, msg)

            else:

                def func(msg, keycode):
                    return custom_func(msg, keycode)

            self._general_key_func_maps.setdefault(hot_key_func_name, [])
            if func:
                hot_key, msg_func_dict = self.prepare_key_callback(hot_key_func_name, str_message, func)
                if hot_key is not None and msg_func_dict is not None:
                    for msg, func in six.iteritems(msg_func_dict):
                        self.register_key_callback(hot_key, msg, func, hot_key_func_name)
                        self._general_key_func_maps[hot_key_func_name].append((hot_key, msg, func))

        else:
            msg_func_list = self._general_key_func_maps.get(hot_key_func_name)
            if not msg_func_list:
                return
        for hot_key, msg, func in msg_func_list:
            self.unregister_key_callback(hot_key, msg, func)

        if hot_key_func_name in self._general_key_func_maps:
            del self._general_key_func_maps[hot_key_func_name]
        return

    def process_key_binding(self, binding_short_name, is_bind=True):
        _keyboardMouseOperations = self.keyboardMouseOperations
        down_func = _keyboardMouseOperations.get_binding_func(binding_short_name, True)
        up_func = _keyboardMouseOperations.get_binding_func(binding_short_name, False)

        def callback(msg, keycode):
            if msg in [game.MSG_MOUSE_DOWN, game.MSG_KEY_DOWN]:
                down_func(msg, keycode)
            else:
                up_func(msg, keycode)

        hot_key, msg_func_dict = self.prepare_key_callback(binding_short_name, 'DOWN_UP', callback)
        from logic.gutils.hot_key_utils import is_keyboard_hot_key
        if hot_key is not None and msg_func_dict is not None:
            if is_bind:
                if is_keyboard_hot_key(hot_key):
                    for msg, func in six.iteritems(msg_func_dict):
                        self.register_keyboard_callback(hot_key, msg, func, binding_short_name)

                else:
                    if not global_data.mouse_mgr:
                        return
                    register_mouse_callback = global_data.mouse_mgr.register_mouse_callback
                    for msg, func in six.iteritems(msg_func_dict):
                        register_mouse_callback(hot_key, msg, func, binding_short_name)

            else:
                raise NotImplementedError('Now we do not support hot key unbinding')
        return

    def hot_key_conf_refresh(self):
        if not self._pc_control_switch_enabled:
            self.update_google_play_input_mapping()
            return
        if self._keyboard_ctrl:
            self._keyboard_ctrl.reset()
        self._general_key_func_maps = {}
        if global_data.mouse_mgr:
            global_data.mouse_mgr.reset_mouse_ctrl()
        global_data.emgr.hot_key_conf_refresh_event.emit()
        self.process_keyboard_center_binding(True)
        self.update_google_play_input_mapping()

    def update_google_play_input_mapping(self):
        if global_data.is_google_pc:
            from logic.gutils.hot_key_utils import get_google_play_pc_input_sdk_key_map
            mapping_str = get_google_play_pc_input_sdk_key_map()
            if hasattr(game3d, 'update_google_input_sdk_mapping'):
                game3d.update_google_input_sdk_mapping(mapping_str)

    def set_pc_hidden_ui_list_block_state(self, is_block):
        from common.cfg import confmgr
        hot_key_par = confmgr.get('c_hot_key_parameter')
        ui_list = hot_key_par.get('block_ui_list', [])
        if is_block:
            self.add_blocking_ui_list(ui_list)
        else:
            self.remove_blocking_ui_list(ui_list)

    def add_blocking_ui_list(self, ui_name_list):
        global_data.ui_mgr.add_blocking_ui_list(ui_name_list, self.__class__.__name__)

    def remove_blocking_ui_list(self, ui_name_list):
        global_data.ui_mgr.remove_blocking_ui_list(ui_name_list, self.__class__.__name__)

    def trigger_keyboard_event(self, key, msg=None):
        from logic.gutils.hot_key_utils import is_keyboard_hot_key
        if not is_keyboard_hot_key(key):
            log_error('try trigger_keyboard_event with a non-keyboard key!', key)
        if self._keyboard_ctrl:
            if msg:
                self._keyboard_ctrl.trigger_key_handler(key, msg)
            else:
                self._keyboard_ctrl.trigger_key_handler(key, game.MSG_KEY_DOWN)
                self._keyboard_ctrl.trigger_key_handler(key, game.MSG_KEY_UP)

    def on_ime_open(self):
        from logic.client.const import hotkey_const
        for hotkey_name in hotkey_const.HOTKEY_BLOCK_SET_WHEN_TYPEING:
            self.block_hotkey(hotkey_name, 'ime_switch')

    def on_ime_close(self):
        from logic.client.const import hotkey_const
        for hotkey_name in hotkey_const.HOTKEY_BLOCK_SET_WHEN_TYPEING:
            self.unblock_hotkey(hotkey_name, 'ime_switch')

    def on_set_window_size(self):
        w, h, _, _, _ = game3d.get_window_size()
        from common.const import common_const
        hw_new = h * 1.0 / w
        common_const.WINDOW_WIDTH = w
        common_const.WINDOW_HEIGHT = h
        global_data.really_window_ratio = 1.0 / hw_new

    def on_finish_fullscreen_setting(self, is_open):
        if self._req_fullscreen_from_setting_ui:
            global_data.reshow_settings_after_reload = True
            self._req_fullscreen_from_setting_ui = False
        self.on_set_window_size()
        global_data.ui_mgr.on_window_size_changed()
        global_data.emgr.resolution_changed.emit()
        global_data.emgr.resolution_changed_end.emit()

    def set_pc_control_switch_enabled(self, enabled):
        self._pc_control_switch_enabled = enabled

    def get_pc_control_switch_enabled(self):
        return self._pc_control_switch_enabled

    def sync_some_members_with_user_setting(self):
        if global_data.player:
            val = global_data.player.get_setting_ext_2(uoc.PC_HOTKEY_HINT_DISPLAY_OPTION_KEY, default=pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_DEFAULT)
            self.set_hotkey_hint_display_option(val, False)
            val = global_data.player.get_setting_ext_2(uoc.PC_HOTKEY_HINT_SWITCH_KEY, default=pc_const.PC_HOTKEY_SWITCH_DEFAULT)
            self.set_pc_hotkey_hint_switch(val, False)

    def set_hotkey_hint_display_option(self, option, persistent):
        old = self._pc_hotkey_hint_display_option
        self._pc_hotkey_hint_display_option = option
        if persistent:
            if global_data.player:
                global_data.player.write_setting_2(uoc.PC_HOTKEY_HINT_DISPLAY_OPTION_KEY, option, sync_to_server=False)
        if old != self._pc_hotkey_hint_display_option:
            if global_data.emgr.pc_hotkey_hint_display_option_changed:
                global_data.emgr.pc_hotkey_hint_display_option_changed.emit(old, option)

    def get_hotkey_hint_display_option(self):
        return self._pc_hotkey_hint_display_option

    def set_pc_hotkey_hint_switch(self, enable, persistent):
        old = self._pc_hotkey_hint_switch
        self._pc_hotkey_hint_switch = enable
        if persistent:
            if global_data.player:
                global_data.player.write_setting_2(uoc.PC_HOTKEY_HINT_SWITCH_KEY, enable, sync_to_server=False)
        if old != enable:
            global_data.emgr.pc_hotkey_hint_switch_toggled.emit(old, enable)

    def get_pc_hotkey_hint_switch(self):
        return self._pc_hotkey_hint_switch

    def release_movement_keys(self):
        game_hook.release_key(game.VK_W)
        game_hook.release_key(game.VK_A)
        game_hook.release_key(game.VK_S)
        game_hook.release_key(game.VK_D)