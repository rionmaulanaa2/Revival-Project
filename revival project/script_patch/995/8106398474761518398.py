# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/EscapeManagerAgent.py
from __future__ import absolute_import
import six_ex
from functools import cmp_to_key
from logic.manager_agents import ManagerAgentBase
import time
import game3d
import game
import logic.vscene.parts.ctrl.GamePyHook as game_hook
from inspect import getargspec
import six
DLG_UI_NAME = ('NormalConfirmUI', 'NormalConfirmUI2', 'SecondConfirmDlg2', 'SecondConfirmDlgForBind',
               'LoginReconnectConfirmDlg', 'ExitConfirmDlg')
BACK_BTN_NAME = ('on_click_close_btn', 'on_click_back_btn')
BACK_TRIGGER_TIME = 0.5

class EscapeManagerAgent(ManagerAgentBase.ManagerAgentBase):
    ALIAS_NAME = 'escape_mgr_agent'

    def zorder_cmp(self, name_a, name_b):
        ui_inst_a = global_data.ui_mgr.get_ui(name_a)
        ui_inst_b = global_data.ui_mgr.get_ui(name_b)
        if ui_inst_a:
            zorder_a = ui_inst_a.on_get_template_zorder()
        else:
            zorder_a = 0
        if ui_inst_b:
            zorder_b = ui_inst_b.on_get_template_zorder()
        else:
            zorder_b = 0
        return six_ex.compare(zorder_a, zorder_b)

    def init(self, *args):
        super(EscapeManagerAgent, self).init()
        self.last_press_back_time = 0
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            game_hook.add_key_handler(game.MSG_KEY_UP, (game.VK_ESCAPE,), self.on_key_msg)
        else:
            game_hook.add_key_handler(game.MSG_KEY_UP, (game3d.AVK_BACK,), self.on_key_msg)
            if global_data.is_android_pc or global_data.is_mumu_pc_control:
                game_hook.add_key_handler(game.MSG_KEY_UP, (game.VK_ESCAPE,), self.on_key_msg)
        self._block_reasons = []

    def block(self, reason):
        if reason is None:
            return
        else:
            self._block_reasons.append(reason)
            return

    def unblock(self, reason):
        if reason is None:
            return
        else:
            if reason in self._block_reasons:
                self._block_reasons.remove(reason)
            return

    def is_blocked(self):
        return bool(self._block_reasons)

    def use_close_btn(self, ui_name):
        from common.const.uiconst import UI_VKB_CLOSE, UI_VKB_CUSTOM, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
        import inspect
        ui = global_data.ui_mgr.get_ui(ui_name)
        if ui and not ui.isPanelVisible():
            return False
        else:
            if ui and ui.UI_VKB_TYPE == UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME:
                for name in BACK_BTN_NAME:
                    func = getattr(ui, name, None)
                    if func:
                        if six.PY2:
                            args, varargs, varkw, defaults = getargspec(func)
                            if len(args) == 1 or defaults and len(args) == len(defaults) + 1:
                                func()
                                return True
                        else:
                            sig = inspect.signature(func)
                            args = list(sig.parameters.keys())
                            param_values = list(sig.parameters.values())
                            has_self = len(args) > 0 and args[0] == 'self'
                            has_varargs = any((p.kind == inspect.Parameter.VAR_POSITIONAL for p in param_values))
                            has_varkwargs = any((p.kind == inspect.Parameter.VAR_KEYWORD for p in param_values))
                            default_count = len([ p for p in param_values if p.default != inspect.Parameter.empty ])
                            need_fill_count = len(args) - default_count
                            if has_varargs:
                                need_fill_count -= 1
                            if has_varkwargs:
                                need_fill_count -= 1
                            if len(inspect.signature(func).parameters) == 0:
                                func()
                                return True
                            if len(args) == 1 and has_varargs:
                                func()
                                return True
                            if len(args) == 2 and has_varkwargs and has_varargs:
                                func()
                                return True
                            if need_fill_count == 0:
                                func()
                                return True

            if ui and ui.UI_VKB_TYPE == UI_VKB_CLOSE:
                ui.close()
                return True
            if ui and ui.UI_VKB_TYPE == UI_VKB_CUSTOM:
                if hasattr(ui, 'ui_vkb_custom_func') and ui.ui_vkb_custom_func:
                    ret = ui.ui_vkb_custom_func()
                    return bool(ret)
            return False

    def on_key_msg(self, msg, key_code):
        if self.is_blocked():
            return
        else:
            if time.time() - self.last_press_back_time < BACK_TRIGGER_TIME:
                return
            self.last_press_back_time = time.time()
            if not global_data.ui_mgr.dlg_stack:
                return
            visible_dlg_stack = []
            for ui_name in global_data.ui_mgr.dlg_stack:
                ui_inst = global_data.ui_mgr.get_ui(ui_name)
                if ui_inst:
                    ui_inst.isPanelVisible()
                    visible_dlg_stack.append(ui_name)

            visible_dlg_stack = sorted(visible_dlg_stack, key=cmp_to_key(self.zorder_cmp))
            if len(global_data.ui_mgr.dlg_stack) > 0:
                top_ui_name = global_data.ui_mgr.dlg_stack[-1]
            else:
                top_ui_name = None
            exit_flag = True
            if top_ui_name in DLG_UI_NAME:
                global_data.ui_mgr.close_ui(top_ui_name)
                return
            if global_data.player and global_data.player.is_in_battle():
                for ui_name in reversed(visible_dlg_stack):
                    if self.use_close_btn(ui_name):
                        return

            elif top_ui_name == 'LobbyReconnectUI':
                ui = global_data.ui_mgr.get_ui('LobbyReconnectUI')
                if ui:
                    ui.on_close_dialog()
                    return
            elif 'LobbyUI' in global_data.ui_mgr.dlg_stack or 'MainLoginUI' in global_data.ui_mgr.dlg_stack:
                for ui_name in reversed(visible_dlg_stack):
                    if self.use_close_btn(ui_name):
                        return

            if exit_flag:
                import game3d
                if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_pc_mode:
                    if global_data.pc_ctrl_mgr:
                        global_data.pc_ctrl_mgr.trigger_keyboard_event(game.VK_ESCAPE)
                else:
                    self.show_exit_game_confirm_dialog()
            return

    @staticmethod
    def show_exit_game_confirm_dialog--- This code section failed: ---

 172       0  LOAD_GLOBAL           0  'global_data'
           3  LOAD_ATTR             1  'channel'
           6  LOAD_ATTR             2  'try_exit'
           9  CALL_FUNCTION_0       0 
          12  POP_JUMP_IF_FALSE    19  'to 19'

 173      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

 176      19  LOAD_CONST               '<code_object exit_callback>'
          22  MAKE_FUNCTION_0       0 
          25  STORE_FAST            0  'exit_callback'

 178      28  LOAD_CONST               '<code_object continue_game>'
          31  MAKE_FUNCTION_0       0 
          34  STORE_FAST            1  'continue_game'

 181      37  LOAD_CONST            3  ''
          40  LOAD_CONST            4  ('ExitConfirmDlg',)
          43  IMPORT_NAME           3  'logic.comsys.common_ui.NormalConfirmUI'
          46  IMPORT_FROM           4  'ExitConfirmDlg'
          49  STORE_FAST            2  'ExitConfirmDlg'
          52  POP_TOP          

 182      53  LOAD_FAST             2  'ExitConfirmDlg'
          56  CALL_FUNCTION_0       0 
          59  LOAD_ATTR             5  'confirm'
          62  LOAD_CONST            5  'content'

 183      65  LOAD_GLOBAL           6  'get_text_local_content'
          68  LOAD_CONST            6  2101
          71  CALL_FUNCTION_1       1 
          74  LOAD_CONST            7  'cancel_text'

 184      77  LOAD_GLOBAL           6  'get_text_local_content'
          80  LOAD_CONST            8  140
          83  CALL_FUNCTION_1       1 
          86  LOAD_CONST            9  'cancel_callback'
          89  LOAD_CONST           10  'confirm_text'

 185      92  LOAD_GLOBAL           6  'get_text_local_content'
          95  LOAD_CONST           11  18808
          98  CALL_FUNCTION_1       1 
         101  LOAD_CONST           12  'confirm_callback'
         104  LOAD_FAST             1  'continue_game'
         107  CALL_FUNCTION_1280  1280 
         110  POP_TOP          

Parse error at or near `CALL_FUNCTION_1280' instruction at offset 107