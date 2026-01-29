# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/pc_utils.py
from __future__ import absolute_import
from logic.client.const import pc_const
from common.utils import pc_platform_utils
FORCE_IGNORE_NODE_NAMES = {
 'nd_effects', 'nd_other_effects'}

def check_can_enable_pc_mode():
    import game3d
    if game3d.get_platform() == game3d.PLATFORM_WIN32 or global_data.is_android_pc or global_data.is_mumu_pc_control:
        return True
    else:
        return False


def init_pc_ctrl_manager():
    if global_data.is_pc_mode:
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        PCCtrlManager()
        from logic.gcommon.common_const import ui_operation_const as uoc
        archive_data = global_data.achi_mgr.get_general_archive_data()
        is_fullscreen = archive_data.get_field(uoc.PC_FULL_SCREEN_KEY, uoc.LOCAL_SETTING_CONF.get(uoc.PC_FULL_SCREEN_KEY))
        global_data.pc_ctrl_mgr.request_fullscreen(is_fullscreen, req_from_setting_ui=False)
        from logic.gutils.pc_resolution_utils import ensure_pc_windowed_resolution
        ensure_pc_windowed_resolution()
        global_data.pc_ctrl_mgr.enable_keyboard_control(False)


def adjust_setting_panel_pos_and_size(parent_scroll, parent_panel, panel, total_size=None, swallow_height_map=None, hide_list=[]):
    if total_size is not None:
        panel_w, panel_h = total_size
    else:
        panel_w, panel_h = panel.GetContentSize()
    offset_tbl = {}
    children = panel.GetChildren()
    y_offset = 0
    for child in children:
        name = child.widget_name
        if 'static' in name:
            continue
        if name in FORCE_IGNORE_NODE_NAMES:
            offset_tbl[child] = y_offset
            continue
        if name.startswith('nd_render'):
            child.setVisible(pc_platform_utils.is_redirect_scale_enable())
        if name.startswith('nd_pc'):
            child.setVisible(global_data.is_pc_mode)
        if name.startswith('nd_mobile') or name.startswith('nd_digit'):
            child.setVisible(not global_data.is_pc_mode)
        if name.startswith('nd_graphics_style') and not global_data.is_ue_model:
            child.setVisible(False)
        if child in hide_list:
            child.setVisible(False)
        if not child.IsVisible():
            _, h = child.GetContentSize()
            y_offset += h
        elif swallow_height_map is not None and name in swallow_height_map:
            y_offset += swallow_height_map[name]
        else:
            offset_tbl[child] = y_offset

    panel_h -= y_offset
    panel.SetContentSize(panel_w, panel_h)
    parent_scroll.SetInnerContentSize(panel_w, panel_h)
    for child in children:
        if child in offset_tbl:
            y_offset = offset_tbl[child]
            child.InitConfPosition()
            x, y = child.GetPosition()
            y += y_offset
            child.SetPosition(x, y)
        else:
            child.ReConfPosition()

    parent_scroll.SetContainer(panel)
    parent_scroll.ScrollToTop()
    parent_panel.adjust_container_pos()
    return


def skip_when_debug_key_disabled(func):

    def wrapped(*args, **kwargs):
        if not can_run_debug_key_logic():
            return None
        else:
            return func(*args, **kwargs)
            return None

    return wrapped


def can_run_debug_key_logic():
    if not global_data.game_mgr.scene:
        return False
    if global_data.game_mgr.scene.scene_type in ('Test', 'TestFly', 'TestSimple'):
        return True
    if global_data.is_pc_mode:
        if not global_data.is_inner_server:
            return False
        else:
            if not global_data.enable_debug_key_in_inner_server:
                return False
            return True

    else:
        import game3d
        return game3d.get_platform() == game3d.PLATFORM_WIN32


def is_pc_control_enable():
    if global_data.is_pc_mode and global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
        return True
    else:
        return False


def get_hotkey_hint_display_option():
    if global_data.is_pc_mode and global_data.pc_ctrl_mgr:
        return global_data.pc_ctrl_mgr.get_hotkey_hint_display_option()
    else:
        return pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_DEFAULT


def get_pc_hotkey_hint_switch():
    if global_data.is_pc_mode and global_data.pc_ctrl_mgr:
        return global_data.pc_ctrl_mgr.get_pc_hotkey_hint_switch()
    else:
        return False


def should_pc_key_hint_related_uis_show(question_display_option, against_hint_switch, against_display_option, against_pc_op_mode):
    if question_display_option == pc_const.PC_HOTKEY_HINT_DIPLAY_OPTION_VAL_HIDE:
        return False
    else:
        if question_display_option == pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_ICON:
            return not against_pc_op_mode or against_hint_switch and against_display_option == pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_ICON
        if question_display_option == pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_TEXT:
            return against_hint_switch and against_pc_op_mode and against_display_option == pc_const.PC_HOTKEY_HINT_DISPLAY_OPTION_VAL_TEXT
        return True


def get_user_settings_path():
    import game3d
    import os
    from logic.client.const import pc_const
    cwd = game3d.get_root_dir()
    return os.path.join(cwd, pc_const.USER_SETTINGS_XML_FILENAME)


def get_neox_xml_path():
    import game3d
    import os
    from logic.client.const import pc_const
    cwd = game3d.get_root_dir()
    return os.path.join(cwd, pc_const.NEOX_XML_FILENAME)


def log_when_in_inner_server(log_func, *args, **kwargs):
    if not global_data.is_inner_server:
        return
    log_func(*args, **kwargs)