# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/BattleSceneOnlyUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
import social
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
from common.uisys.uielment.CCSprite import CCSprite
import cc
from logic.comsys.share.ShareManager import ShareManager
from logic.comsys.lobby.LobbyInteractionUI import LobbyInteractionUI
from logic.gutils.share_utils import get_pc_share_save_path
import math3d
DELAY_HIDE_LIST = []
from logic.comsys.battle.spray.SprayUI import SprayUI
from logic.comsys.share.LobbySceneOnlyUI import LobbySceneOnlyUI, CameraModifyWidget
from logic.gutils.CameraHelper import is_free_type_camera

class BattleCameraModifyWidget(CameraModifyWidget):

    def __init__(self, panel):
        self._is_direction_helper = False
        super(BattleCameraModifyWidget, self).__init__(panel)
        self.move_ranges = [(-30, 30), (-25, 50), (-50, 10)]
        self._default_pos = [
         0, 20, 30]
        self._focus_pos = [0, 20, 0]
        self._hfov = 45
        self.update_data()
        self.panel.nd_setting.setVisible(False)

    def destroy(self):
        self.panel.btn_reset.OnClick(None)
        super(BattleCameraModifyWidget, self).destroy()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        event_info = {'camera_switch_to_state_event': self.on_camera_state_changed
           }
        if is_bind:
            emgr.bind_events(event_info)
        else:
            emgr.unbind_events(event_info)

    def on_camera_state_changed(self, new_type, old_type, *args):

        def inner_update():
            self.update_data()

        self.panel.SetTimeOut(0.3, inner_update)

    def set_custom_camera(self, focus_point, default_pos, fov):
        part_cam = self.get_partcam()
        import math3d
        if not self._is_direction_helper:
            from logic.gutils.CameraHelper import cal_horizontal_default_pos
            new_default_pos = cal_horizontal_default_pos(math3d.vector(*default_pos), math3d.vector(*focus_point))
            part_cam.cam_manager.update_camera_config(new_default_pos, math3d.vector(*focus_point))
            if fov:
                part_cam.cam_manager.set_hoz_fov(fov)
            global_data.emgr.slerp_into_setupped_camera_event.emit(0)
        elif fov:
            part_cam.cam_manager.set_hoz_fov(fov)

    def get_partcam(self):
        part_cam = global_data.game_mgr.scene.get_com('PartCameraSimple')
        if not part_cam:
            part_cam = global_data.game_mgr.scene.get_com('PartCamera')
        return part_cam

    def update_data(self):
        part_cam = self.get_partcam()
        camera_manager = part_cam.cam_manager
        if not camera_manager:
            return
        else:
            default_pos = camera_manager.get_default_cam_pos()
            if default_pos is None:
                return
            focus_pos = camera_manager.get_default_cam_focus()
            if focus_pos is None:
                return
            self._default_pos = [default_pos.x, default_pos.y, default_pos.z]
            self._focus_pos = [focus_pos.x, focus_pos.y, focus_pos.z]
            self._hfov = camera_manager.get_default_hfov()
            return

    def reset_camera_show(self):
        if self._is_direction_helper:
            if global_data.judge_camera_mgr:
                global_data.judge_camera_mgr.reset_camera_to_original_pos()
            return
        else:
            self.focus_offset = None
            self.pos_offset = None
            self.fov_offset = None
            self.hoffset = None
            self.fov_offset_idx = 0
            self.height_idx = 0
            self.update_fov_button_show()
            self.update_height_button_show()
            self.update_camera_show()
            return

    def update_camera_show(self):
        new_focus_point = self._focus_pos
        if self.focus_offset:
            new_focus_point = [ self.focus_offset[idx] + self._focus_pos[idx] for idx in range(len(self.focus_offset)) ]
        new_def_pos = self._default_pos
        if self.pos_offset:
            new_def_pos = [ self.pos_offset[idx] + self._default_pos[idx] for idx in range(len(self.pos_offset)) ]
        new_focus_point[1] = new_def_pos[1]
        new_hfov = self._hfov
        if self.fov_offset:
            new_hfov = self._hfov + self.fov_offset
        self.set_custom_camera(new_focus_point, new_def_pos, new_hfov)

    def on_add_camera_offset(self, x, y, z):
        if not global_data.cam_lctarget:
            return
        if self.pos_offset:
            self.pos_offset = [
             x + self.pos_offset[0], y + self.pos_offset[1], z + self.pos_offset[2]]
        else:
            self.pos_offset = [
             x, y or 0, z]
        ranges = self.move_ranges
        for i, val in enumerate(self.pos_offset):
            bound = ranges[i]
            self.pos_offset[i] = min(max(bound[0], self.pos_offset[i]), bound[1])

        self.update_camera_show()

    def set_move_ranges(self, x_range, y_range, z_range):
        self.move_ranges = [
         x_range, y_range, z_range]

    def get_move_direction(self):
        if self._rocker_direction and self.btn_dragged:
            return math3d.vector(self._rocker_direction.x, 0, self._rocker_direction.y)
        else:
            return None
            return None

    def get_move_speed(self):
        return self._rocker_move_percent * 3

    def set_is_direction_helper(self, val):
        self._is_direction_helper = val


