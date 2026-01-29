# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/keyboard/CommonKeyboard.py
from __future__ import absolute_import
from __future__ import print_function
import six
from .CtrlKeyboardBase import CtrlKeyboardBase
import game

class CommonKeyboard(CtrlKeyboardBase):

    def __init__(self):
        super(CommonKeyboard, self).__init__()
        self.key_up_func = {}
        self.key_down_func = {game.VK_DELETE: {0: ['_key_func_1']},game.VK_HOME: {0: ['leave_only_aim_ui']},game.VK_INSERT: {0: ['switch_scene_col_drawing']}}

    def switch_scene_col_drawing(self, *args):
        from logic.gutils import scene_utils
        scene_utils.show_scene_collision()

    def _key_func_1(self, msg, keycode):
        if not global_data.is_inner_server:
            return
        import game3d
        import cc
        is_show = global_data.can_show_cockpit_decor
        if is_show:
            global_data.can_show_cockpit_decor = False
            if not global_data.del_show_ui_list:
                global_data.ui_mgr.set_all_ui_visible(False)
            else:
                global_data.ui_mgr.add_ui_show_whitelist(global_data.del_show_ui_list, 'KEY_DEL')
            if global_data.cam_lplayer:
                global_data.cam_lplayer.send_event('E_CLOSE_MECHA_UI')
            game3d.show_render_info(False)
            cc.Director.getInstance().setDisplayStats(False)
        else:
            global_data.can_show_cockpit_decor = True
            if not global_data.del_show_ui_list:
                global_data.ui_mgr.set_all_ui_visible(True)
            else:
                global_data.ui_mgr.remove_ui_show_whitelist('KEY_DEL')
            cc.Director.getInstance().setDisplayStats(True)
        open_hot_key_list = [
         'WeaponBarSelectUI', 'WeaponBarSelectUIPC']
        for ui_name in open_hot_key_list:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                ui.HOT_KEY_CHECK_VISIBLE = not is_show

    def _test_1(self, msg, keycode):
        self._change_rotation(0, 1, 0)

    def _test_2(self, msg, keycode):
        self._change_rotation(0, -1, 0)

    def _test_3(self, msg, keycode):
        self._change_rotation(1, 0, 0)

    def _test_4(self, msg, keycode):
        self._change_rotation(-1, 0, 0)

    def _test_5(self, msg, keycode):
        self._change_rotation(0, 0, 1)

    def _test_6(self, msg, keycode):
        self._change_rotation(0, 0, -1)

    def _test_end(self, msg, keycode):
        global_data.emgr.update_map_test_touch_event.emit()

    def enable_distorted(self, msg, keycode):
        import cc
        a = global_data.ui_mgr.get_ui('MechaControlMain')
        if a:
            nd = getattr(a, '_cur_move_node') if hasattr(a, '_cur_move_node') else None
            if nd:
                nd.setRotation3D(cc.Vec3(0, 0, 0))
        return

    def _scale_x_sm(self, msg, keycode):
        self._change_scale(-0.01, 0)

    def _scale_x_bg(self, msg, keycode):
        self._change_scale(+0.01, 0)

    def _scale_y_sm(self, msg, keycode):
        self._change_scale(0, -0.01)

    def _scale_y_bg(self, msg, keycode):
        self._change_scale(0, +0.01)

    def open_move(self, msg, keycode):
        if not hasattr(global_data, 'enable_move'):
            global_data.enable_move = False
        a = global_data.ui_mgr.get_ui('MechaControlMain')
        if a:
            if not global_data.enable_move:
                a.panel.SetEnableTouch(True)
                a.init_test_move_logic()
                global_data.enable_move = True
            else:
                a.panel.SetEnableTouch(False)
                global_data.enable_move = False

    def chose_node(self, msg, keycode):
        a = global_data.ui_mgr.get_ui('MechaControlMain')
        if a:
            if global_data.enable_move:
                a.switch_test_move_node()

    def leave_only_aim_ui(self, msg, keycode):
        if not global_data.is_inner_server:
            return
        else:
            if not hasattr(global_data, 'hide_leave_aim_ui'):
                global_data.hide_leave_aim_ui = False
            from common.uisys.basepanel import MAIN_UI_LIST, MECHA_AIM_UI_LSIT
            from common.debug.debug_util import set_ui_show_whitelist
            blocking_list = list(MAIN_UI_LIST)
            leave_list = list()
            leave_list.extend(MECHA_AIM_UI_LSIT)
            leave_list.append('FrontSightUI')
            global_data.is_yunying = True
            from common.uisys.basepanel import BasePanel
            BasePanel.HOT_KEY_CHECK_VISIBLE = False
            for dlg_name, dlg in six.iteritems(global_data.ui_mgr.dialogs):
                dlg.HOT_KEY_CHECK_VISIBLE = False

            for ui_name in leave_list:
                if ui_name in blocking_list:
                    blocking_list.remove(ui_name)

            if not global_data.hide_leave_aim_ui:
                set_ui_show_whitelist(leave_list, 'FROM HOTKEY')
                global_data.hide_leave_aim_ui = True
            else:
                set_ui_show_whitelist([], None)
                global_data.hide_leave_aim_ui = False
            return

    def _change_scale(self, added_scale_x, added_scale_y):
        a = global_data.ui_mgr.get_ui('MechaControlMain')
        if a:
            nd = getattr(a, '_cur_move_node') if hasattr(a, '_cur_move_node') else None
            if nd:
                if added_scale_x != 0:
                    nd.setScaleX(nd.getScaleX() + added_scale_x)
                    print('new_scaleX', nd.getScaleX())
                if added_scale_y != 0:
                    nd.setScaleY(nd.getScaleY() + added_scale_y)
                    print('new_scaleY', nd.getScaleY())
        return

    def _change_rotation(self, added_rot_x, added_rot_y, added_rot_z):
        a = global_data.ui_mgr.get_ui('MechaControlMain')
        if a:
            nd = getattr(a, '_cur_move_node') if hasattr(a, '_cur_move_node') else None
            if nd:
                old_one = nd.getRotation3D()
                old_one.x += added_rot_x
                old_one.y += added_rot_y
                old_one.z += added_rot_z
                nd.setRotation3D(old_one)
                log_error('new rotate', old_one)
        return