class BattleSceneOnlyUI(LobbySceneOnlyUI):
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self):
        super(BattleSceneOnlyUI, self).on_init_panel()
        self.close_cb = None
        if not is_free_type_camera(global_data.cam_data.camera_state_type):
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_FREE_CAMERA_STATE', True)
        from logic.client.const import game_mode_const
        self.panel.nd_lens.setVisible(True)
        global_data.emgr.switch_cam_state_enable_event.emit(False)
        global_data.emgr.switch_cam_ani_enable_event.emit(False)
        self.old_pc_control = None
        if global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
            self.old_pc_control = True
            global_data.pc_ctrl_mgr.enable_PC_control(False)
            return
        else:
            return

    def init_camera_modify_widget(self):
        self._camera_modify_widget = BattleCameraModifyWidget(self.panel)

    def on_finalize_panel(self):
        super(BattleSceneOnlyUI, self).on_finalize_panel()
        if self.old_pc_control is not None:
            if global_data.pc_ctrl_mgr:
                global_data.pc_ctrl_mgr.enable_PC_control(self.old_pc_control)
                self.old_pc_control = None
        global_data.emgr.switch_cam_state_enable_event.emit(True)
        global_data.emgr.switch_cam_ani_enable_event.emit(True)
        global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
        if self.close_cb:
            self.close_cb()
        self.close_cb = None
        if is_free_type_camera(global_data.cam_data.camera_state_type):
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_FREE_CAMERA_STATE', False)
        global_data.emgr.recover_observe_camera_event.emit()
        return

    def init_interaction_btn(self):
        from logic.comsys.map.InteractionInvokeBtnWidget import InteractionInvokeBtnWidget
        self._inter_invoke_btn_widget = InteractionInvokeBtnWidget(self.panel.btn_interaction, self.panel, SprayUI, self.__class__.__name__)
        self.panel.btn_interaction.BindMethod('OnBegin', self._inter_invoke_btn_widget.on_touch_inter_begin)
        self.panel.btn_interaction.BindMethod('OnDrag', self._inter_invoke_btn_widget.on_touch_inter_drag)
        self.panel.btn_interaction.BindMethod('OnEnd', self._inter_invoke_btn_widget.on_touch_inter_end)
        self.panel.btn_interaction.BindMethod('OnCancel', self._inter_invoke_btn_widget.on_touch_inter_cancel)

    def set_left_center_btns_vis(self, vis):
        self.panel.nd_left_mid.setVisible(vis)

    def hide_grid(self):
        self.panel.nd_line.setVisible(False)

    def block_ui_show(self, white_list):
        white_ls = white_list
        from logic.gutils.pc_ui_utils import MOBILE_2_PC_UI_DICT, PC_2_MOBILE_UI_DICT
        for ui_name in white_ls:
            if ui_name in MOBILE_2_PC_UI_DICT:
                white_ls.append(MOBILE_2_PC_UI_DICT[ui_name])

        global_data.ui_mgr.add_ui_show_whitelist(white_ls, self.__class__.__name__)

    def set_close_cb(self, func):
        self.close_cb = func

    def set_move_ranges(self, x_range, y_range, z_range):
        if self._camera_modify_widget:
            self._camera_modify_widget.set_move_ranges(x_range, y_range, z_range)

    def set_is_direction_helper(self, val):
        if self._camera_modify_widget:
            self._camera_modify_widget.set_is_direction_helper(val)
        self.panel.nd_scale_height.setVisible(not val)

    def get_move_direction(self):
        if self._camera_modify_widget:
            return self._camera_modify_widget.get_move_direction()
        else:
            return None
            return None

    def get_move_speed(self):
        if self._camera_modify_widget:
            return self._camera_modify_widget.get_move_speed()
        else:
            return 0